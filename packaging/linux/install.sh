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

refresh() {
    command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APP_DIR" >/dev/null 2>&1 || true
    command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -q -t "$DATA_HOME/icons/hicolor" >/dev/null 2>&1 || true
}

if [ "${1:-}" = "--uninstall" ]; then
    rm -f "$BIN_DIR/renemya" "$BIN_DIR/renemya-cli" "$APP_DIR/renemya.desktop" "$ICON_DIR/renemya.png"
    refresh
    echo "Renemya removido. (Histórico e predefinições continuam em $DATA_HOME/Renemya)"
    exit 0
fi

for f in renemya renemya-cli renemya.png renemya.desktop; do
    if [ ! -f "$HERE/$f" ]; then
        echo "Arquivo não encontrado: $HERE/$f" >&2
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

echo "Renemya instalado:"
echo "  programa:  $BIN_DIR/renemya  (e renemya-cli)"
echo "  atalho:    $APP_DIR/renemya.desktop"
case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *) echo "Dica: adicione $BIN_DIR ao PATH para usar 'renemya' e 'renemya-cli' no terminal." ;;
esac
echo "Abra pelo menu de aplicativos ou rode: renemya"
