#!/bin/bash
# Install general-purpose tools for server admin, debugging, and AI-assisted
# work (Claude Code) from the code-server terminal.
#
# Idempotent: each tool is skipped if already on the PATH.
set -e

apt_updated=0
apt_ensure() {
    if [ "$apt_updated" = "0" ]; then
        apt-get update -qq
        apt_updated=1
    fi
    apt-get install -y -qq "$@"
}

echo "[init.d/install-tools] checking tools..."

# --- ripgrep ---------------------------------------------------------------
# Fast search — used internally by Claude Code's Grep tool.
if ! command -v rg >/dev/null 2>&1; then
    echo "[init.d/install-tools] installing ripgrep..."
    apt_ensure ripgrep
fi

# --- jq --------------------------------------------------------------------
# JSON parsing — Docker inspect output, API responses, .env validation.
if ! command -v jq >/dev/null 2>&1; then
    echo "[init.d/install-tools] installing jq..."
    apt_ensure jq
fi

# --- yq --------------------------------------------------------------------
# YAML processor — reading and patching docker-compose.yml programmatically.
if ! command -v yq >/dev/null 2>&1; then
    echo "[init.d/install-tools] installing yq..."
    YQ_VERSION=$(curl -fsSL https://api.github.com/repos/mikefarah/yq/releases/latest \
        | grep '"tag_name"' | cut -d'"' -f4)
    curl -fsSL "https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64" \
        -o /usr/local/bin/yq
    chmod +x /usr/local/bin/yq
fi

# --- ncdu ------------------------------------------------------------------
# Interactive disk usage — essential once video files are involved.
if ! command -v ncdu >/dev/null 2>&1; then
    echo "[init.d/install-tools] installing ncdu..."
    apt_ensure ncdu
fi

# --- dig -------------------------------------------------------------------
# DNS lookup — debugging subdomain / Pangolin routing issues.
if ! command -v dig >/dev/null 2>&1; then
    echo "[init.d/install-tools] installing dig (dnsutils)..."
    apt_ensure dnsutils
fi

# --- ss / netstat ----------------------------------------------------------
# Port and socket inspection — confirming what's actually bound on the host.
if ! command -v ss >/dev/null 2>&1; then
    echo "[init.d/install-tools] installing ss (iproute2)..."
    apt_ensure iproute2
fi

# --- rsync -----------------------------------------------------------------
# File transfer and backups — moving data/ off-host cleanly.
if ! command -v rsync >/dev/null 2>&1; then
    echo "[init.d/install-tools] installing rsync..."
    apt_ensure rsync
fi

# --- lazydocker ------------------------------------------------------------
# TUI dashboard for containers, logs, and stats — friendlier than raw docker commands.
if ! command -v lazydocker >/dev/null 2>&1; then
    echo "[init.d/install-tools] installing lazydocker..."
    LD_VERSION=$(curl -fsSL https://api.github.com/repos/jesseduffield/lazydocker/releases/latest \
        | grep '"tag_name"' | cut -d'"' -f4 | tr -d 'v')
    curl -fsSL "https://github.com/jesseduffield/lazydocker/releases/download/v${LD_VERSION}/lazydocker_${LD_VERSION}_Linux_x86_64.tar.gz" \
        | tar -xz -C /usr/local/bin lazydocker
    chmod +x /usr/local/bin/lazydocker
fi

echo "[init.d/install-tools] done"
