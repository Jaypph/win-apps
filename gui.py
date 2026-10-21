"""Cross-platform Win Apps graphical app browser, inspired by Flathub's layout.

Run with: python -m pip install -r requirements.txt && python gui.py
"""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QProcess
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMessageBox, QPushButton,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget, QProgressBar
)

try:
    from winapps import APPS, package_command
except ImportError:
    APPS = {
        "firefox": {"name": "Firefox", "description": "A fast, private web browser.", "category": "Internet", "icon": "🦊"},
        "vlc": {"name": "VLC media player", "description": "Play almost any video or audio format.", "category": "Audio & Video", "icon": "🎬"},
        "git": {"name": "Git", "description": "Distributed version control for developers.", "category": "Developer Tools", "icon": "🌿"},
        "vscode": {"name": "Visual Studio Code", "description": "A code editor for building and debugging apps.", "category": "Developer Tools", "icon": "🧩"},
        "7zip": {"name": "7-Zip", "description": "File archiver with high compression ratios.", "category": "Utilities", "icon": "🗜️"},
    }
    package_command = None

APP_META = {
    "firefox": ("Firefox", "A fast, private web browser.", "Internet", "🦊"),
    "vlc": ("VLC media player", "Play almost any video or audio format.", "Audio & Video", "🎬"),
    "git": ("Git", "Distributed version control for developers.", "Developer Tools", "🌿"),
    "vscode": ("Visual Studio Code", "A code editor for building and debugging apps.", "Developer Tools", "🧩"),
    "7zip": ("7-Zip", "File archiver with high compression ratios.", "Utilities", "🗜️"),
}
BG = "#f7f8fa"
INK = "#202124"
MUTED = "#687078"
GREEN = "#287a4b"
BORDER = "#e2e6e9"
CARD = "#ffffff"

