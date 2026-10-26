"""Monta a documentação e os pacotes de distribuição do Renemya.

Uso (a partir da raiz do repositório):

    python packaging/build_release.py sync-readme
        Copia docs/guia.md e docs/guide.en.md para dentro do README.md / README.en.md
        (entre os marcadores GUIA:INICIO/GUIA:FIM).

    python packaging/build_release.py docs --out DIR
        Gera o README.md e o LEIA-ME.html que vão dentro dos pacotes.

    python packaging/build_release.py package --platform windows|linux [--dist dist] [--out release]
        Monta a pasta Renemya-<versão>-<plataforma>-x64 com os executáveis, LICENSE.txt e os
        guias, e compacta em .zip (Windows) ou .tar.gz (Linux).

    python packaging/build_release.py appdir [--dist dist] [--out release/Renemya.AppDir]
        Monta o AppDir usado pelo appimagetool para gerar o AppImage.

    python packaging/build_release.py version
        Mostra a versão (lida de renemya/__init__.py).
"""

from __future__ import annotations

import argparse
import base64
import html
import re
import shutil
import stat
import sys
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
ASSETS = ROOT / "renemya" / "gui" / "assets"
LINUX = Path(__file__).resolve().parent / "linux"

START = (
    "<!-- GUIA:INICIO (gerado de docs/{src}; "
    "edite lá e rode packaging/build_release.py sync-readme) -->"
)
END = "<!-- GUIA:FIM -->"


def version() -> str:
    text = (ROOT / "renemya" / "__init__.py").read_text(encoding="utf-8")
    m = re.search(r'^__version__\s*=\s*"([^"]+)"', text, re.M)
    if not m:
        raise SystemExit("__version__ não encontrado")
    return m.group(1)


# --------------------------------------------------------------------------- README do repositório
def _replace_block(text: str, src: str, body: str) -> str:
    start = START.format(src=src)
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(END), re.S)
    if not pattern.search(text):
        raise SystemExit(f"Marcadores do guia não encontrados para {src}")
    return pattern.sub(lambda _m: f"{start}\n\n{body.strip()}\n\n{END}", text)


def sync_readme() -> None:
    pairs = (("README.md", "guia.md"), ("README.en.md", "guide.en.md"))
    for readme, src in pairs:
        path = ROOT / readme
        body = (DOCS / src).read_text(encoding="utf-8")
        new = _replace_block(path.read_text(encoding="utf-8"), src, body)
        path.write_text(new, encoding="utf-8", newline="\n")
        print(f"{readme} atualizado a partir de docs/{src}")


# --------------------------------------------------------------------------- guias do pacote
def user_readme(ver: str) -> str:
    guia = (DOCS / "guia.md").read_text(encoding="utf-8").strip()
    guide_en = (DOCS / "guide.en.md").read_text(encoding="utf-8").strip()
    guia = guia.replace("<versão>", ver)
    guide_en = guide_en.replace("<version>", ver)
    return f"""# Renemya {ver}

**Renomeador de arquivos em lote — seguro, reversível e bonito.**
Monte regras, confira a prévia ao vivo, renomeie e desfaça quando quiser.

Feito por **CleitinhoDEV** · Licença **GPL-3.0** (texto completo em `LICENSE.txt`) ·
<https://github.com/cleitinhodev/renemya>

> 🇺🇸 English: see the *English (short guide)* section at the end of this file.

{guia}

---

{guide_en}

---

## 📜 Licença e créditos

O Renemya é software livre, distribuído sob a **GNU General Public License v3.0** (arquivo
`LICENSE.txt`). Você pode usar, estudar, compartilhar e modificar; o código-fonte está em
<https://github.com/cleitinhodev/renemya>.

Usa: PySide6 / Qt for Python (LGPL-3.0), platformdirs (MIT), Pillow (MIT-CMU),
mutagen (GPL-2.0-or-later) e Python (PSF). Empacotado com PyInstaller.

Gostou? Apoie em <https://www.bugzinho.com/donate> ❤️ · By CleitinhoDEV
"""


