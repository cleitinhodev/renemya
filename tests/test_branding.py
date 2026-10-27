"""Nome Renemya, ícones, janela "Sobre" e opção de animações."""

import os
import sys
from pathlib import Path

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
pytest.importorskip("PySide6.QtWidgets", exc_type=ImportError)

from PySide6.QtCore import QSettings  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

import renemya  # noqa: E402
from renemya.core import Journal  # noqa: E402
from renemya.core.journal import default_data_dir  # noqa: E402
from renemya.gui import neon, resources, theme  # noqa: E402
from renemya.gui.app import create_app  # noqa: E402
from renemya.gui.dialogs import ABOUT_LINKS, DONATE_LINK, AboutDialog  # noqa: E402
from renemya.gui.main_window import MainWindow  # noqa: E402
from renemya.i18n import LANGUAGES, set_language, tr  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def app():
    return create_app([])


def make_window(tmp_path, name="settings.ini"):
    settings = QSettings(str(tmp_path / name), QSettings.Format.IniFormat)
    return MainWindow(settings=settings, journal=Journal(tmp_path / "j"), check_incomplete=False)


# ------------------------------------------------------------------ nome
def test_package_and_entry_points():
    assert renemya.APP_NAME == "Renemya"
    # sem tomllib (Python 3.10 também roda os testes): confere as linhas do pyproject
    lines = (ROOT / "pyproject.toml").read_text(encoding="utf-8").splitlines()
    for expected in (
        'name = "renemya"',
        'renemya-cli = "renemya.cli:main"',
        'renemya = "renemya.gui.app:main"',
        'Homepage = "https://github.com/cleitinhodev/renemya"',
    ):
        assert expected in lines


def test_no_old_name_left_in_sources():
    old = ("rename" + "this", "rename " + "this")
    for path in list((ROOT / "renemya").rglob("*")) + [ROOT / "pyproject.toml"]:
        if path.suffix in {".py", ".json", ".qss", ".toml"}:
            text = path.read_text(encoding="utf-8").lower()
            assert not any(o in text for o in old), path


@pytest.mark.parametrize("lang", sorted(LANGUAGES))
def test_translated_title(lang):
    set_language(lang)
    try:
        assert tr("app.title") == "Renemya"
        assert "Renemya" in tr("about.title")
    finally:
        set_language("pt_BR")


def test_data_dir_env(monkeypatch, tmp_path):
    monkeypatch.setenv("RENEMYA_DATA_DIR", str(tmp_path / "x"))
    assert default_data_dir() == tmp_path / "x"
    monkeypatch.delenv("RENEMYA_DATA_DIR")
    assert "renemya" in str(default_data_dir()).lower()


def test_theme_env(monkeypatch):
    monkeypatch.setenv("RENEMYA_THEME", "dark")
    assert theme.system_prefers_dark() is True


# ------------------------------------------------------------------ ícones
def test_icons_are_multi_size():
    pil = pytest.importorskip("PIL.Image")
    for name in ("renemya_icon", "renemya_favicon"):
        with pil.open(resources.asset_path(f"{name}.ico")) as im:
            assert {(16, 16), (32, 32), (48, 48), (256, 256)} <= set(im.info["sizes"])
        assert resources.asset_path(f"{name}.png") is not None


def test_window_and_app_icons(app, tmp_path):
    assert not app.windowIcon().isNull()
    w = make_window(tmp_path)
    try:
        assert not w.windowIcon().isNull()
        # barra de título (favicon) é diferente do ícone geral do app
        assert w.windowIcon().cacheKey() != app.windowIcon().cacheKey()
    finally:
        w.close()


@pytest.mark.skipif(sys.platform == "win32", reason="só testa o caminho fora do Windows")
def test_windows_integration_is_noop_elsewhere(app, tmp_path):
    assert resources.set_windows_app_id() is False
    w = make_window(tmp_path)
    try:
        assert resources.set_windows_taskbar_icon(w) is False
    finally:
        w.close()


# ------------------------------------------------------------------ "Sobre"
def test_about_links(app, monkeypatch):
    set_language("pt_BR")
    opened = []
    monkeypatch.setattr(
        "renemya.gui.dialogs.QDesktopServices.openUrl", lambda url: opened.append(url.toString())
    )
    dlg = AboutDialog(animations=False)
    expected = {
        "https://github.com/cleitinhodev",
        "https://github.com/cleitinhodev/renemya",
        "https://www.bugzinho.com/",
        "https://www.bugzinho.com/donate",
    }
    assert set(dlg.link_buttons) == expected
    assert {url for *_, url in ABOUT_LINKS} | {DONATE_LINK[2]} == expected
    assert dlg.donate_button.objectName() == "DonateButton"  # botão destacado
    assert dlg.donate_button.property("url") == "https://www.bugzinho.com/donate"
    for button in dlg.link_buttons.values():
        assert not button.icon().isNull()
        button.click()
    assert opened == list(dlg.link_buttons)
    assert not dlg.logo.pixmap().isNull()
    dlg.deleteLater()


