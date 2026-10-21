#!/usr/bin/env python3
"""Small cross-platform Win-Apps CLI using native package managers.

This is a separate, deliberately small first working client. It does not try to
execute the existing Pi-Apps Bash scripts on Windows.
"""
from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys

CATALOG = {
    "firefox": {
        "name": "Mozilla Firefox",
        "windows": ("winget", "Mozilla.Firefox"),
        "linux": {
            "apt": ("firefox",),
            "dnf": ("firefox",),
            "pacman": ("firefox",),
            "zypper": ("MozillaFirefox",),
            "apk": ("firefox",),
        },
    },
    "vlc": {
        "name": "VLC media player",
        "windows": ("winget", "VideoLAN.VLC"),
        "linux": {
            "apt": ("vlc",),
            "dnf": ("vlc",),
            "pacman": ("vlc",),
            "zypper": ("vlc",),
            "apk": ("vlc",),
        },
    },
    "git": {
        "name": "Git",
        "windows": ("winget", "Git.Git"),
        "linux": {
            "apt": ("git",),
            "dnf": ("git",),
            "pacman": ("git",),
            "zypper": ("git",),
            "apk": ("git",),
        },
    },
    "vscode": {
        "name": "Visual Studio Code",
        "windows": ("winget", "Microsoft.VisualStudioCode"),
        "linux": {
            "apt": ("code",),
            "dnf": ("code",),
            "pacman": ("code",),
            "zypper": ("code",),
            "apk": None,
        },
    },
    "7zip": {
        "name": "7-Zip",
        "windows": ("winget", "7zip.7zip"),
        "linux": {
            "apt": ("7zip",),
            "dnf": ("p7zip",),
            "pacman": ("7zip",),
            "zypper": ("7zip",),
            "apk": ("7zip",),
        },
    },
}

MANAGERS = (
    ("apt-get", "apt"),
    ("dnf", "dnf"),
    ("pacman", "pacman"),
    ("zypper", "zypper"),
    ("apk", "apk"),
)


def detect_platform() -> tuple[str, str | None]:
    system = platform.system().lower()
    if system == "windows":
        return "windows", "winget" if shutil.which("winget") else None
    if system == "linux":
        for executable, manager in MANAGERS:
            if shutil.which(executable):
                return "linux", manager
        return "linux", None
    return system, None


def run_command(command: list[str]) -> int:
    print("+ " + " ".join(command))
    try:
        return subprocess.run(command, check=False).returncode
    except FileNotFoundError:
        print(f"Required command not found: {command[0]}", file=sys.stderr)
        return 127
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


def package_command(app_id: str, os_name: str, manager: str | None) -> list[str] | None:
    app = CATALOG[app_id]
    if os_name == "windows":
        if manager != "winget":
            return None
        package_id = app["windows"][1]
        return [
            "winget", "install", "--id", package_id, "--exact",
            "--accept-package-agreements", "--accept-source-agreements",
        ]
    if os_name != "linux" or manager is None:
        return None
    packages = app["linux"].get(manager)
    if not packages:
        return None
    if manager == "apt":
        return ["sudo", "apt-get", "install", "-y", *packages]
    if manager == "dnf":
        return ["sudo", "dnf", "install", "-y", *packages]
    if manager == "pacman":
        return ["sudo", "pacman", "-S", "--needed", "--noconfirm", *packages]
    if manager == "zypper":
        return ["sudo", "zypper", "--non-interactive", "install", *packages]
    if manager == "apk":
        return ["sudo", "apk", "add", *packages]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Win-Apps: a small cross-platform package installer."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("list", help="list apps in the built-in catalog")
    install_parser = subparsers.add_parser("install", help="install an app")
    install_parser.add_argument("app", help="app ID; use 'list' to see options")
    args = parser.parse_args()

    os_name, manager = detect_platform()
    if args.action == "list":
        print(f"Detected platform: {os_name}; package manager: {manager or 'not found'}")
        for app_id, app in CATALOG.items():
            print(f"{app_id:10} {app['name']}")
        return 0

    app_id = args.app.lower()
    if app_id not in CATALOG:
        print(f"Unknown app: {app_id}. Run 'python winapps.py list'.", file=sys.stderr)
        return 2
    command = package_command(app_id, os_name, manager)
    if command is None:
        print(
            f"{CATALOG[app_id]['name']} has no configured installer for "
            f"{os_name}/{manager or 'no package manager'}.",
            file=sys.stderr,
        )
        return 3
    if os_name == "windows" and not shutil.which("winget"):
        print(
            "winget is not available. Install/update 'App Installer' from the "
            "Microsoft Store, then reopen the terminal.",
            file=sys.stderr,
        )
        return 4
    return run_command(command)


if __name__ == "__main__":
    raise SystemExit(main())
