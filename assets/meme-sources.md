# Meme & Image Sources — PIA Session 2026

Manifest of every visual referenced in `presentation-slides-memes.md`. Most memes are **auto-downloaded** by `download-memes.py` via [memegen.link](https://memegen.link) (open-source, free, no API key). Three illustrations are provided as Excalidraw files in this same folder. One real photo is yours to take.

## How to populate this folder

```bash
cd /path/to/pia-session/assets
python3 download-memes.py            # downloads 14 captioned PNGs
python3 download-memes.py --list     # show URLs without downloading
python3 download-memes.py --force    # re-download even if files exist
```

Then open the three `.excalidraw.md` files in Obsidian (command palette → *Excalidraw: Switch to Excalidraw view*) and *Export → PNG* to produce `.png` siblings the slide deck can embed.

Finally take the Lenovo photo with your phone, save as `photo-pia-server.jpg`.

## Manifest

| # | Filename | Slide | Source | memegen ID | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | `meme-always-has-been.png` | The Political Industrial Complex | memegen.link | `astronaut` | Always Has Been |
| 2 | `meme-this-is-fine.png` | We lose | memegen.link | `fine` | This Is Fine |
| 3 | `meme-same-picture.png` | You have seen this movie | memegen.link | `same` | They're The Same Picture (Pam line is template-baked-in; we only supply the two paper labels) |
| 4 | `meme-and-its-gone.png` | What you're actually renting | memegen.link | `gone` | And It's Gone (South Park) |
| 5 | `meme-change-my-mind.png` | What is FOSS | memegen.link | `cmm` | **Substituted from Bernie "Once Again Asking"** — memegen has no Bernie template. Change My Mind is stronger here anyway (dare-to-disagree framing). |
| 6 | `meme-galaxy-brain.png` | Translated to your work | memegen.link | `gb` | Galaxy Brain (4-panel) |
| 7 | `meme-distracted-boyfriend.png` | What it costs you | memegen.link | `db` | Distracted Boyfriend |
| 8 | `meme-spiderman-pointing.png` | But who maintains it? | memegen.link | `spiderman` | Spider-Man Pointing |
| 9 | `diagram-thousand-lists.excalidraw.md` | The thesis | **Excalidraw** (in this folder) | — | Centralized vs. distributed network. Open in Obsidian Excalidraw, export PNG. |
| 10 | `photo-pia-server.jpg` | The Bunker thesis | **Phone photo** (Reed) | — | Plain background, coffee mug for scale. Take before session. |
| 11 | `illustration-tag-yourself-btd.excalidraw.md` | Build · Teach · Distribute | **Excalidraw** (in this folder) | — | Three-panel Builder/Teacher/Distributor. Open in Obsidian Excalidraw, export PNG. |
| 12 | `meme-roll-safe.png` | Your task | memegen.link | `rollsafe` | **Substituted from Patrick-with-typewriter** — memegen has no Patrick Typewriter. Roll Safe fits the "you've got this" energy. |
| 13 | `meme-success-kid.png` | The site you just built | memegen.link | `success` | **Substituted from "We Did It Reddit"** — memegen has no Reddit template. Success Kid is the canonical celebration meme. |
| 14 | `meme-wonka.png` | And here is the repo | memegen.link | `wonka` | Condescending Wonka |
| 15 | `meme-oprah.png` | (alternative to Wonka, also downloaded) | memegen.link | `oprah` | Oprah You Get A — pick whichever lands better in rehearsal |
| 16 | `illustration-worker-coop.excalidraw.md` | The Bunker Operations | **Excalidraw** (in this folder) | — | Hammer crossed with laptop. Open in Obsidian Excalidraw, export PNG. |
| 17 | `meme-epic-handshake.png` | The ask | memegen.link | `handshake` | Epic Handshake |
| 18 | `meme-bugs-our.png` | Nothing to lose | memegen.link | `cbb` | Communist Bugs Bunny |

## How memegen.link works (short version)

URL pattern: `https://api.memegen.link/images/<template>/<line1>/<line2>.png?width=1200`

Captions are baked into the image at request time. Special characters in captions get encoded (`_` → `__`, ` ` → `_`, etc.) — `download-memes.py` handles this. To change a caption, edit the relevant entry in the script and re-run with `--force`.

To browse other templates: <https://api.memegen.link/templates>

## Why not imgflip?

We tried first. Imgflip lazy-loads template images via JavaScript and Cloudflare blocks slug-based CDN paths to bot fetches. Wikimedia doesn't host most meme templates (copyright). Without imgflip's paid API, bulk-download isn't viable from there. memegen.link is purpose-built for this — open-source, free, returns final PNGs directly.

## Attribution & licensing notes

- memegen.link images carry a small "memegen.link" watermark in the corner. Acceptable for a session deck; if you want it removed, the project supports a self-hosted deployment.
- The meme templates themselves are mostly fair-use parody under most jurisdictions, but the underlying photos (e.g. *Distracted Boyfriend*'s stock shot by Antonio Guillem) have copyright. Don't sell t-shirts of these.
- The Excalidraw drawings and your Lenovo photo are yours.
