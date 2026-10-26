"""Ícones do aplicativo e integração com o Windows (barra de tarefas).

Os ícones ficam dentro do pacote (``renemya/gui/assets``), então funcionam no
código-fonte, no ``pip install`` e no executável do PyInstaller (``--collect-data``).
"""

from __future__ import annotations

import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().with_name("assets")

APP_ICON = "renemya_icon"  # ícone geral: executável, barra de tarefas, "Sobre", README
TITLE_ICON = "renemya_favicon"  # ícone da barra de título da janela

# Identificador próprio para o Windows agrupar as janelas com o ícone do app
# (sem ele, a barra de tarefas pode mostrar o ícone genérico do Python).
APP_USER_MODEL_ID = "CleitinhoDEV.Renemya"


def asset_path(name: str) -> Path | None:
    """Caminho de um arquivo em ``assets`` (``None`` se não existir — o app abre mesmo assim)."""
    candidates = [ASSETS_DIR / name]
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass) / "renemya" / "gui" / "assets" / name)
    for path in candidates:
        if path.exists():
            return path
    return None


def load_icon(name: str):
    """``QIcon`` com todos os tamanhos do .ico (16 a 256 px)."""
    from PySide6.QtGui import QIcon

    path = asset_path(f"{name}.ico") or asset_path(f"{name}.png")
    return QIcon(str(path)) if path else QIcon()


def load_pixmap(name: str, size: int):
    """Imagem do ícone em alta resolução (PNG de 256 px), reduzida com suavização."""
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QPixmap

    path = asset_path(f"{name}.png")
    if not path:
        return QPixmap()
    pix = QPixmap(str(path))
    return pix.scaled(
        size,
        size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )


def set_windows_app_id() -> bool:
    """No Windows, define o AppUserModelID antes de criar janelas. Nos outros sistemas, nada."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_USER_MODEL_ID)
        return True
    except (AttributeError, OSError):  # pragma: no cover - depende do Windows
        return False


def set_windows_taskbar_icon(widget) -> bool:
    """No Windows, deixa a barra de título com o favicon e a barra de tarefas com o ícone geral.

    O Qt usa o mesmo ícone para as duas; aqui o ícone *grande* (barra de tarefas,
    Alt+Tab) é trocado pelo ``renemya_icon`` direto pela API do Windows.
    """
    if sys.platform != "win32":
        return False
    path = asset_path(f"{APP_ICON}.ico")
    if not path:
        return False
    try:  # pragma: no cover - depende do Windows
        import ctypes

        user32 = ctypes.windll.user32
        user32.LoadImageW.restype = ctypes.c_void_p
        user32.SendMessageW.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint,
            ctypes.c_size_t,
            ctypes.c_void_p,
        ]
        image_icon, lr_loadfromfile, wm_seticon, icon_big = 1, 0x10, 0x80, 1
        size = user32.GetSystemMetrics(11)  # SM_CXICON
        hicon = user32.LoadImageW(None, str(path), image_icon, size, size, lr_loadfromfile)
        if not hicon:
            return False
        user32.SendMessageW(int(widget.winId()), wm_seticon, icon_big, hicon)
        return True
    except (AttributeError, OSError, ValueError):  # pragma: no cover
        return False
