<p align="center">
  <img src="renemya/gui/assets/renemya_icon.png" alt="Renemya" width="160">
</p>

<h1 align="center">Renemya</h1>

<p align="center">
  Safe, reversible — and good-looking — batch file renamer.<br>
  🇧🇷 <a href="README.md">Versão em português</a>
</p>

**Renemya** (the new name of *Rename This!*) renames thousands of files at once, and does it
**quickly, predictably and safely**. It is a from-scratch rewrite in **Python + PySide6 (Qt)**.
Before it touches anything it shows a full preview, refuses dangerous names, never overwrites a
file, and lets you **undo** the last operation.

> ⚠️ **Testing version.** Back up your important files until a stable release is out.

## Download

- Windows executables (`Renemya.exe` and `renemya-cli.exe`) are built on every push to `main`:
  open the [Actions](https://github.com/cleitinhodev/renemya/actions) tab, pick the latest
  **Build (Windows .exe)** run and download the **Renemya-windows** artifact.
- Stable versions will be published under [Releases](https://github.com/cleitinhodev/renemya/releases).

## Highlights

### Safety first
- **Plan, then apply.** Every new name is computed and validated before any file is touched.
  If there is an error, nothing is renamed.
- **Never overwrites.** Conflicts are resolved in the preview, either by adding a ` (2)`, ` (3)`…
  suffix or by skipping the file. When renaming, the program uses the OS calls that refuse an
  existing target (Linux/macOS) and runs a final check before every step.
- **Swaps and chains work.** Cases like `a → b` plus `b → a`, or `1.txt → 2.txt → 3.txt`, go
  through temporary names in two phases.
- **Automatic rollback.** If something fails midway (file open in another program, permission
  denied…), everything already done is reverted.
- **Undo and history.** Every operation is recorded in a JSON journal. You can undo the last one
  from the GUI, with `Ctrl+Z`, or from the CLI.
- **Crash recovery.** If the computer shuts down during an operation, the next launch offers to
  restore the original names.
- **Windows-safe names on every OS.** Blocks:
  - the characters `\ / : * ? " < > |` and control characters
  - reserved names (`CON`, `NUL`, `COM1`…)
  - a trailing dot or space, names over 255 bytes, and `..`
  - names that differ only in letter case, on filesystems that ignore case
- **System files protected.** `desktop.ini`, `Thumbs.db`, `.DS_Store` and hidden files are left
  alone unless you choose to include them.

### Composable rules
Rules are applied top to bottom. Each one can be enabled, disabled, duplicated or reordered:

- **Prefix / suffix**
- **Replace**: case sensitivity, **regex**, and whether it applies to the name, the extension or both
- **Remove**: specific characters, a range, the first or last N characters, digits, or text in `()` `[]` `{}`
- **Insert**: text at a position, counting from the start or the end
- **Counter**: start, step, zero padding, position and separator; can restart per folder
- **Letters**: A, B, … Z, AA…
- **Date**: modified, created or **photo taken (EXIF)**, with a custom format
- **Case**: lower, UPPER, Title, Sentence, iNVERT
- **Cleanup**: spaces, accents, invalid characters, repeated separators
- **Extension**: lower, upper, change or remove
- **Template**: build the name from tokens
- **Music tags**: artist, title, album, track

Template tokens:
- `{name}`: original name; `{current}`: the name after the previous rules
- `{ext}`, `{parent}`, `{size}`
- `{n:03}`: counter; `{letter[:lower]}`: letters
- `{date|modified|created|exif|now[:%Y-%m-%d]}`: dates
- `{artist}` `{title}` `{album}` `{track:02}` `{year}` `{genre}`: music tags

### GUI
- Drag & drop folders.
- Live preview with color-coded statuses.
- Natural sorting by name, date, size or type.
- Extension filters, subfolders, folders, hidden and system files.
- Confirmation before applying, progress bar, final summary and Undo.
- JSON presets.
- Portuguese/English switch at runtime.
- Light/dark theme that follows the system, with **neon orange** accents (the fox's color):
  glowing streaks run along the header, the **Rename** button, the progress bar and the active
  panel. Turn them off in *Edit → Animations* (saved). They pause when the window is minimized
  or in the background.
- The last session is restored on launch.

## Install from source (Python 3.10+)

```bash
git clone https://github.com/cleitinhodev/renemya.git
cd renemya
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[media]"   # media = EXIF dates (Pillow) + music tags (mutagen); optional
```

## Usage

```bash
renemya                     # GUI (or: python -m renemya)

renemya-cli rename ./photos --sort modified --template "Photo_{n:03}" --dry-run
renemya-cli rename ./photos --sort modified --template "Photo_{n:03}" -y
renemya-cli rename ./docs --add remove mode=brackets --add case mode=lower
renemya-cli rules | undo | history | recover
```

Exit codes: `0` success, `1` error or aborted, `2` usage error.

The journal and presets are stored in the platform's user data folder (for example
`%LOCALAPPDATA%\Renemya` on Windows). Set `RENEMYA_DATA_DIR` to use a different folder and
`RENEMYA_THEME=light|dark` to force a theme.

## Development

```bash
pip install -e ".[dev]"
ruff check . && ruff format --check . && pytest
```

CI runs lint and tests on Ubuntu and Windows. Every push to `main` builds `Renemya.exe` and
`renemya-cli.exe` with PyInstaller as workflow artifacts (no Release is created). If you push a
`v*` tag, they are also attached to that tag's Release.

## Credits

By [CleitinhoDEV](https://github.com/cleitinhodev). Support: [❤️ Donate](https://www.bugzinho.com/donate) · [Patreon](https://www.patreon.com/CleitinhoDEV) · [Bugzinho.com](https://www.bugzinho.com)

Licensed under **GPL-3.0**. Built with:
- PySide6 (LGPL-3.0)
- platformdirs (MIT)
- Pillow (MIT-CMU, optional)
- mutagen (GPL-2.0-or-later, optional)
