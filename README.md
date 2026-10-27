<p align="center">
  <img src="renemya/gui/assets/renemya_icon.png" alt="Renemya" width="160">
</p>

<h1 align="center">Renemya</h1>

<p align="center">
  Renomeador de arquivos em lote — seguro, reversível e bonito.<br>
  🇺🇸 <a href="README.en.md">English version</a>
</p>

**Renemya** (novo nome do antigo *Rename This!*) renomeia milhares de arquivos de uma vez de forma
**rápida, previsível e segura**. Foi reescrito do zero em **Python + PySide6 (Qt)**. Antes de mexer
em qualquer coisa ele mostra uma prévia completa, recusa nomes perigosos, nunca sobrescreve arquivos
e deixa **desfazer** a operação. Funciona no **Windows** e no **Linux** (e no macOS pelo código-fonte),
em **15 idiomas**: português (Brasil), inglês, espanhol, chinês simplificado, hindi, árabe, francês, russo, bengali, japonês, alemão, indonésio, coreano, turco e italiano.

<p align="center">
  <img src="docs/img/claro.png" alt="Renemya no tema claro" width="49%">
  <img src="docs/img/escuro.png" alt="Renemya no tema escuro" width="49%">
</p>
<p align="center">
  <img src="docs/img/neon.gif" alt="Detalhes animados em laranja neon" width="70%">
</p>

## ⬇️ Download