_CSS = """
:root { --accent:#FD9128; --bg:#f6f7fb; --card:#ffffff; --fg:#1d2433; --muted:#5b6475;
        --border:#dde2ec; --code:#eef1f7; --link:#2563eb; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#141824; --card:#1c2232; --fg:#e6e9f0; --muted:#a3abbd; --border:#2c3448;
          --code:#252c3f; --link:#7aa7ff; }
}
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--fg);
       font:16px/1.6 "Segoe UI", system-ui, -apple-system, "Noto Sans", Ubuntu, sans-serif; }
main { max-width: 980px; margin: 0 auto; padding: 24px 28px 64px; background: var(--card);
       border-left: 1px solid var(--border); border-right: 1px solid var(--border);
       min-height: 100vh; }
header.hero { text-align:center; padding: 12px 0 8px; }
header.hero img.logo { width:112px; height:112px; }
header.hero h1 { margin: 4px 0 0; font-size: 2.2em; border:0; }
header.hero p { margin: 4px 0; color: var(--muted); }
img.shot { display:block; max-width:100%; margin: 18px auto; border-radius:10px;
           border:1px solid var(--border); box-shadow: 0 6px 24px rgba(0,0,0,.18); }
h1, h2 { border-bottom: 2px solid var(--accent); padding-bottom: .2em; }
h2 { margin-top: 2em; } h3 { margin-top: 1.6em; }
a { color: var(--link); }
code { background: var(--code); padding: .1em .35em; border-radius: 5px; font-size: .92em;
       font-family: "Cascadia Mono", Consolas, "DejaVu Sans Mono", monospace; }
pre { background: var(--code); padding: 12px 14px; border-radius: 8px; overflow:auto;
      border-left: 4px solid var(--accent); }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: .95em; }
th, td { border: 1px solid var(--border); padding: 6px 9px; vertical-align: top; text-align:left; }
th { background: var(--code); }
blockquote { margin: 12px 0; padding: 4px 14px; border-left: 4px solid var(--accent);
             color: var(--muted); }
hr { border: 0; border-top: 1px solid var(--border); margin: 32px 0; }
"""


def _data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def user_html(ver: str) -> str:
    import markdown  # pip install markdown (só para gerar o pacote)

    body_md = user_readme(ver).split("\n", 1)[1]  # o título vai no cabeçalho do HTML
    body = markdown.markdown(body_md, extensions=["tables", "fenced_code", "sane_lists"])
    body = re.sub(
        r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', body
    )
    logo = _data_uri(ASSETS / "renemya_icon.png", "image/png")
    shot_path = DOCS / "img" / "claro.png"
    shot = (
        f'<img class="shot" alt="Janela do Renemya" src="{_data_uri(shot_path, "image/png")}">'
        if shot_path.exists()
        else ""
    )
    title = html.escape(f"Renemya {ver} — Leia-me")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="{logo}">
<style>{_CSS}</style>
</head>
<body>
<main>
<header class="hero">
  <img class="logo" src="{logo}" alt="">
  <h1>Renemya {html.escape(ver)}</h1>
  <p>Leia-me · Guia do usuário · <em>English section at the end</em></p>
