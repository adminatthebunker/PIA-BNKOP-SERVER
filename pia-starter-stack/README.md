# PIA Starter Stack

A take-home campaign-comms stack for advocacy organizations. Co-designed at the *Free & Open Source Campaigning* session at Public Interest Alberta, 2026, and maintained as a living, forkable repo by [The Bunker Operations](https://bnkops.com).

One `docker-compose.yml`. A handful of services. Runs on any Linux machine with Docker. Replaces what most small advocacy orgs are paying Squarespace + Mailchimp for.

## What's in the stack

| Service | Replaces | Reachable from inside `pia-stack` network as |
| --- | --- | --- |
| **Newt** (Pangolin tunnel client) | Cloudflare Tunnel | *(forwards out to Pangolin — no listening port)* |
| **MkDocs Material** (dev server, hot-reload) | Squarespace / a half-built WordPress | `mkdocs:8000` |
| **Nginx** (serves the built `./site/` directory) | The above, in production | `mkdocs-site-server:80` |
| **Listmonk** + Postgres | Mailchimp / Constant Contact | `listmonk:9000` |
| **Apache Answer** | Stack Overflow Teams / Zendesk Guide | `answer:80` |
| **Homepage** ([gethomepage.dev](https://gethomepage.dev)) | Hand-rolled `index.html`, "where do I log in to ___?" Slack threads | `homepage:3000` |
| **Code Server** (web IDE — admin convenience) | SSH + vim | `127.0.0.1:8889` (host loopback — exception to no-host-ports rule) |
| **CryptPad** *(optional, session profile)* | Google Docs / Etherpad-as-SaaS | `cryptpad:3000` (HTTP) + `cryptpad:3003` (WS) |

**No host ports are bound.** The whole stack is reachable only from inside the `pia-stack` docker network. Newt is the one path in from the public internet (via Pangolin). For local testing without Pangolin, see "Quick start" below.

The MkDocs site is your org's public knowledge base — landing page, research, "subscribe" page, anything else. Edit `docs/*.md`, save, refresh; the dev server rebuilds. For production, run `mkdocs build` and let the Nginx service serve the static output. Listmonk handles email: subscriber lists, campaigns, sending. Homepage is the service dashboard for staff and members — point `lander.yourorg.org` at it and every other tool in the stack is one click away; config lives in [`configs/homepage/`](./configs/homepage/). CryptPad is session-only — it's the collaborative editor used during the live workshop, not something most forks of this stack need to run.

## Deployment assumption: there's a tunnel in front

This stack assumes a [Pangolin / Newt](https://docs.fossorial.io/) tunnel sits in front and handles TLS + host-header routing. Newt — the tunnel client — runs as a service inside this compose, on the same `pia-stack` docker network as everything else. Other services don't bind host ports at all; they're reachable only by service name (`listmonk:9000`, `cryptpad:3000`) from inside that network, which is exactly where newt is. Newt forwards traffic from your Pangolin server to those service:port targets per the resource rules you configure in Pangolin's UI. **There is no in-stack reverse proxy.**

If you use a different tunnel (Cloudflared, Tailscale Funnel) instead of Pangolin, comment out the `newt` service in `docker-compose.yml` and run your own tunnel client alongside the stack — everything else is tunnel-agnostic. If you have no tunnel at all and want to expose this to the public internet, you need to add a TLS layer (certbot + nginx, a separate Caddy instance, Cloudflare proxy mode at the DNS level) before doing so.

This is a deliberate scope choice: tunnel-fronted deployments are now the default Bunker pattern, and stacking a reverse proxy inside the compose to also do TLS was just duplicating what the tunnel already does.

## Hardware requirements

- Any Linux machine with **2 GB RAM** and **5 GB disk free** for the default profile. **4 GB / 10 GB** if you also run the `session` profile (CryptPad).
- Docker Engine and Docker Compose plugin installed.
- A domain name and a Pangolin/Newt site (or equivalent tunnel) for public access.

## Quick start (local, no tunnel)

For testing on your laptop or a home server before going public.

```bash
git clone https://git.publicinterestalberta.org/pia-starter-stack.git
cd pia-starter-stack

cp .env.example .env
# Edit .env — at minimum, set LISTMONK_DB_PASSWORD

docker compose --profile session up -d
```

### First-boot one-time steps

These are needed once on a fresh deployment. The compose file can't do them for you — they're side effects of how the upstream images are packaged.

**Listmonk database init** (Listmonk refuses to boot on an empty DB until you've explicitly initialized the schema):

```bash
docker compose run --rm listmonk ./listmonk --install --idempotent --yes
docker compose --profile session up -d listmonk   # restart it once init succeeds
```

**CryptPad data-directory ownership** (the upstream image runs as UID 4001 inside the container; bind-mounted host dirs default to root and the process can't write to them):

```bash
docker run --rm -v "$(pwd)/data/cryptpad:/data" alpine:3 chown -R 4001:4001 /data
docker compose --profile session restart cryptpad
```

**Build the static site** (Nginx serves a linuxserver welcome page until you populate `./site/` with `mkdocs build`):

```bash
docker compose run --rm mkdocs build
```

**Code Server** (only if using the upstream `codercom/code-server:latest` default — has no mkdocs preinstalled). Either install in-container once:

```bash
docker compose exec code-server bash -c "apt-get update -qq && apt-get install -y -qq python3-pip && pip install --break-system-packages 'mkdocs-material[recommended]'"
```

(Note: install lives in the container's writable layer — survives restarts, lost on `--force-recreate`. For permanence, build a custom code-server image with mkdocs baked in.)

Then visit `http://localhost:8889/` (or via SSH tunnel for remote), log in with `CODE_SERVER_PASSWORD` from `.env`, open the workspace, run `mkdocs build` from the integrated terminal.

### Hitting services for testing

Backend services don't bind host ports — hit them from inside the `pia-stack` network:

```bash
docker run --rm --network pia-stack curlimages/curl:latest -sI http://mkdocs:8000/
docker run --rm --network pia-stack curlimages/curl:latest -sI http://listmonk:9000/
docker run --rm --network pia-stack curlimages/curl:latest -sI http://mkdocs-site-server:80/
docker run --rm --network pia-stack curlimages/curl:latest -sI http://homepage:3000/
docker run --rm --network pia-stack curlimages/curl:latest -sI http://cryptpad:3000/
```

Once you're testing for real, configure Pangolin (or whichever tunnel) to expose the services to the public internet — see *Public deployment* below.

## Editing the docs site

The dev server rebuilds automatically when you edit markdown:

- **Home page** — `docs/index.md`
- **Research** — `docs/research.md`
- **Subscribe** — `docs/subscribe.md`
- **Add a new page** — drop a `.md` file under `docs/`, then add an entry to `nav:` in `mkdocs.yml`

The site name, theme colour, and navigation order live in `mkdocs.yml`. Edit there once at the start.

For the production-grade Nginx serve, build the static site:

```bash
docker compose run --rm mkdocs mkdocs build
```

This drops a static bundle into `./site/`, which the Nginx service serves immediately. Re-run after each content change — the static server does not auto-rebuild.

## Public deployment with Pangolin/Newt

The newt client is bundled in this compose; you just need to point it at your Pangolin instance and register the resources.

**1. Register this host in Pangolin.** In the Pangolin admin UI, add a new site of type `newt`. It generates a `NEWT_ID` and `NEWT_SECRET`. Paste both into your `.env` along with `PANGOLIN_ENDPOINT` (the public URL of your Pangolin server). Bring the stack up — newt connects out and registers itself.

**2. Add a Pangolin resource per subdomain you want public.** Each resource forwards to one or more docker service names on the `pia-stack` network — no host ports involved:

| Subdomain | Target(s) |
| --- | --- |
| `docs.yourorg.org` | `mkdocs-site-server:80` *(static Nginx — production)* or `mkdocs:8000` *(dev MkDocs — hot reload, useful during the session)* |
| `mail.yourorg.org` | `listmonk:9000` |
| `answers.yourorg.org` | `answer:80` *(visit `/install` once on first boot to run the setup wizard)* |
| `lander.yourorg.org` | `homepage:3000` *(service dashboard — set `HOMEPAGE_ALLOWED_HOSTS=lander.yourorg.org` in `.env` once you've picked the public hostname)* |
| `pad.yourorg.org` | **Two targets** — see CryptPad notes below |
| `pad-sandbox.yourorg.org` | `cryptpad:3000` *(same backend as `pad.*`; sandbox separation is by Host header)* |

In each Pangolin resource: leave **Match Path** empty for the default HTTP target. Use a **Prefix** match only when you need to send a specific path to a different upstream port (the CryptPad WebSocket is the only example here). Leave **Rewrite Path** blank — that field expects a path replacement (e.g. `/`), not a host:port.

Pangolin handles TLS via Let's Encrypt at the tunnel edge.

### CryptPad gotchas

These will catch you out at 8am session-day if you miss them:

- **Two Pangolin resources, not one.** Both `pad.*` and `pad-sandbox.*` need their own resource, both pointing at `cryptpad:3000`. CryptPad enforces sandbox separation by Host header, so the sandbox subdomain has to actually resolve. If only `pad.*` works, the editor loads but the editing surface stays blank.
- **The `pad.*` resource needs two targets.** A default target (no Match Path) → `cryptpad:3000` for all HTTP, plus a second target with **Prefix** match `/cryptpad_websocket` → `cryptpad:3003` for the WebSocket. The WS port is **3003**, not 3013.
- **`CRYPTPAD_MAIN_DOMAIN` and `CRYPTPAD_SANDBOX_DOMAIN` in `.env` must match the Pangolin URLs character-for-character.** CryptPad bakes them into its `Content-Security-Policy` response header. A single-letter typo (e.g. `publicinterstalberta` vs `publicinterestalberta`) means the browser refuses to load CryptPad's own assets — page goes blank with `(index)` and `/favicon.ico` 404s in DevTools. Restart the container after editing `.env`.

## Running the session profile (CryptPad)

CryptPad lives behind a profile so default `docker compose up` doesn't drag it along for forks that don't want it.

```bash
# Set your CryptPad domains in .env first.
docker compose --profile session up -d
```

Bring it down without affecting the rest of the stack:

```bash
docker compose --profile session down
```

## Customizing for your org

The stack is intentionally minimal so you can fork it and change things without untangling layers.

- **Add a service** — drop a new entry in `docker-compose.yml`, declare its container port via `expose:`, register a Pangolin resource pointing at `<service-name>:<port>`.
- **Swap MkDocs for something heavier** — Ghost (newsletter-shaped), Hugo (static-site generator), WordPress (kitchen sink) all fit the same slot.
- **Drop a service** — comment it out in `docker-compose.yml`. The stack is loosely coupled; nothing breaks.

## Operational reality

Self-hosting is not free. It costs maintenance hours instead of dollars. Specifically:

- **Backups.** Decide your story before you put anything important in this stack. Listmonk's database is in a named volume (`listmonk-db`); CryptPad's data lives under `./data/cryptpad/`. Back both off-host. Markdown content in `./docs/` lives in your Git repo, which is its own backup if you're pushing regularly. A second copy in a different physical location, tested at least quarterly.
- **Updates.** `docker compose pull && docker compose up -d` once a month minimum. Subscribe to the MkDocs Material, Listmonk, and CryptPad release notes.
- **Email deliverability.** Listmonk needs an SMTP relay (Postmark, SES, Mailgun, Scaleway) to land in inboxes reliably. Don't try to run your own outbound mail server.
- **Monitoring.** Bare minimum: Uptime Kuma. Free, single container, will text you when something dies.

If your org wants help with any of this, talk to us. The first conversation is free. — [bnkops.com](https://bnkops.com) · admin@thebunkerops.ca

## Contributing

This repo is the canonical home of the PIA starter stack. Issues and PRs welcome.

The session at PIA 2026 captured a list of additions for v0.2 in the linked CryptPad. Those become tracked issues here.

## License

AGPL-3.0. Same as the rest of the BNKops ecosystem.

---

*Co-designed live at Public Interest Alberta 2026. Maintained by The Bunker Operations.*