Baixe a versão mais recente na página de **[Releases](https://github.com/cleitinhodev/renemya/releases/latest)**:

| Sistema | Arquivo |
|---|---|
| **Windows 10/11 (64 bits)** | `Renemya-<versão>-windows-x64.zip` — portátil, é só extrair e abrir `Renemya.exe` |
| **Linux x86-64** | `Renemya-<versão>-linux-x64.tar.gz` — extraia e rode `./install.sh` (ou `./renemya`) |
| **Linux (arquivo único)** | `Renemya-<versão>-x86_64.AppImage` — quando disponível no Release |

Todo pacote traz o **guia do usuário** (`README.md` e `LEIA-ME.html`) e a licença (`LICENSE.txt`).
O `SHA256SUMS.txt` do Release serve para conferir os downloads. Detalhes em
[Instalação](#-instalação).

## ✨ Destaques

### Segurança em primeiro lugar
- **Planejar, depois aplicar.** Todos os novos nomes são calculados e validados antes de qualquer
  arquivo ser tocado. Se houver um erro, nada é renomeado.
- **Nunca sobrescreve.** Conflitos são resolvidos na prévia: o programa adiciona um sufixo
  ` (2)`, ` (3)`… ou pula o arquivo, conforme você escolher. Na hora de renomear, o programa usa
  as chamadas do sistema que recusam um destino já existente (Linux/macOS) e faz uma última
  verificação antes de cada passo.
- **Trocas e cadeias funcionam.** Casos como `a → b` e `b → a`, ou `1.txt → 2.txt → 3.txt`,
  passam por nomes temporários em duas fases.
- **Reversão automática.** Se algo falhar no meio do caminho (arquivo aberto em outro
  programa, permissão negada…), tudo o que já tinha sido feito é desfeito.
- **Desfazer e histórico.** Cada operação fica registrada num diário (JSON). Dá para desfazer
  a última pela interface, pelo atalho `Ctrl+Z` ou pela linha de comando.
- **Recuperação após queda.** Se o computador desligar no meio de uma operação, o programa
  avisa na próxima vez que for aberto e oferece restaurar os nomes originais.
- **Validação de nomes no padrão do Windows em qualquer sistema.** Bloqueia:
  - os caracteres `\ / : * ? " < > |` e caracteres de controle
  - nomes reservados (`CON`, `NUL`, `COM1`…)
  - ponto ou espaço no final, nomes acima de 255 bytes e `..`
  - nomes que diferem só em maiúsculas/minúsculas, em sistemas que não diferenciam isso
- **Arquivos de sistema protegidos.** `desktop.ini`, `Thumbs.db`, `.DS_Store` e arquivos ocultos
  ficam fora, a menos que você marque para incluir.

### E mais
- **12 regras combináveis** (prefixo/sufixo, substituir com regex, remover, inserir, numeração,
  letras, data/EXIF, maiúsculas, limpeza, extensão, modelo com tokens e tags de música).
- **Prévia ao vivo** colorida, ordenação natural, filtros, predefinições e linha de comando.
- Tema **claro/escuro** que segue o sistema, com detalhes animados em **laranja neon**.

<!-- GUIA:INICIO (gerado de docs/guia.md; edite lá e rode packaging/build_release.py sync-readme) -->

## 🔗 Links

| Para quê | Link |
|---|---|
| 📦 **Downloads (Releases)** | <https://github.com/cleitinhodev/renemya/releases> |
| 💻 **Código-fonte** | <https://github.com/cleitinhodev/renemya> |
| 🐞 **Relatar um problema / sugerir algo** | <https://github.com/cleitinhodev/renemya/issues> |
| 👤 **Perfil do autor no GitHub** | <https://github.com/cleitinhodev> |
| 🌐 **Site** | <https://www.bugzinho.com/> |
| ❤️ **Apoie o projeto (doar)** | <https://www.bugzinho.com/donate> |

## 📥 Instalação

### Windows (10 e 11, 64 bits)

1. Baixe `Renemya-<versão>-windows-x64.zip` na página de
   [Releases](https://github.com/cleitinhodev/renemya/releases).
2. Clique com o botão direito no arquivo → **Extrair tudo…** e escolha uma pasta (por exemplo,
   `Documentos\Renemya`).
3. Abra **`Renemya.exe`**. Não precisa instalar nada: o programa é portátil.
4. Na primeira vez, o Windows pode mostrar **"O Windows protegeu o computador"** (SmartScreen).
   Isso acontece com programas novos que ainda não têm assinatura digital paga. Clique em
   **Mais informações → Executar assim mesmo**. Se preferir, confira antes o arquivo com o
   `SHA256SUMS.txt` do Release (veja a seção *Segurança*).
5. Opcional: clique com o botão direito em `Renemya.exe` → **Mostrar mais opções → Enviar para →
   Área de trabalho (criar atalho)**.

`renemya-cli.exe` é a versão de linha de comando (para o Prompt de Comando ou o PowerShell).

### Linux (x86-64)

O pacote foi gerado no Ubuntu 22.04 e funciona em distribuições com **glibc 2.35 ou mais nova**
(Ubuntu 22.04+, Debian 12+, Fedora 36+, Linux Mint 21+, openSUSE Tumbleweed…).

**Opção A — pacote `.tar.gz` (recomendado):**

```bash
tar -xzf Renemya-<versão>-linux-x64.tar.gz
cd Renemya-<versão>-linux-x64
./install.sh            # instala só para o seu usuário, sem sudo
```

O `install.sh` copia `renemya` e `renemya-cli` para `~/.local/bin`, o ícone para
`~/.local/share/icons` e o atalho para `~/.local/share/applications`. Depois disso o Renemya
aparece no menu de aplicativos. Para remover: `./install.sh --uninstall`.

Também dá para usar sem instalar:

```bash
chmod +x renemya renemya-cli   # só se as permissões se perderem
./renemya                      # interface gráfica
./renemya-cli --help           # linha de comando
```

**Opção B — AppImage (arquivo único), quando disponível no Release:**

```bash
chmod +x Renemya-<versão>-x86_64.AppImage
./Renemya-<versão>-x86_64.AppImage
```

Se aparecer um erro sobre **FUSE**, instale `libfuse2` (Ubuntu 22.04: `sudo apt install libfuse2`;
Ubuntu 24.04: `sudo apt install libfuse2t64`) ou rode com `--appimage-extract-and-run`.

**Dependências do sistema.** As bibliotecas do Qt (incluindo as do X11/xcb, como
`libxcb-cursor0`) já vão dentro do programa. O sistema só precisa ter o básico de qualquer
desktop: drivers gráficos com **OpenGL/EGL** (Mesa), `fontconfig` e um servidor gráfico
(X11 ou Wayland). Se o programa não abrir e mostrar algo como *"Could not load the Qt platform
plugin xcb"*, instale:

```bash
# Debian/Ubuntu/Mint
sudo apt install libegl1 libgl1 libxkbcommon-x11-0 libxcb-cursor0 libfontconfig1
# Fedora
sudo dnf install mesa-libEGL mesa-libGL libxkbcommon-x11 xcb-util-cursor fontconfig
```

### Pelo código-fonte (Windows, Linux e macOS)

Requer **Python 3.10 ou mais novo**:

```bash
git clone https://github.com/cleitinhodev/renemya.git
cd renemya
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate
pip install -e ".[media]"    # [media] = datas EXIF de fotos e tags de música
renemya                      # abre a interface (ou: python -m renemya)
```

## 🧭 Tutorial passo a passo

A janela tem quatro partes, de cima para baixo: **Pasta**, **Regras** (à esquerda), **Configurar
regra** (à direita) e a **Prévia** com o botão **Renomear**. Nada é alterado no disco até você
clicar em **Renomear** e confirmar.

### 1. Escolha a pasta

- Clique em **Procurar…** e escolha a pasta com os arquivos, **ou arraste a pasta** (do Explorador
  de Arquivos, Nautilus, Dolphin…) para dentro da janela. Também vale digitar ou colar o caminho.
- Menu **Arquivo → Abrir pasta…** faz o mesmo.
- O botão de atualizar (↻) relê a pasta, caso você tenha mexido nos arquivos por fora.
- No Linux, também dá para abrir direto: `renemya ~/Imagens/Viagem`.

### 2. Adicione e ordene as regras

- Clique em **Adicionar regra** e escolha o tipo. A regra aparece na lista e seus campos aparecem
  em **Configurar regra**. A prévia muda na hora, enquanto você digita.
- As regras são aplicadas **de cima para baixo**: cada uma recebe o nome já modificado pela
  anterior. A ordem importa! Exemplo: "Limpeza do nome" antes de "Numeração" é diferente de
  "Numeração" antes de "Limpeza".
- **Reordenar:** arraste a regra na lista ou use as setas ↑ ↓.
- **Desativar sem apagar:** desmarque a caixinha ao lado da regra.
- **Duplicar**, **remover** a selecionada ou **remover todas**: botões ao lado da lista.

### 3. As 12 regras

Os exemplos partem do nome à esquerda da seta.

| # | Regra | O que faz | Exemplo |
|---|---|---|---|
| 1 | **Prefixo / sufixo** | Coloca um texto antes e/ou depois do nome (a extensão é preservada). | prefixo `Viagem_`: `IMG_0001.JPG` → `Viagem_IMG_0001.JPG` |
| 2 | **Substituir texto** | Procura e troca um texto. Opções: diferenciar maiúsculas, usar **regex** e agir no *nome*, na *extensão* ou no *nome completo*. | `IMG_` → `Foto `: `IMG_0001.JPG` → `Foto 0001.JPG` · regex `(\d+)` → `n\1` |
| 3 | **Remover caracteres** | Remove: certos caracteres, um trecho (início + quantidade), os N primeiros ou últimos, todos os números ou o texto entre `( )` `[ ]` `{ }`. | entre parênteses/colchetes: `Música (Ao Vivo) [2020].mp3` → `Música.mp3` |
| 4 | **Inserir texto** | Insere um texto numa posição, contando do início ou do fim. | `-final` na posição 0 a partir do fim: `relatorio.txt` → `relatorio-final.txt` |
| 5 | **Numeração** | Contador com início, passo, **zeros à esquerda**, posição (início, fim ou substituir o nome) e separador. Pode reiniciar em cada subpasta. | 3 dígitos, no início, separador ` - `: `aula.mp4` → `001 - aula.mp4` |
| 6 | **Letras (A, B… AA)** | Como a numeração, mas com letras: A, B… Z, AA, AB… (maiúsculas ou minúsculas). | `foto.jpg`, `foto.png` → `foto_A.jpg`, `foto_B.png` |
| 7 | **Data** | Usa a data de **modificação**, de **criação** ou a **data em que a foto foi tirada (EXIF)**, no formato que você quiser, no início, no fim ou no lugar do nome. | EXIF, `%Y-%m-%d`: `IMG_0001.JPG` → `2024-01-15_IMG_0001.JPG` |
| 8 | **Maiúsculas / minúsculas** | minúsculas, MAIÚSCULAS, Título (Cada Palavra), Frase (só a primeira) ou iNVERTER. Opcionalmente também na extensão. | Título: `aula 2.txt` → `Aula 2.txt` |
| 9 | **Limpeza do nome** | Troca espaços por `_` `-` `.` (ou remove), remove acentos (ç → c), remove caracteres inválidos, junta separadores repetidos e apara as pontas. | espaços → `_` + sem acentos: `Relatório Final  (cópia).PDF` → `Relatorio_Final_(copia).PDF` |
| 10 | **Extensão** | Deixa a extensão em minúsculas ou maiúsculas, troca por outra ou remove. | minúsculas: `IMG_0001.JPG` → `IMG_0001.jpg` |
| 11 | **Modelo personalizado** | Monta o nome inteiro com *tokens* (tabela abaixo). Tem início, passo e reinício por pasta para `{n}`. | `Viagem_{exif:%Y-%m-%d}_{n:03}` → `Viagem_2024-01-15_001.jpg` |
| 12 | **Tags de música** | Monta o nome com as tags dos arquivos de áudio (MP3, FLAC, M4A, OGG…). | `{track:02} - {artist} - {title}` → `01 - Artista - Título.mp3` |

**Tokens do modelo** (menu **Ajuda → Tokens do modelo** mostra esta lista dentro do programa):

| Token | Resultado |
|---|---|
| `{name}` | nome original, sem a extensão |
| `{current}` | nome como está depois das regras anteriores |
| `{ext}` | extensão original, sem o ponto |
| `{parent}` | nome da pasta onde o arquivo está |
| `{n}` · `{n:03}` | numeração · com 3 dígitos (001, 002…) |
| `{letter}` · `{letter:lower}` | A, B… AA · a, b… |
| `{date:%Y-%m-%d}` · `{modified}` | data de modificação |
| `{created:%Y}` | data de criação |
| `{exif:%Y-%m-%d_%H%M}` | data em que a foto foi tirada |
| `{now:%Y-%m-%d}` | data de hoje |
| `{size}` | tamanho em bytes |
| `{artist}` `{title}` `{album}` `{track:02}` `{year}` `{genre}` | tags de música |

Formatos de data: `%Y` ano · `%m` mês · `%d` dia · `%H` hora · `%M` minuto · `%S` segundo ·
`%B` nome do mês. Exemplo: `%d-%m-%Y` → `15-01-2024`.

### 4. Ordenação e filtros (painel "Arquivos e ordem")

- **Ordenar por:** nome (ordem natural: `2.txt` vem antes de `10.txt`), data de modificação,
  data de criação, tamanho, tipo (extensão) ou ordem do sistema. Marque **Ordem decrescente** para
  inverter. A ordem define a numeração: para numerar fotos na ordem em que foram tiradas, ordene
  por data.
- **Somente extensões:** ex. `jpg, png` (vazio = todas). **Ignorar extensões:** ex. `tmp, log`.
- **Incluir subpastas:** também processa os arquivos dentro das subpastas (cada um continua na
  sua pasta; a coluna *Pasta* mostra onde ele está).
- **Renomear arquivos / Renomear pastas:** escolha o que entra na lista.
- **Incluir arquivos ocultos** e **Incluir arquivos de sistema** (`desktop.ini`, `Thumbs.db`,
  `.DS_Store`…): desligados por padrão, por segurança.

### 5. Leia a prévia

A tabela mostra o **Nome atual**, o **Novo nome**, a **Pasta** e a **Situação**. A cor diz o que vai
acontecer com cada item:

| Situação | Cor | Significado |
|---|---|---|
| **Será renomeado** | 🟢 verde | Tudo certo: o item vai receber o novo nome. |
| **Aviso** | 🟠 laranja | Vai renomear, mas preste atenção (ex.: extensão trocada, nome que começa com espaço, nome ajustado com sufixo, caminho muito longo). O motivo aparece na coluna *Situação*. |
| **Pulado** | ⚪ cinza | Não será renomeado por conflito de nome (quando a opção é *Pular*). |
| **Erro** | 🔴 vermelho | Nome inválido (ex.: `CON`, caracteres `\ / : * ? " < > \|`, nome vazio ou longo demais). **Enquanto houver erro, o botão Renomear fica bloqueado.** |
| **Sem alteração** | ponto discreto | O nome já está certo; nada muda. |

- Marque **Mostrar só o que muda** para esconder os itens sem alteração.
- A linha de resumo mostra quantos itens serão renomeados, pulados e com erro.

### 6. Conflitos de nome

Em **Se o nome já existir:** escolha

- **Adicionar sufixo (2), (3)…** — o Renemya ajusta o nome (`foto.jpg` → `foto (2).jpg`) e marca com
  aviso; ou
- **Pular o arquivo** — o item fica com o nome atual e aparece como *Pulado*.

Isso vale tanto para arquivos que já existem na pasta quanto para dois itens que ficariam com o
mesmo nome. O Renemya **nunca sobrescreve** um arquivo. Trocas como `a → b` e `b → a` funcionam
normalmente.

### 7. Aplique

Clique em **Renomear**, confira a janela de confirmação (quantidade, pasta, avisos e pulados) e
confirme. Uma barra de progresso aparece e, no fim, um resumo. Se algo falhar no meio (arquivo
aberto em outro programa, sem permissão…), **tudo o que já tinha sido feito é revertido** e
nenhum arquivo fica pela metade.

### 8. Desfazer e histórico

- **Desfazer última** (botão ao lado de Renomear), **Editar → Desfazer última renomeação** ou
  **Ctrl+Z**: volta os nomes originais da última operação (pede confirmação).
- **Arquivo → Histórico de operações…** lista todas as renomeações, com data, pasta, quantidade e
  situação (Concluída, Desfeita, Falhou/revertida…). O botão *Abrir pasta do histórico* mostra os
  arquivos JSON do diário.
- **Editar → Recuperar operação interrompida:** se o computador desligou ou o programa fechou no
  meio de uma renomeação, use isto para restaurar os nomes. O Renemya também pergunta sozinho ao
  abrir, se detectar uma operação pendente.

### 9. Predefinições

Montou um conjunto de regras que vai usar de novo? **Arquivo → Salvar predefinição…** grava as
regras e as opções num arquivo `.json`. Para usar depois: **Arquivo → Carregar predefinição…**.
A mesma predefinição funciona na linha de comando (`--preset arquivo.json`). A última sessão
(pasta, regras e opções) também é restaurada automaticamente quando você reabre o programa.

### 10. Idioma, tema e animações

- **Idioma:** menu **Idioma**, com 15 idiomas: Português (Brasil), English, Español, 中文（简体）,
  हिन्दी, العربية, Français, Русский, বাংলা, 日本語, Deutsch, Bahasa Indonesia, 한국어, Türkçe e
  Italiano. A troca é imediata e fica salva. Na primeira vez, o Renemya usa o idioma do sistema
  (ou inglês, se o idioma do sistema não estiver na lista). Em árabe, a janela fica espelhada
  (da direita para a esquerda). Para forçar um idioma, use a variável `RENEMYA_LANG` (ex.:
  `RENEMYA_LANG=ja`).
- **Tema:** claro ou escuro, **seguindo o tema do sistema** automaticamente (inclusive se você
  trocar com o programa aberto). Para forçar, defina a variável de ambiente
  `RENEMYA_THEME=light` ou `RENEMYA_THEME=dark`.
- **Animações:** os riscos de luz em **laranja neon** (no cabeçalho, no botão Renomear, na barra de
  progresso e no painel ativo) podem ser desligados em **Editar → Animações**. A escolha fica salva,
  e elas pausam sozinhas com a janela minimizada.
- **Ajuda → Sobre** mostra a versão e os links do projeto.

## 🍳 Receitas prontas

**Fotos de viagem pela data em que foram tiradas** — `IMG_4821.JPG` → `Viagem_2024-01-15_001.jpg`
1. *Ordenar por:* Data de modificação (ou deixe por nome se a câmera numera em sequência).
2. *Somente extensões:* `jpg, jpeg, heic, png`.
3. Regra **Modelo personalizado**: `Viagem_{exif:%Y-%m-%d}_{n:03}`.
4. Regra **Extensão** → minúsculas.

Fotos sem EXIF (prints, imagens baixadas) usam a data de modificação e recebem um aviso.

**Numeração com zeros** — `aula 1.mp4`, `aula 10.mp4` → `Aula 001.mp4`, `Aula 010.mp4`
- *Ordenar por:* Nome (a ordem natural já põe `2` antes de `10`).
- Regra **Modelo personalizado**: `Aula {n:03}`; ou regra **Numeração** com 3 dígitos,
  posição *Substituir o nome*. Use *Início* e *Passo* para começar em outro número.

**Limpar acentos e espaços (nomes "seguros" para web/pendrive)** —
`Relatório Final  (cópia).PDF` → `relatorio_final.pdf`
1. **Remover caracteres** → *Texto entre ( ) [ ] { }* (opcional).
2. **Limpeza do nome** → espaços *Trocar por _*, marque *Remover acentos*.
3. **Maiúsculas / minúsculas** → minúsculas, marcando *Aplicar também na extensão*.

**Músicas pelas tags** — `faixa03.mp3` → `03 - Legião Urbana - Tempo Perdido.mp3`
1. *Somente extensões:* `mp3, flac, m4a, ogg`.
2. Regra **Tags de música**: `{track:02} - {artist} - {title}` (ou
   `{artist} - {album} - {track:02} - {title}`).
3. Arquivos sem tags aparecem com aviso: confira antes de aplicar.

## ⌨️ Linha de comando (renemya-cli)

```bash
renemya-cli --help                 # ajuda geral
renemya-cli rules                  # lista as 12 regras e seus parâmetros
renemya-cli --version

# Sempre comece com --dry-run (-n): mostra a prévia e não altera nada
renemya-cli rename ./fotos --sort modified --template "Viagem_{exif:%Y-%m-%d}_{n:03}" --dry-run

# Aplica (pede confirmação; -y pula a pergunta)
renemya-cli rename ./fotos --sort modified --template "Viagem_{exif:%Y-%m-%d}_{n:03}"

# Atalhos: --prefix, --suffix, --replace DE PARA, --regex PADRÃO TROCA, --template, --case
renemya-cli rename ./docs --replace "rascunho" "final" --case lower -n

# Qualquer regra com --add TIPO chave=valor (aplicadas na ordem em que aparecem)
renemya-cli rename ./musicas --ext mp3,flac \
    --add cleanup spaces=underscore strip_accents=true \
    --add counter padding=3 position=prefix separator=" - " -n
renemya-cli rename ./musicas --add music "template={track:02} - {artist} - {title}" -n

# Predefinições feitas na interface ou na linha de comando
renemya-cli rename ./fotos --preset viagem.json -n
renemya-cli rename ./fotos --template "Foto_{n:03}" --save-preset fotos.json -n

renemya-cli undo        # desfaz a última renomeação
renemya-cli history     # histórico
renemya-cli recover     # restaura uma operação interrompida
renemya-cli --lang en rename ...   # mensagens em inglês (ou es, fr, de, ja, ar…)
```

Opções do `rename`: `--sort name|modified|created|size|type|none`, `--desc`, `-r` (subpastas),
`--dirs` (também pastas), `--no-files`, `--hidden`, `--system`, `--ext jpg,png`,
`--exclude-ext tmp`, `--on-conflict suffix|skip`, `--all` (mostra também os sem alteração).
Códigos de saída: `0` sucesso, `1` erro ou cancelado, `2` uso incorreto.
No Windows, use `renemya-cli.exe` no Prompt de Comando/PowerShell (aspas duplas nos valores com
espaço).

## 🛡️ Segurança

- **Prévia antes de tudo:** todos os nomes são calculados e validados antes de qualquer arquivo
  ser tocado. Com qualquer erro, nada é renomeado.
- **Nunca sobrescreve** arquivos existentes; conflitos são resolvidos na prévia.
- **Reversão automática** se algo falhar no meio, **desfazer** a qualquer momento e
  **recuperação** após queda de energia.
- Nomes são validados no **padrão do Windows** em qualquer sistema, para seus arquivos não darem
  problema ao serem copiados para outro computador ou pendrive.
- Arquivos ocultos e de sistema ficam de fora por padrão.
- O Renemya **só muda nomes**: nunca altera o conteúdo dos arquivos e não usa internet.
- Mesmo assim, para coleções insubstituíveis, um backup antes de grandes mudanças é sempre uma boa
  ideia.
- **Conferir o download:** cada Release traz um `SHA256SUMS.txt`. No Windows (PowerShell):
  `Get-FileHash .\Renemya-<versão>-windows-x64.zip -Algorithm SHA256`; no Linux:
  `sha256sum -c SHA256SUMS.txt --ignore-missing`. O valor deve ser igual ao do arquivo.

**Onde ficam os dados** (histórico/diário e predefinições):
Windows `%LOCALAPPDATA%\Renemya` · Linux `~/.local/share/Renemya` · macOS
`~/Library/Application Support/Renemya`. Para usar outra pasta, defina `RENEMYA_DATA_DIR`.

## ❓ Perguntas frequentes

**Por que a extensão mudou?**
A extensão só muda se alguma regra mexer nela: **Extensão** (por exemplo, *minúsculas*
transforma `.JPG` em `.jpg`), **Substituir texto** com *Aplicar em* = *Extensão* ou *Nome
completo*, ou **Maiúsculas / minúsculas** com *Aplicar também na extensão*. Trocar a extensão
**não converte o arquivo** (um `.png` renomeado para `.jpg` continua sendo PNG); por isso a prévia
mostra um aviso laranja. As demais regras, incluindo o **Modelo**, preservam a extensão original.

**O botão Renomear está desativado. Por quê?**
Há itens com **Erro** (vermelho) na prévia, nenhuma regra ativa ou nada para mudar. Corrija ou
desative a regra que causa o erro (o motivo aparece na coluna *Situação*).

**Renomeei errado. E agora?**
Use **Ctrl+Z** / **Desfazer última**. Operações antigas aparecem em *Arquivo → Histórico*.

**A data EXIF não aparece.**
Só fotos de câmeras/celulares têm EXIF. Sem EXIF, o Renemya usa a data de modificação e mostra um
aviso. No programa baixado do Release o suporte a EXIF e a tags de música já vem incluído; pelo
código-fonte, instale com `pip install -e ".[media]"`.

**Por que alguns arquivos não aparecem na lista?**
Confira os filtros: *Somente extensões*, *Ignorar extensões*, *Incluir subpastas*, *ocultos* e
*de sistema*.

**O Windows bloqueou o programa (SmartScreen).**
É normal para programas novos sem assinatura digital paga. Clique em *Mais informações →
Executar assim mesmo* e, se quiser, confira o `SHA256SUMS.txt`.

**No Linux não abre ("Qt platform plugin xcb").**
Instale as dependências listadas em *Instalação → Linux*. Para ver a mensagem de erro completa,
rode `./renemya` pelo terminal.

**Achei um bug ou tenho uma ideia.**
Abra uma *issue* em <https://github.com/cleitinhodev/renemya/issues>.

<!-- GUIA:FIM -->

## Desenvolvimento

```bash
pip install -e ".[dev]"
ruff check . && ruff format --check .
pytest                      # a interface é testada em modo offscreen
```

Estrutura:

```
renemya/
  core/      motor sem Qt: varredura, regras, planejamento, validação, execução, diário, predefinições
  gui/       interface PySide6 (janela, prévia, editor de regras, worker em QThread, animações)
  gui/assets ícones (renemya_icon = ícone geral, renemya_favicon = barra de título)
  i18n/      traduções pt_BR.json e en.json
  cli.py     linha de comando
tests/       testes (pytest)
packaging/   PyInstaller, pacotes do Release (build_release.py) e arquivos do Linux
docs/        guia do usuário (guia.md, guide.en.md) e capturas de tela
```

### Gerar os executáveis e o Release

A cada push na `main`, o GitHub Actions (workflow **Build e Release**) roda os testes, gera os
executáveis com PyInstaller no **Windows** e no **Ubuntu 22.04**, faz um teste rápido de
abertura (`--smoke-test`) e guarda os pacotes como artefatos da execução. Ao enviar uma tag
`vX.Y.Z` (igual à versão do `pyproject.toml`), ele também publica o Release com o `.zip` do
Windows, o `.tar.gz` do Linux, o AppImage (quando a geração funciona) e o `SHA256SUMS.txt`.

Para gerar localmente:

```bash
pip install -e ".[dev,build]" markdown
pyinstaller --onefile --windowed --name Renemya --icon renemya/gui/assets/renemya_icon.ico \
  --collect-data renemya --paths . packaging/gui_launcher.py
pyinstaller --onefile --console --name renemya-cli --collect-data renemya --paths . packaging/cli_launcher.py
python packaging/build_release.py package --platform windows   # ou linux
```

O guia do usuário fica em `docs/guia.md` (e `docs/guide.en.md`). Depois de editar, rode
`python packaging/build_release.py sync-readme` para atualizar este README.

## Considerações finais

Fico feliz em compartilhar esta ferramenta com a comunidade! É um prazer buscar soluções práticas
para facilitar a vida de todos. Não tenho interesse em lucrar com isso, mas, caso queira ajudar com
alguma contribuição: [❤️ Doar](https://www.bugzinho.com/donate) ·
[Patreon - CleitinhoDEV](https://www.patreon.com/CleitinhoDEV).

Mais informações: [Bugzinho.com](https://www.bugzinho.com) · GitHub: [@cleitinhodev](https://github.com/cleitinhodev)

By CleitinhoDEV

## Créditos e licenças

O Renemya é distribuído sob a licença **GPL-3.0** (veja [LICENSE](LICENSE)). Ele usa estas
bibliotecas de código aberto:

- [**PySide6 / Qt for Python**](https://doc.qt.io/qtforpython-6/), interface gráfica, licença LGPL-3.0
- [**platformdirs**](https://github.com/tox-dev/platformdirs), pastas de dados por sistema, licença MIT
- [**Pillow**](https://python-pillow.org/), leitura de EXIF (opcional), licença MIT-CMU
- [**mutagen**](https://github.com/quodlibet/mutagen), tags de música (opcional), licença GPL-2.0-or-later
- [**Python**](https://www.python.org/) e sua biblioteca padrão, licença PSF