@pytest.mark.parametrize(
    ("lang", "labels"),
    [
        ("pt_BR", ["Perfil no GitHub", "Repositório", "Site", "Apoie o projeto — Doar"]),
        ("en", ["GitHub profile", "Repository", "Website", "Support the project — Donate"]),
    ],
)
def test_about_labels_translated(app, lang, labels):
    set_language(lang)
    try:
        dlg = AboutDialog(animations=False)
        assert [b.text() for b in dlg.link_buttons.values()] == labels
        dlg.deleteLater()
    finally:
        set_language("pt_BR")


def test_show_about_from_window(app, tmp_path, monkeypatch):
    monkeypatch.setattr(AboutDialog, "exec", lambda self: 0)
    w = make_window(tmp_path)
    try:
        w.show_about()
        assert isinstance(w.about_dialog, AboutDialog)
        assert w.about_dialog.neon_clock.enabled == w.animations_enabled()
    finally:
        w.close()


# ------------------------------------------------------------------ animações
def test_animation_toggle_persists(app, tmp_path):
    set_language("pt_BR")
    w = make_window(tmp_path)
    try:
        assert w.animations_enabled() is True  # ligado por padrão
        assert w.act_animations.isCheckable() and w.act_animations.isChecked()
        assert w.act_animations.text() == "Animações"
        w.act_animations.setChecked(False)
        assert w.animations_enabled() is False
        assert not w.neon_clock.is_running()
        assert all(not o.isVisible() for o in w.neon_clock.overlays())
        w.settings.sync()
    finally:
        w.close()
    w2 = make_window(tmp_path)
    try:
        assert w2.animations_enabled() is False
        assert not w2.act_animations.isChecked()
        w2.set_animations(True)
        assert w2.act_animations.isChecked()
        assert neon.settings_bool(w2.settings.value("animations")) is True
    finally:
        w2.close()


def test_overlays_are_installed_and_click_through(app, tmp_path):
    from PySide6.QtCore import Qt

    w = make_window(tmp_path)
    try:
        overlays = w.neon_clock.overlays()
        targets = {o.target for o in overlays}
        assert {w.top_bar, w.apply_button, w.progress, w.preview_box} <= targets
        for o in overlays:
            assert o.testAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            assert o.geometry() == o.target.rect()
        # trocar o tema/idioma reconstrói a interface sem acumular camadas
        count = len(overlays)
        w.rebuild_for_theme()
        assert len(w.neon_clock.overlays()) == count
    finally:
        w.close()


def test_clock_pauses_and_resumes(app, tmp_path):
    w = make_window(tmp_path)
    try:
        clock = w.neon_clock
        clock.set_suspended(False)
        assert clock.is_running()
        clock.set_suspended(True)  # janela minimizada / sem foco
        assert not clock.is_running()
        clock.set_suspended(False)
        clock.set_enabled(False)
        assert not clock.is_running()
        clock.set_enabled(True)
        assert clock.is_running()
        w.hide()
        clock.refresh_window_state()
        assert clock.suspended and not clock.is_running()
    finally:
        w.close()


def test_frames_paint_only_live_streaks(app, tmp_path):
    w = make_window(tmp_path)
    try:
        w.show()
        QApplication.processEvents()
        assert not w.neon_progress.is_live()  # barra escondida fora de uma operação
        w.progress.setVisible(True)
        w.progress.setValue(40)
        assert w.neon_progress.is_live()
        assert w.neon_header.is_live()
        before = w.neon_clock.t
        for _ in range(5):
            w.neon_clock.advance(0.05)
        QApplication.processEvents()
        assert w.neon_clock.t == pytest.approx(before + 0.25)
        # só uma área pequena é redesenhada por quadro
        rects = w.neon_header.dirty_rects()
        assert len(rects) == 2  # dois riscos no cabeçalho
        total = w.top_bar.width() * w.top_bar.height()
        assert all(0 < r.width() * r.height() < total / 3 for r in rects)
        image = w.grab()
        assert not image.isNull()
    finally:
        w.close()
