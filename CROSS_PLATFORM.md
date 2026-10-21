# Win-Apps on Windows and Linux

Win-Apps currently contains legacy Pi-Apps-derived Bash scripts. Those scripts
are not a native Windows application and are not compatible with every Linux
distribution. The new `winapps.py` CLI is a separate cross-platform starting
point that uses the operating system's package manager.

## Requirements

- Python 3.10 or newer
- Windows: Windows 10/11 with Microsoft's `winget` command (App Installer)
- Linux: one of `apt-get`, `dnf`, `pacman`, `zypper`, or `apk`, plus `sudo`

## Use

From the repository folder:

```text
python winapps.py list
python winapps.py install firefox
python winapps.py install vlc
python winapps.py install git
python winapps.py install vscode
python winapps.py install 7zip
```

On Windows, use `py winapps.py list` if `python` is not on PATH. Installation
commands call winget with exact package IDs and ask winget to accept the package
and source agreements. Review prompts and publisher information before
confirming installations.

On Linux, the CLI uses the detected package manager and `sudo`. Package names
and availability vary by distribution; an app is reported as unsupported if no
mapping is configured. It does not execute the old app-specific Bash scripts.

## Current limits

This is a small initial catalog, not full parity with the legacy GUI. The
existing GUI and app scripts have not yet been ported to Windows, and no
software catalog can honestly promise every application on every Linux distro
or CPU architecture. Support should be added per app and tested on clean
Windows/Linux environments before it is advertised as stable.
