"""Ponto de entrada da interface gráfica."""

from __future__ import annotations

import os
import sys
import tempfile

from PySide6.QtCore import QSettings, QTimer
from PySide6.QtWidgets import QApplication

from .. import __version__
from ..i18n import detect_language, set_language
from . import theme
from .locale_support import apply_language
from .resources import APP_ICON, load_icon, set_windows_app_id


def create_app(argv: list[str] | None = None) -> QApplication:
    set_windows_app_id()  # antes de qualquer janela: barra de tarefas com o ícone do Renemya
    app = QApplication.instance() or QApplication(argv if argv is not None else sys.argv)
    app.setApplicationName("Renemya")
    app.setOrganizationName("CleitinhoDEV")
    app.setApplicationVersion(__version__)
    # Liga a janela ao renemya.desktop no Linux (ícone certo no Wayland/GNOME)
    app.setDesktopFileName("renemya")
    # Tema colorido (claro/escuro conforme o sistema), sobre o estilo Fusion
    theme.apply_theme(app)
    app.setWindowIcon(load_icon(APP_ICON))  # ícone geral (barra de tarefas, Alt+Tab)
    return app


def _parse_args(argv: list[str]) -> tuple[str, str | None]:
    """Lê as opções simples da interface: ``--version``, ``--smoke-test`` e uma pasta.

    Retorna ``(ação, pasta)``, onde ação é ``"run"``, ``"version"`` ou ``"smoke"``.
    Opções desconhecidas (ex.: as do Qt, como ``-platform``) são ignoradas.
    """
    action = "run"
    folder = None
    for arg in argv[1:]:
        if arg in ("--version", "-V"):
            return "version", None
        if arg == "--smoke-test":
            action = "smoke"
        elif not arg.startswith("-") and folder is None and os.path.isdir(arg):
            folder = arg
    return action, folder


def _print(text: str) -> None:
    # No executável "windowed" do Windows não há console: sys.stdout pode ser None.
    if sys.stdout is not None:
        print(text, flush=True)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv if argv is None else argv)
    action, folder = _parse_args(argv)
    if action == "version":
        _print(f"Renemya {__version__}")
        return 0
    if action == "smoke":
        return _smoke_test(argv)

    app = create_app(argv)
    settings = QSettings("CleitinhoDEV", "Renemya")
    set_language(str(settings.value("language", "") or detect_language()))
    apply_language(app)
    from .main_window import MainWindow

    window = MainWindow(settings=settings)
    theme.follow_system_theme(app, on_change=window.rebuild_for_theme)
    window.show()
    if folder:
        window.set_folder(folder)
    return app.exec()


def _smoke_test(argv: list[str]) -> int:
    """Abre a janela principal por um instante e fecha (usado na CI dos executáveis).

    Usa configurações e pasta de dados temporárias, para não tocar nas do usuário.
    """
    with tempfile.TemporaryDirectory(prefix="renemya-smoke-") as tmp:
        os.environ["RENEMYA_DATA_DIR"] = os.path.join(tmp, "data")
        sample = os.path.join(tmp, "pasta")
        os.makedirs(sample)
        for name in ("Foto 1.JPG", "foto 2.jpg", "música.mp3"):
            open(os.path.join(sample, name), "wb").close()
        app = create_app(argv)
        settings = QSettings(os.path.join(tmp, "settings.ini"), QSettings.Format.IniFormat)
        set_language(detect_language())
        apply_language(app)
        from .main_window import MainWindow

        window = MainWindow(settings=settings)
        window.show()
        window.set_folder(sample)
        QTimer.singleShot(1500, app.quit)
        code = app.exec()
        window.close()
        _print(f"Renemya {__version__}: smoke test ok (Qt {app.platformName()})")
        return code


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
