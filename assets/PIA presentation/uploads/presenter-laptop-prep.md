# PIA Session — Infrastructure & Laptop Prep

Hand-off document for everything that has to be ready before the *Free & Open Source Campaigning* session at Public Interest Alberta 2026.

The session runs on **PIA's own n3-pia server**. CryptPad (the writing surface), the starter stack (MkDocs site + Listmonk), and the public URLs all live there — fronted by PIA's existing Cloudflared tunnel under `publicinterestalberta.org`. **Reed's laptop is the operator station only**: SSH terminal, CryptPad browser tab, projector. Nothing critical to the session runs locally.

The room writes in CryptPad. Reed pulls each group's section, SSHs into n3-pia, pastes into a markdown file. MkDocs auto-rebuilds. The public URL updates in real time. That's the whole flow.

## Architecture

```
Attendee browsers (any device, no install)
        ↓
CryptPad on n3-pia ────────────── pad.publicinterestalberta.org
        ↓ (Reed reads sections via browser)
Reed's laptop  (browser tab + SSH terminal + projector)
        ↓ (SSH paste into docs/research/group-N.md)
n3-pia: pia-starter-stack
   ├── mkdocs container ────────── pia2026.publicinterestalberta.org
   └── listmonk container ──────── mail.publicinterestalberta.org (optional)
        ↑
PIA's existing Cloudflared tunnel handles TLS + DNS for all three
```

Three subdomains under `publicinterestalberta.org` need to resolve to n3-pia by session day:

| Subdomain | Local container | Service |
| --- | --- | --- |
| `pad.publicinterestalberta.org` | CryptPad on its own port | The room's writing surface |
| `pia2026.publicinterestalberta.org` | MkDocs container, port 8080 | The live site the room builds |
| `mail.publicinterestalberta.org` | Listmonk container, port 9001 | Optional — only if you demo the newsletter half |

## Five prep tracks

**Track 1** — Publish the take-home repo (the deliverable)
**Track 2** — Deploy CryptPad on n3-pia
**Track 3** — Deploy the starter stack on n3-pia
**Track 4** — Wire up Cloudflared routes for all three subdomains
**Track 5** — Reed's laptop: SSH config, editor, projector dry-run

Tracks 1 and 2–4 can run in parallel (different machines). Track 5 depends on 2–4 being done.

## Prerequisites — verify before doing any work

On n3-pia (the PIA server):

```bash
ssh pia-bnkops@n3-pia
docker --version && docker compose version
git --version
ls /etc/cloudflared/   # confirm existing tunnel config is there
ls /srv/                # where the new compose stacks will live
```

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

## Track 2: deploy CryptPad on n3-pia

CryptPad's official deployment is Docker-based. The container runs the full app + storage on a single port; we proxy via Cloudflared.

```bash
ssh pia-bnkops@n3-pia
sudo mkdir -p /srv/pia-session/cryptpad
sudo chown $USER:$USER /srv/pia-session/cryptpad
cd /srv/pia-session/cryptpad

cat > docker-compose.yml <<'YAML'
services:
  cryptpad:
    image: cryptpad/cryptpad:latest
    container_name: pia-session-cryptpad
    ports:
      - "127.0.0.1:3010:3000"  # main UI
      - "127.0.0.1:3011:3001"  # sandbox (required by CryptPad, must be a different hostname)
    environment:
      CPAD_MAIN_DOMAIN: "https://pad.publicinterestalberta.org"
      CPAD_SANDBOX_DOMAIN: "https://pad-sandbox.publicinterestalberta.org"
    volumes:
      - cryptpad-data:/cryptpad/data
      - cryptpad-blob:/cryptpad/blob
      - cryptpad-block:/cryptpad/block
      - cryptpad-customize:/cryptpad/customize
    restart: unless-stopped

volumes:
  cryptpad-data:
  cryptpad-blob:
  cryptpad-block:
  cryptpad-customize:
YAML

docker compose pull
docker compose up -d
sleep 30
curl -sI http://127.0.0.1:3010/ | head -1   # expect 200 or 302
```

