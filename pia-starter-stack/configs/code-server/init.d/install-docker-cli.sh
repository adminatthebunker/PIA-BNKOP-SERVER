#!/bin/bash
# Install the Docker CLI so `docker` and `docker compose` work from the
# code-server terminal (and from Claude Code running inside it).
#
# The Docker socket is mounted in from the host (see docker-compose.yml) —
# this script ensures the CLI binary is present and that the linuxserver
# `abc` user (UID 1000) is in a group matching the socket's host GID so it
# can actually connect.
#
# Idempotent: skips the apt install when docker is on PATH; re-checks the
# socket group on every run.
set -e

if command -v docker >/dev/null 2>&1; then
    echo "[init.d/install-docker-cli] $(docker --version) — already installed, skipping"
else
    echo "[init.d/install-docker-cli] installing Docker CLI..."
    apt-get update -qq
    apt-get install -y -qq ca-certificates curl
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
      https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" \
      > /etc/apt/sources.list.d/docker.list
    apt-get update -qq
    apt-get install -y -qq docker-ce-cli docker-compose-plugin
    echo "[init.d/install-docker-cli] $(docker --version)"
fi

# Grant the abc user access to the bind-mounted docker socket. The host
# socket is owned by root:docker (gid varies per host), and the container
# has no matching group out of the box — so `docker ps` from the IDE
# terminal hits "permission denied" until we line the GIDs up.
SOCK=/var/run/docker.sock
if [ -S "$SOCK" ]; then
    SOCK_GID=$(stat -c '%g' "$SOCK")
    if [ "$SOCK_GID" -eq 0 ]; then
        echo "[init.d/install-docker-cli] socket is root:root — nothing to do"
    else
        # Make sure a group with the socket's GID exists, then add abc to it.
        # If a group with that GID already exists (any name), reuse it; else
        # create one called `docker` (or `hostdocker` if the name is taken).
        GROUP_NAME=$(getent group "$SOCK_GID" | cut -d: -f1 || true)
        if [ -z "$GROUP_NAME" ]; then
            GROUP_NAME=docker
            if getent group docker >/dev/null; then GROUP_NAME=hostdocker; fi
            groupadd -g "$SOCK_GID" "$GROUP_NAME"
            echo "[init.d/install-docker-cli] created group $GROUP_NAME (gid $SOCK_GID)"
        fi
        if id -nG abc | tr ' ' '\n' | grep -qx "$GROUP_NAME"; then
            echo "[init.d/install-docker-cli] abc already in $GROUP_NAME (gid $SOCK_GID)"
        else
            usermod -aG "$GROUP_NAME" abc
            echo "[init.d/install-docker-cli] added abc to $GROUP_NAME (gid $SOCK_GID)"
        fi
    fi
else
    echo "[init.d/install-docker-cli] $SOCK not mounted — skipping group setup"
fi
