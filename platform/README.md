# Cross-platform foundation

This directory introduces platform detection for Win-Apps. It is deliberately
separate from the existing Pi-Apps-derived Bash application, because the current
GUI, installer, and many app scripts rely on Linux-specific commands and
packages.

## Detect the host

### Linux

```bash
bash platform/detect.sh
bash platform/detect.sh --json
``

Reads `/etc/os-release` and `uname`; it does not install packages or require
root privileges.

### Windows

Run PowerShell 5.1 or PowerShell 7:

```powershell
.\platform\detect.ps1
.\platform\detect.ps1 -Json
``

The Windows detector reads OS metadata and checks whether `winget` is present.
It does not install anything.

## Compatibility policy

Detection is not the same as application support. A future app manifest should
declare supported operating systems, architectures, install/uninstall methods,
and verified versions. The installer must refuse unsupported combinations with
a clear explanation rather than running a Linux Bash script on Windows.

The intended initial test targets are Windows 10/11 and mainstream Linux
distributions (Debian/Ubuntu, Fedora, and Arch-based systems) on x86_64 and
ARM64 where the individual application supports that architecture. This is a
goal, not a claim that every existing app works on every target.

## Next implementation stages

1. Add a shared app manifest with per-platform install definitions.
2. Implement Windows install/uninstall using PowerShell and winget or official
   vendor installers.
3. Add Linux package-manager adapters (apt, dnf, pacman, zypper, apk) while
   preserving app-specific prerequisites.
4. Migrate and test applications one by one; mark unported apps as unsupported.
5. Test installs, updates, uninstalls, and failure recovery on clean VMs.

Do not run arbitrary app install scripts with administrator/root privileges
without reviewing their contents. Only use trusted sources and verify downloads.
