# AGENTS.md

Instructions for an agent (or a human in a hurry) bringing up `pia-starter-stack` on a target Linux host. Read top-to-bottom; every step has an explicit success check.

If a step's check fails, jump to **Failure modes** at the bottom — every observed failure during development has a labeled remediation.

## Goal

Bring up the full stack so:
1. All services are reachable on the `pia-stack` docker network by service name.
2. (If a Pangolin tunnel is configured) public subdomains route via Newt to the right backend services.
3. The first-boot one-time initialization steps are complete (Listmonk DB schema, CryptPad data ownership, MkDocs build).

## Prerequisites — verify first

```bash
docker --version && docker compose version    # both must succeed
df -h .                                        # need 5GB free (10GB with --profile session)
free -m                                        # need 2GB RAM (4GB with --profile session)
```

If any check fails, stop and report — do not attempt to install Docker or free space autonomously.

## Inputs the agent needs

**Required for all deployments:**
- `LISTMONK_DB_PASSWORD` — strong password for the Listmonk Postgres user
- `CODE_SERVER_PASSWORD` — strong password for the web IDE login

**Required if using a Pangolin tunnel** (otherwise `newt` will retry-loop harmlessly):
- `PANGOLIN_ENDPOINT` — public URL of the Pangolin server, e.g. `https://pangolin.example.org`
- `PANGOLIN_NEWT_ID` — generated when you register this host as a "site" (type `newt`) in the Pangolin admin UI
- `PANGOLIN_NEWT_SECRET` — generated alongside `NEWT_ID`

**Required if using `--profile session` for CryptPad:**
- `CRYPTPAD_MAIN_DOMAIN` — e.g. `https://pad.yourorg.org` — *MUST be set before first boot, baked into client bundles*
- `CRYPTPAD_SANDBOX_DOMAIN` — e.g. `https://pad-sandbox.yourorg.org` — *MUST be a different domain from main, both must route via Pangolin*

If any required input is missing, ask the user. Do not make up domain names or generate passwords without confirming with the user first.

## Steps

### 1. Clone and enter the repo

```bash
git clone https://github.com/adminatthebunker/PIA-BNKOP-SERVER.git pia-session
cd pia-session/pia-starter-stack
```

**Check:** `ls docker-compose.yml mkdocs.yml .env.example` returns three filenames without errors.

### 2. Configure `.env`

```bash
cp .env.example .env
# Then edit .env to set the inputs above.
```

**Check:** none of these patterns appear in the final `.env`:
```bash
grep -E '^(LISTMONK_DB_PASSWORD|CODE_SERVER_PASSWORD)=changeme$' .env   # must return nothing
grep -E 'example\.org' .env                                             # OK only if not exposing publicly
```

If either grep returns a match for a deployment that goes public, fix before continuing.

### 3. Pre-create data directories with correct ownership

The compose file mounts `./data/cryptpad/`, `./data/code-server/`, and `./site/` into containers. If Docker auto-creates them (root-owned), the containers can't write. Pre-create as the right UIDs:

```bash
mkdir -p data/cryptpad data/code-server site
docker run --rm -v "$(pwd)/data/cryptpad:/data" alpine:3 chown -R 4001:4001 /data
docker run --rm -v "$(pwd)/site:/data" alpine:3 chown -R 1000:1000 /data
```

**Check:** `ls -la data/cryptpad/ site/` shows `4001` and `1000` as owners (not `root`).

### 4. Pull images and bring up

```bash
docker compose --profile session pull        # ~5 min on first run, ~1GB total
docker compose --profile session up -d
```

