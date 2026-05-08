# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This directory is a Git repo nested inside the parent Obsidian vault. The vault-wide CLAUDE.md at `/media/bunker-admin/Internal/docs/CLAUDE.md` still applies (kebab-case file names, no wikilink-breaking renames from the shell, executive-assistant tone). Everything below is specific to this folder.

## What this directory is

Materials for **PIA-BNKOP-SERVER — Free & Open Source Campaigning**, an 80-minute Public Interest Alberta training session (May 2026). The folder serves two distinct purposes that share a tree:

1. **Session deliverables** — slide decks, handout, prep notes, assets. Presenter-authored, not redistributable. Lives in the top level of this folder.
2. **`pia-starter-stack/`** — a forkable Docker Compose project (MkDocs Material + Listmonk + Apache Answer + a Homepage/[gethomepage.dev](https://gethomepage.dev) service dashboard, plus optional CryptPad) that attendees take home. It carries its own `README.md`, `LICENSE` (AGPL-3.0), and `.gitignore`. Its canonical public home will be `git.publicinterestalberta.org/pia-starter-stack` (or `repo.bnkops.com/pia-starter-stack`) — it's a repo-in-waiting embedded as a subdirectory. **Treat anything under `pia-starter-stack/` as a near-standalone project**: keep the README forkable-by-strangers, no PIA branding or names baked in. The one deliberate concession is the `../scripts` bind mount on `code-server` in `docker-compose.yml`, which lets the presenter run the parent vault's `pangolin-push.py` from the IDE during the session; the line is commented in-file with a "FORKERS: delete this" note so strangers can spot it.

The session itself runs entirely on PIA's `n3-pia` server (the starter stack with `--profile session` to include CryptPad, fronted by a Pangolin/Newt tunnel). The presenter's laptop is just an SSH terminal and projector. See `PIA-Session-2026.md` for the cadence and `presenter-laptop-prep.md` for the infra steps.

## The slide-deck triplet

Three parallel decks share content but diverge by audience:

- `presentation-slides.md` — annotated, with speaker notes inline. **Rehearsal only**, never projected.
- `presentation-slides-clean.md` — projection version, no notes, no memes. For boardrooms.
- `presentation-slides-memes.md` — projection version with meme images embedded via `assets/meme-*.png`. The likely-actual deck for PIA.

When edits to one are content-level (wording of an argument, a statistic update, a section reorder), they generally need mirroring across all three. Layout-only changes (meme swaps, note additions) stay local. If you're unsure, ask before touching only one — drift between the three is a known maintenance hazard.

## Common commands

### Re-download or re-caption memes

Memes are not committed as source images — they're downloaded from [memegen.link](https://memegen.link) (no API key, no account, baked-in captions via URL parameters). To re-fetch all 14:

```bash
cd assets
python3 download-memes.py            # download all (skips existing)
python3 download-memes.py --list     # print the URLs without downloading
python3 download-memes.py --force    # re-download even if files exist
```

To swap a caption: edit the `MEMES` list at the top of `download-memes.py`, then run with `--force`. Three slide-version templates that memegen.link doesn't host (Bernie "once again asking", Patrick Typewriter, "We Did It Reddit") use documented substitutions — see comments in the script and `assets/meme-sources.md` for attribution.

### Run the starter stack locally

For testing the take-home stack on your laptop before the session:

```bash
cd pia-starter-stack
cp .env.example .env
# Edit .env — at minimum, set LISTMONK_DB_PASSWORD
docker compose up -d
```

- MkDocs at `http://localhost:8080`
- Listmonk at `http://localhost:9001` (run through the setup wizard on first boot)

The compose file binds all service ports to `127.0.0.1` only — the assumption is that an upstream tunnel (Pangolin/Newt by default; the `newt` service is in the compose) handles TLS and public exposure. Don't change the binds to `0.0.0.0` without thinking about what's in front of the box.

### Public deployment paths

Two supported, kept deliberately simple:

- **Caddy auto-TLS** (own server, own domain): `docker compose -f docker-compose.yml -f docker-compose.caddy.yml up -d`. The Caddyfile is referenced but not committed yet — create `pia-starter-stack/caddy/Caddyfile` with your domains.
- **Pangolin / Newt tunnel** (the n3-pia path used in the session): the `newt` service in the compose connects out to a Pangolin instance; resources configured in Pangolin's admin UI route public subdomains to loopback ports. No additional tunnel client needed on the host.

### Push a new Pangolin subdomain

To expose a new internal service on n3-pia (or any Newt-tunneled site) via a public subdomain, use `scripts/pangolin-push.py`. It drives Pangolin's [Integration API](https://docs.pangolin.net/manage/integration-api) so you don't have to click-drive the admin UI. Python 3 stdlib only.

Setup once: `cp scripts/.env.example scripts/.env`, then fill in two required values — `PANGOLIN_API_BASE` and `PANGOLIN_API_KEY`. **Note**: PIA's API lives at `https://api.bnkserve.org/v1`, *not* the admin-UI host `pangolin.bnkserve.org` (which serves the Next.js frontend and 401s the API). The optional defaults `PANGOLIN_DEFAULT_SITE=PIA-confrence-2026` and `PANGOLIN_DEFAULT_DOMAIN=publicinterestalberta.org` make most calls one-liners.

```bash
python3 scripts/pangolin-push.py --list                       # discover orgs/sites/domains
python3 scripts/pangolin-push.py docs nginx:80 --dry-run      # preview the two PUT bodies
python3 scripts/pangolin-push.py docs nginx:80                # create resource + target
python3 scripts/pangolin-push.py demo myservice:8080 --site changemaker-publicinterestalberta.org
```

Idempotent on `fullDomain` — re-running prints `SKIP` instead of clobbering. The script does **not** handle per-path rules (e.g. CryptPad's `/cryptpad_websocket → cryptpad:3003`); those are still UI-only because the public API docs don't expose that endpoint.

### Verify session URLs from the laptop

```bash
for sub in pad pad-sandbox pia2026 mail lander; do
  curl -sI -o /dev/null -w "${sub}: %{http_code}\n" \
    "https://${sub}.publicinterestalberta.org/"
done
```

All six should return `200` or `302` (note: `pia2026` will 404 until `mkdocs build` runs; `lander` is the Homepage dashboard at `homepage:3000` — confirm `HOMEPAGE_ALLOWED_HOSTS` in `.env` includes `lander.publicinterestalberta.org` or `*`). `502` = container down. TLS error = Pangolin resource not fully provisioned. DNS-fail = the CNAME for the subdomain isn't pointed at Pangolin. **CryptPad needs both `pad` AND `pad-sandbox` resources** — easy to miss, painful at 8am session-day.

## Excalidraw diagrams

Three illustrations in `assets/` are stored as `.excalidraw.md` files (Obsidian's Excalidraw plugin format — markdown with embedded JSON). They have to be exported to PNG from inside Obsidian (command palette → *Excalidraw: Switch to Excalidraw view* → *Export → PNG*) for the slide deck to embed them. Don't try to render them with shell tools — the format is plugin-specific.

## Key documents and their roles

| File | Role |
| --- | --- |
| `PIA-Session-2026.md` | Master plan: agenda, audience framing, 80-min cadence, take-home artifacts |
| `presenter-laptop-prep.md` | Step-by-step n3-pia + laptop infra setup. The operational doc on session day. |
| `handoff.md` | Day-before checklist. Already-done vs still-to-do. Treat as a working file, not a deliverable. |
| `foss-resources-handout.md` | Take-home one-pager. Goes live at `publicinterestalberta.org/resources/foss-campaigning/`. |
| `pia-starter-stack/README.md` | The public-facing README attendees see when they scan the repo QR. Write for strangers, not insiders. |

## Things to avoid

- **Don't commit `.env`** in `pia-starter-stack/` — only `.env.example`. The `.gitignore` allowlist covers this; don't override it.
- **Don't rename files from the shell.** They're referenced in slide decks and Obsidian backlinks across the parent vault. Use Obsidian's rename if you must.
- **Don't add PIA-specific content under `pia-starter-stack/`.** Branding, names, dates, and hardcoded session URLs all live at the top level — the starter stack is supposed to be useful to any small advocacy org. The one allowed bleed across the boundary is the `../scripts` mount on `code-server` (commented in `docker-compose.yml` for forkers to delete); don't add more parent-relative paths without a similarly clear note.
- **Don't change `pia-starter-stack/`'s license** without checking — AGPL-3.0 is deliberate and matches the rest of the BNKops ecosystem.