class AppCard(QFrame):
    def __init__(self, app_id: str, meta: tuple[str, str, str, str], install_callback):
        super().__init__()
        name, description, category, emoji = meta
        self.app_id = app_id
        self.setObjectName("appCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 16)
        layout.setSpacing(10)

        top = QHBoxLayout()
        icon = QLabel(emoji)
        icon.setObjectName("appIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setFixedSize(58, 58)
        top.addWidget(icon, 0, Qt.AlignmentFlag.AlignTop)
        top.addStretch(1)
        cat = QLabel(category)
        cat.setObjectName("categoryTag")
        cat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top.addWidget(cat, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(top)

        title = QLabel(name)
        title.setObjectName("appTitle")
        title.setWordWrap(True)
        layout.addWidget(title)
        desc = QLabel(description)
        desc.setObjectName("appDescription")
        desc.setWordWrap(True)
        desc.setMinimumHeight(42)
        layout.addWidget(desc)
        bottom = QHBoxLayout()
        bottom.addStretch(1)
        self.install = QPushButton("Installér")
        self.install.setObjectName("installButton")
        self.install.setCursor(Qt.CursorShape.PointingHandCursor)
        self.install.clicked.connect(lambda: install_callback(app_id, name))
        bottom.addWidget(self.install)
        layout.addLayout(bottom)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Win Apps")
        self.resize(1120, 760)
        self.setMinimumSize(760, 560)
        self.process = None
        self.active_category = "Alle apps"

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(18, 22, 14, 18)
        side.setSpacing(8)
        brand = QLabel("◈  Win Apps")
        brand.setObjectName("brand")
        side.addWidget(brand)
        tagline = QLabel("Find apps for your computer")
        tagline.setObjectName("sideTagline")
        tagline.setWordWrap(True)
        side.addWidget(tagline)
        side.addSpacing(20)
        nav_label = QLabel("UDFORSK")
        nav_label.setObjectName("navLabel")
        side.addWidget(nav_label)
        self.nav = QListWidget()
        self.nav.setObjectName("navList")
        categories = ["Alle apps", "Internet", "Audio & Video", "Developer Tools", "Utilities"]
        for category in categories:
            self.nav.addItem(QListWidgetItem(category))
        self.nav.setCurrentRow(0)
        self.nav.currentTextChanged.connect(self.change_category)
        side.addWidget(self.nav, 1)
        foot = QLabel("Windows  •  Linux\nInstallerer via systemets pakkehåndtering")
        foot.setObjectName("sideFoot")
        foot.setWordWrap(True)
        side.addWidget(foot)
        outer.addWidget(side)

        content = QWidget()
        content.setObjectName("content")
        main = QVBoxLayout(content)
        main.setContentsMargins(30, 24, 30, 24)
        main.setSpacing(18)

        header = QHBoxLayout()
        page_title = QLabel("Udforsk apps")
        page_title.setObjectName("pageTitle")
        header.addWidget(page_title)
        header.addStretch(1)
        self.search = QLineEdit()
        self.search.setPlaceholderText("⌕  Søg efter apps…")
        self.search.setClearButtonEnabled(True)
        self.search.setObjectName("searchBox")
        self.search.setFixedWidth(320)
        self.search.textChanged.connect(self.refresh_cards)
        header.addWidget(self.search)
        main.addLayout(header)

        hero = QFrame()
        hero.setObjectName("hero")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 20, 24, 20)
        hero_layout.setSpacing(7)
        hero_title = QLabel("Find din næste favoritapp")
        hero_title.setObjectName("heroTitle")
        hero_sub = QLabel("Et samlet sted at opdage og installere programmer på Windows og Linux.")
        hero_sub.setObjectName("heroSub")
        hero_sub.setWordWrap(True)
        hero_layout.addWidget(hero_title)
        hero_layout.addWidget(hero_sub)
        main.addWidget(hero)

        section = QHBoxLayout()
        self.section_title = QLabel("Populære apps")
        self.section_title.setObjectName("sectionTitle")
        section.addWidget(self.section_title)
        section.addStretch(1)
        self.result_count = QLabel("")
        self.result_count.setObjectName("muted")
        section.addWidget(self.result_count)
        main.addLayout(section)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("appScroll")
        self.grid_host = QWidget()
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(2, 2, 8, 12)
        self.grid.setHorizontalSpacing(14)
        self.grid.setVerticalSpacing(14)
        scroll.setWidget(self.grid_host)
        main.addWidget(scroll, 1)

        self.status = QLabel("Klar")
        self.status.setObjectName("status")
        main.addWidget(self.status)
        outer.addWidget(content, 1)

        self.setStyleSheet(f"""
            QWidget#root, QWidget#content {{ background: {BG}; color: {INK}; }}
            QWidget#sidebar {{ background: #fff; border-right: 1px solid {BORDER}; }}
            QLabel#brand {{ font-size: 22px; font-weight: 750; color: {GREEN}; padding: 2px 0; }}
            QLabel#sideTagline {{ color: {MUTED}; font-size: 12px; }}
            QLabel#navLabel {{ color: #818990; font-size: 10px; font-weight: 700; letter-spacing: 1px; }}
            QListWidget#navList {{ border: none; background: transparent; outline: 0; }}
            QListWidget#navList::item {{ padding: 11px 12px; border-radius: 8px; color: #394047; }}
            QListWidget#navList::item:selected {{ background: #e8f4ec; color: {GREEN}; font-weight: 650; }}
            QLabel#sideFoot {{ color: #818990; font-size: 11px; padding-top: 12px; }}
            QLabel#pageTitle {{ font-size: 27px; font-weight: 750; }}
            QLineEdit#searchBox {{ background: #fff; border: 1px solid {BORDER}; border-radius: 10px; padding: 11px 13px; font-size: 13px; }}
            QLineEdit#searchBox:focus {{ border: 1px solid {GREEN}; }}
            QFrame#hero {{ background: #e8f4ec; border: 1px solid #d5e9db; border-radius: 14px; }}
            QLabel#heroTitle {{ font-size: 21px; font-weight: 750; color: #174e30; }}
            QLabel#heroSub {{ color: #3d654d; font-size: 13px; }}
            QLabel#sectionTitle {{ font-size: 18px; font-weight: 700; }}
            QLabel#muted {{ color: {MUTED}; font-size: 12px; }}
            QFrame#appCard {{ background: {CARD}; border: 1px solid {BORDER}; border-radius: 12px; }}
            QFrame#appCard:hover {{ border: 1px solid #a8cbb4; }}
            QLabel#appIcon {{ background: #f1f5f2; border-radius: 12px; font-size: 27px; }}
            QLabel#appTitle {{ font-size: 15px; font-weight: 700; }}
            QLabel#appDescription {{ color: {MUTED}; font-size: 12px; }}
            QLabel#categoryTag {{ background: #f0f2f3; color: #596168; border-radius: 7px; padding: 5px 7px; font-size: 10px; }}
            QPushButton#installButton {{ background: {GREEN}; color: white; border: none; border-radius: 8px; padding: 8px 15px; font-weight: 650; }}
            QPushButton#installButton:hover {{ background: #1e633b; }}
            QPushButton#installButton:disabled {{ background: #b8c7bd; }}
            QLabel#status {{ color: {MUTED}; font-size: 11px; padding-top: 3px; }}
            QScrollArea#appScroll {{ background: transparent; }}
        """)
        self.refresh_cards()

    def change_category(self, category):
        if not category:
            return
        self.active_category = category
        self.section_title.setText("Populære apps" if category == "Alle apps" else category)
        self.refresh_cards()

    def refresh_cards(self, *_):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        query = self.search.text().strip().casefold()
        visible = []
        for app_id, meta in APP_META.items():
            name, description, category, _ = meta
            if self.active_category != "Alle apps" and category != self.active_category:
                continue
            if query and query not in " ".join((app_id, name, description, category)).casefold():
                continue
            visible.append((app_id, meta))
        for i, (app_id, meta) in enumerate(visible):
            self.grid.addWidget(AppCard(app_id, meta, self.install_app), i // 3, i % 3)
        self.result_count.setText(f"{len(visible)} apps")
        if not visible:
            empty = QLabel("Ingen apps matcher din søgning.")
            empty.setObjectName("muted")
            self.grid.addWidget(empty, 0, 0)

    def install_app(self, app_id, name):
        import platform
        system = platform.system().lower()
        if system == "windows":
            import shutil
            if not shutil.which("winget"):
                QMessageBox.warning(self, "Winget mangler", "Installér eller aktivér Windows Package Manager (winget), og prøv igen.")
                return
            command = ["winget", "install", "--id", {"firefox":"Mozilla.Firefox","vlc":"VideoLAN.VLC","git":"Git.Git","vscode":"Microsoft.VisualStudioCode","7zip":"7zip.7zip"}[app_id], "--exact", "--accept-package-agreements", "--accept-source-agreements"]
        elif system == "linux":
            import shutil
            managers = [("apt-get", ["sudo", "apt-get", "install", "-y"]), ("dnf", ["sudo", "dnf", "install", "-y"]), ("pacman", ["sudo", "pacman", "-S", "--noconfirm"]), ("zypper", ["sudo", "zypper", "--non-interactive", "install"]), ("apk", ["sudo", "apk", "add"])]
            found = next(((exe, prefix) for exe, prefix in managers if shutil.which(exe)), None)
            if not found:
                QMessageBox.warning(self, "Ikke understøttet", "Fandt ingen understøttet pakkehåndtering (apt, dnf, pacman, zypper eller apk).")
                return
            exe, prefix = found
            package = {"firefox":"firefox","vlc":"vlc","git":"git","vscode":"code","7zip":"7zip"}[app_id]
            command = prefix + [package]
        else:
            QMessageBox.warning(self, "System ikke understøttet", "Win Apps understøtter i øjeblikket Windows og Linux.")
            return
        answer = QMessageBox.question(self, "Bekræft installation", f"Vil du installere {name}?\n\nKommando: {' '.join(command)}")
        if answer != QMessageBox.StandardButton.Yes:
            return
        self.status.setText(f"Installerer {name}…")
        self.set_install_buttons_enabled(False)
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.read_process_output)
        self.process.finished.connect(lambda code, status: self.install_finished(name, code))
        self.process.start(command[0], command[1:])

    def read_process_output(self):
        if self.process:
            output = bytes(self.process.readAllStandardOutput()).decode(errors="replace").strip()
            if output:
                self.status.setText(output[-180:])

    def install_finished(self, name, code):
        self.set_install_buttons_enabled(True)
        if code == 0:
            self.status.setText(f"{name} blev installeret.")
            QMessageBox.information(self, "Installation færdig", f"{name} blev installeret.")
        else:
            self.status.setText(f"Installation af {name} fejlede (kode {code}).")
            QMessageBox.warning(self, "Installation fejlede", f"Installationen af {name} fejlede. Se terminalen/status for detaljer.")

    def set_install_buttons_enabled(self, enabled):
        for i in range(self.grid.count()):
            widget = self.grid.itemAt(i).widget()
            if isinstance(widget, AppCard):
                widget.install.setEnabled(enabled)

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