CryptPad **requires two domains** — a main one and a sandbox one — for security reasons (cross-origin sandboxing of the editor iframe). So you'll need both `pad.publicinterestalberta.org` and `pad-sandbox.publicinterestalberta.org` routed in Track 4. If that's a hassle, the public `cryptpad.fr` instance is still a valid fallback (and it's still FOSS); you just lose the "everything on PIA's server" purity.

## Track 3: deploy the starter stack on n3-pia

```bash
ssh pia-bnkops@n3-pia
sudo mkdir -p /srv/pia-session/pia-starter-stack
sudo chown $USER:$USER /srv/pia-session/pia-starter-stack
cd /srv/pia-session

git clone https://git.publicinterestalberta.org/pia-starter-stack.git
cd pia-starter-stack

cat > .env <<'ENV'
LISTMONK_DB_USER=listmonk
LISTMONK_DB_PASSWORD=<set-a-strong-password>
LISTMONK_DB_NAME=listmonk
ENV
```

Edit `mkdocs.yml` to set the session's site name and URL:

```yaml
site_name: Free & Open Source Campaigning — PIA 2026
site_description: Live writing from the room.
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

Bring it up:

```bash
docker compose pull
docker compose up -d
sleep 20
curl -sI http://127.0.0.1:8080/ | head -1   # expect 200
curl -sI http://127.0.0.1:9001/ | head -1   # expect 200/302
```

## Track 4: Cloudflared routes

PIA's existing tunnel config lives at `~/.cloudflared/PIA-config.yml` on n3-pia. Add ingress rules for the three new subdomains.

Edit the config:

```bash
ssh pia-bnkops@n3-pia
nano ~/.cloudflared/PIA-config.yml
```

Add (or update) the `ingress:` block to include:

```yaml
ingress:
  - hostname: pad.publicinterestalberta.org
    service: http://127.0.0.1:3010

  - hostname: pad-sandbox.publicinterestalberta.org
    service: http://127.0.0.1:3011

  - hostname: pia2026.publicinterestalberta.org
    service: http://127.0.0.1:8080

  - hostname: mail.publicinterestalberta.org
    service: http://127.0.0.1:9001

  # ... existing PIA ingress rules below ...

  - service: http_status:404
```

Validate and reload:

```bash
cloudflared tunnel ingress validate
sudo systemctl restart cloudflared   # or whatever the existing tunnel start command is
```

Add DNS records via the Cloudflare dashboard (or `cloudflared tunnel route dns <tunnel-name> <hostname>`):

```bash
cloudflared tunnel route dns PIA-tunnel pad.publicinterestalberta.org
cloudflared tunnel route dns PIA-tunnel pad-sandbox.publicinterestalberta.org
cloudflared tunnel route dns PIA-tunnel pia2026.publicinterestalberta.org
cloudflared tunnel route dns PIA-tunnel mail.publicinterestalberta.org
```

Test from anywhere:

```bash
for sub in pad pad-sandbox pia2026 mail; do
  curl -sI -o /dev/null -w "${sub}: %{http_code}\n" \
    "https://${sub}.publicinterestalberta.org/"
done
```

All four should return 2xx or 3xx within a minute.

## Track 5: Reed's laptop prep

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
ssh n3-pia "uptime && docker ps | grep -E 'cryptpad|mkdocs|listmonk'"
```

### Editor for the live segment

Two options, pick one and rehearse with it:

**Option A — VS Code with Remote-SSH extension.** Open `n3-pia:/srv/pia-session/pia-starter-stack/` as a remote workspace. Edit files with full GUI. Pasting from CryptPad is the cleanest experience here. Recommended.

**Option B — Plain SSH + vim/nano.** No client-side install. `ssh n3-pia`, `cd /srv/pia-session/pia-starter-stack/docs/research`, `vim group-1.md`, paste, save. Works offline as a backup if VS Code Remote-SSH misbehaves.

### CryptPad pad creation

Create the room's pad **after** Track 2 is up. Visit `https://pad.publicinterestalberta.org`, sign in (CryptPad supports anonymous use too, but a logged-in session preserves admin control of the pad).

- Create a new **Code/Markdown** pad (not Rich Text).
- Pre-fill with the skeleton (see below).
- Set sharing to **edit access via URL** — no login required for collaborators.
- Save the URL. Generate a QR.

Skeleton:

```markdown
# PIA 2026 — Group Research

Each group gets a section below. Pick a corporate tool, find FOSS alternatives, write your 200-word writeup under your group's heading. Reed will copy your section to pia2026.publicinterestalberta.org as you finish.

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
qrencode -o qr-livesite.png  "https://pia2026.publicinterestalberta.org/"
```

All four go on every table from minute 0. The CryptPad QR is the most prominent — it's the action prompt.

## Workflow rehearsal

Before the session, run the live segment twice end-to-end on real infrastructure:

1. SSH into n3-pia, confirm all three containers are `Up`.
2. Open the CryptPad in a browser tab.
3. Open VS Code Remote-SSH (or a second terminal) on `/srv/pia-session/pia-starter-stack/`.
4. From a second device, type a paragraph into the pad's Group 1 section.
5. From the laptop, copy the Group 1 section markdown.
6. Paste into a new file `docs/research/group-1.md`.
7. Save. Refresh `https://pia2026.publicinterestalberta.org/research/group-1/`.
8. Time it: pad-write → published. Should be under 30 seconds with VS Code, under 60 with vim.

The choreography matters more than the technology. Practice the *finger-flow* until it's automatic.

## Day-of checklist

```bash
# All public URLs reachable?
for sub in pad pad-sandbox pia2026 mail; do
  curl -sI -o /dev/null -w "${sub}: %{http_code}\n" \
    "https://${sub}.publicinterestalberta.org/"
done

# Repo published?
curl -sf -o /dev/null -w "repo: %{http_code}\n" https://git.publicinterestalberta.org/pia-starter-stack

# Handout still up?
curl -sf -o /dev/null -w "handout: %{http_code}\n" https://publicinterestalberta.org/resources/foss-campaigning/

# All three containers running on n3-pia?
ssh n3-pia "docker ps --format '{{.Names}}: {{.Status}}' | grep -E 'cryptpad|mkdocs|listmonk'"

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

**Cloudflared route returns 502.**
Container isn't up, or isn't bound to the right loopback port. On n3-pia: `docker compose ps` from the relevant compose dir; `ss -ltnp | grep <port>`. Compare to the `127.0.0.1:<port>` in the compose file.

**CryptPad loads but the editor doesn't.**
Sandbox domain isn't routed correctly. Both `pad.` and `pad-sandbox.` need to resolve. Check Cloudflared ingress and DNS.

**MkDocs container exits because a pasted section had a YAML-breaking character.**
`docker logs pia-session-mkdocs` (or whatever the container is named) shows the offending file. Edit or delete the bad file via SSH. Container restarts on its own.

**Pasted markdown has weird formatting.**
CryptPad markdown mode keeps things clean, but if a group pasted from elsewhere you may get HTML cruft. VS Code's "paste as plain text" (Ctrl+Shift+V) is the fix.

**Cloudflared tunnel drops mid-session.**
On n3-pia: `sudo systemctl restart cloudflared`. Reconnects in seconds.

**SSH dies mid-session.**
Reed's laptop got bumped off WiFi or VPN. Reconnect. The remote vim/VS Code session is gone but the files on disk are fine — just reopen.

**Anything weirder.**
The Claude Code live-debug agent has SSH to n3-pia. Hand off.

## What's *not* on Reed's laptop

For clarity:

- ❌ No CryptPad container — runs on n3-pia
- ❌ No MkDocs container — runs on n3-pia
- ❌ No Listmonk container — runs on n3-pia
- ❌ No Newt / Pangolin tunnel — uses PIA's existing Cloudflared
- ❌ No local docker-compose for the demo

What's on the laptop:

- ✅ SSH config for n3-pia
- ✅ A browser with the CryptPad pad open
- ✅ VS Code with Remote-SSH (or a terminal with vim)
- ✅ A backup screen recording of a successful pull-paste-publish cycle

That's it.
