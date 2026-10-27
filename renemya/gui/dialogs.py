"""Diálogos auxiliares."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from .. import __version__
from ..core import metadata
from ..core.journal import Journal
from ..i18n import tr
from . import neon, theme
from .resources import APP_ICON, load_pixmap

# (ícone, chave de tradução, endereço) — botões da janela "Sobre"
ABOUT_LINKS = [
    ("github", "about.github", "https://github.com/cleitinhodev"),
    ("code", "about.repo", "https://github.com/cleitinhodev/renemya"),
    ("globe", "about.site", "https://www.bugzinho.com/"),
]
DONATE_LINK = ("heart", "about.donate", "https://www.bugzinho.com/donate")


class HistoryDialog(QDialog):
    def __init__(self, journal: Journal, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("history.title"))
        self.resize(820, 420)
        layout = QVBoxLayout(self)
        entries = journal.entries()
        if not entries:
            layout.addWidget(QLabel(tr("history.empty")))
        cols = ["col_date", "col_kind", "col_count", "col_status", "col_folder"]
        table = QTableWidget(len(entries), len(cols))
        table.setHorizontalHeaderLabels([tr(f"history.{c}") for c in cols])
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.verticalHeader().setVisible(False)
        for row, e in enumerate(entries):
            status = "undone" if e.undone else e.status
            values = [
                e.created_dt.strftime("%Y-%m-%d %H:%M:%S"),
                tr(f"kind.{e.kind}"),
                str(e.count),
                tr(f"jstatus.{status}"),
                ", ".join(e.folders),
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setToolTip(value)
                table.setItem(row, col, item)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        table.resizeColumnsToContents()
        layout.addWidget(table)
        self.table = table

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.button(QDialogButtonBox.StandardButton.Close).setText(tr("button.close"))
        open_dir = QPushButton(tr("history.open_dir"))
        buttons.addButton(open_dir, QDialogButtonBox.ButtonRole.ActionRole)
        open_dir.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(journal.directory)))
        )
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


class AboutDialog(QDialog):
    """Janela "Sobre": logo, versão, créditos e botões para os links do projeto."""

    def __init__(self, parent=None, animations: bool = True) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("about.title"))
        self.setObjectName("AboutDialog")
        self.opened_urls: list[str] = []
        self.link_buttons: dict[str, QPushButton] = {}
        palette = theme.current()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 22, 26, 18)
        layout.setSpacing(6)

        logo = QLabel()
        logo.setObjectName("AboutLogo")
        ratio = self.devicePixelRatioF() or 1.0
        pix = load_pixmap(APP_ICON, round(128 * ratio))
        pix.setDevicePixelRatio(ratio)
        logo.setPixmap(pix)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        self.logo = logo

        title = QLabel("Renemya")
        title.setObjectName("AboutTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        version = QLabel(tr("about.version", version=__version__))
        version.setObjectName("VersionChip")
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(version)
        row.addStretch(1)
        layout.addLayout(row)

        tagline = QLabel(tr("about.tagline"))
        tagline.setObjectName("AboutTagline")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline.setWordWrap(True)
        layout.addSpacing(4)
        layout.addWidget(tagline)

        def avail(ok: bool) -> str:
            return tr("about.available") if ok else tr("about.missing")

        info = QLabel(
            tr("about.credits")
            + "<br>"
            + tr(
                "about.libs",
                pillow=avail(metadata.has_pillow()),
                mutagen=avail(metadata.has_mutagen()),
            )
        )
        info.setObjectName("AboutInfo")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        layout.addSpacing(10)

        links = QHBoxLayout()
        links.setSpacing(8)
        for icon_name, key, url in ABOUT_LINKS:
            links.addWidget(self._link_button(icon_name, key, url, "LinkButton", palette.accent))
        layout.addLayout(links)

        icon_name, key, url = DONATE_LINK
        self.donate_button = self._link_button(
            icon_name, key, url, "DonateButton", palette.text_on_accent
        )
        self.donate_button.setMinimumHeight(42)
        layout.addSpacing(4)
        layout.addWidget(self.donate_button)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.button(QDialogButtonBox.StandardButton.Close).setText(tr("about.close"))
        buttons.rejected.connect(self.reject)
        layout.addSpacing(6)
        layout.addWidget(buttons)

        # risco neon no botão de doação (mesma opção "Animações" da janela principal)
        self.neon_clock = neon.NeonClock(self, enabled=animations)
        self.neon_clock.watch(self)
        neon.install(
            self.donate_button,
            self.neon_clock,
            speed=150,
            trail=150,
            streaks=2,
            radius=12,
            inset=1.5,
            width=2.2,
            glow=8,
            phase=0.15,
            color="#fff4e6",  # risco claro: sobre o botão laranja o neon laranja sumiria
        )
        self.setMinimumWidth(500)

    def _link_button(self, icon_name: str, key: str, url: str, name: str, color: str):
        button = QPushButton(tr(key))
        button.setObjectName(name)
        button.setIcon(theme.icon(icon_name, color))
        button.setIconSize(QSize(18, 18))
        button.setToolTip(url)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setAutoDefault(False)
        button.setProperty("url", url)
        button.clicked.connect(lambda _c=False, u=url: self.open_url(u))
        self.link_buttons[url] = button
        return button

    def open_url(self, url: str) -> None:
        self.opened_urls.append(url)
        QDesktopServices.openUrl(QUrl(url))
