from __future__ import annotations

import argparse
import sys
from pathlib import Path

from thero.audit.auditor import audit_project, print_audit_workflow
from thero.claude_md.merger import merge_claude_md
from thero.integrations.athena_bridge import run_athena_index
from thero.reporting.summary import print_summary
from thero.settings import CLAUDE_DIR, DEFAULT_COMMAND_NAME, GLOBAL_CLAUDE_MD
from thero.shell_command.naming import prompt_command_name
from thero.shell_command.windows import install_global_command
from thero.skills.installer import check_skills, install_all_skills, update_skills
from thero.system.environment import ensure_claude_dir, validate_environment
from thero.system.process import command_exists

_HELP_EPILOG_TEMPLATE = r"""
REQUISITOS
    Python 3.10+
    Node.js / npx
    Claude Code instalado e autenticado
    (skills funcionam sem "claude"; merge/audit exigem "claude")
    Comando global exige Windows PowerShell

COMANDOS
    (sem argumentos)   Fluxo completo: instala skills, consolida
                       o CLAUDE.md global e instala/atualiza o
                       comando global "%s".
    --skills-only      Instala apenas as skills, sem tocar no
                       CLAUDE.md nem no comando global.
    --merge-only       Consolida apenas o CLAUDE.md global.
    --audit-only       Audita o projeto atual (somente leitura),
                       sem instalar nada.
    --audit            Executa o fluxo completo (inclui o comando
                       global) e, em seguida, audita o projeto
                       atual.
    --install-command [NOME]
                       Instala/atualiza somente o comando (global
                       ou local, ver --local) no PowerShell
                       (padrao: "%s"), sem mexer em skills nem no
                       CLAUDE.md.
    --index            Roda a Athena (indexador de arquitetura,
                       github.com/netovieira/athena) na pasta
                       atual, se estiver instalada. Nao instala
                       skills, nem mexe no CLAUDE.md/comando.
    --check            Verifica se alguma skill instalada (via
                       "npx skills" e "impeccable") tem atualizacao
                       disponivel. Nao instala nem muda nada.
    --update           Atualiza as skills instaladas (via
                       "npx skills" e "impeccable") para a versao
                       mais recente. Nao mexe no CLAUDE.md nem no
                       comando.
    --local            Opera na pasta do projeto atual em vez do
                       usuario global: CLAUDE.md vira ./CLAUDE.md
                       (nao ~/.claude/CLAUDE.md), skills instalam
                       em ./.claude/skills (nao ~/.claude/skills),
                       e --install-command cria um comando restrito
                       a esta pasta (ver secao COMANDO LOCAL).
                       Combina com qualquer outra flag.
    -h, --help         Mostra esta ajuda e sai (exit code 0), sem
                       instalar nada, sem modificar arquivos e sem
                       chamar o Claude.

EXEMPLOS
    python thero.py
    python thero.py --local
    python thero.py --skills-only
    python thero.py --skills-only --local
    python thero.py --merge-only
    python thero.py --audit-only
    python thero.py --audit
    python thero.py --install-command
    python thero.py --install-command meunome
    python thero.py --index
    python thero.py --check
    python thero.py --update
    python thero.py --help

FLUXO RECOMENDADO
    1. python thero.py
    2. Reinicie o Claude Code e o PowerShell (ou ". $PROFILE").
    3. Dentro do projeto: "%s audit-only" (equivale a
       "python thero.py --audit-only", rodando na pasta
       atual, nao na pasta deste script).
    4. Leia o CLAUDE_AUDIT.md gerado.
    5. Corrija CRITICAL, depois BUG, depois RISK.
    6. Rode typecheck/lint/testes novamente.
    7. Revise o git diff.
    8. Só então considere MAINTENANCE; trate IMPROVEMENT como
       opcional.

COMANDO GLOBAL (PowerShell)
    O fluxo padrao (sem flags) e o --audit ja instalam/atualizam
    a funcao "%s" no seu $PROFILE do PowerShell. Ela roda este
    script a partir de QUALQUER pasta, usando o diretorio atual
    (nao a pasta deste script):
        %s              -> instala tudo (skills + CLAUDE.md +
                            comando global)
        %s skills       -> --skills-only
        %s merge        -> --merge-only
        %s audit        -> --audit
        %s audit-only   -> --audit-only
        %s index        -> --index
        %s check        -> --check
        %s update       -> --update
        %s help         -> --help
    Qualquer outro argumento (ex.: "%s -h") e repassado cru para
    o script. Rodar a instalacao de novo so atualiza a funcao
    existente (nao duplica); requer reiniciar o terminal ou
    ". $PROFILE" para valer na sessao atual.

COMANDO LOCAL (--install-command --local)
    Em vez de mexer no $PROFILE global, cria "<nome>.local.ps1"
    na pasta do projeto atual. Carregue na sessao com:
        . .\<nome>.local.ps1
    A funcao so executa se o diretorio atual for aquele projeto
    (ou uma subpasta dele); fora dali, recusa com erro. Cada
    chamada ja inclui "--local" ao rodar o script (skills e
    CLAUDE.md tambem ficam locais ao projeto). So funciona no
    Windows por enquanto (macOS/Linux: planejado).

ATHENA (--index)
    A Athena (github.com/netovieira/athena) indexa a arquitetura do
    projeto atual em ./.athena, resumindo arquivos e pastas via
    Claude. "--index" so roda se ela estiver instalada: procura
    athena.py na pasta irma "athena/" (layout padrao do monorepo
    myscripts) ou no caminho apontado pela variavel de ambiente
    THERO_ATHENA_PATH. O CLAUDE.md gerado pelo thero ja instrui o
    Claude a consultar esse indice quando existir, em vez de reler
    cada arquivo do zero. Zeus (planejador que cruza o pedido do
    usuario com o indice da Athena) ainda nao foi implementado.

SKILLS
    Skills sao instaladas individualmente a partir de repositorios
    externos (Engineering/Reasoning, Supabase, React/Frontend,
    Agents Inc, Caveman); a falha em uma skill nao interrompe as
    demais. "impeccable" usa seu proprio instalador
    ("npx impeccable install"), fora do CLI generico de skills. Ao
    final, o que falhou fica listado em SKILLS_INSTALL_FAILED.md
    (mesma pasta deste script; com --local, na pasta do projeto)
    para envio ao Claude. Sem --local instala em ~/.claude/skills;
    com --local, em ./.claude/skills do projeto. Use --check para
    ver se ha atualizacoes e --update para aplica-las (cobre tanto
    o CLI generico de skills quanto "impeccable").

CLAUDE.md
    O CLAUDE.md alvo (~/.claude/CLAUDE.md, ou ./CLAUDE.md com
    --local) nunca e apagado. Fluxo: backup com timestamp ->
    Claude consolida o conteudo existente com o novo Engineering
    Operating System -> validacao (tamanho minimo, sem markdown
    fences) -> substituicao atomica. Se qualquer etapa falhar, o
    arquivo original permanece intacto.

TROUBLESHOOTING
    [ERROR] node/npx was not found
        Instale o Node.js e garanta que estejam no PATH.
    [WARN] claude was not found
        Instalacao de skills ainda funciona; merge/audit exigem o
        Claude Code instalado e autenticado.
    [WARN] Could not install <skill> from <repo>
        Skill pode ter sido renomeada/removida; as demais
        continuam normalmente.
    [ERROR] Claude returned an error / empty output
        Rode "claude -p \"hello\"" manualmente para checar CLI e
        autenticacao.
    [ERROR] Generated CLAUDE.md is suspiciously small / contains
    unexpected markdown fences
        Consolidacao rejeitada por seguranca; CLAUDE.md original
        nao foi alterado.
    Backups ficam ao lado do arquivo original, com sufixo
    ".backup_<AAAAMMDD_HHMMSS>".
    [ERROR] Could not resolve the PowerShell $PROFILE path
        Comando global so suporta Windows PowerShell; rode o
        script em um PowerShell normal (nao dentro de outro
        shell ou ambiente restrito).
    Nome do comando global pedido interativamente?
        Isso so acontece em terminal interativo (TTY). Em modo
        nao interativo (ex.: automacao/CI) o nome sugerido
        ("%s") e usado direto, sem travar esperando entrada.

Documentacao completa: README.md (mesma pasta deste script).
"""

