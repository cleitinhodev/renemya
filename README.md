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
e deixa **desfazer** a última operação.

> ⚠️ **Versão em testes.** Até sair a versão estável, faça backup dos arquivos importantes.

## Download

- Os executáveis do Windows (`Renemya.exe` e `renemya-cli.exe`) são gerados a cada atualização da
  branch `main`: abra a aba [Actions](https://github.com/cleitinhodev/renemya/actions), entre na
  execução mais recente do **Build (Windows .exe)** e baixe o artefato **Renemya-windows**.
- Quando uma versão estável for publicada, ela aparece na aba
  [Releases](https://github.com/cleitinhodev/renemya/releases).

## O que há de novo

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

### Regras de renomeação combináveis
Monte uma lista de regras. Elas são aplicadas de cima para baixo, e cada uma pode ser ativada,
desativada, duplicada ou reordenada.

| Regra | O que faz |
|---|---|
| Prefixo / sufixo | Adiciona texto antes e/ou depois do nome |
| Substituir texto | Procura e substitui; pode diferenciar maiúsculas, usar **regex** e agir no nome, na extensão ou nos dois |
| Remover caracteres | Remove caracteres específicos, um intervalo, os N primeiros/últimos, os dígitos ou o texto entre `()` `[]` `{}` |
| Inserir texto | Insere texto numa posição (contando do início ou do fim) |
| Numeração | Contador com início, passo, zeros à esquerda, posição e separador; pode reiniciar em cada pasta |
| Letras | A, B, … Z, AA, AB… |
| Data | Data de modificação, criação ou **da foto (EXIF)**, com formato personalizável |
| Maiúsculas / minúsculas | minúsculas, MAIÚSCULAS, Título, Frase, iNVERTER |
| Limpeza do nome | Troca espaços, remove acentos e caracteres inválidos, junta separadores repetidos |
| Extensão | Minúsculas, maiúsculas, trocar ou remover a extensão |
| Modelo personalizado | Monta o nome com *tokens* (tabela abaixo) |
| Tags de música | Usa artista, título, álbum e faixa dos arquivos de áudio (MP3, FLAC, M4A, OGG…) |

#### Tokens do modelo

| Token | Resultado |
|---|---|
| `{name}` | nome original, sem a extensão |
| `{current}` | nome como está depois das regras anteriores |
| `{ext}` | extensão, sem o ponto |
| `{parent}` | nome da pasta |
| `{n}` `{n:03}` | numeração (com 3 dígitos: 001, 002…) |
| `{letter}` `{letter:lower}` | letras A, B… / a, b… |
| `{date}` `{modified:%d-%m-%Y}` `{created}` `{exif}` `{now}` | datas (formato opcional, ex.: `%Y-%m-%d_%H%M`) |
| `{size}` | tamanho em bytes |
| `{artist}` `{title}` `{album}` `{track:02}` `{year}` `{genre}` | tags de música |

Exemplo: `Viagem_{exif:%Y-%m-%d}_{n:03}` vira `Viagem_2024-01-15_001.jpg`.

### Interface
- Escolha a pasta pelo botão **Procurar** ou **arrastando-a para a janela**.
- **Prévia ao vivo**: tabela com o nome atual e o novo nome. As cores indicam o que vai
  acontecer (renomear, aviso, pular, erro, sem alteração), e o motivo de cada aviso aparece na
  coluna de situação.
- **Ordenação** natural (`2.txt` antes de `10.txt`) por nome, data, tamanho ou tipo, crescente ou decrescente.
- **Filtros**: só algumas extensões, ignorar extensões, incluir subpastas, renomear pastas, incluir ocultos e de sistema.
- **Confirmação** antes de aplicar, barra de progresso, resumo no final e **Desfazer**.
- **Predefinições**: salve e carregue conjuntos de regras e opções em JSON.
- **Português e inglês**, com troca imediata no menu *Idioma*.
- Tema **claro ou escuro**, seguindo o sistema, com detalhes em **laranja neon** (a cor da
  raposa do ícone). Riscos de luz percorrem o cabeçalho, o botão **Renomear**, a barra de
  progresso e o painel ativo. Para desligar: menu *Editar → Animações* (a escolha fica salva).
  As animações pausam sozinhas com a janela minimizada ou em segundo plano.
- A última sessão (pasta, regras e opções) é restaurada ao reabrir.

## Instalação a partir do código

Requer **Python 3.10 ou mais novo**.

```bash
git clone https://github.com/cleitinhodev/renemya.git
cd renemya

python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate

pip install -e .            # básico
pip install -e ".[media]"   # + datas EXIF de fotos (Pillow) e tags de música (mutagen)
```

## Como usar

### Interface gráfica
```bash
renemya
# ou
python -m renemya
```

### Linha de comando
```bash
# Prévia (não altera nada): numeração com 3 dígitos, ordenando por data de modificação
renemya-cli rename ./fotos --sort modified --template "Foto_{n:03}" --dry-run

# Aplica (pede confirmação; use -y para pular)
renemya-cli rename ./fotos --sort modified --template "Foto_{n:03}"

# Várias regras, aplicadas na ordem em que aparecem
renemya-cli rename ./musicas --ext mp3,flac \
    --add cleanup spaces=underscore strip_accents=true \
    --case lower

# Regras avançadas com --add TIPO chave=valor
renemya-cli rename ./docs --add remove mode=brackets --add date source=modified position=prefix

renemya-cli rules      # lista todas as regras e parâmetros
renemya-cli undo       # desfaz a última operação
renemya-cli history    # mostra o histórico
renemya-cli recover    # restaura uma operação interrompida
renemya-cli --lang en rename ...   # mensagens em inglês
```

Outras opções do `rename`:
- `-r` inclui subpastas; `--dirs` também renomeia pastas
- `--hidden` e `--system` incluem arquivos ocultos e de sistema
- `--exclude-ext` ignora extensões
- `--on-conflict skip|suffix` define o que fazer quando o nome já existe
- `--preset arquivo.json` / `--save-preset arquivo.json` carregam ou salvam regras e opções

Códigos de saída: `0` sucesso, `1` erro ou cancelado, `2` uso incorreto.

### Onde ficam os dados
O histórico (diário) e as predefinições ficam em:
- **Windows:** `%LOCALAPPDATA%\Renemya`
- **Linux:** `~/.local/share/Renemya`
- **macOS:** `~/Library/Application Support/Renemya`

Para usar outra pasta, defina a variável `RENEMYA_DATA_DIR`. Para forçar o tema, use
`RENEMYA_THEME=light` ou `RENEMYA_THEME=dark`.

> Quem usou a versão de testes com o nome antigo: o histórico antigo continua em
> `%LOCALAPPDATA%\RenameThis`. O Renemya começa com um histórico novo.

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
packaging/   scripts de entrada do PyInstaller
```

**Gerar o executável do Windows:** a cada push na `main`, o GitHub Actions roda os testes e gera
`Renemya.exe` e `renemya-cli.exe` com PyInstaller (ficam como artefatos da execução, sem criar
Release). Se você criar uma tag `v*`, os arquivos também são anexados ao Release dessa tag.
Para gerar localmente:

```bash
pip install -e ".[dev,build]"
pyinstaller --onefile --windowed --name Renemya --icon renemya/gui/assets/renemya_icon.ico ^
  --collect-data renemya --paths . packaging/gui_launcher.py
```

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
