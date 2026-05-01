# PIA-BNKOP-SERVER — Free & Open Source Campaigning

Materials and infrastructure for a Public Interest Alberta training session on running campaigns with Free and Open Source tools instead of renting them from political-industrial-complex vendors.

This repo is two things in one: the **session deliverables** (slides, handout, supporting notes) that anyone can read or remix, and the **starter stack** (`pia-starter-stack/`) — a forkable Docker Compose project that stands up an MkDocs research site and a Listmonk mailing list, ready for an organization to run on a five-dollar VPS.

## What's in here

| Path | What it is |
| --- | --- |
| [`PIA-Session-2026.md`](./PIA-Session-2026.md) | Session brief — agenda, audience, framing |
| [`presentation-slides.md`](./presentation-slides.md) | Full slide deck (canonical version) |
| [`presentation-slides-clean.md`](./presentation-slides-clean.md) | Same deck, no memes — for boardrooms |
| [`presentation-slides-memes.md`](./presentation-slides-memes.md) | Same deck, meme-augmented — for the room we're actually in |
| [`foss-resources-handout.md`](./foss-resources-handout.md) | One-pager attendees take home — tools, links, where to start |
| [`assets/`](./assets/) | Slide visuals: memes (auto-downloaded via `download-memes.py`), Excalidraw diagrams, meme attribution manifest |
| [`pia-starter-stack/`](./pia-starter-stack/) | The deliverable. MkDocs + Listmonk in Docker, with docs and a Caddy reverse-proxy variant |

## Use the starter stack

The stack is the part you're most likely here for. Clone it, edit `.env`, `docker compose up`, and you have a research microsite plus a mailing list running side-by-side. Full setup steps live in [`pia-starter-stack/README.md`](./pia-starter-stack/README.md).

## Use the slides

The decks are written in plain Markdown so they render cleanly in GitHub, in Obsidian, and in any Markdown-to-slides tool (Marp, Slidev, reveal.js). Pick whichever variant matches your audience. The meme version downloads its images via `assets/download-memes.py` from [memegen.link](https://memegen.link) — no API key, no account, no scraping.

## License

The starter stack carries its own license — see [`pia-starter-stack/LICENSE`](./pia-starter-stack/LICENSE). The training materials in this repo (slides, handout, manifest) are presenter-authored content; if you want to remix or re-deliver them, get in touch.

## Who runs this

Built and delivered by **The Bunker Operations** — an Edmonton-based worker co-op that builds, teaches, and distributes Free and Open Source infrastructure for movements, unions, and progressive organizations. If your org wants help standing this up, the first conversation is free.

[bnkops.com](https://bnkops.com) · admin@thebunkerops.ca
