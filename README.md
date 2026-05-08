# PIA-BNKOP-SERVER

Materials and infrastructure from a Public Interest Alberta training session — *Free & Open Source Campaigning* — on running campaigns with FOSS instead of renting them from political-industrial-complex vendors.

The session is over. What's left is the part that's still useful: a forkable Docker Compose stack any small advocacy org can stand up on a five-dollar VPS, plus the resource handout we wrote for the room.

---

## :rocket: Stand up the stack

The deliverable lives in **[`pia-starter-stack/`](./pia-starter-stack/)**. One `docker-compose.yml`, eight services (MkDocs, Listmonk, Apache Answer, [Homepage](https://gethomepage.dev/) dashboard, code-server, Nginx, a Pangolin tunnel client, and optional CryptPad), about ten minutes from `git clone` to live URLs.

**→ Full setup steps: [`pia-starter-stack/README.md`](./pia-starter-stack/README.md)**

If you only want the headlines:

```bash
git clone https://git.publicinterestalberta.org/pia-starter-stack.git
cd pia-starter-stack
cp .env.example .env
# edit .env — at minimum, set LISTMONK_DB_PASSWORD
docker compose up -d
```

That's it for local testing. For public deployment with TLS, see the [Public deployment](./pia-starter-stack/README.md#public-deployment-with-pangolinnewt) section of the stack's README.

---

## :books: Read the handout

The take-home resource list — what to use instead of Mailchimp, Squarespace, Eventbrite, Google Docs, etc., with a Canadian-context section — is published as a page on the same MkDocs site the stack ships:

**→ [pia2026.publicinterestalberta.org/resources/](https://pia2026.publicinterestalberta.org/resources/)**

The source is at [`pia-starter-stack/docs/resources.md`](./pia-starter-stack/docs/resources.md). Fork it, edit it for your members, host it yourself.

---

## :wrench: Operator tooling

[`scripts/pangolin-push.py`](./scripts/pangolin-push.py) — one-shot subdomain provisioning for [Pangolin](https://docs.pangolin.net) instances. If you're running this stack behind a Pangolin/Newt tunnel and want to expose a new service without click-driving the admin UI, this is for you:

```bash
python3 scripts/pangolin-push.py --list                  # see orgs/sites/domains
python3 scripts/pangolin-push.py docs nginx:80           # create resource + target
```

Auto-discovers org/site/domain IDs from friendly names; idempotent on `fullDomain`. Python stdlib only — no `pip install`. See [`scripts/README.md`](./scripts/README.md).

---

## What's in this repo

| Path | What it is |
| --- | --- |
| [`pia-starter-stack/`](./pia-starter-stack/) | **The take-home.** Forkable Docker Compose project. Has its own README, license, `.env.example`. |
| [`scripts/`](./scripts/) | Operator tooling — currently `pangolin-push.py` (above). Presenter-side, not part of the take-home. |
| [`assets/`](./assets/) | Slide visuals — memes (auto-downloaded via `download-memes.py`), Excalidraw diagrams, attribution manifest. |
| [`archive/`](./archive/) | Session materials — slide decks (clean / annotated / meme variants), session brief, presenter prep notes. Kept for reference; not actively maintained. |
| [`CLAUDE.md`](./CLAUDE.md) | Project instructions for Claude Code working in this repo. |

---

## License

The starter stack carries its own license — see [`pia-starter-stack/LICENSE`](./pia-starter-stack/LICENSE) (AGPL-3.0).

The training materials in [`archive/`](./archive/) are presenter-authored content. Remix or re-deliver with attribution; get in touch if you'd like help adapting them.

## Who runs this

Built and delivered by **[The Bunker Operations](https://bnkops.com)** — an Edmonton-based worker co-op that builds, teaches, and distributes Free and Open Source infrastructure for movements, unions, and progressive organizations. If your org wants help standing this up, the first conversation is free.

[bnkops.com](https://bnkops.com) · admin@thebunkerops.ca