HELP_EPILOG = _HELP_EPILOG_TEMPLATE % (
    (DEFAULT_COMMAND_NAME,) * 15
)


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "Configure Claude Code for "
            "professional software engineering."
        ),
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--skills-only",
        action="store_true",
        help=(
            "Install skills without changing CLAUDE.md."
        ),
    )

    parser.add_argument(
        "--merge-only",
        action="store_true",
        help=(
            "Only consolidate the global CLAUDE.md."
        ),
    )

    parser.add_argument(
        "--audit",
        action="store_true",
        help=(
            "Install/configure everything and then "
            "audit the current project."
        ),
    )

    parser.add_argument(
        "--audit-only",
        action="store_true",
        help=(
            "Only audit the current project."
        ),
    )

    parser.add_argument(
        "--install-command",
        nargs="?",
        const="",
        default=None,
        metavar="NAME",
        help=(
            "Install/update only the PowerShell command that "
            "runs this script, e.g. "
            f"'{DEFAULT_COMMAND_NAME} audit'. Does not "
            "install skills or touch CLAUDE.md. If NAME is "
            "omitted, prompts interactively for a name "
            f"(default suggestion: '{DEFAULT_COMMAND_NAME}'"
            "). Note: the default run (no flags) and --audit "
            "already install this command automatically, also "
            "prompting for a name. Combine with --local to "
            "install a project-scoped command instead of a "
            "global one."
        ),
    )

    parser.add_argument(
        "--local",
        action="store_true",
        help=(
            "Operate on the current project folder instead of "
            "the global user configuration: CLAUDE.md goes to "
            "./CLAUDE.md (not ~/.claude/CLAUDE.md), skills "
            "install into ./.claude/skills (not ~/.claude/skills), "
            "and --install-command creates a command scoped to "
            "this project folder instead of a global one. Without "
            "this flag, everything targets the global user config "
            "(current/default behavior)."
        ),
    )

    parser.add_argument(
        "--index",
        action="store_true",
        help=(
            "Run Athena (https://github.com/netovieira/athena) to "
            "index the current project's architecture into "
            "./.athena, if Athena is installed. Does not install "
            "skills, touch CLAUDE.md, or manage the shortcut "
            "command."
        ),
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Check whether any installed skill has an update "
            "available (runs 'npx skills check' and "
            "'npx impeccable check'). Does not install or change "
            "anything."
        ),
    )

    parser.add_argument(
        "--update",
        action="store_true",
        help=(
            "Update installed skills to their latest version (runs "
            "'npx skills update' and 'npx impeccable update'). Does "
            "not touch CLAUDE.md or the shortcut command."
        ),
    )

    return parser.parse_args()


