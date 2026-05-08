#!/bin/bash
# Self-heal the /config/.venv mkdocs install. The BNKops code-server image
# ships mkdocs in /config/.venv, but /config is a host volume — so when the
# underlying image's system Python changes path (or, as of 2026-05, is
# dropped entirely), the persisted venv's shebangs break. This script
# guarantees a working `mkdocs` on the IDE's PATH at every container start.
#
# Idempotent: no-op when python3 + a working venv are already present.
set -e

if ! command -v python3 >/dev/null 2>&1; then
    echo "[init.d/install-mkdocs] installing python3..."
    apt-get update -qq
    apt-get install -y -qq python3 python3-venv
fi

if ! /config/.venv/bin/mkdocs --version >/dev/null 2>&1; then
    echo "[init.d/install-mkdocs] (re)building venv..."
    rm -rf /config/.venv
    python3 -m venv /config/.venv
    /config/.venv/bin/pip install --quiet --upgrade pip
    /config/.venv/bin/pip install --quiet "mkdocs-material[recommended]"
    chown -R abc:abc /config/.venv
fi

echo "[init.d/install-mkdocs] $(/config/.venv/bin/mkdocs --version 2>/dev/null)"
