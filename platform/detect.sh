#!/usr/bin/env bash
# Detect the current Linux platform without modifying the host.
# Usage: bash platform/detect.sh [--json]
set -euo pipefail

if [[ "${OSTYPE:-}" != linux* ]] && [[ "$(uname -s 2>/dev/null || true)" != Linux ]]; then
  printf 'error: this detector supports Linux only; use detect.ps1 on Windows.\n' >&2
  exit 2
fi

. /etc/os-release 2>/dev/null || true
os_id="${ID:-unknown}"
os_like="${ID_LIKE:-}"
version_id="${VERSION_ID:-unknown}"
arch="$(uname -m 2>/dev/null || printf unknown)"

case "$arch" in
  x86_64|amd64) arch="x86_64" ;;
  aarch64|arm64) arch="arm64" ;;
  armv7l|armv7*) arch="armv7" ;;
  i386|i486|i586|i686) arch="x86" ;;
esac

# Family is a hint for choosing a package manager, not a guarantee that every
# application supports the distribution.
family="unknown"
case " $os_id $os_like " in
  *" debian "*|*" ubuntu "*|*" linuxmint "*|*" pop "*|*" raspbian "*) family="debian" ;;
  *" fedora "*|*" rhel "*|*" centos "*|*" rocky "*|*" almalinux "*) family="redhat" ;;
  *" arch "*|*" manjaro "*|*" endeavouros "*) family="arch" ;;
  *" opensuse "*|*" suse "*) family="suse" ;;
  *" alpine "*) family="alpine" ;;
esac

if [[ "${1:-}" == "--json" ]]; then
  printf '{"os":"linux","id":"%s","id_like":"%s","version":"%s","arch":"%s","family":"%s"}\n' \
    "$os_id" "$os_like" "$version_id" "$arch" "$family"
else
  printf 'os=linux\nid=%s\nid_like=%s\nversion=%s\narch=%s\nfamily=%s\n' \
    "$os_id" "$os_like" "$version_id" "$arch" "$family"
fi
