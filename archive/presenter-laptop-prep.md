# PIA Session — Infrastructure & Laptop Prep

Hand-off document for everything that has to be ready before the *Free & Open Source Campaigning* session at Public Interest Alberta 2026.

The session runs on **PIA's own n3-pia server**. The full `pia-starter-stack` (CryptPad, MkDocs dev, Nginx static, Listmonk, Newt tunnel client) and the public URLs all live there — fronted by a Pangolin/Newt tunnel routing `*.publicinterestalberta.org` subdomains to n3-pia loopback ports. **Reed's laptop is the operator station only**: SSH terminal, CryptPad browser tab, projector. Nothing critical to the session runs locally.

The room writes in CryptPad. Reed pulls each group's section, SSHs into n3-pia, pastes into a markdown file. MkDocs auto-rebuilds. The public URL updates in real time. That's the whole flow.

## Architecture

```
Attendee browsers (any device, no install)
        ↓
CryptPad on n3-pia ──────────────── pad.publicinterestalberta.org
        ↓ (Reed reads sections via browser)
Reed's laptop  (browser tab + SSH terminal + projector)
        ↓ (SSH paste into docs/research/group-N.md)
n3-pia: pia-starter-stack
   ├── mkdocs (dev, hot-reload) ─── live.publicinterestalberta.org
   ├── nginx (static ./site/) ───── pia2026.publicinterestalberta.org
   └── listmonk container ──────── mail.publicinterestalberta.org (optional)
        ↑
A Pangolin/Newt tunnel handles TLS + routing for all of them.
Newt runs as a service inside the starter-stack compose; Pangolin lives off-host.
```

Four (or five, with sandbox) subdomains under `publicinterestalberta.org` need to resolve to n3-pia by session day:

| Subdomain | Local container | Service |
| --- | --- | --- |
| `pad.publicinterestalberta.org` | `cryptpad:3000` (docker service) | The room's writing surface |
| `pad-sandbox.publicinterestalberta.org` | `cryptpad:3000` (same target, Host-header-routed) | Required — editor surface won't render without it |
| `live.publicinterestalberta.org` | `mkdocs:8000` (docker service) | The hot-reload site the room watches *during* the session |
| `pia2026.publicinterestalberta.org` | `mkdocs-site-server:80` (docker service) | The static permanent record, built once at the climax via `mkdocs build` |
| `mail.publicinterestalberta.org` | `listmonk:9000` (docker service) | Optional — only if you demo the newsletter half |
| *(local-only)* `127.0.0.1:8889` | code-server | Web IDE for editing docs and running `mkdocs build` — reach via SSH tunnel from your laptop, NOT a public subdomain |

## Four prep tracks

**Track 1** — Publish the take-home repo (the deliverable)
**Track 2** — Deploy the starter stack on n3-pia (`--profile session` brings up CryptPad with the rest)
**Track 3** — Configure Pangolin resources for all five subdomains
**Track 4** — Reed's laptop: SSH config, editor, projector dry-run

Tracks 1 and 2–3 can run in parallel (different machines). Track 4 depends on 2–3 being done.

## Prerequisites — verify before doing any work

On n3-pia (the PIA server):

```bash
ssh pia-bnkops@n3-pia
docker --version && docker compose version
git --version
ls /srv/                # where the compose stack will live
```

You also need access to a Pangolin admin UI to register n3-pia as a site and add resources. The assumed endpoint here is `https://pangolin.bnkops.com` — replace with PIA's actual Pangolin endpoint if different.

On Reed's laptop:

```bash
ssh pia-bnkops@n3-pia "echo 'ssh ok'"  # passwordless SSH should work
which qrencode
```

If any of these fail, fix before continuing.

## Track 1: publish the take-home repo

1. Take the scaffold at `bunker-ops/trainings/pia-session/pia-starter-stack/` from the docs vault.
2. Push to the canonical Git home — `git.publicinterestalberta.org/pia-starter-stack` is the natural choice now that everything else lives on PIA's domain. Alternative: `repo.bnkops.com/pia-starter-stack`.
3. Verify the repo loads in a browser and the README renders.
4. Generate the QR for table cards: `qrencode -o qr-repo.png "https://git.publicinterestalberta.org/pia-starter-stack"`.

