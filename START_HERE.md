# Win-Apps: Windows and Linux quick start

The legacy GUI and Pi-Apps-derived Bash scripts are Linux-specific. They do not
run natively on Windows. This repository now includes a separate cross-platform
CLI for a small initial catalog, using native package managers.

## Requirements

- Python 3.10+
- Windows 10/11: Microsoft's `winget` command (App Installer)
- Linux: `apt-get`, `dnf`, `pacman`, `zypper`, or `apk`, and `sudo`

## Run it

From the repository directory:

```text
python winapps.py list
python winapps.py install firefox
python winapps.py install vlc
python winapps.py install git
python winapps.py install vscode
python winapps.py install 7zip
```

On Windows, use `py winapps.py list` if `python` is not on PATH. Linux installs
use `sudo` and the detected native package manager. Review package and publisher
details before confirming installation.

This is an initial working CLI, not yet a full port of the legacy GUI. The
catalog is deliberately small, and package availability varies by distribution.
It is not realistic to promise every application on every OS or CPU without
per-app support definitions and testing. See [CROSS_PLATFORM.md](CROSS_PLATFORM.md).
