import json
import re
from pathlib import Path

import pytest

from renemya.core.rules import RULE_TYPES
from renemya.i18n import (
    LANGUAGES,
    RTL_LANGUAGES,
    detect_language,
    is_rtl,
    keys,
    language_list,
    normalize_language,
    set_language,
    tr,
)

SRC = Path(__file__).resolve().parents[1] / "renemya"


def test_all_languages_have_same_keys():
    base = keys("pt_BR")
    assert base
    for lang in LANGUAGES:
        assert keys(lang) == base, set(base) ^ keys(lang)


def test_every_issue_code_is_translated():
    code_re = re.compile(
        r'(?:add|warn)\(\s*"([a-z_]+)"'
        r'|RuleError\(\s*"([a-z_]+)"'
        r'|\("([a-z_]+)", Level\.'
    )
    found = set()
    for py in (SRC / "core").glob("*.py"):
        for m in code_re.finditer(py.read_text(encoding="utf-8")):
            found.add(next(g for g in m.groups() if g))
    assert found
    missing = {c for c in found if f"issue.{c}" not in keys("pt_BR")}
    assert not missing


def test_rules_and_fields_translated():
    k = keys("pt_BR")
    for kind, cls in RULE_TYPES.items():
        assert f"rule.{kind}" in k and f"desc.{kind}" in k
        for spec in cls.FIELDS:
            assert f"field.{spec.name}" in k
            for choice in spec.choices:
                assert f"choice.{choice}" in k


def test_tr_fallbacks_and_params():
    set_language("en")
    assert tr("button.apply") == "Rename"
    assert tr("nao.existe") == "nao.existe"
    assert tr("issue.reserved_name", name="CON") == "“CON” is a reserved name on Windows."
    assert "{name}" in tr("issue.reserved_name")  # sem parâmetros, não formata
    set_language("pt_BR")
    assert tr("button.apply") == "Renomear"


def test_normalize_language():
    assert normalize_language("pt-PT") == "pt_BR"
    assert normalize_language("en_US") == "en"
    assert normalize_language("de_DE") == "de"
    assert normalize_language(None) == "pt_BR"
    assert normalize_language("xx_YY") == "en"  # desconhecido: inglês
    assert normalize_language("ja_JP.UTF-8") == "ja"
    assert normalize_language("zh-Hans-CN") == "zh_CN"
    assert normalize_language("zh_CN.utf8@pinyin") == "zh_CN"
    assert normalize_language("ar_EG") == "ar"
    assert normalize_language("in_ID") == "id"  # código antigo do Java/Android
    assert normalize_language("Japanese_Japan") == "ja"  # locale.getlocale() no Windows
    assert normalize_language("Portuguese_Brazil") == "pt_BR"
    assert normalize_language("Chinese (Simplified)_China") == "zh_CN"


I18N = SRC / "i18n"
PLACEHOLDER = re.compile(r"\{[^{}]*\}")


def _load(lang):
    return json.loads((I18N / f"{lang}.json").read_text(encoding="utf-8"))


def test_fifteen_languages_with_json_files():
    assert len(LANGUAGES) == 15
    files = {p.stem for p in I18N.glob("*.json")}
    assert files == set(LANGUAGES)
    for code, name in LANGUAGES.items():
        assert _load(code)["_language"] == name  # nome nativo no menu
    assert set(language_list().split(", ")) == set(LANGUAGES)


@pytest.mark.parametrize("lang", sorted(LANGUAGES))
def test_locale_matches_english_keys_and_placeholders(lang):
    en, other = _load("en"), _load(lang)
    assert set(other) == set(en), set(other) ^ set(en)
    for key, text in en.items():
        assert sorted(PLACEHOLDER.findall(other[key])) == sorted(PLACEHOLDER.findall(text)), key
        assert other[key].strip(), key


@pytest.mark.parametrize("lang", sorted(LANGUAGES))
def test_locale_formats_without_errors(lang):
    set_language(lang)
    try:
        assert tr("rules.empty_hint") != "rules.empty_hint"
        assert "7" in tr("confirm.text", count=7)
        assert "/x" in tr("err.folder_not_found", path="/x")
        assert "{token}" in tr("issue.template_unknown_token", token="foo") or "foo" in tr(
            "issue.template_unknown_token", token="foo"
        )
    finally:
        set_language("pt_BR")


def test_rtl_only_arabic():
    assert {"ar"} == RTL_LANGUAGES
    assert is_rtl("ar") and not is_rtl("en") and not is_rtl("he_IL")


def test_detect_language(monkeypatch):
    for var in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("RENEMYA_LANG", "ko")
    assert detect_language() == "ko"
    monkeypatch.delenv("RENEMYA_LANG")
    monkeypatch.setenv("LANG", "tr_TR.UTF-8")
    assert detect_language() == "tr"
    monkeypatch.setenv("LC_ALL", "C")  # ignorado
    assert detect_language() == "tr"
    monkeypatch.setenv("LANG", "sv_SE.UTF-8")  # sem tradução: inglês
    assert detect_language() == "en"
