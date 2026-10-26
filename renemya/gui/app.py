"""Ponto de entrada da interface gráfica."""

from __future__ import annotations

import sys

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from .. import __version__
from ..i18n import detect_language, set_language
from . import theme
from .resources import APP_ICON, load_icon, set_windows_app_id


def create_app(argv: list[str] | None = None) -> QApplication:
    set_windows_app_id()  # antes de qualquer janela: barra de tarefas com o ícone do Renemya
    app = QApplication.instance() or QApplication(argv if argv is not None else sys.argv)
    app.setApplicationName("Renemya")
    app.setOrganizationName("CleitinhoDEV")
    app.setApplicationVersion(__version__)
    # Tema colorido (claro/escuro conforme o sistema), sobre o estilo Fusion
    theme.apply_theme(app)
    app.setWindowIcon(load_icon(APP_ICON))  # ícone geral (barra de tarefas, Alt+Tab)
    return app


def main(argv: list[str] | None = None) -> int:
    app = create_app(argv)
    settings = QSettings("CleitinhoDEV", "Renemya")
    set_language(str(settings.value("language", "") or detect_language()))
    from .main_window import MainWindow

    window = MainWindow(settings=settings)
    theme.follow_system_theme(app, on_change=window.rebuild_for_theme)
    window.show()
    return app.exec()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
