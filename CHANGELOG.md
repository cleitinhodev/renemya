# Changelog

Todas as mudanças importantes do Renemya ficam registradas aqui.
O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o projeto usa
[versionamento semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] — 2026-10-26

Primeira versão estável do **Renemya**: o antigo *Rename This!* reescrito do zero em Python +
PySide6 (Qt).

### Adicionado
- **12 regras combináveis**, aplicadas de cima para baixo. Cada regra pode ser ativada,
  desativada, duplicada ou reordenada:
  - prefixo/sufixo e substituir texto (com regex);
  - remover caracteres, inserir texto, numeração e letras;
  - data de modificação, de criação ou EXIF da foto;
  - maiúsculas/minúsculas, limpeza do nome e extensão;
  - modelo com tokens e tags de música.
- **Prévia ao vivo** com cores por situação: será renomeado, aviso, pulado, erro e sem alteração.
- **Ordenação natural** e **filtros**: extensões, subpastas, pastas, ocultos e arquivos de sistema.
- **Segurança:** validação de nomes no padrão do Windows. O Renemya nunca sobrescreve arquivos.
  Ele também cuida de:
  - conflitos, com sufixo `(2)` ou pulando o arquivo;
  - trocas e cadeias, renomeando em duas fases;
  - reversão automática se algo falhar no meio.
- **Desfazer** (Ctrl+Z), **histórico** de operações e **recuperação** de operações interrompidas.
- **Predefinições** em JSON e restauração da última sessão.
- **Linha de comando** `renemya-cli`, com os comandos `rename`, `rules`, `undo`, `history` e
  `recover`.
- **Português e inglês**, com troca imediata.
- **Visual novo:** tema claro e escuro que segue o sistema, ícones da raposa e detalhes animados
  em laranja neon, que podem ser desligados em *Editar → Animações*.
- Janela **Sobre** com links para o GitHub, o repositório, o site e doações.
- A interface aceita uma pasta como argumento (`renemya ~/Fotos`) e as opções `--version` e
  `--smoke-test`.
- **Pacotes oficiais:**
  - Windows: `.zip` portátil;
  - Linux: `.tar.gz` com `install.sh` e atalho no menu, além de AppImage quando disponível.
  - Todos trazem o guia do usuário (`README.md` e `LEIA-ME.html`) e a licença GPL-3.0.
  - O `SHA256SUMS.txt` serve para conferir os downloads.
