from __future__ import annotations

import os
from pathlib import Path

from thero.shell_command import upsert_marked_block
from thero.shell_command.templates import (
    GLOBAL_COMMAND_TEMPLATE_POSIX,
    LOCAL_COMMAND_TEMPLATE_POSIX,
)
from thero.system.backup import backup_file

POSIX_SUPPORT_WARNING = (
    "[WARN] Suporte a macOS/Linux e novo e foi validado via Git Bash "
    "no Windows; zsh/bash reais em macOS/Linux ainda nao foram "
    "testados. Reporte problemas se encontrar algum."
)


def resolve_shell_rc_file() -> Path:
    """
    Escolhe o arquivo de perfil do shell a editar, com base na
    variavel de ambiente $SHELL. Sem match conhecido (zsh/bash),
    usa ~/.profile (criado se ainda nao existir).
    """

    shell = os.environ.get("SHELL", "")

    if "zsh" in shell:
        return Path.home() / ".zshrc"

    if "bash" in shell:
        return Path.home() / ".bashrc"

    return Path.home() / ".profile"


def install_local_command_posix(
    command_name: str,
    entry_path: Path,
) -> None:

    project_dir = Path.cwd().resolve()
    target = project_dir / f"{command_name}.local.sh"

    if target.exists():
        backup_file(
            target,
            prefix=target.stem,
        )

    content = LOCAL_COMMAND_TEMPLATE_POSIX % {
        "project_dir": str(project_dir),
        "local_filename": target.name,
        "command_name": command_name,
        "script_path": str(entry_path),
    }

    # Force LF newlines: this is a POSIX shell script and a CRLF terminator
    # breaks bash ("syntax error near unexpected token `$'{\r'`") when thero
    # is run under Git Bash on Windows. write_text() would otherwise emit the
    # host os.linesep.
    target.write_text(
        content,
        encoding="utf-8",
        newline="\n",
    )

    print(
        f"[OK] Local command '{command_name}' created at:"
    )
    print(
        f"     {target}"
    )
    print()
    print(
        "Load it in your current shell session with:"
    )
    print(
        f"    source ./{target.name}"
    )
    print()
    print("Usage (only works inside this project's folder):")
    print(
        f"    {command_name}              "
        "-> full local install (skills + CLAUDE.md)"
    )
    print(
        f"    {command_name} skills       -> --skills-only --local"
    )
    print(
        f"    {command_name} merge        -> --merge-only --local"
    )
    print(
        f"    {command_name} audit        -> --audit --local"
    )
    print(
        f"    {command_name} audit-only   -> --audit-only --local"
    )
    print(
        f"    {command_name} help         -> --help"
    )
    print(
        f"\nValid only in: {project_dir}"
    )
    print()
    print(POSIX_SUPPORT_WARNING)


def install_global_command_posix(
    command_name: str,
    entry_path: Path,
) -> None:

    rc_path = resolve_shell_rc_file()

    rc_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if rc_path.exists():
        backup_file(
            rc_path,
            prefix=rc_path.stem,
        )
        existing = rc_path.read_text(
            encoding="utf-8",
            errors="replace",
        )
    else:
        existing = ""

    block = GLOBAL_COMMAND_TEMPLATE_POSIX % (
        command_name,
        str(entry_path),
    )

    updated = upsert_marked_block(existing, block)

    rc_path.write_text(
        updated,
        encoding="utf-8",
        newline="\n",
    )

    print(
        f"[OK] Global command '{command_name}' installed in:"
    )
    print(
        f"     {rc_path}"
    )
    print()
    print(
        "Reload your shell session to use it now:"
    )
    print(
        f"    source {rc_path}"
    )
    print(
        "(or just open a new terminal window)"
    )
    print()
    print("Usage:")
    print(
        f"    {command_name}              "
        "-> full install (skills + CLAUDE.md)"
    )
    print(
        f"    {command_name} skills       -> --skills-only"
    )
    print(
        f"    {command_name} merge        -> --merge-only"
    )
    print(
        f"    {command_name} audit        -> --audit"
    )
    print(
        f"    {command_name} audit-only   -> --audit-only"
    )
    print(
        f"    {command_name} help         -> --help"
    )
    print(
        "\nRuns against the directory you are currently in, "
        "not the thero.py folder."
    )
    print()
    print(POSIX_SUPPORT_WARNING)