## Track 2: deploy the starter stack on n3-pia

The starter stack now bundles every service the session needs — CryptPad (under the `session` profile), MkDocs dev server, Nginx serving the built site, Listmonk, and Newt as the tunnel client. One compose, one `up`.

```bash
ssh pia-bnkops@n3-pia
sudo mkdir -p /srv/pia-session
sudo chown $USER:$USER /srv/pia-session
cd /srv/pia-session

git clone https://git.publicinterestalberta.org/pia-starter-stack.git
cd pia-starter-stack
```

Get a Newt ID/secret first by registering n3-pia as a site in Pangolin's admin UI (Sites → New → type `newt`). Paste the values along with the rest of the config:

```bash
cat > .env <<'ENV'
# Pangolin / Newt
PANGOLIN_ENDPOINT=https://pangolin.bnkops.com
PANGOLIN_NEWT_ID=<from Pangolin admin UI>
PANGOLIN_NEWT_SECRET=<from Pangolin admin UI>

# Listmonk
LISTMONK_DB_USER=listmonk
LISTMONK_DB_PASSWORD=<set-a-strong-password>
LISTMONK_DB_NAME=listmonk

# linuxserver image user mapping (mkdocs-site-server)
USER_ID=1000
GROUP_ID=1000
TZ=America/Edmonton

# CryptPad public URLs (baked into the served HTML — set before first boot)
CRYPTPAD_MAIN_DOMAIN=https://pad.publicinterestalberta.org
CRYPTPAD_SANDBOX_DOMAIN=https://pad-sandbox.publicinterestalberta.org
ENV
```