def main(entry_path: Path) -> None:

    args = parse_args()

    print("=" * 70)
    print(" Claude Code Engineering Stack Installer")
    print("=" * 70)

    if args.local:
        print()
        print(
            "[INFO] --local: operating on the current project "
            f"folder ({Path.cwd()}), not the global user config."
        )

    # --------------------------------------------------------
    # Targets: global (~/.claude) vs local (project folder)
    # --------------------------------------------------------

    if args.local:
        claude_dir = Path.cwd() / ".claude"
        claude_md_path = Path.cwd() / "CLAUDE.md"
        global_install = False
    else:
        claude_dir = CLAUDE_DIR
        claude_md_path = GLOBAL_CLAUDE_MD
        global_install = True

    # --------------------------------------------------------
    # Athena (indexação de arquitetura)
    # --------------------------------------------------------

    if args.index:

        if not run_athena_index(entry_path):
            sys.exit(1)

        return

    # --------------------------------------------------------
    # Check / update skills
    # --------------------------------------------------------

    if args.check:

        if not validate_environment(require_claude=False):
            sys.exit(1)

        if not check_skills(global_install):
            sys.exit(1)

        return

    if args.update:

        if not validate_environment(require_claude=False):
            sys.exit(1)

        if not update_skills(global_install):
            sys.exit(1)

        return

    # --------------------------------------------------------
    # Install command (global or local)
    # --------------------------------------------------------

    if args.install_command is not None:

        command_name = args.install_command or prompt_command_name(
            DEFAULT_COMMAND_NAME
        )

        install_global_command(
            command_name,
            entry_path,
            local=args.local,
        )

        return

    # --------------------------------------------------------
    # Audit only
    # --------------------------------------------------------

    if args.audit_only:

        if not validate_environment(
            require_claude=True
        ):
            sys.exit(1)

        audit_project()
        print_audit_workflow()

        return

    # --------------------------------------------------------
    # Merge only
    # --------------------------------------------------------

    if args.merge_only:

        if not validate_environment(
            require_claude=True
        ):
            sys.exit(1)

        ensure_claude_dir(claude_dir)
        merge_claude_md(claude_md_path)

        return

    # --------------------------------------------------------
    # Normal environment
    # --------------------------------------------------------

    if not validate_environment(
        require_claude=False
    ):
        sys.exit(1)

    ensure_claude_dir(claude_dir)

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    if not args.merge_only:

        install_all_skills(entry_path, global_install)

    # --------------------------------------------------------
    # CLAUDE.md
    # --------------------------------------------------------

    if not args.skills_only:

        if not command_exists("claude"):

            print()
            print(
                "[WARN] Claude Code is not available."
            )

            print(
                "[WARN] Skills may have been installed, "
                "but CLAUDE.md could not be consolidated."
            )

        else:

            merge_claude_md(claude_md_path)

    # --------------------------------------------------------
    # Global/local command
    #
    # Só roda no fluxo completo (não em --skills-only), como
    # parte de "instalar tudo".
    # --------------------------------------------------------

    if not args.skills_only:

        global_command_name = prompt_command_name(
            DEFAULT_COMMAND_NAME
        )

        install_global_command(
            global_command_name,
            entry_path,
            local=args.local,
        )

    # --------------------------------------------------------
    # Audit
    # --------------------------------------------------------

    if args.audit:

        audit_project()
        print_audit_workflow()

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print_summary(claude_md_path)
