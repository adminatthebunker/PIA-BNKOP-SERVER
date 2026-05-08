# scripts/

Presenter-side glue for **PIA-BNKOP-SERVER** (the parent repo, *not* the take-home `pia-starter-stack/`).

## `pangolin-push.py`

Expose a new internal service on n3-pia (or any Newt site) via a Pangolin subdomain in one command. Drives the [Pangolin Integration API](https://docs.pangolin.net/manage/integration-api) so you don't have to click through the admin UI every time you stand something up. Python 3 stdlib only — no `pip install`.

Setup, once:

```bash
cp scripts/.env.example scripts/.env
$EDITOR scripts/.env    # set PANGOLIN_API_BASE + PANGOLIN_API_KEY at minimum
```

See what's there:

```bash
python3 scripts/pangolin-push.py --list
```

Push a new subdomain:

```bash
python3 scripts/pangolin-push.py pad cryptpad:3000
python3 scripts/pangolin-push.py mail listmonk:9000
python3 scripts/pangolin-push.py docs nginx:80 --domain publicinterestalberta.org
```

The script discovers org/site/domain IDs from the API at runtime and only requires friendly names. If `PANGOLIN_DEFAULT_SITE` and `PANGOLIN_DEFAULT_DOMAIN` are set in `.env`, you don't need the flags. If you're standing up a service on a different site (`--site changemaker-publicinterestalberta.org`), pass it explicitly.

It's idempotent: matches on `fullDomain` and prints `SKIP` instead of clobbering an existing resource. `--dry-run` prints the would-be PUT bodies; `--force` PUTs anyway.

Things this script does **not** do (handle in the Pangolin UI):

- Per-path routing rules (e.g. CryptPad's `/cryptpad_websocket → cryptpad:3003`) — the public API docs don't cover the path-rule endpoint. Check your instance's `/v1/docs` Swagger if you need to wire this in.
- Auth/SSO/whitelist policy on a resource.
- Anything DNS-side: Pangolin handles CNAME + Let's Encrypt automatically when the domain is configured for it.

`scripts/.env` is gitignored (covered by the parent repo's `.gitignore`). Never commit credentials.
