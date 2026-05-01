#!/usr/bin/env python3
"""
Downloads captioned meme images for the PIA Session deck via memegen.link.

memegen.link is a free, open-source meme API — no key, no Cloudflare blocking,
direct PNG output. Captions are baked in via URL parameters so what you
download is the final captioned image (no further editing needed).

Usage:
    python3 download-memes.py            # download all
    python3 download-memes.py --list     # print URLs without downloading
    python3 download-memes.py --force    # re-download even if files exist

Three of the meme-version slides specified templates that memegen.link
doesn't host (Bernie I-Am-Once-Again-Asking, Patrick Typewriter, We Did It
Reddit). For those, on-brand substitutions are used and noted below.
"""
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ASSETS = Path(__file__).resolve().parent
BASE = "https://api.memegen.link/images"
WIDTH = 1200  # high-res output

# (filename, template_id, [caption_lines])
# Captions follow the conventions in meme-sources.md.
# Substitutions are flagged in comments.
MEMES = [
    (
        "meme-always-has-been.png",
        "astronaut",
        ["Wait — the same SaaS sells to my union AND the cops?", "Always has been."],
    ),
    (
        "meme-this-is-fine.png",
        "fine",
        ["Our movement, on Mailchimp."],
    ),
    (
        "meme-same-picture.png",
        "same",
        [
            # Pam's "they're the same picture" line is baked into this template,
            # so we only supply the two paper labels.
            "Twitter / Reddit / Substack / Mailchimp",
            "An enshittification curve",
        ],
    ),
    (
        "meme-and-its-gone.png",
        "gone",
        [
            "Your subscriber list when you try to export it",
            "Aaaaand it's gone.",
        ],
    ),
    # SUBSTITUTION: memegen has no Bernie "I Am Once Again Asking".
    # Change My Mind is a stronger fit anyway — direct dare-to-disagree energy.
    (
        "meme-change-my-mind.png",
        "cmm",
        ["Open-source software is the only honest answer for an advocacy org. Change my mind."],
    ),
    (
        "meme-galaxy-brain.png",
        "gb",
        [
            "Pay Mailchimp $300/month",
            "Self-host Listmonk on a VPS",
            "Self-host Listmonk on a $150 used Lenovo",
            "...that ALSO runs your docs site, calendar, and CRM",
        ],
    ),
    (
        "meme-distracted-boyfriend.png",
        "db",
        [
            "Your campaign budget",
            "Mailchimp ($20K / 5 yrs)",
            "Listmonk ($600 / 10 yrs) + everything else you could fund",
        ],
    ),
    (
        "meme-spiderman-pointing.png",
        "spiderman",
        [
            "You, paying for Mailchimp's maintenance",
            "You, doing your own maintenance",
        ],
    ),
    # SUBSTITUTION: memegen has no Patrick Typewriter. Roll Safe (point-at-head)
    # has the right "you've got this" energy for a writing-task slide.
    (
        "meme-roll-safe.png",
        "rollsafe",
        ["Can't lose 25 minutes drafting", "if your group already has a doc open."],
    ),
    # SUBSTITUTION: memegen has no "We Did It Reddit". Success Kid is the
    # canonical celebration meme; same payload.
    (
        "meme-success-kid.png",
        "success",
        ["Built a public website together", "in 80 minutes."],
    ),
    (
        "meme-wonka.png",
        "wonka",
        [
            "Tell me again how Mailchimp's price",
            "will only go up.",
        ],
    ),
    (
        "meme-oprah.png",
        "oprah",
        [
            "You get a starter stack!",
            "EVERYBODY gets a starter stack!",
        ],
    ),
    (
        "meme-epic-handshake.png",
        "handshake",
        ["BNKops + your org", "Sovereign infrastructure"],
    ),
    (
        "meme-bugs-our.png",
        "cbb",
        ["Infrastructure, members, lists,", "tools, futures... ours."],
    ),
]


def encode_caption(text: str) -> str:
    """memegen.link path-style encoding rules.
    See https://memegen.link/templates/ for the canonical reference."""
    if not text or text.strip() == "":
        return "_"
    # Order matters: do _ → __ before space → _, otherwise we double-encode.
    text = text.replace("_", "__")
    text = text.replace("-", "--")
    text = text.replace(" ", "_")
    text = text.replace("?", "~q")
    text = text.replace("&", "~a")
    text = text.replace("%", "~p")
    text = text.replace("#", "~h")
    text = text.replace("/", "~s")
    text = text.replace("\\", "~b")
    text = text.replace("<", "~l")
    text = text.replace(">", "~g")
    text = text.replace('"', "''")
    text = text.replace("\n", "~n")
    return urllib.parse.quote(text, safe="_-~'.,()!:;")


def build_url(template: str, captions: list[str], filename: str) -> str:
    # Path-style: /images/<template>/<line1>/<line2>.png?width=N
    encoded = "/".join(encode_caption(c) for c in captions)
    return f"{BASE}/{template}/{encoded}.png?width={WIDTH}"


def main():
    args = sys.argv[1:]
    list_only = "--list" in args
    force = "--force" in args

    if list_only:
        print(f"{'FILENAME':<32}  URL")
        print(f"{'-' * 32}  ---")
        for filename, tpl, caps in MEMES:
            url = build_url(tpl, caps, filename)
            print(f"{filename:<32}  {url}")
        return

    ok = fail = skip = 0
    for filename, tpl, caps in MEMES:
        out = ASSETS / filename
        if out.exists() and not force:
            print(f"SKIP  {filename} (exists; --force to re-download)")
            skip += 1
            continue

        url = build_url(tpl, caps, filename)
        print(f"GET   {filename:<32} ", end="", flush=True)
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "pia-session-meme-downloader/1.0"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                if not data.startswith(b"\x89PNG"):
                    print(f"FAIL (not PNG, got {data[:8]!r})")
                    fail += 1
                    continue
                out.write_bytes(data)
                print(f"OK ({len(data):,} bytes)")
                ok += 1
        except Exception as e:
            print(f"FAIL ({e})")
            fail += 1

    print()
    print(f"Summary: {ok} ok, {fail} failed, {skip} skipped")
    if ok:
        print(f"Files saved in {ASSETS}/")


if __name__ == "__main__":
    main()
