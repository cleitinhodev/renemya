#!/bin/sh
# Instala o Renemya só para o usuário atual (sem sudo).
#   ./install.sh              instala/atualiza
#   ./install.sh --uninstall  remove
# Install Renemya for the current user only (no sudo). Use --uninstall to remove it.
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BIN_DIR="${XDG_BIN_HOME:-$HOME/.local/bin}"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
APP_DIR="$DATA_HOME/applications"
ICON_DIR="$DATA_HOME/icons/hicolor/256x256/apps"

# Mensagens em português se o sistema estiver em português; senão, em inglês.
# Messages in Portuguese on Portuguese systems, English otherwise.
case "${LC_ALL:-${LC_MESSAGES:-${LANG:-}}}" in
    pt*) PT=1 ;;
    *) PT=0 ;;
esac
say() { # say "english" "português"
    if [ "$PT" = 1 ]; then echo "$2"; else echo "$1"; fi
}

refresh() {
    command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APP_DIR" >/dev/null 2>&1 || true
    command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -q -t "$DATA_HOME/icons/hicolor" >/dev/null 2>&1 || true
}

if [ "${1:-}" = "--uninstall" ]; then
    rm -f "$BIN_DIR/renemya" "$BIN_DIR/renemya-cli" "$APP_DIR/renemya.desktop" "$ICON_DIR/renemya.png"
    refresh
    say "Renemya removed. (History and presets are kept in $DATA_HOME/Renemya)" \
        "Renemya removido. (Histórico e predefinições continuam em $DATA_HOME/Renemya)"
    exit 0
fi

for f in renemya renemya-cli renemya.png renemya.desktop; do
    if [ ! -f "$HERE/$f" ]; then
        say "File not found: $HERE/$f" "Arquivo não encontrado: $HERE/$f" >&2
        exit 1
    fi
done

mkdir -p "$BIN_DIR" "$APP_DIR" "$ICON_DIR"
install -m 755 "$HERE/renemya" "$BIN_DIR/renemya"
install -m 755 "$HERE/renemya-cli" "$BIN_DIR/renemya-cli"
install -m 644 "$HERE/renemya.png" "$ICON_DIR/renemya.png"
# O atalho aponta para o caminho completo: funciona mesmo se ~/.local/bin não estiver no PATH
sed "s|^Exec=renemya|Exec=\"$BIN_DIR/renemya\"|" "$HERE/renemya.desktop" > "$APP_DIR/renemya.desktop"
chmod 644 "$APP_DIR/renemya.desktop"
refresh

say "Renemya installed:" "Renemya instalado:"
say "  program:   $BIN_DIR/renemya  (and renemya-cli)" "  programa:  $BIN_DIR/renemya  (e renemya-cli)"
say "  shortcut:  $APP_DIR/renemya.desktop" "  atalho:    $APP_DIR/renemya.desktop"
case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *) say "Tip: add $BIN_DIR to your PATH to run 'renemya' and 'renemya-cli' from a terminal." \
        "Dica: adicione $BIN_DIR ao PATH para usar 'renemya' e 'renemya-cli' no terminal." ;;
esac
say "Open it from the applications menu or run: renemya" "Abra pelo menu de aplicativos ou rode: renemya"
