# Thero

Configura um ambiente profissional para o [Claude Code](https://claude.com/claude-code):
instala Agent Skills, consolida o `CLAUDE.md`, audita projetos e cria um
comando de atalho (`thero`) para tudo isso.

## Descrição

O `thero.py` automatiza a configuração do Claude Code para um fluxo de
engenharia de software profissional. Ele:

- instala Agent Skills relevantes (React/Frontend, Supabase, Stripe,
  Firebase, TypeScript, testes, etc.);
- preserva skills já instaladas (`caveman`, `impeccable`);
- preserva o `CLAUDE.md` existente;
- cria backup antes de qualquer alteração;
- usa o próprio Claude Code para consolidar o `CLAUDE.md`, mesclando as
  instruções existentes com um novo "Engineering Operating System" enxuto;
- separa comportamento global (CLAUDE.md) de conhecimento especializado
  (Agent Skills), para manter o CLAUDE.md pequeno e eficiente em tokens;
- permite auditar um projeto (modo somente leitura) antes de qualquer
  alteração de código;
- pode operar globalmente (usuário, `~/.claude`) ou localmente (projeto
  atual, `--local`);
- instala um comando de atalho (PowerShell no Windows; bash/zsh no
  macOS/Linux), global ou local ao projeto, para rodar o script de
  qualquer lugar;
- favorece mudanças pequenas e verificáveis.

## Requisitos

- Python 3.10+ (só biblioteca padrão, sem dependências externas)
- Node.js e `npx` (necessários para instalar skills via `npx skills add`)
- Claude Code instalado e autenticado (necessário para consolidar o
  `CLAUDE.md` e para rodar auditorias — `claude -p`)
- Comando de atalho (`--install-command`): Windows (PowerShell) ou
  macOS/Linux (bash/zsh, detectado via `$SHELL`); suporte
  macOS/Linux é novo, validado via Git Bash no Windows, zsh/bash
  reais ainda não testados

Se `claude` não estiver disponível, a instalação de skills ainda funciona;
apenas a consolidação do `CLAUDE.md` e a auditoria são puladas (com aviso).

## Instalação

Não há instalação via `pip`. Basta clonar e rodar:

```
git clone https://github.com/netovieira/thero.git
cd thero
python thero.py
```

## Uso

```
python thero.py [opções]
```

## Comandos

| Comando                    | O que faz                                                          |
|-----------------------------|---------------------------------------------------------------------|
| *(sem argumentos)*          | Fluxo completo: instala skills, consolida o `CLAUDE.md` e instala/atualiza o comando `thero` (global). |
| `--skills-only`             | Instala apenas as skills, sem tocar no `CLAUDE.md` nem no comando. |
| `--merge-only`               | Consolida apenas o `CLAUDE.md` (requer `claude`).                  |
| `--audit-only`               | Audita o projeto atual (somente leitura), sem instalar nada.       |
| `--audit`                    | Executa o fluxo completo e, em seguida, audita o projeto atual.    |
| `--install-command [NOME]`   | Instala/atualiza somente o comando de atalho (padrão: `thero`). Sem `NOME`, pergunta interativamente (Enter aceita o sugerido). |
| `--index`                    | Roda a [Athena](https://github.com/netovieira/athena) na pasta atual (indexa a arquitetura em `.athena/`); instala/atualiza automaticamente via git se preciso e o terminal for interativo. |
| `--check`                    | Verifica se alguma skill instalada tem atualização disponível (`npx skills check` + `npx impeccable check`). |
| `--update`                   | Atualiza as skills instaladas para a versão mais recente (`npx skills update` + `npx impeccable update`). |
| `--local`                    | Faz tudo (`CLAUDE.md`, skills, comando) mirar a pasta do projeto atual em vez do usuário global. Combina com qualquer outra flag. |
| `-h`, `--help`               | Mostra a ajuda e sai, sem instalar nada, sem modificar arquivos e sem chamar o Claude. |

## Exemplos

Instalar e configurar tudo (skills + CLAUDE.md + comando `thero`):

```
python thero.py
```

Instalar tudo na pasta do projeto atual (CLAUDE.md, skills e comando
ficam locais ao projeto, não no usuário global):

```
python thero.py --local
```

Instalar somente as skills:

```
python thero.py --skills-only
```

Consolidar somente o `CLAUDE.md`:

```
python thero.py --merge-only
```

Auditar o projeto atual sem modificar código:

```
python thero.py --audit-only
```

Instalar/configurar e, na sequência, auditar o projeto atual:

```
python thero.py --audit
```

Instalar só o comando de atalho (pergunta o nome, Enter aceita `thero`):

```
python thero.py --install-command
```

Instalar o comando de atalho com nome customizado, sem perguntar:

```
python thero.py --install-command meunome
```

Instalar o comando de atalho restrito à pasta do projeto atual (não mexe
no `$PROFILE` global):

```
python thero.py --install-command --local
```

Indexar a arquitetura do projeto atual com a Athena (se instalada):

```
python thero.py --index
```

Ver se alguma skill tem atualização, e atualizar:

```
python thero.py --check
python thero.py --update
```

Ver a ajuda (não instala nada, não modifica nada, não chama o Claude):

```
python thero.py --help
python thero.py -h
```

## Fluxo recomendado

1. Rode `python thero.py` (ou `--skills-only` seguido de `--merge-only`,
   se preferir controlar as etapas separadamente).
2. Reinicie o Claude Code e o PowerShell (ou `. $PROFILE`) para carregar
   as skills, o `CLAUDE.md` e o comando `thero`.
3. Ao trabalhar em um projeto específico, rode `thero audit-only`
   (ou `python thero.py --audit-only`) dentro do projeto para gerar
   `CLAUDE_AUDIT.md` (somente leitura, nada é alterado).
4. Leia o `CLAUDE_AUDIT.md`.
5. Corrija primeiro os achados `CRITICAL`, depois `BUG`, depois `RISK`.
6. Rode novamente typecheck/lint/testes.
7. Revise o `git diff`.
8. Só então considere itens de `MAINTENANCE`.
9. Trate itens de `IMPROVEMENT` como opcionais.

Um prompt útil para a etapa de correção, usado com o próprio Claude Code:

```
Read CLAUDE_AUDIT.md and correct the CRITICAL, BUG and RISK
findings that are supported by the current code. Do not perform
unrelated refactors. Verify every correction.
```

## Comando de atalho (PowerShell)

O `thero` instala um comando de atalho (`thero` por padrão) que roda o
script a partir de qualquer pasta, usando a pasta atual como alvo
(equivalente a rodar `python thero.py --audit` etc. de dentro daquele
projeto).

**Global** (padrão, sem `--local`): cria/atualiza uma função no seu
`$PROFILE` do PowerShell (Windows) ou em `~/.zshrc` / `~/.bashrc` /
`~/.profile` (macOS/Linux, detectado via `$SHELL`). Funciona em
qualquer pasta, em qualquer sessão, depois de recarregar o terminal
(`. $PROFILE` / `source ~/.zshrc` ou abrir um novo).

```
thero              -> thero.py (instala tudo)
thero skills       -> --skills-only
thero merge        -> --merge-only
thero audit        -> --audit
thero audit-only   -> --audit-only
thero index        -> --index
thero check        -> --check
thero update       -> --update
thero help         -> --help
thero -h           -> repassado cru (qualquer flag não mapeada)
```

**Local** (`--install-command --local`): cria `<nome>.local.ps1`
(Windows) ou `<nome>.local.sh` (macOS/Linux) na pasta do projeto
atual, em vez de mexer no perfil global. Carregue na sessão com
`. .\thero.local.ps1` ou `source ./thero.local.sh`. A função só
executa se o diretório atual for aquele projeto (ou uma subpasta
dele); fora dali, recusa com erro. Cada chamada já roda o script com
`--local` (skills e CLAUDE.md também ficam locais ao projeto).

Rodar a instalação de novo (global ou local) atualiza a função existente
— não duplica, mesmo trocando de nome.

## Athena e Zeus

O `thero` pode se integrar com a [Athena](https://github.com/netovieira/athena)
(indexador recursivo de arquitetura via Claude Code) como parte do
fluxo de trabalho, não só como instalação:

- `thero --index` (ou `thero index`) roda `athena index .` na pasta
  atual. Ele procura a Athena numa pasta irmã `athena/` (layout padrão
  do monorepo `myscripts`) ou no caminho apontado pela variável de
  ambiente `THERO_ATHENA_PATH`; se não achar em nenhum dos dois, e o
  terminal for interativo, oferece clonar automaticamente
  (`git clone`) numa cópia gerenciada em `~/.thero/tools/athena` — e,
  se essa cópia já existir mas estiver desatualizada em relação ao
  remoto, oferece atualizá-la (`git pull`) antes de rodar. Requer
  `git` instalado; em sessão não interativa (ex.: agente de IA), pula
  o clone/update automático em vez de travar esperando confirmação.
- O `CLAUDE.md` que o `thero` gera/consolida já instrui o Claude a
  checar `.athena/summary.md` e `.athena/tree/**` antes de explorar um
  projeto desconhecido, usando os resumos como primeira fonte de
  contexto em vez de reler cada arquivo do zero (cai de volta pro
  arquivo real quando o resumo não é suficiente).

**Zeus** — um planejador que cruzaria o pedido do usuário com o índice
da Athena para decidir exatamente quais arquivos importam para uma
tarefa — está planejado, mas **ainda não foi implementado**. O
`CLAUDE.md` gerado já reconhece um `.claude/zeus-plan.md` opcional
como ponto de partida, para quando o Zeus existir.

## Skills

As skills são instaladas individualmente (uma chamada `npx skills add`
por skill), para que a falta ou renomeação de uma skill não interrompa a
instalação das demais. Sem `--local`, instalam em `~/.claude/skills`
(`--global` no `npx skills add`); com `--local`, instalam em
`./.claude/skills` do projeto (sem `--global`). `impeccable` usa seu
próprio instalador (`npx impeccable install -y --force --providers=claude`,
sem prompts), fora desse mecanismo genérico. `--check`/`--update`
cobrem os dois mecanismos (`npx skills` e `impeccable`).

Ao final da instalação, o script gera automaticamente
`SKILLS_INSTALL_FAILED.md` — na pasta deste script (modo global) ou na
pasta do projeto (modo `--local`) — listando cada skill que falhou
(grupo, repositório, nome da skill e o comando `npx` usado). Se tudo
instalar com sucesso, esse arquivo é removido/não é criado. Envie o
conteúdo desse arquivo para o Claude corrigir os nomes de skills ou
repositórios desatualizados.

Grupos de skills instalados a partir de repositórios externos:

- **Engineering / Reasoning** (`darasoba/agent-skills`):
  `fable-reasoning`, `engineering-manager`
- **Supabase** (`supabase/agent-skills`):
  `supabase`, `supabase-postgres-best-practices`
- **React / Frontend** (`PyModel/react-frontend-skills`):
  `react`, `react-hooks`, `nextjs`, `typescript`, `tailwind`,
  `shadcn`, `ui-design`, `accessibility`, `performance`,
  `feature-architecture`, `vercel-react-best-practices`,
  `react-hook-form`, `zod`, `tanstack-query`, `vitest`, `playwright`,
  `msw`, `tdd`
- **Agents Inc** (`agents-inc/skills`):
  `typescript`, `react`, `nextjs`, `python`, `firebase`, `stripe`,
  `supabase`, `tailwind`, `mui`, `testing`, `security`,
  `code-review`, `performance`, `accessibility`
- **Caveman** (`JuliusBrussee/caveman`): `caveman`

Instalada à parte (não usa `npx skills add`):

- **impeccable** — `npx impeccable install`

## CLAUDE.md

O script nunca apaga o `CLAUDE.md` existente — `~/.claude/CLAUDE.md` por
padrão, ou `./CLAUDE.md` (na pasta do projeto) com `--local`. O fluxo de
consolidação é:

```
~/.claude/CLAUDE.md  (ou ./CLAUDE.md com --local)
        |
        v
backup com timestamp (CLAUDE.md.backup_<timestamp>.md)
        |
        v
Claude consolida (existente + Engineering Operating System)
        |
        v
validação do resultado (tamanho mínimo, sem markdown fences)
        |
        v
novo CLAUDE.md (substituição atômica via arquivo temporário)
```

Se o `CLAUDE.md` alvo ainda não existir, ele é criado diretamente a
partir do "Engineering Operating System" padrão, sem chamar o Claude.

Se a consolidação falhar (Claude indisponível, erro na chamada, saída
vazia ou validação reprovada), o arquivo original **permanece intacto**
e um aviso é impresso.

## Estrutura do projeto

```
thero/
├── thero.py                 # ponto de entrada (python thero.py ...)
├── src/thero/
│   ├── cli.py                # argparse + orquestração (main)
│   ├── settings.py           # paths e constantes globais
│   ├── domain/                # conteúdo/conhecimento (Engineering System)
│   ├── skills/                 # catálogo + instalador de Agent Skills
│   ├── claude_md/               # cliente `claude -p` + merge do CLAUDE.md
│   ├── audit/                    # auditoria de projeto (read-only)
│   ├── shell_command/             # comando de atalho (PowerShell + bash/zsh, global/local)
│   ├── integrations/               # ponte com ferramentas externas (Athena)
│   └── system/                      # processo, backup, ambiente
├── README.md
└── .gitignore
```

Cada pasta representa um contexto isolado (skills, CLAUDE.md, auditoria,
comando de atalho, infraestrutura de sistema), para facilitar manutenção
e crescimento sem acoplar regras de negócio diferentes no mesmo arquivo.

## Known issues

- O repositório `agents-inc/skills` atualmente falha para praticamente
  todas as skills listadas (0 instaladas em testes reais). Os demais
  repositórios funcionam parcialmente (algumas skills individuais podem
  ter sido renomeadas/removidas). Use `SKILLS_INSTALL_FAILED.md` para ver
  exatamente o que falhou.
- Comando de atalho (`--install-command`) no macOS/Linux é novo:
  validado via Git Bash no Windows (`bash -n` e execução real da
  função gerada), mas zsh/bash reais em macOS/Linux ainda não foram
  testados.

## Troubleshooting

**`[ERROR] node was not found`**
Instale o Node.js e garanta que `node` esteja no `PATH`.

**`[ERROR] npx was not found`**
Instale o Node.js (o `npx` normalmente já vem junto) e garanta que esteja
no `PATH`.

**`[WARN] claude was not found. Skill installation may still work.`**
A instalação de skills não depende do Claude Code. Esse aviso aparece no
fluxo padrão e em `--skills-only`; a consolidação do `CLAUDE.md` será
pulada até o Claude Code estar instalado e autenticado.

**`[ERROR] claude was not found` (com `--merge-only` ou `--audit-only`)**
Esses comandos exigem o Claude Code instalado e autenticado. Instale com
`npm install -g @anthropic-ai/claude-code` (ou o método oficial mais
recente) e rode `claude` uma vez para autenticar.

**`[WARN] Could not install <skill> from <repo>`**
A skill pode ter sido renomeada ou removida do repositório. As demais
skills continuam sendo instaladas normalmente; nenhuma ação manual é
necessária a menos que você precise especificamente dessa skill.

**`[ERROR] Claude returned an error.` / `[ERROR] Claude returned empty output.`**
Rode `claude -p "hello"` manualmente para confirmar que o CLI funciona e
está autenticado. Verifique conectividade e limites de uso.

**`[ERROR] Generated CLAUDE.md is suspiciously small.` / `... contains unexpected markdown fences.`**
A consolidação foi rejeitada por segurança. O `CLAUDE.md` original não
foi alterado. Rode `--merge-only` novamente; se persistir, revise
manualmente com `claude -p` fora do script.

**`[ERROR] Could not replace CLAUDE.md: ...`**
Falha ao substituir o arquivo (por exemplo, permissão de arquivo). O
`CLAUDE.md` original é preservado; verifique permissões em `~/.claude/`.

**`[ERROR] Could not resolve the PowerShell $PROFILE path`**
Só ocorre no Windows; rode o script em um PowerShell normal, não dentro
de outro shell ou ambiente restrito.

**`'thero' e um comando local do projeto '...'`**
Você tentou usar um comando instalado com `--install-command --local`
fora da pasta do projeto (ou de uma subpasta dela). Volte para essa
pasta, ou instale o comando global (sem `--local`) se quiser usá-lo de
qualquer lugar.

**Onde ficam os backups?**
Ao lado do arquivo original, com sufixo `.backup_<AAAAMMDD_HHMMSS>`
(ex.: `CLAUDE.md.backup_20260101_120000.md`). Nada é apagado
automaticamente.

**`--help` / `-h` não faz nada além de mostrar texto?**
Correto — por design, `--help`/`-h` nunca instala skills, nunca modifica
arquivos e nunca chama o Claude. É seguro rodar mesmo em uma máquina sem
Node.js ou Claude Code configurados.

## Autor

**Anthero Vieira Neto**

- E-mail: antherovn@gmail.com
- WhatsApp Business: +55 17 9210-1133
- LinkedIn: https://www.linkedin.com/in/anthero-vieira-neto-aa7a6b8a
- GitHub: http://github.com/netovieira
