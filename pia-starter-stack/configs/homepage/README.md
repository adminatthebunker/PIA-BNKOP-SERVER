# Homepage configuration

Drives [gethomepage.dev](https://gethomepage.dev) — the dashboard at `lander.<your-domain>` (or wherever you point a Pangolin resource targeting `homepage:3000`).

## Files

| File | What it sets |
| --- | --- |
| [settings.yaml](./settings.yaml) | Site title / description / theme / color / status pill style / per-group layout |
| [services.yaml](./services.yaml) | Service cards, grouped — public URLs, descriptions, docker container monitoring |
| [bookmarks.yaml](./bookmarks.yaml) | External links grouped by purpose (movement, source) |
| [widgets.yaml](./widgets.yaml) | Top-bar widgets — search, datetime, host resources |
| [docker.yaml](./docker.yaml) | Docker daemon socket(s) — referenced by `server:` in services.yaml |
| [custom.css](./custom.css) | Theming — Space Grotesk + JetBrains Mono + Fraunces, deep-purple accent |

`kubernetes.yaml` is auto-seeded by Homepage on first boot; safe to ignore (we're not running k8s).

## Reload after editing

Homepage statically pre-renders `settings.yaml` into the page bundle at image-build time. Edits to settings.yaml don't show until you tell Homepage to re-render:

```bash
docker compose exec homepage curl -sX POST http://localhost:3000/api/revalidate
# → {"revalidated":true}
```

Or, equivalently, from outside the container with the public URL — but you must use a `?cachebust=$(date +%s)` query string to bypass Pangolin's edge cache, so the in-network call above is faster and more reliable.

`services.yaml`, `bookmarks.yaml`, and `widgets.yaml` are read at request time via `/api/services` etc., so they hot-reload — no revalidate needed. `custom.css` is fetched fresh each page load. Only `settings.yaml` (and `docker.yaml` server connection definitions) need the revalidate poke.

## Docker container monitoring

Each service entry that wants the container CPU / memory / status pill must set:

```yaml
server: my-docker          # matches the key in docker.yaml
container: pia-starter-stack-<service>-1
```

The exact container name comes from `docker compose ps`. If you rename the compose project (the parent directory name), the prefix changes — update services.yaml accordingly.

## Adding a new public service to the dashboard

1. Push the subdomain via `python3 scripts/pangolin-push.py <sub> <docker-service>:<port>` (in the parent repo, see [scripts/README.md](../../../scripts/README.md)).
2. Add the entry under the relevant group in [services.yaml](./services.yaml). Set `siteMonitor:` to the public URL so Homepage shows an up/down dot.
3. If it has docker container monitoring, set `server: my-docker` and `container: pia-starter-stack-<service>-1`.
4. `docker compose exec homepage curl -sX POST http://localhost:3000/api/revalidate` (only needed if you edited settings.yaml/layout; services.yaml hot-reloads).
