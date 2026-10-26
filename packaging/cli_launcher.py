"""Ponto de entrada usado pelo PyInstaller para gerar o executável de linha de comando."""

from renemya.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
