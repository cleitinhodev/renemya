"""Gera as fontes de fallback embutidas em ``renemya/gui/assets/fonts``.

Builds the small fallback fonts bundled in ``renemya/gui/assets/fonts`` so the
interface renders CJK, Devanagari, Bengali and Arabic text even on systems
without those fonts (e.g. a minimal Ubuntu running the AppImage).

Uso / usage (needs ``fonttools``; source fonts from github.com/google/fonts, ofl/)::

    python packaging/fonts/build_fonts.py /path/to/downloaded/fonts

Expected source files (variable fonts)::

    NotoSansSC[wght].ttf  NotoSansJP[wght].ttf  NotoSansKR[wght].ttf
    NotoSansDevanagari[wdth,wght].ttf  NotoSansBengali[wdth,wght].ttf
    NotoSansArabic[wdth,wght].ttf

CJK fonts are subset to the characters used by the translations (they are
huge otherwise); the other scripts keep their whole Unicode block, so any
file name in those scripts also renders. Run again after editing translations.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parents[2]
I18N = ROOT / "renemya" / "i18n"
OUT = ROOT / "renemya" / "gui" / "assets" / "fonts"

WEIGHTS = {"Regular": 400, "Bold": 700}

# (arquivo de origem, prefixo de saída, idiomas cujo texto entra no subset, blocos Unicode)
FONTS = [
    ("NotoSansSC[wght].ttf", "NotoSansSC", ["zh_CN"], []),
    ("NotoSansJP[wght].ttf", "NotoSansJP", ["ja"], []),
    ("NotoSansKR[wght].ttf", "NotoSansKR", ["ko"], [(0x3131, 0x318E)]),
    (
        "NotoSansDevanagari[wdth,wght].ttf",
        "NotoSansDevanagari",
        [],
        [(0x0900, 0x097F), (0xA8E0, 0xA8FF)],
    ),
    ("NotoSansBengali[wdth,wght].ttf", "NotoSansBengali", [], [(0x0980, 0x09FF)]),
    (
        "NotoSansArabic[wdth,wght].ttf",
        "NotoSansArabic",
        [],
        [(0x0600, 0x06FF), (0x0750, 0x077F), (0xFB50, 0xFDFF), (0xFE70, 0xFEFF)],
    ),
]


def _texts(langs: list[str]) -> str:
    chars = set()
    for lang in langs:
        data = json.loads((I18N / f"{lang}.json").read_text(encoding="utf-8"))
        for value in data.values():
            chars.update(value)
    # nomes nativos de todos os idiomas (menu Idioma)
    sys.path.insert(0, str(ROOT))
    from renemya.i18n import LANGUAGES

    for name in LANGUAGES.values():
        chars.update(name)
    chars.update("0123456789（）()、。，：；！？「」『』…—·“”‘’ ")
    return "".join(sorted(chars))


def build(src_dir: Path) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for src, prefix, langs, ranges in FONTS:
        for style, wght in WEIGHTS.items():
            font = TTFont(src_dir / src)
            axes = {"wght": wght}
            if "wdth" in {a.axisTag for a in font["fvar"].axes}:
                axes["wdth"] = 100
            font = instancer.instantiateVariableFont(font, axes, updateFontNames=True)
            options = subset.Options()
            options.layout_features = ["*"]
            options.name_IDs = ["*"]
            options.name_languages = ["*"]
            options.notdef_outline = True
            options.drop_tables += ["STAT"]
            sub = subset.Subsetter(options)
            unicodes = [cp for lo, hi in ranges for cp in range(lo, hi + 1)]
            text = _texts(langs) if langs else ""
            if langs:
                # só caracteres da escrita (o resto vem da fonte principal)
                text = "".join(c for c in text if ord(c) > 0x2000)
            sub.populate(text=text, unicodes=unicodes + [0x0020, 0x00A0, 0x200C, 0x200D, 0x25CC])
            sub.subset(font)
            dest = OUT / f"{prefix}-{style}.ttf"
            font.save(dest)
            print(f"{dest.relative_to(ROOT)}: {dest.stat().st_size // 1024} KiB")


if __name__ == "__main__":
    build(Path(sys.argv[1] if len(sys.argv) > 1 else "."))