CryptPad **requires two domains** — a main one and a sandbox one — for security reasons (cross-origin sandboxing of the editor iframe). The compose handles the routing internally, but you'll still need both `pad.publicinterestalberta.org` and `pad-sandbox.publicinterestalberta.org` registered as separate Pangolin resources in Track 3. If that's a hassle, the public `cryptpad.fr` instance is still a valid fallback (and it's still FOSS); you just lose the "everything on PIA's server" purity.

Edit `mkdocs.yml` to set the session's site name and URL:

```yaml
site_name: Free & Open Source Campaigning — PIA 2026
site_description: Live writing from the room.
# site_url is the canonical/permanent URL — set it to the static-site
# domain, NOT the dev-server domain. Sitemaps and OpenGraph links use this.
site_url: https://pia2026.publicinterestalberta.org

# ... rest unchanged ...

nav:
  - Home: index.md
  - Research:
    - Overview: research.md
    - Group submissions: research/
  - Subscribe: subscribe.md
```

Pre-create the research directory:

```bash
mkdir -p docs/research
cat > docs/research/index.md <<'MD'
# Group submissions

Each group's research will land here as it's submitted during the session.
MD
```

Edit `docs/index.md` to give it a session-flavoured opener:

```markdown
# Free & Open Source Campaigning

Welcome to the live site for the *Free & Open Source Campaigning* session
at Public Interest Alberta 2026. Everything below this line was written
by the room you're in. Refresh this page during the session to watch
the research roll in.

## Research

The groups in this room are about to dump their findings into [Research](research/).
Once they do, this page will link to all of it.
```

Bring it up — `--profile session` is what pulls CryptPad in alongside the other services:

```bash
docker compose pull
docker compose --profile session up -d
sleep 30
docker compose --profile session ps   # all five services should be Up
```

**Three first-boot one-time steps** (the compose file can't do these — they're side effects of how the upstream images are packaged):

```bash
# 1. Initialize Listmonk's database schema (Listmonk refuses to boot on empty DB)
docker compose run --rm listmonk ./listmonk --install --idempotent --yes
docker compose --profile session up -d listmonk

# 2. Chown CryptPad data dirs to UID 4001 (CryptPad runs as a non-root user)
docker run --rm -v "$(pwd)/data/cryptpad:/data" alpine:3 chown -R 4001:4001 /data
docker compose --profile session restart cryptpad

# 3. Build the static site once (nginx serves a linuxserver default until ./site/ is populated)
docker compose run --rm mkdocs build

# 4. (If using upstream codercom/code-server image) install mkdocs into code-server
#    — skip this if your CODE_SERVER_IMAGE has mkdocs prebuilt.
docker compose exec code-server bash -c "apt-get update -qq && apt-get install -y -qq python3-pip && pip install --break-system-packages 'mkdocs-material[recommended]'"
```

Verify connectivity from inside the docker network:

```bash
docker run --rm --network pia-stack curlimages/curl:latest -sI http://mkdocs:8000/                # → 200
docker run --rm --network pia-stack curlimages/curl:latest -sI http://mkdocs-site-server:80/      # → 200 (after step 3)
docker run --rm --network pia-stack curlimages/curl:latest -sI http://listmonk:9000/              # → 200
docker run --rm --network pia-stack curlimages/curl:latest -sI http://cryptpad:3000/              # → 200

docker compose logs newt | tail -5    # should report a successful Pangolin handshake
```

If `newt` keeps reconnecting, double-check `PANGOLIN_ENDPOINT` and the ID/secret in `.env`. Pangolin's admin UI shows the site as Connected once the handshake succeeds.

## Track 3: Pangolin resources

Newt is connected (Track 2). Now tell Pangolin which loopback ports map to which public hostnames. All of this happens in Pangolin's admin UI — there's no CLI.

For each subdomain below, in Pangolin: **Resources → New Resource**, attach it to the n3-pia site, and fill in:

| Public hostname | Target | Protocol |
| --- | --- | --- |
| `pad.publicinterestalberta.org` | `cryptpad:3000` | HTTP (with WebSocket upgrade) |
| `pad-sandbox.publicinterestalberta.org` | `cryptpad:3000` | HTTP (same target, different Host) |
| `live.publicinterestalberta.org` | `mkdocs:8000` | HTTP (with WebSocket upgrade — MkDocs hot-reload uses one) |
| `pia2026.publicinterestalberta.org` | `mkdocs-site-server:80` | HTTP |
| `mail.publicinterestalberta.org` | `listmonk:9000` | HTTP |

CryptPad also needs its WebSocket path proxied. Add a path rule on the `pad.publicinterestalberta.org` resource:

| Path | Target | Protocol |
| --- | --- | --- |
| `/cryptpad_websocket` | `cryptpad:3003` | WebSocket |

Newt resolves these service names via the docker DNS on the `pia-stack` network.

DNS: each subdomain needs a CNAME pointing at Pangolin's edge. If Pangolin has DNS-zone access for `publicinterestalberta.org`, this happens automatically when you save the resource. Otherwise add the CNAMEs manually in PIA's DNS provider.

TLS: Pangolin auto-issues Let's Encrypt certs once DNS resolves. First-request cold-start can take ~30 seconds; subsequent requests are instant.

Test from anywhere:

```bash
for sub in pad pad-sandbox live pia2026 mail; do
  curl -sI -o /dev/null -w "${sub}: %{http_code}\n" \
    "https://${sub}.publicinterestalberta.org/"
done
```

All five should return 2xx or 3xx within a minute. *Note: `pia2026` will 404 until you run `mkdocs build` to populate `./site/` — that's the planned state up until the session climax.*

## Track 4: Reed's laptop prep

The laptop is just a terminal and a browser. Three things to set up.

### SSH config

```bash
# ~/.ssh/config (on the laptop)
Host n3-pia
  HostName <n3-pia public hostname or Tailscale name>
  User pia-bnkops
  IdentityFile ~/.ssh/id_ed25519
  ServerAliveInterval 60
  ServerAliveCountMax 10
```

Test:
```bash
ssh n3-pia "uptime && docker ps --format '{{.Names}}: {{.Status}}' | grep -E 'cryptpad|mkdocs|listmonk|newt|nginx'"
```

### Editor for the live segment

Two options, pick one and rehearse with it:

**Option A — code-server (the web IDE running on n3-pia, in the stack).** SSH-tunnel `127.0.0.1:8889` from your laptop:

```bash
ssh -L 8889:127.0.0.1:8889 n3-pia
# then in your laptop's browser: http://localhost:8889/
```

Log in with `CODE_SERVER_PASSWORD` from n3-pia's `.env`. Open the workspace, edit `docs/research/group-N.md`, save. Open the integrated terminal and run `mkdocs build` for the climax static-site refresh. No client install on your laptop, no network round-trip per save.

**Option B — VS Code with Remote-SSH extension.** Open `n3-pia:/srv/pia-session/pia-starter-stack/` as a remote workspace. Same workflow, native VS Code instead of a browser tab.

**Option C — Plain SSH + vim/nano.** No client-side install. `ssh n3-pia`, `cd /srv/pia-session/pia-starter-stack/docs/research`, `vim group-1.md`, paste, save. Works offline as a backup if A or B misbehaves.

### CryptPad pad creation

Create the room's pad **after** Track 2 is up. Visit `https://pad.publicinterestalberta.org`, sign in (CryptPad supports anonymous use too, but a logged-in session preserves admin control of the pad).

- Create a new **Code/Markdown** pad (not Rich Text).
- Pre-fill with the skeleton (see below).
- Set sharing to **edit access via URL** — no login required for collaborators.
- Save the URL. Generate a QR.

Skeleton:

```markdown
# PIA 2026 — Group Research

Each group gets a section below. Pick a corporate tool, find FOSS alternatives, write your 200-word writeup under your group's heading. Reed will copy your section to live.publicinterestalberta.org as you finish.

---

## Group 1 — [your tool]

*Members:* [first names]
*Replacing:* [the corporate tool]
*FOSS alternatives we found:*
1. [tool name](url) — one line on what it does
2. [tool name](url) — one line on what it does
*Why this matters for our org:*

(200 words here)

---

## Group 2 — [your tool]
[...]

## Group 3 — [your tool]
[...]

(repeat up to ~8 groups)
```

### QR cards

```bash
qrencode -o qr-repo.png      "https://git.publicinterestalberta.org/pia-starter-stack"
qrencode -o qr-handout.png   "https://publicinterestalberta.org/resources/foss-campaigning/"
qrencode -o qr-cryptpad.png  "https://pad.publicinterestalberta.org/pad/<your-pad-id>"
qrencode -o qr-livesite.png  "https://live.publicinterestalberta.org/"
qrencode -o qr-permanent.png "https://pia2026.publicinterestalberta.org/"
```

The first four go on every table from minute 0. The CryptPad QR is the most prominent — it's the action prompt. The `qr-permanent.png` is for the closing slide / final segment, after `mkdocs build` makes the static site real.

## Workflow rehearsal

Before the session, run the live segment twice end-to-end on real infrastructure:

1. SSH into n3-pia, run `docker compose --profile session ps`, confirm all five services are `Up`.
2. Open the CryptPad in a browser tab.
3. Open VS Code Remote-SSH (or a second terminal) on `/srv/pia-session/pia-starter-stack/`.
4. From a second device, type a paragraph into the pad's Group 1 section.
5. From the laptop, copy the Group 1 section markdown.
6. Paste into a new file `docs/research/group-1.md`.
7. Save. Refresh `https://live.publicinterestalberta.org/research/group-1/` — the dev server's filesystem watcher should have already rebuilt.
8. Time it: pad-write → published. Should be under 30 seconds with VS Code, under 60 with vim.

After the workflow rehearsal, run the climax-publish step once:

```bash
ssh n3-pia
cd /srv/pia-session/pia-starter-stack
docker compose run --rm mkdocs mkdocs build   # populates ./site/
curl -sI https://pia2026.publicinterestalberta.org/research/group-1/ | head -1   # expect 200
```

That's the "make it permanent" beat at minute ~70 of the session. Practice it once so the command is muscle memory.

The choreography matters more than the technology. Practice the *finger-flow* until it's automatic.

## Day-of checklist

```bash
# All public URLs reachable?
for sub in pad pad-sandbox live pia2026 mail; do
  curl -sI -o /dev/null -w "${sub}: %{http_code}\n" \
    "https://${sub}.publicinterestalberta.org/"
done

# Repo published?
curl -sf -o /dev/null -w "repo: %{http_code}\n" https://git.publicinterestalberta.org/pia-starter-stack

# Handout still up?
curl -sf -o /dev/null -w "handout: %{http_code}\n" https://publicinterestalberta.org/resources/foss-campaigning/

# All five services running on n3-pia?
ssh n3-pia "cd /srv/pia-session/pia-starter-stack && docker compose --profile session ps"

# Pad still has its skeleton content?
# (manual — open in browser; CryptPad pads can expire if untouched for ~90 days)
```

## Live-segment script (for Reed's eyes)

1. **Minute ~20**: project the empty live site. Show the docs/research/ index — empty.
2. **Minute ~22**: project the CryptPad. Walk the room through the loop: write here → I pull → site updates.
3. **Minute ~28**: groups start writing. You walk the room — help groups pick a tool, point them at the handout. Off-stage for ~25 minutes.
4. **Minute ~55**: announce "I'm pulling in now." VS Code window up. Open the pad on a second screen. Pull each group's section: copy from pad → paste into `docs/research/group-N.md` → save. Refresh the live URL on the projector. **The room sees their content go public.** Read each title aloud, applaud.
5. **Minute ~70**: refresh the `/research/` index. Everyone's work, public, real domain. Pause. Let pride land.
6. **Minute ~73**: closing slide — repo URL.
7. **Minute ~75**: BNKops + the ask + sign-up.

## Troubleshooting

**Pangolin resource returns 502.**
Container isn't up, or isn't bound to the right loopback port. On n3-pia: `docker compose --profile session ps`; `ss -ltnp | grep <port>`. Compare to the `127.0.0.1:<port>` in the compose file.

**CryptPad loads but the editor doesn't.**
Sandbox domain resource isn't configured. Both `pad.` and `pad-sandbox.` need to resolve and serve. Check Pangolin's admin UI — both should be listed as Active.

**MkDocs container exits because a pasted section had a YAML-breaking character.**
`docker compose logs mkdocs | tail -50` shows the offending file. Edit or delete the bad file via SSH. Container restarts on its own.

**Pasted markdown has weird formatting.**
CryptPad markdown mode keeps things clean, but if a group pasted from elsewhere you may get HTML cruft. VS Code's "paste as plain text" (Ctrl+Shift+V) is the fix.

**Newt drops mid-session.**
On n3-pia: `docker compose restart newt`. Reconnects in seconds. Watch `docker compose logs -f newt` for the handshake log line.

**Pangolin server itself is unreachable.**
There is no quick fix from session-day Reed. Cut to the backup screen recording and narrate.

**SSH dies mid-session.**
Reed's laptop got bumped off WiFi or VPN. Reconnect. The remote vim/VS Code session is gone but the files on disk are fine — just reopen.

**Anything weirder.**
The Claude Code live-debug agent has SSH to n3-pia. Hand off.

## What's *not* on Reed's laptop

For clarity:

- ❌ No CryptPad container — runs on n3-pia
- ❌ No MkDocs container — runs on n3-pia
- ❌ No Listmonk container — runs on n3-pia
- ❌ No Newt tunnel client — runs on n3-pia (it's a service in the starter-stack compose)
- ❌ No local docker-compose for the demo

What's on the laptop:

- ✅ SSH config for n3-pia
- ✅ A browser with the CryptPad pad open
- ✅ VS Code with Remote-SSH (or a terminal with vim)
- ✅ A backup screen recording of a successful pull-paste-publish cycle

That's it.
