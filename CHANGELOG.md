# Changelog

Todas as mudanças importantes do Renemya ficam registradas aqui.
O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o projeto usa
[versionamento semântico](https://semver.org/lang/pt-BR/).

## [1.1.0] — 2026-10-27

O Renemya agora fala **15 idiomas**. As funcionalidades são as mesmas da 1.0.0.

### Adicionado
- **13 idiomas novos** na interface e na linha de comando, além de português e inglês: espanhol,
  chinês simplificado, hindi, árabe, francês, russo, bengali, japonês, alemão, indonésio,
  coreano, turco e italiano. O menu **Idioma** mostra cada um com o nome nativo.
- **Árabe da direita para a esquerda:** a janela inteira fica espelhada, inclusive a tabela de
  prévia e os selos de situação.
- **Fontes embutidas** (Noto, licença OFL) para chinês, japonês, coreano, hindi, bengali e árabe.
  Elas só são usadas quando o sistema não tem fonte para essas escritas, por exemplo num Linux
  mínimo com o AppImage.
- `RENEMYA_LANG` e `renemya-cli --lang` aceitam os 15 códigos (`pt_BR`, `en`, `es`, `zh_CN`, `hi`,
  `ar`, `fr`, `ru`, `bn`, `ja`, `de`, `id`, `ko`, `tr`, `it`).
- Atalho do Linux (`renemya.desktop`) com descrição traduzida.

### Mudado
- Na primeira execução, o idioma segue o do sistema, inclusive no Windows (antes, nomes como
  `Portuguese_Brazil` não eram reconhecidos). Se o idioma do sistema não estiver na lista, a
  interface abre em inglês.
- Datas da dica e da confirmação de **Desfazer** no formato do idioma escolhido (antes, sempre
  dd/mm/aaaa).
- Botões das caixas de diálogo (Sim, Cancelar, OK, Fechar) traduzidos. Os diálogos padrão do Qt
  usam as traduções do próprio Qt quando existem.
- `install.sh` com mensagens em inglês, ou em português se o sistema estiver em português.

### Corrigido
- O texto de ajuda da lista de regras vazia (`rules.empty_hint`) não existia e aparecia como a
  chave crua.

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
