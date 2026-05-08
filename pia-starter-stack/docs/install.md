# Install for beginners

This guide is for people who've **never run a server before**. It walks through Docker, Docker Compose, and the whole "I have a Linux box and a domain — now what?" pipeline, ending with this stack live on the public internet.

If you already know Docker, the [README](https://github.com/adminatthebunker/PIA-BNKOP-SERVER/tree/main/pia-starter-stack#quick-start) has a five-line quick start. Come back here when something breaks and you want the longer explanation.

Plan on **45–90 minutes** the first time. Most of that is reading and waiting for installs to finish.

## The mental model

Before any commands, the concepts. Skipping this is the #1 reason self-hosting feels confusing later.

### What is a server?

A **server** is just a computer that's always on, connected to the internet, and runs programs that other computers ("clients" — your laptop, your phone) talk to over the network. A laptop running a website at `localhost:8080` is technically a server too; it's just not reachable from outside your house.

For this stack, you need a Linux machine you can leave running. Three realistic ways to get one:

- **A local box you own** — an old laptop, a desktop, a NUC, a Raspberry Pi 4 (8 GB) — sitting on your desk or in a closet, running Ubuntu. **Easiest path on the wallet, what this guide assumes throughout, and what we quietly recommend for most small advocacy orgs.** See *Recommended hardware* below for what to look for.
- **A VPS** (virtual private server) from a hosting provider — Hetzner, DigitalOcean, OVH, Vultr, Scaleway. ~$5–10/month. The path of least friction if you don't have spare hardware lying around. Notes for VPS users are called out where the steps differ.
- **A friend's spare server.** Solidarity hosting is a thing. Just make sure you have admin access.

**This guide assumes the local-box path.** The commands and prerequisites checklist all expect a freshly installed **Ubuntu 22.04 / 24.04 LTS** machine you can sit at — keyboard and screen attached — with `sudo` access. New to Ubuntu? Use one of these install walkthroughs first:

- [Install Ubuntu Desktop](https://ubuntu.com/tutorials/install-ubuntu-desktop) — the right choice for an old laptop or any machine where having a GUI is helpful. This is what most readers want.
- [Install Ubuntu Server](https://ubuntu.com/tutorials/install-ubuntu-server) — minimal, no GUI, lower RAM use. Pick this if you'll only ever SSH into the box.

Come back here once you've got a working Ubuntu login prompt.

### What is Docker?

Software has dependencies — specific versions of Python, Postgres, Node, system libraries. Installing five different programs on one server used to mean five different sets of conflicting dependencies fighting over the same machine. Docker fixes this.

A **container** is a sealed bag of "this program plus everything it needs to run." Docker is the tool that runs those bags. Each container is isolated: Listmonk's container can't see Postgres's container's files, and they can't break each other's installs.

A **Docker image** is the recipe; a **container** is a running instance of the recipe. You can stop a container, throw it away, and start a fresh one from the image — same program, clean state.

You don't install Listmonk on your server. You install **Docker** on your server, and Docker downloads and runs the Listmonk image. When you upgrade, Docker pulls a newer image and replaces the container. The server itself stays clean.

### What is Docker Compose?

A real app is rarely one container. This stack alone has eight: a tunnel client, a docs site (dev), a static-file server (production), an email tool, a database for the email tool, a Q&A platform, a service dashboard, and a web IDE. Running them all by hand — wiring up the network between them, remembering the right flags, restarting them in the right order — is tedious and error-prone.

**Docker Compose** is one YAML file (`docker-compose.yml`) that describes the whole set of containers as a single unit. One command (`docker compose up -d`) starts all of them. One command (`docker compose down`) stops all of them. The file is checked into the repo, so anyone with the file can recreate your exact setup.

Read [`docker-compose.yml`](https://github.com/adminatthebunker/PIA-BNKOP-SERVER/blob/main/pia-starter-stack/docker-compose.yml) at some point — it's heavily commented. Each `service:` block is one container. Each `image:` line is the recipe Docker downloads.

### What's a "tunnel"?

This stack assumes a **tunnel** sits in front of it for public access — specifically Pangolin/Newt, but Cloudflare Tunnel and Tailscale Funnel work the same way conceptually.

A tunnel is an outbound connection from your server to a relay somewhere on the public internet. Visitors hit the relay; the relay forwards the request through your tunnel to your server; your server replies the same way back. The advantages:

- **You don't expose ports on your server.** No firewall holes to worry about.
- **TLS (HTTPS) is handled at the relay.** No certificate setup on your server.
- **It works behind a home router** with no port forwarding or static IP.

The trade-off is that your traffic goes through someone else's relay. For a self-hosted Pangolin instance you own, that "someone else" is also you. For Cloudflare Tunnel, that's Cloudflare. Pick what fits your threat model.

If you don't want a tunnel at all, you'll need to handle TLS yourself (Caddy, certbot+nginx, etc.) — that's outside the scope of this guide.

> **Don't have a Pangolin instance?** The Bunker Ops runs a Pangolin server on a secure VPS in Toronto, and we'll host any aligned non-profit campaign on it — no setup fee, just get in touch at [admin@thebunkerops.ca](mailto:admin@thebunkerops.ca). You bring the server and the domain; we register your organization, your site, hand you the `NEWT_ID` / `NEWT_SECRET`, you can manage your instance remotely, and you skip straight to Step 6.

---

## Recommended hardware

**An old laptop running Ubuntu is hard to beat.** That's the recommendation for most small advocacy orgs.

Why a laptop:

- **Built-in UPS.** The battery is a free uninterruptible power supply. The grid flickers, the lid stays closed, the server keeps running. A desktop or NUC will reboot on every brownout.
- **Built-in console.** When SSH breaks (it will, eventually), you flip the lid open and you've already got a keyboard, screen, and trackpad attached. No "where did I put the HDMI cable" energy at midnight.
- **Dual-purpose.** Ubuntu is a perfectly good desktop OS. The same machine that hosts your newsletter can be the office laptop someone uses for browsing, writing, video calls — pick it up, use it, set it back down. As long as you don't shut it off, the containers keep running.
- **Cheap.** A 5-year-old ThinkPad with 8 GB of RAM and a working battery runs $100–200 used. That's roughly a year of VPS fees.

What to look for in a used machine:

- **8 GB RAM minimum**, 16 GB if you'll run the full suite.
- **A 256 GB SSD minimum** — spinning disks technically work, but Listmonk and CryptPad both feel sluggish on them. And the moment video gets involved (which it usually does), you'll want the space.
- **A working battery** — the whole point. If the cell is dead, you've just bought a desktop.
- **Wired Ethernet** — Wi-Fi will do, but a cable is more reliable for 24/7 operation.

Once you have the hardware, install Ubuntu on it. Canonical's official walkthroughs cover the full process — download the ISO, write it to a USB stick, boot from USB, install:

- **[Install Ubuntu Desktop](https://ubuntu.com/tutorials/install-ubuntu-desktop)** — recommended. The GUI is useful when something's wrong and you need to plug in a monitor and click around. Disk and RAM cost is negligible on modern hardware.
- **[Install Ubuntu Server](https://ubuntu.com/tutorials/install-ubuntu-server)** — for headless boxes (Raspberry Pi, NUC in a closet) where you'll only ever SSH in.
- **[Create a USB installer (from another machine)](https://ubuntu.com/tutorials/create-a-usb-stick-on-ubuntu)** — the prerequisite for either install path above. Works from Linux, [macOS](https://ubuntu.com/tutorials/create-a-usb-stick-on-macos), or [Windows](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows) (separate guides per host OS).

Pick **22.04 LTS (Jammy)** or **24.04 LTS (Noble)** — both supported. During install, when prompted: create a regular user account (not root), enable OpenSSH server (handy if you ever want to manage the box from another machine), and skip every "snaps" upsell offered by the installer. You don't need them for this stack.

> **Other on-prem options.** A Raspberry Pi 4 (8 GB) or a small NUC works too. They're cheaper and quieter, but you lose the built-in UPS and console. Pair one with a $50 USB UPS and you're back on equal footing.

### If you're using a VPS instead

Trade-offs the laptop path solves and a VPS reintroduces:

- **You're renting hardware you don't own.** The provider can suspend your account, and your data lives in their datacenter. Self-sovereignty is a spectrum.
- **Cost is recurring.** ~$5–10/month forever vs. a one-time $150 for a used ThinkPad.

What a VPS gives you back:

- **Public IP and uplink reliability.** A datacenter has redundant power and internet; your office probably doesn't.
- **No hardware failure on you.** RAM dies, fans clog, batteries swell — that's the provider's problem.

If you go VPS: any of Hetzner / DigitalOcean / OVH / Vultr / Scaleway works. Provision an Ubuntu 22.04 or 24.04 image with at least 8 GB RAM and 256 GB disk (16 GB RAM if you'll run the full suite), then in **Step 1** below, SSH into it instead of opening a terminal locally. Everything else in this guide is identical.

> **Hardware failure is yours, either way.** RAM dies, fans clog with dust, batteries swell. Plan for it: keep your `.env` and `data/` backed up off-machine so you can restore onto a new box in an hour.

---

## What you need before you start

A checklist. If any of these are missing, sort them out first.

- [ ] **A Linux box** with at least **8 GB RAM and 256 GB SSD** (16 GB RAM if you'll run everything — CryptPad, Answer, the works; and you'll want that disk space as soon as video enters the picture, which it usually does pretty quickly), running a fresh **[Ubuntu 22.04 or 24.04 LTS](https://ubuntu.com/tutorials/install-ubuntu-desktop)** install. An old laptop is ideal — see *Recommended hardware* above. A VPS works fine too; the only step that differs is Step 1 (you SSH in instead of opening a terminal locally).
- [ ] **A user account on the box with `sudo`.** The Ubuntu installer creates one for you during install — that's the account you'll use throughout. Don't run any of these commands as `root`.
- [ ] **A domain name** you control (you can set DNS records on it). $10–15/year at any registrar — Namecheap, Porkbun, Gandi.
- [ ] **A tunnel** in front of the box. For this guide we assume you have a [Pangolin](https://docs.fossorial.io/) instance (your own, or a friend's) where you can register this machine as a "site" and add resources. If you don't, see the README's [public deployment section](https://github.com/adminatthebunker/PIA-BNKOP-SERVER/tree/main/pia-starter-stack#public-deployment-with-pangolinnewt) for alternatives. The tunnel is the only reason a home/office box can serve public traffic without a static IP or open firewall ports.
- [ ] **Roughly an hour** of uninterrupted time. The first install always takes longer than the second.

Got all that? Read on.

---

## Step 1: Open a terminal on the box

Sit at the machine you just installed Ubuntu on. Log in with the user account the installer created. On Ubuntu Desktop, open the **Terminal** app — press `Ctrl+Alt+T`, or hit the Super (Windows) key and type "terminal". On Ubuntu Server, you're already at a terminal once you log in.

You should land at a shell prompt that looks something like `your-username@hostname:~$`. From now on, every command in this guide runs **at this prompt** unless explicitly stated.

> **Using a VPS, or want to manage a headless box from your laptop?** SSH in instead:
>
> ```bash
> ssh your-username@your-server-ip
> ```
>
> Replace `your-username` with the user account on the server, and `your-server-ip` with the box's IP (or hostname). On a first connection, accept the host key fingerprint when prompted. The rest of this guide is identical whether you're on the box directly or SSH'd in.

### Update the system first

```bash
sudo apt update
sudo apt upgrade -y
```

This pulls the latest security patches. Do it now and again before each Docker upgrade later. On Ubuntu it takes 1–5 minutes the first time. You'll be prompted for your `sudo` password — that's the password you set when you installed Ubuntu.

---

## Step 2: Install Docker

The official Docker repo is more current than what ships in Ubuntu, and it includes the Compose plugin. Use it.

```bash
# Get Docker's installer script and run it
curl -fsSL https://get.docker.com | sudo sh
```

This fetches a script from `get.docker.com` and pipes it to a privileged shell. **Read it first if you don't trust the source** (`curl -fsSL https://get.docker.com | less`) — it's the official Docker convenience installer, but a healthy reflex is to check before piping anything to `sudo sh`.

The script installs:

- **Docker Engine** — the daemon that runs containers.
- **Docker CLI** — the `docker` command.
- **Docker Compose plugin** — the `docker compose` subcommand.

When it finishes, verify:

```bash
docker --version
docker compose version
```

You should see something like `Docker version 27.x.x` and `Docker Compose version v2.x.x`.

### Run Docker without sudo

By default `docker` requires `sudo`. Add your user to the `docker` group so you don't have to type `sudo` every time:

```bash
sudo usermod -aG docker $USER
```

**Then log out and back in.** Group membership only takes effect on a fresh login. After re-logging:

```bash
docker run hello-world
```

You should see a "Hello from Docker!" message. If that works without `sudo`, Docker is set up.

> **Security note.** Being in the `docker` group is effectively root on the host — Docker can mount any directory into a container as root. Only add trusted users.

---

## Step 3: Get the starter stack

Install Git if it's not there:

```bash
sudo apt install -y git
```

Pick a directory where this will live — `~/apps/` is a fine convention:

```bash
mkdir -p ~/apps
cd ~/apps
git clone https://github.com/adminatthebunker/PIA-BNKOP-SERVER.git
cd PIA-BNKOP-SERVER/pia-starter-stack
ls
```

You should see `docker-compose.yml`, `README.md`, `.env.example`, a `docs/` folder, and a few others. From this point on, every command assumes you're in this `pia-starter-stack/` directory.

---

## Step 4: Configure your secrets in `.env`

The repo ships with `.env.example` — a template with placeholder values. The real `.env` (with passwords and tunnel credentials) is **never committed to Git**. You create it locally on each server.

```bash
cp .env.example .env
nano .env
```

`nano` is a basic editor. Arrow keys to move, type to edit, **Ctrl+O** to save, **Ctrl+X** to exit. (If you prefer `vim` or `vi`, use that.)

The values you must change before going public:

| Variable | What to set it to |
| --- | --- |
| `LISTMONK_DB_PASSWORD` | A long random string. `openssl rand -base64 32` generates one. |
| `CODE_SERVER_PASSWORD` | Another long random string. Code Server gives a browser-based shell — this password is your only line of defense. |
| `PANGOLIN_ENDPOINT` | The public URL of your Pangolin server, e.g. `https://pangolin.example.org` |
| `PANGOLIN_NEWT_ID` | Generated when you register this server in the Pangolin admin UI (next step) |
| `PANGOLIN_NEWT_SECRET` | Same — from Pangolin |
| `CRYPTPAD_MAIN_DOMAIN` | Only if you'll run the optional CryptPad. Must match a Pangolin resource character-for-character. |
| `CRYPTPAD_SANDBOX_DOMAIN` | Same — see the README's CryptPad gotchas section. |

Generate a password right now and paste it in:

```bash
openssl rand -base64 32
```

> **Where do `.env` files live?** This file is read by Docker Compose at startup and the values are passed into containers as environment variables. If you change `.env`, you must restart the affected containers for them to pick up the new values:
> ```bash
> docker compose restart <service>
> ```

> **Don't commit `.env`.** The repo's `.gitignore` already excludes it. If you fork this repo and start adding your own commits, double-check `.env` is not staged before you push:
> ```bash
> git status
> ```

---

## Step 5: Register the server with Pangolin

This is the tunnel-specific step. If you're using a different tunnel, skip to Step 6 and bring up your tunnel client separately.

In your Pangolin admin UI:

1. **Sites → New Site.** Type: `newt`. Give it a name (e.g. `our-server`). Click create.
2. Pangolin shows a `NEWT_ID` and `NEWT_SECRET`. Copy them.
3. Back on the server, paste them into `.env` (`PANGOLIN_NEWT_ID=` and `PANGOLIN_NEWT_SECRET=`).

You'll come back to Pangolin in Step 8 to add resources (the `pad.*`, `mail.*`, etc. subdomains). Right now we just need the site registered so the newt service in this stack can connect.

---

## Step 6: First boot

Bring everything up:

```bash
docker compose up -d
```

The `-d` means "detached" — start the containers in the background and give you the shell back. Without `-d`, you'd see all six services' logs streaming together in your terminal.

The first time, Docker downloads several gigabytes of images. **Expect 2–5 minutes.** You'll see lines like:

```
[+] Pulling 27/27
 ✔ listmonk Pulled    47.3s
 ✔ mkdocs   Pulled    52.1s
 ...
[+] Running 7/7
 ✔ Network pia-stack       Created
 ✔ Container ...-newt-1    Started
 ...
```

When it finishes, check what's running:

```bash
docker compose ps
```

You should see all services with `STATUS: Up`. If something says `Restarting` or `Exited`, see the **Troubleshooting** section below — don't move on until everything is `Up`.

---

## Step 7: First-boot bootstrap

The compose file can't do these for you. They're one-time setup steps the upstream images need.

### Initialize the Listmonk database

Listmonk refuses to start cleanly until you run its DB installer:

```bash
docker compose run --rm listmonk ./listmonk --install --idempotent --yes
docker compose up -d listmonk
```

The first command runs a one-shot container that creates the schema and exits (`--rm` means "delete this container after"). The second command starts the real Listmonk service now that the DB is ready.

### Build the static MkDocs site

The Nginx service serves files from `./site/`, which is empty until you build:

```bash
docker compose run --rm mkdocs build
```

This generates HTML from the markdown in `docs/` and drops it into `site/`. You'll re-run this every time you want production changes to show up. (The dev server at `mkdocs:8000` rebuilds automatically — but you don't expose that publicly outside the live-editing scenarios in the README.)

### Build the site from Code Server

MkDocs is already installed in the Code Server container. Open the in-browser IDE, open a terminal, and run:

```bash
mkdocs build
```

That's it — no extra install needed.

### Optional: bring up CryptPad (`session` profile)

Only if you need the collaborative-editor service. CryptPad is gated behind a profile so it doesn't start by default:

```bash
# First, fix data directory ownership (CryptPad runs as UID 4001 inside its container)
docker run --rm -v "$(pwd)/data/cryptpad:/data" alpine:3 chown -R 4001:4001 /data

docker compose --profile session up -d
```

---

## Step 8: Verify the stack is healthy

The quick check — should show all services with `STATUS: Up`. If everything looks green, you're done:

```bash
docker compose ps
```

If you want to go deeper and confirm each service is actually responding to HTTP (not just running), you can curl them from inside the `pia-stack` network:

```bash
docker run --rm --network pia-stack curlimages/curl:latest -sI http://mkdocs:8000/
docker run --rm --network pia-stack curlimages/curl:latest -sI http://listmonk:9000/
docker run --rm --network pia-stack curlimages/curl:latest -sI http://mkdocs-site-server:80/
docker run --rm --network pia-stack curlimages/curl:latest -sI http://answer:80/
docker run --rm --network pia-stack curlimages/curl:latest -sI http://homepage:3000/
```

`-sI` means "silent, headers only". You want `HTTP/1.1 200 OK` (or `302` for the Listmonk login redirect). Anything else means that service didn't come up cleanly:

```bash
docker compose logs <service>
```

### Expose to the public internet

Now that everything works internally, configure Pangolin to forward traffic in:

1. **Resources → New Resource** for each subdomain you want public.
2. Set the target to the Docker service name + port, using the mappings below.
3. Add the corresponding **DNS record** at your registrar — a `CNAME` from `docs.yourorg.org` to your Pangolin server's hostname.

| Subdomain | Target |
| --- | --- |
| `docs.yourorg.org` | `mkdocs-site-server:80` *(or `mkdocs:8000` for hot-reload during writing sessions)* |
| `mail.yourorg.org` | `listmonk:9000` |
| `answers.yourorg.org` | `answer:80` |
| `lander.yourorg.org` | `homepage:3000` *(the dashboard linking everything else)* |
| `pad.yourorg.org` | `cryptpad:3000` *(plus a second target for the WebSocket — see CryptPad gotchas)* |

!!! tip
    **Live preview:** Expose `mkdocs:8000` instead and gate it with Pangolin's built-in authentication. Edits appear in real time — no `mkdocs build` needed until you're ready to publish.

    **Root domain:** MkDocs is a full site generator, not just a docs tool. Add a homepage, a contact page, whatever you need — then point your root domain (`yourorg.org`) straight at `mkdocs-site-server:80`. It can be your whole website.

Pangolin issues a Let's Encrypt cert and starts forwarding. Visit `https://docs.yourorg.org/` from your laptop — you should see your MkDocs site.

The README's [Public deployment section](https://github.com/adminatthebunker/PIA-BNKOP-SERVER/tree/main/pia-starter-stack#public-deployment-with-pangolinnewt) has the resource cheat-sheet, including the [CryptPad gotchas](https://github.com/adminatthebunker/PIA-BNKOP-SERVER/tree/main/pia-starter-stack#cryptpad-gotchas) you'll trip over if you skip it.

If you have shell access on the parent repo and a Pangolin API key, the [`pangolin-push.py`](https://github.com/adminatthebunker/PIA-BNKOP-SERVER/tree/main/scripts) helper provisions any of those subdomains in one command — does the same thing the admin UI does, but in seconds:

```bash
python3 scripts/pangolin-push.py lander homepage:3000
```

---

## Day-to-day operations

A short reference once the stack is up.

| Task | Command |
| --- | --- |
| See what's running | `docker compose ps` |
| Tail logs from one service | `docker compose logs -f listmonk` |
| Tail logs from everything | `docker compose logs -f` |
| Restart one service | `docker compose restart listmonk` |
| Stop the stack | `docker compose down` *(keeps named volumes — Listmonk DB survives)* |
| Stop AND wipe data | `docker compose down -v` ⚠ **destroys Listmonk's DB** |
| Pull updates and re-up | `docker compose pull && docker compose up -d` |
| Open a shell in a container | `docker compose exec listmonk sh` |
| Rebuild the MkDocs site | `docker compose run --rm mkdocs build` |
| Disk usage by Docker | `docker system df` |
| Clean up unused images | `docker image prune -a` |

`docker compose <command>` always operates on services defined in the `docker-compose.yml` in your current directory. Run them from inside `pia-starter-stack/`.

---

## Troubleshooting

The most common failures, in roughly the order they bite people.

### `docker: permission denied while trying to connect to the Docker daemon socket`

You skipped the "log out and back in" step after `usermod -aG docker`. Log out of the desktop session (or `exit` your SSH connection and reconnect), log back in, retry.

### A service shows `Restarting (1)` in `docker compose ps`

Something inside it crashed. Read its logs:

```bash
docker compose logs --tail 50 <service-name>
```

Common cases:

- **Listmonk** crashing with `pq: relation "settings" does not exist` — you skipped Step 7's DB init.
- **CryptPad** crashing with permission errors on `/cryptpad/data` — you skipped the `chown -R 4001:4001 ./data/cryptpad` step.
- **Any service** failing with `address already in use` — something else on the host is bound to the same host port. Only Code Server binds a host port in this stack (`127.0.0.1:8889` by default); change `CODE_SERVER_PORT` in `.env` if 8889 is taken.

### Pangolin says my site is "offline"

The newt client either isn't running or can't reach Pangolin.

```bash
docker compose logs newt
```

You want to see lines like `connected to pangolin server`. If you see auth errors, your `PANGOLIN_NEWT_ID` or `PANGOLIN_NEWT_SECRET` is wrong — double-check `.env` and re-register the site if needed, then:

```bash
docker compose restart newt
```

### Pangolin says the resource is up, but visiting the URL gives 502

The tunnel is fine; the backend service isn't responding. Confirm the service is actually `Up` in `docker compose ps`, then verify it from inside the network:

```bash
docker run --rm --network pia-stack curlimages/curl:latest -sI http://listmonk:9000/
```

If that works internally but Pangolin gets 502, the resource target is misconfigured (wrong service name or port).

### `mkdocs build` says "Config file 'mkdocs.yml' does not exist"

You're in the wrong directory. Run this before any `docker compose` commands:

```bash
cd ~/apps/pia-starter-stack
```

### I edited `mkdocs.yml` and the site looks the same

The `mkdocs.yml` file is bind-mounted into the container by inode, not by path. Restart the mkdocs service after editing it:

```bash
docker compose restart mkdocs
```

### CryptPad loads but the editor surface is blank

`CRYPTPAD_MAIN_DOMAIN` and `CRYPTPAD_SANDBOX_DOMAIN` in `.env` don't exactly match the URLs your Pangolin resources serve. CryptPad bakes those URLs into Content-Security-Policy headers — a single-letter typo blocks asset loading. See the README's CryptPad gotchas.

### I broke `.env` and want to start over

`.env.example` is the pristine template:

```bash
cp .env.example .env
# edit it again, more carefully this time
docker compose up -d
```

Restart any services whose env vars you changed. (Compose only re-applies env on container restart, not on file change alone.)

---

## What's next

You have a self-hosted website and newsletter system. Now what?

- **Edit the site.** [`docs/index.md`](https://github.com/adminatthebunker/PIA-BNKOP-SERVER/blob/main/pia-starter-stack/docs/index.md) is your homepage. Edit it, then rebuild and refresh:
  ```bash
  docker compose run --rm mkdocs build
  ```
- **Customize the dashboard** at `https://lander.yourorg.org/`. The [Homepage](https://gethomepage.dev/) config is a handful of YAML files in [`configs/homepage/`](https://github.com/adminatthebunker/PIA-BNKOP-SERVER/tree/main/pia-starter-stack/configs/homepage) — change `services.yaml` to add or remove cards, `bookmarks.yaml` for external links, `custom.css` for theming. Most edits hot-reload; `settings.yaml` needs a poke:
  ```bash
  docker compose exec homepage curl -sX POST http://localhost:3000/api/revalidate
  ```
- **Configure Listmonk.** Visit `https://mail.yourorg.org/`, run through the setup wizard, create your first list, import subscribers, send a test campaign. [Listmonk docs](https://listmonk.app/docs/).
- **Set up SMTP.** Listmonk needs a relay (Postmark, SES, Mailgun, Scaleway) to deliver mail reliably. Inside Listmonk: **Settings → SMTP**.
- **Run the Apache Answer setup wizard.** First visit to `https://answers.yourorg.org/install` walks you through admin account creation and DB choice (SQLite is fine).
- **Plan backups.** The Listmonk database is in a Docker named volume; CryptPad data is in `./data/cryptpad/`. Both need to be backed up off-host, with restore tested at least quarterly.
- **Set up monitoring.** Homepage's docker-socket integration already shows container CPU / memory / status on the dashboard. For pager-style alerts (texts when something dies), add [Uptime Kuma](https://github.com/louislam/uptime-kuma) — one container, free, slots into your `docker-compose.yml`.
- **Update monthly.** Subscribe to release notes for MkDocs Material, Listmonk, and CryptPad so you know what changed, then:
  ```bash
  docker compose pull && docker compose up -d
  ```

---

## Where to get help

- **This stack's repo** — issues and PRs at [github.com/adminatthebunker/PIA-BNKOP-SERVER](https://github.com/adminatthebunker/PIA-BNKOP-SERVER) (the starter stack lives under `pia-starter-stack/`).
- **The README** — [Public deployment section](https://github.com/adminatthebunker/PIA-BNKOP-SERVER/tree/main/pia-starter-stack#public-deployment-with-pangolinnewt) has the Pangolin-specific cheat-sheet.
- **Docker docs** — [docs.docker.com](https://docs.docker.com/) is unusually good.
- **Pangolin docs** — [docs.fossorial.io](https://docs.fossorial.io/).
- **The Bunker Operations** — [bnkops.com](https://bnkops.com) · admin@thebunkerops.ca. First conversation is free.
