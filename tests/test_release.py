"""Verificações do material de distribuição: versão, guias, pacotes e entrada da interface."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest

from renemya import __version__

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def _load_build_release():
    spec = importlib.util.spec_from_file_location(
        "renemya_build_release", ROOT / "packaging" / "build_release.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pyproject_version() -> str:
    for line in (ROOT / "pyproject.toml").read_text(encoding="utf-8").splitlines():
        m = re.match(r'^version\s*=\s*"([^"]+)"', line)
        if m:
            return m.group(1)
    raise AssertionError("versão não encontrada no pyproject.toml")


def test_version_is_consistent():
    assert _pyproject_version() == __version__
    assert re.fullmatch(r"\d+\.\d+\.\d+", __version__), "versão de release deve ser X.Y.Z"
    assert _load_build_release().version() == __version__


def test_changelog_and_release_notes_cover_version():
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert f"## [{__version__}]" in changelog
    notes = (ROOT / ".github" / "release-notes" / f"v{__version__}.md").read_text(encoding="utf-8")
    assert f"Renemya-{__version__}-windows-x64.zip" in notes
    assert f"Renemya-{__version__}-linux-x64.tar.gz" in notes
    assert "SmartScreen" in notes and "SHA256SUMS.txt" in notes and "English" in notes


@pytest.mark.parametrize(
    ("readme", "src"), [("README.md", "guia.md"), ("README.en.md", "guide.en.md")]
)
def test_readme_contains_current_guide(readme, src):
    text = (ROOT / readme).read_text(encoding="utf-8")
    guide = (DOCS / src).read_text(encoding="utf-8").strip()
    assert guide in text, f"{readme} desatualizado: rode packaging/build_release.py sync-readme"


LINKS = (
    "https://github.com/cleitinhodev",
    "https://github.com/cleitinhodev/renemya",
    "https://github.com/cleitinhodev/renemya/releases",
    "https://github.com/cleitinhodev/renemya/issues",
    "https://www.bugzinho.com/",
    "https://www.bugzinho.com/donate",
)


def test_guide_has_links_rules_and_sections():
    guia = (DOCS / "guia.md").read_text(encoding="utf-8")
    for link in LINKS:
        assert link in guia
    pt = json.loads((ROOT / "renemya" / "i18n" / "pt_BR.json").read_text(encoding="utf-8"))
    rule_names = [v for k, v in pt.items() if k.startswith("rule.") and k.count(".") == 1]
    assert len(rule_names) == 12
    for name in rule_names:
        assert name in guia, f"regra sem explicação no guia: {name}"
    for status in (
        "status.ok",
        "status.warning",
        "status.skipped",
        "status.error",
        "status.unchanged",
    ):
        assert pt[status] in guia
    for section in (
        "Instalação",
        "Tutorial",
        "Receitas",
        "Linha de comando",
        "Segurança",
        "Perguntas frequentes",
    ):
        assert section in guia


def test_user_readme_for_packages():
    br = _load_build_release()
    text = br.user_readme(__version__)
    assert text.startswith(f"# Renemya {__version__}")
    assert "LICENSE.txt" in text and "GPL-3.0" in text
    assert "English" in text
    assert "<versão>" not in text and "<version>" not in text
    assert f"Renemya-{__version__}-windows-x64.zip" in text
    for link in LINKS:
        assert link in text


def test_linux_packaging_files():
    linux = ROOT / "packaging" / "linux"
    desktop = (linux / "renemya.desktop").read_text(encoding="utf-8")
    assert "Exec=renemya" in desktop and "Icon=renemya" in desktop
    install = (linux / "install.sh").read_text(encoding="utf-8")
    assert install.startswith("#!/bin/sh")
    assert ".local/bin" in install or "XDG_BIN_HOME" in install
    assert "--uninstall" in install
    assert (linux / "AppRun").is_file()
    assert (
        (ROOT / "LICENSE")
        .read_text(encoding="utf-8")
        .lstrip()
        .startswith("GNU GENERAL PUBLIC LICENSE")
    )


def test_gui_arguments(tmp_path):
    from renemya.gui import app

    assert app._parse_args(["renemya", "--version"]) == ("version", None)
    assert app._parse_args(["renemya", "--smoke-test"]) == ("smoke", None)
    assert app._parse_args(["renemya", str(tmp_path)]) == ("run", str(tmp_path))
    assert app._parse_args(["renemya", str(tmp_path / "nao-existe"), "-platform", "offscreen"]) == (
        "run",
        None,
    )


def test_gui_version_flag(capsys):
    from renemya.gui import app

    assert app.main(["renemya", "--version"]) == 0
    assert capsys.readouterr().out.strip() == f"Renemya {__version__}"
