"""Traduções da interface e da linha de comando.

Os textos ficam em arquivos JSON (um por idioma, ex.: ``pt_BR.json``, ``en.json``). Para criar
uma tradução nova basta copiar ``en.json``, traduzir os valores (mantendo as chaves e os
``{marcadores}``) e registrar o código em ``LANGUAGES``.
"""

from __future__ import annotations

import json
import locale
import os
import sys
from functools import cache
from importlib import resources
from typing import Any

DEFAULT_LANGUAGE = "pt_BR"
FALLBACK_LANGUAGE = "en"

# Código -> nome do idioma na própria língua (é assim que aparece no menu Idioma).
LANGUAGES = {
    "pt_BR": "Português (Brasil)",
    "en": "English",
    "es": "Español",
    "zh_CN": "中文（简体）",
    "hi": "हिन्दी",
    "ar": "العربية",
    "fr": "Français",
    "ru": "Русский",
    "bn": "বাংলা",
    "ja": "日本語",
    "de": "Deutsch",
    "id": "Bahasa Indonesia",
    "ko": "한국어",
    "tr": "Türkçe",
    "it": "Italiano",
}

# Idiomas escritos da direita para a esquerda (a interface é espelhada).
RTL_LANGUAGES = frozenset({"ar"})

# Prefixos ISO 639-1 e nomes em inglês (o Windows às vezes informa "Portuguese_Brazil").
_ALIASES = {
    "pt": "pt_BR",
    "portuguese": "pt_BR",
    "en": "en",
    "english": "en",
    "es": "es",
    "spanish": "es",
    "zh": "zh_CN",
    "chinese": "zh_CN",
    "hi": "hi",
    "hindi": "hi",
    "ar": "ar",
    "arabic": "ar",
    "fr": "fr",
    "french": "fr",
    "ru": "ru",
    "russian": "ru",
    "bn": "bn",
    "bengali": "bn",
    "bangla": "bn",
    "ja": "ja",
    "japanese": "ja",
    "de": "de",
    "german": "de",
    "id": "id",
    "in": "id",  # código antigo do indonésio (Java/Android)
    "indonesian": "id",
    "ko": "ko",
    "korean": "ko",
    "tr": "tr",
    "turkish": "tr",
    "it": "it",
    "italian": "it",
}

_current = DEFAULT_LANGUAGE


@cache
def _load(lang: str) -> dict[str, str]:
    try:
        text = resources.files(__package__).joinpath(f"{lang}.json").read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return {}
    return json.loads(text)


def normalize_language(lang: str | None) -> str:
    """Converte um código/nome de locale (``pt-PT``, ``de_DE.UTF-8``, ``Japanese_Japan``…)
    para um dos idiomas de ``LANGUAGES``; desconhecidos caem para o inglês."""
    if not lang:
        return DEFAULT_LANGUAGE
    lang = lang.strip().replace("-", "_")
    if lang in LANGUAGES:
        return lang
    base = lang.split(".")[0].split("@")[0]
    for key in (base, base.lower()):
        if key in LANGUAGES:
            return key
    low = base.lower()
    head = low.split("_")[0].split(" ")[0].split("(")[0]
    return _ALIASES.get(head, FALLBACK_LANGUAGE)


def _windows_ui_locale() -> str:  # pragma: no cover - só no Windows
    """Idioma de exibição do Windows (ex.: ``pt-BR``); se falhar, o formato regional."""
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        buf = ctypes.create_unicode_buffer(85)
        langid = kernel32.GetUserDefaultUILanguage()
        if langid and kernel32.LCIDToLocaleName(langid, buf, len(buf), 0):
            return buf.value
        if kernel32.GetUserDefaultLocaleName(buf, len(buf)):
            return buf.value
    except (AttributeError, OSError, ValueError):
        pass
    return ""


def system_locale() -> str:
    """Locale do sistema (ex.: ``pt_BR``, ``ja-JP``) ou ``""`` se não der para saber."""
    for var in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        value = os.environ.get(var, "")
        if var == "LANGUAGE":
            value = value.split(":")[0]
        if value and value.split(".")[0] not in ("C", "POSIX"):
            return value
    if sys.platform == "win32":
        win = _windows_ui_locale()
        if win:
            return win
    try:
        loc = locale.getlocale()[0] or ""
    except (ValueError, TypeError):  # pragma: no cover
        loc = ""
    return "" if loc in ("C", "POSIX") else loc


def detect_language() -> str:
    """``RENEMYA_LANG`` (se definida) ou o idioma do sistema; sem suporte, inglês."""
    env = os.environ.get("RENEMYA_LANG")
    if env:
        return normalize_language(env)
    loc = system_locale()
    if not loc:
        return FALLBACK_LANGUAGE
    return normalize_language(loc)


def set_language(lang: str) -> str:
    global _current
    _current = normalize_language(lang)
    return _current


def get_language() -> str:
    return _current


def is_rtl(lang: str | None = None) -> bool:
    """Se o idioma (o atual, por padrão) é escrito da direita para a esquerda."""
    return (lang or _current) in RTL_LANGUAGES


def language_list() -> str:
    """Códigos aceitos, separados por vírgula (usado na ajuda da linha de comando)."""
    return ", ".join(LANGUAGES)


class _SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def tr(key: str, **params: Any) -> str:
    """Traduz ``key`` no idioma atual (cai para inglês e, por fim, para a própria chave)."""
    text = _load(_current).get(key)
    if text is None:
        text = _load(FALLBACK_LANGUAGE).get(key, key)
    if params:
        try:
            return text.format_map(_SafeDict(params))
        except (ValueError, IndexError):
            return text
    return text


def issue_text(issue: Any) -> str:
    return tr(f"issue.{issue.code}", **issue.params)


def error_text(code: str, **params: Any) -> str:
    return tr(f"err.{code}", **params)


def keys(lang: str) -> set[str]:
    return set(_load(lang))
