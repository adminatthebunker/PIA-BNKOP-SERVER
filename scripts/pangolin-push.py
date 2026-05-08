#!/usr/bin/env python3
"""Expose a new internal service via a Pangolin subdomain in one command.

Usage:
    pangolin-push <subdomain> <ip>:<port> [--site NAME] [--domain BASE] [--name LABEL]
    pangolin-push --list                  # show orgs / sites / domains the API key can see
    pangolin-push <sub> <ip>:<port> --dry-run

Examples:
    pangolin-push pad cryptpad:3000
    pangolin-push mail listmonk:9000 --site PIA-confrence-2026
    pangolin-push docs nginx:80 --domain publicinterestalberta.org

Required env (in scripts/.env or shell): PANGOLIN_API_BASE, PANGOLIN_API_KEY.
Optional: PANGOLIN_ORG_ID, PANGOLIN_DEFAULT_SITE, PANGOLIN_DEFAULT_DOMAIN.
Anything missing is auto-discovered when there's only one candidate.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def api(method: str, base: str, path: str, key: str, body: dict | None = None) -> dict:
    url = f"{base.rstrip('/')}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} on {method} {path}\n{e.read().decode(errors='replace')}")


def pick_one(items: list[dict], match_fields: list[str], wanted: str | None, kind: str) -> dict:
    """Return the single matching item, or the only item if `wanted` is None."""
    if wanted:
        hits = [i for i in items if any(str(i.get(f)) == wanted for f in match_fields)]
        if not hits:
            names = ", ".join(str(i.get(match_fields[0])) for i in items) or "(none)"
            sys.exit(f"No {kind} matched {wanted!r}. Available: {names}")
        if len(hits) > 1:
            sys.exit(f"Multiple {kind}s matched {wanted!r}; be more specific.")
        return hits[0]
    if len(items) == 1:
        return items[0]
    if not items:
        sys.exit(f"No {kind}s visible to this API key.")
    names = ", ".join(str(i.get(match_fields[0])) for i in items)
    sys.exit(f"Multiple {kind}s exist ({names}); pass --{kind} or set PANGOLIN_DEFAULT_{kind.upper()}.")


def discover_org(base: str, key: str, hint: str | None) -> str:
    if hint:
        return hint
    payload = api("GET", base, "/orgs", key)
    orgs = payload.get("data", {}).get("orgs", [])
    if not orgs:
        sys.exit("API key sees no orgs.")
    if len(orgs) > 1:
        names = ", ".join(o.get("orgId", "?") for o in orgs)
        sys.exit(f"API key sees multiple orgs ({names}); set PANGOLIN_ORG_ID.")
    return orgs[0]["orgId"]


def list_sites(base: str, key: str, org_id: str) -> list[dict]:
    return api("GET", base, f"/org/{org_id}/sites", key).get("data", {}).get("sites", [])


def list_domains(base: str, key: str, org_id: str) -> list[dict]:
    return api("GET", base, f"/org/{org_id}/domains", key).get("data", {}).get("domains", [])


def list_resources(base: str, key: str, org_id: str) -> list[dict]:
    # Pangolin caps the default page at 20 and ignores `?limit=`; `?pageSize=`
    # is the working knob. 1000 is well above any plausible org size.
    return api("GET", base, f"/org/{org_id}/resources?pageSize=1000", key).get("data", {}).get("resources", [])


def cmd_list(base: str, key: str, org_hint: str | None) -> None:
    org_id = discover_org(base, key, org_hint)
    print(f"org: {org_id}")
    print("\nsites:")
    for s in list_sites(base, key, org_id):
        marker = "online" if s.get("online") else "offline"
        print(f"  [{marker:7s}] siteId={s['siteId']:<5} name={s['name']!r}  niceId={s['niceId']!r}")
    print("\ndomains:")
    for d in list_domains(base, key, org_id):
        verified = "verified" if d.get("verified") else "pending"
        print(f"  [{verified:8s}] domainId={d['domainId']!r}  base={d['baseDomain']!r}")


def parse_target(s: str) -> tuple[str, int]:
    if ":" not in s:
        sys.exit(f"Target must be ip:port, got {s!r}")
    ip, _, port = s.rpartition(":")
    if not port.isdigit():
        sys.exit(f"Port must be an integer, got {port!r}")
    return ip, int(port)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("subdomain", nargs="?", help="Subdomain to create, e.g. 'pad'")
    p.add_argument("target", nargs="?", help="Internal target ip:port, e.g. 'cryptpad:3000'")
    p.add_argument("--site", help="Site name or niceId (default: PANGOLIN_DEFAULT_SITE or only site)")
    p.add_argument("--domain", help="Base domain, e.g. publicinterestalberta.org (default: PANGOLIN_DEFAULT_DOMAIN or only domain)")
    p.add_argument("--name", help="Display name in Pangolin (default: same as subdomain)")
    p.add_argument("--list", action="store_true", help="Show available orgs/sites/domains and exit")
    p.add_argument("--dry-run", action="store_true", help="Print what would happen, send nothing")
    p.add_argument("--force", action="store_true", help="Skip the 'already exists' check")
    args = p.parse_args()

    load_dotenv(Path(__file__).with_name(".env"))
    base = os.environ.get("PANGOLIN_API_BASE", "").rstrip("/")
    key = os.environ.get("PANGOLIN_API_KEY", "")
    if not base or not key:
        sys.exit("Set PANGOLIN_API_BASE and PANGOLIN_API_KEY (see scripts/.env.example).")

    org_hint = os.environ.get("PANGOLIN_ORG_ID") or None

    if args.list:
        cmd_list(base, key, org_hint)
        return

    if not args.subdomain or not args.target:
        p.error("subdomain and target are required (or use --list)")

    ip, port = parse_target(args.target)
    org_id = discover_org(base, key, org_hint)

    site_hint = args.site or os.environ.get("PANGOLIN_DEFAULT_SITE")
    site = pick_one(list_sites(base, key, org_id), ["name", "niceId", "siteId"], site_hint, "site")

    domain_hint = args.domain or os.environ.get("PANGOLIN_DEFAULT_DOMAIN")
    domain = pick_one(list_domains(base, key, org_id), ["baseDomain", "domainId"], domain_hint, "domain")

    full = f"{args.subdomain}.{domain['baseDomain']}"
    label = args.name or args.subdomain

    print(f"org    : {org_id}")
    print(f"site   : {site['name']!r}  (siteId={site['siteId']})")
    print(f"domain : {domain['baseDomain']!r}  (domainId={domain['domainId']})")
    print(f"create : {full}  →  {ip}:{port}")

    if not args.force:
        existing = next((r for r in list_resources(base, key, org_id) if r.get("fullDomain") == full), None)
        if existing:
            print(f"\nSKIP: {full} already exists (resourceId={existing['resourceId']}).")
            print("     Use --force to PUT anyway, or update via the Pangolin UI.")
            return

    resource_body = {
        "name": label, "http": True, "subdomain": args.subdomain,
        "domainId": domain["domainId"], "protocol": "tcp",
    }
    # Pangolin defaults new resources to sso=true (auth gateway). For a
    # "expose this internal service publicly" tool, that's the wrong default —
    # the user gets an auth-redirect 302 instead of their service. Disable
    # via a follow-up POST after creation. Re-enable in the UI if needed.
    sso_disable_body = {"sso": False}
    target_body = {"ip": ip, "port": port, "method": "http", "siteId": site["siteId"]}

    if args.dry_run:
        print(f"\nDRY RUN — would PUT /org/{org_id}/resource")
        print(json.dumps(resource_body, indent=2))
        print(f"\nthen POST /resource/<resourceId>  (disable sso for public access)")
        print(json.dumps(sso_disable_body, indent=2))
        print(f"\nthen PUT /resource/<resourceId>/target")
        print(json.dumps(target_body, indent=2))
        return

    resp = api("PUT", base, f"/org/{org_id}/resource", key, resource_body)
    inner = resp.get("data") or resp
    rid = inner.get("resourceId") or inner.get("id")
    if rid is None:
        sys.exit(f"Resource create returned no id: {resp!r}")
    api("POST", base, f"/resource/{rid}", key, sso_disable_body)
    api("PUT", base, f"/resource/{rid}/target", key, target_body)

    print(f"\nOK  https://{full}/  →  {ip}:{port}  (resourceId={rid}, sso=false)")
    print("    First request may take ~30s while Let's Encrypt issues a cert.")


if __name__ == "__main__":
    main()
