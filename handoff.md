# Handoff — Morning of May 1, 2026

Good morning. Coffee, then this doc, then in this order: review, infrastructure, visuals, rehearse. By end of day you should be presentation-ready.

This file is your start-here. Everything else in this folder supports it.

---

## TL;DR — what's left

In rough priority order, with rough time estimates:

- [ ] **Review the slide deck you'll actually present from** (~25 min)
- [ ] **Stand up CryptPad + the starter stack on n3-pia** (~60–90 min)
- [ ] **Wire up the Pangolin resources** for five new subdomains (~20 min)
- [ ] **Push the `pia-starter-stack` repo to its public Git home** (~10 min)
- [ ] **Take the Lenovo phone photo + export the three Excalidraw illustrations** (~15 min)
- [ ] **Rehearse the live-publish workflow** (CryptPad → SSH → save → refresh) (~30 min, do this at least twice)
- [ ] **Print QR cards** (~10 min once URLs are locked)
- [ ] **Decide pricing for a CMlite pilot** — someone will ask Friday at 8pm (~15 min thinking, write it down)

Total: ~3.5 hours of focused work. You can be done before lunch if you don't get pulled into other stuff.

---

## What's in this folder (the inventory)

If you need to remind yourself what each file does:

| File | Role |
| --- | --- |
| `handoff.md` | This document |
| `PIA-Session-2026.md` | Cadence + logistics + framing notes (the master plan) |
| `presentation-slides.md` | Annotated deck — speaker notes inline, for rehearsal |
| `presentation-slides-clean.md` | Projection deck — no notes, for the venue projector |
| `presentation-slides-memes.md` | Same as clean, with meme images embedded |
| `presenter-laptop-prep.md` | Step-by-step infra setup for n3-pia + your laptop |
| `foss-resources-handout.md` | Take-home resource list, deployed to publicinterestalberta.org/resources/foss-campaigning/ |
| `pia-starter-stack/` | The forkable Git repo — MkDocs + Listmonk. The deliverable. |
| `assets/` | Memes (downloaded), Excalidraw illustrations, the meme manifest |

---

## Step 1 — Review my work (25 min)

Read in this order. Mark anything off:

- [ ] **`PIA-Session-2026.md`** — confirm the 80-minute cadence still matches your intent. Specifically: 28 min for the talk, 27 min of group writing, 15 min of live publishing, 7 min closing. If anything feels off, fix it now before you build infra against it.
- [ ] **One slide deck** — pick the one you'll actually present from:
  - **`presentation-slides-memes.md`** if you want warmth/levity (likely yes for PIA)
  - **`presentation-slides-clean.md`** if you want neutral/buttoned-up
  - The annotated version is for rehearsal only — don't project it
- [ ] **`presenter-laptop-prep.md`** — read the Architecture section + Steps 1–8. This is the doc you'll work from in Step 2 below.
- [ ] **`pia-starter-stack/README.md`** — make sure the take-home README reads cleanly. This is what attendees will see when they scan the repo QR.
- [ ] **`foss-resources-handout.md`** — read top-to-bottom once. This goes on PIA's site as the take-home reference.

If anything is wrong or sounds off, mark it. Don't fix mid-review — finish the read first, then go back.

---

## Step 2 — Infrastructure setup on n3-pia (60–90 min)

Follow `presenter-laptop-prep.md` literally. Tracks 1 through 4. Quick summary of what needs to exist by the end:

- [ ] **Repo published** at `git.publicinterestalberta.org/pia-starter-stack` (or `repo.bnkops.com/pia-starter-stack` — pick one and stay there)
- [ ] **All starter-stack services running** on n3-pia (`docker compose --profile session ps` shows six `Up`):
  - MkDocs dev → `mkdocs:8000` (docker network only)
  - Nginx static → `mkdocs-site-server:80` (docker network only — *404 until `mkdocs build` runs, expected*)
  - Listmonk → `listmonk:9000` (docker network only)
  - CryptPad → `cryptpad:3000` (HTTP) + `cryptpad:3003` (WS) (docker network only)
  - Newt → forwards out to Pangolin (no listening port)
  - Code Server → `127.0.0.1:8889` *(host loopback — reach via SSH tunnel from laptop, do NOT publicly expose)*
- [ ] **Pangolin resources added** for five hostnames:
  - `pad.publicinterestalberta.org` *(CryptPad)*
  - `pad-sandbox.publicinterestalberta.org` *(CryptPad sandbox origin)*
  - `live.publicinterestalberta.org` *(MkDocs dev server, port 8080 — used DURING the session for hot-reload)*
  - `pia2026.publicinterestalberta.org` *(Nginx serving the built static site, port 4004 — the permanent post-session URL)*
  - `mail.publicinterestalberta.org` *(Listmonk, optional)*