(Drop `--profile session` if you don't want CryptPad — saves ~600MB.)

**Check:** wait 30 seconds, then:
```bash
docker compose --profile session ps
```
Expected output: 6 services with status `Up` (or 7 with session profile). CryptPad may show `Up (health: starting)` for ~1 min after first boot — that's fine.

If any container shows `Restarting`, jump to **Failure modes** matching its name.

### 5. First-boot one-time initialization

These three commands fix things the upstream images don't handle on their own. Run all three on a fresh deployment.

**5a. Initialize Listmonk's database schema** (Listmonk refuses to boot on an empty DB):
```bash
docker compose run --rm listmonk ./listmonk --install --idempotent --yes
docker compose --profile session up -d listmonk
```

**Check:** `docker compose --profile session ps listmonk` shows `Up` (not `Restarting`).

**5b. Build the initial static site** (Nginx serves a "Welcome to our server" placeholder until `./site/` is populated):
```bash
docker compose run --rm mkdocs build
```

**Check:** `ls site/index.html` returns the file.

**5c. Install mkdocs into code-server** — *only if `CODE_SERVER_IMAGE` is the upstream `codercom/code-server:latest`* (the bnkops prebuilt image already has mkdocs; skip this step for it):
```bash
docker compose exec code-server bash -c "apt-get update -qq && apt-get install -y -qq python3-pip && pip install --break-system-packages 'mkdocs-material[recommended]'"
```

**Check:** `docker compose exec code-server which mkdocs` returns a path.

**Caveat:** the install lives in the container's writable layer; `docker compose --force-recreate code-server` wipes it. For permanence, build a custom code-server image with mkdocs baked in.

### 6. Verify inter-network reachability

```bash
for s in mkdocs:8000 mkdocs-site-server:80 listmonk:9000 cryptpad:3000; do
  code=$(docker run --rm --network pia-stack curlimages/curl:latest \
    -s -o /dev/null -w '%{http_code}' --max-time 5 "http://${s}/" 2>/dev/null)
  echo "  ${s}: ${code:-TIMEOUT}"
done
curl -sI -o /dev/null -w "  127.0.0.1:8889 (code-server): %{http_code}\n" --max-time 3 http://127.0.0.1:8889/
```

**Expected:**
- `mkdocs:8000` → `200`
- `mkdocs-site-server:80` → `200` (serves built site after step 5b)
- `listmonk:9000` → `200`
- `cryptpad:3000` → `200` (only with `--profile session`)
- `127.0.0.1:8889` → `302` (login redirect from code-server)

If any returns `TIMEOUT` or non-2xx/3xx, jump to **Failure modes**.

### 7. (If using Pangolin) Verify tunnel handshake

```bash
docker compose logs newt | tail -10
```

**Expected:** absence of `ERROR: ... Failed to connect`. The tunnel handshake on success is quiet — no news is good news.

If you see `Failed to connect` retry messages, jump to **Newt: Failed to connect**.

### 8. (If using Pangolin) Configure resources

This step happens in the Pangolin admin UI — there is no CLI. For the n3-pia / PIA 2026 deployment, the resource table is:

| Public hostname | → Target | Notes |
| --- | --- | --- |
| `pad.publicinterestalberta.org` | `cryptpad:3000` | HTTP + WebSocket upgrade |
| `pad.publicinterestalberta.org` (path: `/cryptpad_websocket`) | `cryptpad:3003` | WebSocket-only path rule |
| `pad-sandbox.publicinterestalberta.org` | `cryptpad:3000` | Same target as pad.*, Host-header routed |
| `live.publicinterestalberta.org` | `mkdocs:8000` | HTTP + WebSocket upgrade (hot-reload) |
| `pia2026.publicinterestalberta.org` | `mkdocs-site-server:80` | HTTP only |
| `mail.publicinterestalberta.org` | `listmonk:9000` | HTTP only |

For other deployments, swap `publicinterestalberta.org` for the relevant org domain.

**Check** (after Pangolin DNS propagates, ~1 min):
```bash
for sub in pad pad-sandbox live pia2026 mail; do
  curl -sI -o /dev/null -w "  ${sub}: %{http_code}\n" --max-time 5 \
    "https://${sub}.publicinterestalberta.org/"
done
```
Expected: all `200` or `302`. *Note: `pia2026` returns `404` if step 5b (mkdocs build) was skipped — that's diagnostic, not a tunnel problem.*

## Failure modes

Each failure has a name (matching what you'd see in logs or curl output) and a single remediation command. Run the remediation, then re-run the most recent verification check.

### Listmonk: `the database does not appear to be setup`
Step 5a was skipped. Run it.

### CryptPad: `EACCES: permission denied, mkdir '/cryptpad/data/...'`
Step 3 was skipped or didn't include the cryptpad chown. Fix:
```bash
docker run --rm -v "$(pwd)/data/cryptpad:/data" alpine:3 chown -R 4001:4001 /data
docker compose --profile session restart cryptpad
```

### CryptPad: container `Up (healthy)` but curl from network returns nothing
The image's bundled `/cryptpad/config/config.js` overrides our mount, OR the mount didn't apply. Verify:
```bash
docker compose --profile session exec cryptpad grep "httpAddress" /cryptpad/config/config.js
```
Expected: `httpAddress: '0.0.0.0'` (from our mounted config). If it shows `'localhost'`, the mount is missing — verify `./configs/cryptpad/config.js` exists and the volume line in `docker-compose.yml` is present.

### CryptPad: editor surface doesn't render in browser
Sandbox domain (`pad-sandbox.*`) isn't routed by Pangolin. Both `pad.*` and `pad-sandbox.*` must return 200 externally — both target the same `cryptpad:3000`, host-header-routed.

### MkDocs container exits with `Error: No such command 'mkdocs'`
The compose file is wrong. The `mkdocs` service `command:` should be `["serve", "--dev-addr=0.0.0.0:8000"]` — the image's ENTRYPOINT is already `mkdocs`. Fix in `docker-compose.yml`.

### MkDocs build fails with `PermissionError: ... '/config/workspace/site/...'`
`./site/` has files owned by a different UID than your build process. Fix:
```bash
docker run --rm -v "$(pwd)/site:/data" alpine:3 chown -R 1000:1000 /data
```
This happens when builds have been run via mixed paths (root via `docker compose exec`, UID 1000 via the mkdocs service's `user:` directive). The compose file pins `mkdocs` to UID 1000, so just don't run `docker compose exec` builds as root.

### mkdocs-site-server: serves `<title>Welcome to our server</title>`
Step 5b was skipped — `./site/` is empty (or has only the linuxserver default). Run `docker compose run --rm mkdocs build`.

### code-server terminal: `mkdocs: command not found`
The image lacks mkdocs. Either:
- Run step 5c to install it inline, OR
- Override `CODE_SERVER_IMAGE` in `.env` to a prebuilt image that has mkdocs.

### code-server's view of `mkdocs.yml` is stale after host-side edit
Single-file bind-mount inode trap. Either:
- Restart: `docker compose restart code-server`, OR
- Edit the file from inside code-server (in-place writes don't change the inode, so the mount stays valid).

This affects every single-file mount in the compose (`mkdocs.yml`, `docker-compose.yml`, `configs/cryptpad/config.js`, `configs/mkdocs-site/default.conf`). Edits from inside code-server are safe; edits from the host need a service restart.

### Newt: `Failed to connect: ... no such host`
`PANGOLIN_ENDPOINT` in `.env` is wrong or unreachable from this host's DNS. Verify:
```bash
grep PANGOLIN_ENDPOINT .env
docker compose exec newt nslookup $(grep PANGOLIN_ENDPOINT .env | cut -d= -f2 | sed 's|https\?://||;s|/.*||')
```

### Newt: `Failed to connect: ... 401 Unauthorized`
`PANGOLIN_NEWT_ID` or `PANGOLIN_NEWT_SECRET` is wrong. Re-copy from the Pangolin admin UI's Sites page. After fixing `.env`:
```bash
docker compose restart newt
```

### Newt: `Failed to connect: ... timeout`
Outbound network from this host is blocked or filtered. Verify the host can reach the Pangolin endpoint over HTTPS:
```bash
curl -sI --max-time 5 $(grep PANGOLIN_ENDPOINT .env | cut -d= -f2)
```

### Pangolin resource: returns `502 Bad Gateway`
The backend service the resource targets isn't running, OR the Pangolin resource target hostname doesn't match a docker service name on `pia-stack`. Check:
```bash
docker compose --profile session ps           # the targeted service should be Up
docker network inspect pia-stack | grep Name  # the service should be a network member
```

### Pangolin resource: returns TLS error / `530`
DNS for the subdomain hasn't propagated yet, OR Let's Encrypt hasn't issued a cert yet. Wait 1–2 minutes and retry. If still failing after 5 minutes, check the Pangolin admin UI for the resource's TLS status.

## Tear-down

**Stop services, keep all data and built site:**
```bash
docker compose --profile session down
```

**Stop services, drop the Listmonk database volume (keeps ./data/ and ./site/):**
```bash
docker compose --profile session down -v
```

**Wipe everything including bind-mounted runtime state** (DESTRUCTIVE — confirm with user first):
```bash
docker compose --profile session down -v
sudo rm -rf data/ site/
```

## Key invariants

- **No host port bindings except code-server** (`127.0.0.1:8889`). Everything else is reachable only on the `pia-stack` docker network. This is by design — Newt is the one path in from public.
- **Three services touch `./site/`** (`mkdocs`, `mkdocs-site-server`, `code-server`) — all run as UID 1000. CryptPad runs as UID 4001 internally; only `./data/cryptpad/` needs that ownership.
- **`.env` is gitignored and contains secrets.** Never commit it. Never mount it into `code-server` (the compose explicitly omits this).
- **`data/` and `site/` are gitignored** — runtime state, regenerated.
- **`pia-stack` is a single named bridge network** — services find each other by service name (`listmonk`, `cryptpad`, `mkdocs`, etc.) on standard internal ports (`9000`, `3000`, `8000`, etc.). Pangolin resources target these names.