</header>
{shot}
{body}
</main>
</body>
</html>
"""


def write_docs(out: Path, ver: str) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    files = {
        "README.md": user_readme(ver),
        "LEIA-ME.html": user_html(ver),
    }
    written = []
    for name, content in files.items():
        p = out / name
        p.write_text(content, encoding="utf-8", newline="\n")
        written.append(p)
    lic = out / "LICENSE.txt"
    shutil.copyfile(ROOT / "LICENSE", lic)
    written.append(lic)
    return written


# --------------------------------------------------------------------------- pacotes
def _make_exec(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def package(platform: str, dist: Path, out: Path) -> Path:
    ver = version()
    name = f"Renemya-{ver}-{platform}-x64"
    folder = out / name
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)

    if platform == "windows":
        binaries = ["Renemya.exe", "renemya-cli.exe"]
    else:
        binaries = ["renemya", "renemya-cli"]
    for b in binaries:
        src = dist / b
        if not src.is_file():
            raise SystemExit(f"Executável não encontrado: {src}")
        shutil.copy2(src, folder / b)
        if platform == "linux":
            _make_exec(folder / b)

    write_docs(folder, ver)

    if platform == "linux":
        shutil.copyfile(ASSETS / "renemya_icon.png", folder / "renemya.png")
        shutil.copyfile(LINUX / "renemya.desktop", folder / "renemya.desktop")
        shutil.copyfile(LINUX / "install.sh", folder / "install.sh")
        _make_exec(folder / "install.sh")
        archive = out / f"{name}.tar.gz"

        def _norm(ti: tarfile.TarInfo) -> tarfile.TarInfo:
            ti.uid = ti.gid = 0
            ti.uname = ti.gname = ""
            if ti.isdir() or ti.mode & stat.S_IXUSR:
                ti.mode = 0o755
            else:
                ti.mode = 0o644
            return ti

        with tarfile.open(archive, "w:gz", compresslevel=9) as tar:
            tar.add(folder, arcname=name, filter=_norm)
    else:
        archive = out / f"{name}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for p in sorted(folder.rglob("*")):
                zf.write(p, f"{name}/{p.relative_to(folder).as_posix()}")

    print(f"Pacote: {archive} ({archive.stat().st_size:,} bytes)")
    for p in sorted(folder.iterdir()):
        print(f"  {p.name}  ({p.stat().st_size:,} bytes)")
    return archive


def appdir(dist: Path, out: Path) -> Path:
    ver = version()
    if out.exists():
        shutil.rmtree(out)
    bin_dir = out / "usr" / "bin"
    bin_dir.mkdir(parents=True)
    for b in ("renemya", "renemya-cli"):
        shutil.copy2(dist / b, bin_dir / b)
        _make_exec(bin_dir / b)
    shutil.copyfile(LINUX / "AppRun", out / "AppRun")
    _make_exec(out / "AppRun")
    shutil.copyfile(LINUX / "renemya.desktop", out / "renemya.desktop")
    shutil.copyfile(ASSETS / "renemya_icon.png", out / "renemya.png")
    shutil.copyfile(ASSETS / "renemya_icon.png", out / ".DirIcon")
    apps = out / "usr" / "share" / "applications"
    icons = out / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps"
    apps.mkdir(parents=True)
    icons.mkdir(parents=True)
    shutil.copyfile(LINUX / "renemya.desktop", apps / "renemya.desktop")
    shutil.copyfile(ASSETS / "renemya_icon.png", icons / "renemya.png")
    write_docs(out / "usr" / "share" / "doc" / "renemya", ver)
    print(f"AppDir: {out}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("version")
    sub.add_parser("sync-readme")
    d = sub.add_parser("docs")
    d.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("package")
    p.add_argument("--platform", choices=["windows", "linux"], required=True)
    p.add_argument("--dist", type=Path, default=ROOT / "dist")
    p.add_argument("--out", type=Path, default=ROOT / "release")
    a = sub.add_parser("appdir")
    a.add_argument("--dist", type=Path, default=ROOT / "dist")
    a.add_argument("--out", type=Path, default=ROOT / "release" / "Renemya.AppDir")
    args = ap.parse_args(argv)

    if args.cmd == "version":
        print(version())
    elif args.cmd == "sync-readme":
        sync_readme()
    elif args.cmd == "docs":
        for f in write_docs(args.out, version()):
            print(f)
    elif args.cmd == "package":
        package(args.platform, args.dist, args.out)
    elif args.cmd == "appdir":
        appdir(args.dist, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
