## 🇺🇸 English (short guide)

**Renemya** is a safe batch file renamer: combine rules, check the live preview, rename, and undo
whenever you want. Links: [Releases](https://github.com/cleitinhodev/renemya/releases) ·
[source code](https://github.com/cleitinhodev/renemya) ·
[issues](https://github.com/cleitinhodev/renemya/issues) ·
[author](https://github.com/cleitinhodev) · [website](https://www.bugzinho.com/) ·
[donate](https://www.bugzinho.com/donate).

**Install.**
- **Windows:** unzip `Renemya-<version>-windows-x64.zip` and run `Renemya.exe` (portable). If
  SmartScreen appears, click *More info → Run anyway*.
- **Linux** (glibc 2.35+): `tar -xzf Renemya-<version>-linux-x64.tar.gz`, then
  `cd Renemya-<version>-linux-x64 && ./install.sh`. The installer puts the app in `~/.local/bin`
  and adds a menu entry. Or just run `./renemya`. Qt and its xcb libraries are bundled; you only
  need OpenGL/EGL (Mesa) and fontconfig. If you see "Qt platform plugin xcb", install
  `libxcb-cursor0 libxkbcommon-x11-0`.

**How to use.**
1. Pick or drag a folder into the window.
2. Add rules. They run top to bottom; drag to reorder, or untick to disable. There are 12 rules:
   prefix/suffix, replace (regex), remove characters, insert, counter, letters,
   date (modified/created/EXIF), case, cleanup, extension, template with tokens, music tags.
3. Set the sorting and filters, and choose the conflict policy: add a (2) suffix, or skip.
4. Read the preview:
   - green: will be renamed
   - orange: warning
   - gray: skipped
   - red: error (blocks renaming)
   - dot: unchanged
5. Click **Rename**. Undo with **Ctrl+Z**. Your history is under *File → Operation history*.
6. Save and load rule sets with *File → Save/Load preset*. You can also switch the language
   (*Language*), turn off the animations (*Edit → Animations*), and the theme follows the system.
7. Languages: Português (Brasil), English, Español, 中文（简体）, हिन्दी, العربية, Français, Русский,
   বাংলা, 日本語, Deutsch, Bahasa Indonesia, 한국어, Türkçe and Italiano. On first run Renemya follows
   the system language (English if it isn't listed); Arabic uses a right-to-left layout. Force one
   with `RENEMYA_LANG` (e.g. `RENEMYA_LANG=ja`).

**CLI:**
`renemya-cli rename ./photos --sort modified --template "Trip_{exif:%Y-%m-%d}_{n:03}" --dry-run`.
Other commands: `renemya-cli rules`, `undo`, `history`, `recover`, and `--lang <code>` (e.g. `--lang ja`).

**Why did the extension change?** Only the Extension rule, Replace (scope *extension*/*full
name*) or Case (*also the extension*) touch it. Renaming an extension never converts the file,
so the preview shows a warning.