- [ ] **DNS records pointing at Pangolin** for all five subdomains (Pangolin auto-issues TLS once DNS resolves)
- [ ] **All five URLs return 2xx/3xx** when curl'd from anywhere

Verification one-liner (from your laptop):

```bash
for sub in pad pad-sandbox live pia2026 mail; do
  curl -sI -o /dev/null -w "${sub}: %{http_code}\n" \
    "https://${sub}.publicinterestalberta.org/"
done
```

All five should be `200` or `302`. (Note: `pia2026` will return 404 from Nginx until you've run `mkdocs build` to populate `./site/` — that's expected before the session climax.) If you get `502`, the container's down. If you get a TLS error, the Pangolin resource isn't fully provisioned yet (DNS may still be propagating, or the cert hasn't issued). If you get DNS-fail, the CNAME wasn't added or hasn't propagated.

**Critical: CryptPad needs both `pad` AND `pad-sandbox` to work.** If only one is routed, the editor loads but the actual editing surface won't render. Easy mistake; painful to debug at 8am session-day.

---

## Step 3 — Visuals (15 min)

- [ ] **Open the three `.excalidraw.md` files** in Obsidian (command palette → *Excalidraw: Switch to Excalidraw view*) — `assets/diagram-thousand-lists`, `assets/illustration-tag-yourself-btd`, `assets/illustration-worker-coop`. Look at each. Reposition or recolour anything that bugs you. *Export → PNG* into `assets/` for each one (so the slide deck can embed them).
- [ ] **Take the Lenovo photo** with your phone. Plain background. Coffee mug for scale. Save to `assets/photo-pia-server.jpg`.
- [ ] **A/B the Wonka vs Oprah meme** for the repo-reveal slide — both downloaded in `assets/`. Pick whichever feels right; the slide currently references `meme-wonka.png`. If you switch, edit the wikilink in `presentation-slides-memes.md`.
- [ ] **Run `python3 download-memes.py --list`** in `assets/` to see all 14 captioned-meme URLs in case you want to re-render any with different text. Edit `download-memes.py` and re-run with `--force` to swap captions.

---

## Step 4 — QR cards (10 min)

Once your URLs are locked, generate the four cards. From your laptop:

```bash
cd ~/pia-demo  # or wherever you want them saved
qrencode -o qr-repo.png      "https://git.publicinterestalberta.org/pia-starter-stack"
qrencode -o qr-handout.png   "https://publicinterestalberta.org/resources/foss-campaigning/"
qrencode -o qr-cryptpad.png  "https://pad.publicinterestalberta.org/pad/<your-pad-id>"
qrencode -o qr-livesite.png  "https://live.publicinterestalberta.org/"
qrencode -o qr-permanent.png "https://pia2026.publicinterestalberta.org/"
```

Print one of each per table. Bring spares — they get coffee on them.

---

## Step 5 — Practice run (30 min, do twice)

Two rehearsals matter more than three:

### Rehearsal A — the talk itself (15 min)

Run the deck end-to-end at speaking pace. Time each section against the cadence in `PIA-Session-2026.md`:

- 0–5: Intro
- 5–10: Frame the stakes
- 10–22: FOSS + urgency talk (**hard cap 12 min — practice ending here even if you have more to say**)
- 22–32: PIA server tour (live demo — be ready to switch to the docs vault, Cockpit, the tunnel)
- 32–38: Introduce starter stack
- 38–55: Group writing (you walk the room — practice the prompt + how you'll get groups unstuck)
- 55–70: Pull + publish (the **finger-flow** — see Rehearsal B below)
- 70–73: Site reveal moment
- 73–80: Closing + the ask

If your talk runs over 22 minutes, *cut now*. The "Translated to your work" table can be glanced at, not read. The "Governments are doing this" slide can be a 10-second beat. Be ruthless.

### Rehearsal B — the publish workflow (15 min)

This is the technical-execution rehearsal. End-to-end:

1. SSH from your laptop into n3-pia (`ssh n3-pia`).
2. Open VS Code with Remote-SSH connected to `/srv/pia-session/pia-starter-stack/` — or whatever editor you chose.
3. Open the CryptPad in another browser tab.
4. From a second device or your phone, type a paragraph into the pad's "Group 1" section.
5. Copy that section's markdown.
6. Paste into a new file `docs/research/group-1.md`.
7. Save. Refresh `https://live.publicinterestalberta.org/research/group-1/` on your phone — the dev server should already have hot-reloaded.
8. **Time the whole loop.** Should be under 30 seconds with VS Code, under 60 with vim.

Do this twice. The choreography is what matters — practice the *finger-flow* until you're not thinking about it.

If anything in the loop is fragile (slow rebuild, cert weirdness, SSH dropping), fix before the day. The Claude Code live-debug agent is a safety net, not a rehearsal substitute.

### Bonus — record the backup

Once the workflow works clean, record a 60-second screen capture of you doing one full pull-paste-refresh cycle. Save to a known location on your laptop. If the live version stalls past your patience threshold, you cut to this and narrate over it — no one will know the difference.

---

## Step 6 — Decisions only you can make

These are sitting open. Don't go on stage with any of them unresolved.

- [ ] **CMlite pilot pricing.** Have a real number. "$X for setup + sliding-scale monthly $Y–Z" is the format. Someone will ask Friday at 8pm at the bar; "let me get back to you" is the wrong answer.
- [ ] **Sign-up form URL** for the warm-lead list. Either a Listmonk subscription form on the live demo or a CryptPad form or a paper sheet. Decide and have the QR ready.
- [ ] **Whether to demo Listmonk live** during the session. The deck has it as optional. If you do, you also need `mail.publicinterestalberta.org` working and a story for what to demo (creating a list? sending a test campaign?). If you don't, drop the `mail` subdomain from the prep checklist and don't generate that QR.
- [ ] **Ghost vs Wonka for the repo-reveal slide** — wait, that's a typo, I mean Wonka vs Oprah. Pick one.
- [ ] **Whether to mention Israel/Palestine on the PIC slide.** The current line ("the agencies surveilling you all") is deliberately neutral. Reed's de-corp essay is more direct (calls Google's Project Nimbus by name). PIA crowd is progressive enough that the harder line will land — but it's also a derail risk if you don't want the Q&A to go there. Your call.

---

## Risks / what could actually go wrong

In rough order of probability × impact:

1. **CryptPad's two-domain requirement bites you on the day.** If `pad-sandbox` isn't routed properly the editor won't render. Verify in Step 2 *before* you create the pad.
2. **Newt tunnel drops mid-session.** If `newt` exits, all five subdomains stop resolving until it reconnects. Plan: `docker compose restart newt` on n3-pia (~10s recovery), narrate while it reconnects. Don't apologize past the 10-second mark. The Pangolin server itself dropping is unlikely but more painful — no quick fix from session-day Reed.
3. **Conference WiFi blocks something.** Cell-data tether on your phone as backup. CryptPad and the live site are both on PIA's domain — if any standard HTTPS gets through, you're fine. If conference WiFi is a captive portal that blocks WebSockets, CryptPad's collaborative editing degrades — fall back to typing the markdown directly.
4. **A pasted section breaks MkDocs YAML rendering.** Container exits, site shows last good build. Recovery: `docker compose logs mkdocs | tail -20` to find the offender, edit or delete, container restarts. Practice this once in Rehearsal B.
5. **Your laptop dies.** The Claude Code live-debug agent has SSH to n3-pia. They can run the publish workflow from their machine. Make sure they know the workflow before the day.
6. **No one writes anything in the pad.** Wait 30 seconds, then prompt directly: "Group at the back table — what tool are you replacing?" Eye contact. They will.

---

## What's done (so you don't redo it)

For your sanity:

- ✅ Cadence + framing locked
- ✅ Three slide decks written and voice-passed for tone
- ✅ Starter-stack repo scaffolded, AGPL-licensed, ready to push
- ✅ FOSS resource handout written
- ✅ Server-side prep doc written for n3-pia
- ✅ All 14 memes downloaded and captioned via memegen.link
- ✅ Three Excalidraw illustrations created (network diagram, BTD three-panel, worker-coop)
- ✅ Meme sourcing manifest documents every visual
- ✅ All references to old architectures (Bunker Pangolin, attendee Docker installs, Obsidian pre-reqs, etc.) cleaned out

---

## Tomorrow's ideal sequence

If you want a literal hour-by-hour:

| Time | Task |
| --- | --- |
| 8:00–8:30 | Coffee. Read this doc. Read the slide deck you're presenting from. |
| 8:30–10:00 | Stand up the starter stack on n3-pia (`--profile session` for CryptPad). Configure Pangolin resources. Verify all URLs. |
| 10:00–10:30 | Push repo. Generate QR cards. Take Lenovo photo. Export Excalidraw PNGs. |
| 10:30–11:30 | Rehearsal A — talk only. Time it. Cut what's over. |
| 11:30–12:30 | Lunch. Walk. Don't think about it. |
| 12:30–13:30 | Rehearsal B — publish workflow. Twice. Record the backup. |
| 13:30–14:00 | Decisions list (pricing, optional Listmonk, etc.). Write down answers. |
| 14:00 | Done. Either you're presentation-ready or you've found a real problem worth fixing. |

If something's broken at 14:00, you have the rest of the day — that's the buffer. Use it for one thing, not for fiddling with five.

---

## When in doubt

The repo URL slide is the deliverable. The room writing into a pad and watching their words go public is the climax. Everything else is supporting material.

You've built this thing through fifteen architecture pivots. The current shape is clean. Trust it.

— Claude
