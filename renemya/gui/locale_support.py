"""Idioma da interface no Qt: traduções do Qt, direção do texto, locale e fontes.

Applies the current Renemya language to the Qt side of the app:

* installs Qt's own translations (``qtbase_<lang>.qm``) when available, so
  standard dialogs (file picker, context menus…) follow the chosen language;
* sets the default ``QLocale`` (dates, numbers) and the layout direction
  (right-to-left for Arabic);
* registers the bundled Noto fallback fonts for scripts the system has no
  font for (CJK, Devanagari, Bengali, Arabic), e.g. a minimal Linux install.
"""

from __future__ import annotations

import os
import re
from datetime import datetime

from PySide6.QtCore import QDate, QLibraryInfo, QLocale, Qt, QTime, QTranslator
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from ..i18n import get_language, is_rtl
from .resources import asset_path

# (sistema de escrita, família, prefixo do arquivo em assets/fonts, idioma)
_W = QFontDatabase.WritingSystem
SCRIPT_FONTS = [
    (_W.SimplifiedChinese, "Noto Sans SC", "NotoSansSC", "zh_CN"),
    (_W.Japanese, "Noto Sans JP", "NotoSansJP", "ja"),
    (_W.Korean, "Noto Sans KR", "NotoSansKR", "ko"),
    (_W.Devanagari, "Noto Sans Devanagari", "NotoSansDevanagari", "hi"),
    (_W.Bengali, "Noto Sans Bengali", "NotoSansBengali", "bn"),
    (_W.Arabic, "Noto Sans Arabic", "NotoSansArabic", "ar"),
]

# Força o uso das fontes embutidas (testes / capturas simulando um sistema sem fontes)
FORCE_ENV = "RENEMYA_BUNDLED_FONTS"

_fallback: list[tuple[str, str]] | None = None  # (família, idioma) registradas
_translators: list[QTranslator] = []


def qt_locale(lang: str | None = None) -> QLocale:
    code = lang or get_language()
    return QLocale(code)


def load_fallback_fonts() -> list[str]:
    """Registra (uma vez) as fontes embutidas das escritas que o sistema não tem."""
    global _fallback
    if _fallback is None:
        _fallback = []
        force = os.environ.get(FORCE_ENV, "").strip() not in ("", "0")
        for system, family, prefix, lang in SCRIPT_FONTS:
            if not force and QFontDatabase.families(system):
                continue
            ok = False
            for style in ("Regular", "Bold"):
                path = asset_path(f"fonts/{prefix}-{style}.ttf")
                if path and QFontDatabase.addApplicationFont(str(path)) >= 0:
                    ok = True
            if ok:
                _fallback.append((family, lang))
    return [family for family, _lang in _fallback]


def fallback_families(lang: str | None = None) -> list[str]:
    """Famílias de fallback registradas, com a do idioma atual primeiro (glifos CJK certos)."""
    load_fallback_fonts()
    code = lang or get_language()
    assert _fallback is not None
    return [f for f, lg in _fallback if lg == code] + [f for f, lg in _fallback if lg != code]


def _install_qt_translations(app: QApplication, lang: str) -> None:
    for old in _translators:
        app.removeTranslator(old)
    _translators.clear()
    folder = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    for name in dict.fromkeys((lang, lang.split("_")[0])):
        translator = QTranslator(app)
        if translator.load(f"qtbase_{name}", folder):
            app.installTranslator(translator)
            _translators.append(translator)
            break


def apply_language(app: QApplication | None = None) -> None:
    """Aplica o idioma atual ao Qt (chamar depois de ``set_language``)."""
    app = app or QApplication.instance()
    lang = get_language()
    QLocale.setDefault(qt_locale(lang))
    if app is None:
        return
    _install_qt_translations(app, lang)
    app.setLayoutDirection(
        Qt.LayoutDirection.RightToLeft if is_rtl(lang) else Qt.LayoutDirection.LeftToRight
    )
    from . import theme

    theme.apply_font(app)


def format_datetime(value: datetime, seconds: bool = False) -> str:
    """Data e hora no formato curto do idioma atual (ex.: 27/10/2026 14:05, 10/27/26 2:05 PM)."""
    loc = qt_locale()
    fmt = loc.dateFormat(QLocale.FormatType.ShortFormat)
    tfmt = loc.timeFormat(QLocale.FormatType.ShortFormat)
    if seconds and "ss" not in tfmt:
        # segundos com o mesmo separador dos minutos ("HH:mm" → "HH:mm:ss", "HH.mm" → "HH.mm.ss")
        tfmt = re.sub(r"(\W?)mm", lambda m: f"{m.group(1)}mm{m.group(1) or ':'}ss", tfmt, count=1)
    date = QDate(value.year, value.month, value.day)
    time = QTime(value.hour, value.minute, value.second)
    return f"{loc.toString(date, fmt)} {loc.toString(time, tfmt)}"
