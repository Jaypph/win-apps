# Win Apps — cross-platform app browser

Win Apps is being developed as a simple graphical app browser for Windows and Linux. The UI takes inspiration from Flathub's clean app-store layout: a left category sidebar, search field, featured banner, and app cards with install buttons. It is an original implementation and does not copy Flathub's logos, source code, or artwork.

## Run the graphical interface

Requires Python 3.10 or newer.

```bash
python -m pip install -r requirements.txt
python gui.py
```

On Windows, installations use Windows Package Manager (`winget`). On Linux, the initial CLI/GUI prototype supports apt, dnf, pacman, zypper, and apk where packages are available. Linux package names and availability vary by distribution; not every app is available on every system yet.

The current catalogue is a small starter list (Firefox, VLC, Git, Visual Studio Code, and 7-Zip). The GUI is a prototype, not yet a full replacement for Flathub or a complete port of the legacy Win Apps project. Installation requires the appropriate system permissions and package manager. Please review prompts before confirming an install.
