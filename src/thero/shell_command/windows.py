from __future__ import annotations

import os
from pathlib import Path

from thero.settings import COMMAND_MARKER_END, COMMAND_MARKER_START
from thero.shell_command.templates import (
    GLOBAL_COMMAND_TEMPLATE,
    LOCAL_COMMAND_TEMPLATE,
)
from thero.system.backup import backup_file
from thero.system.process import run_command


def resolve_powershell_profile() -> Path | None:

    result = run_command(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "$PROFILE",
        ],
        capture=True,
    )

    if result.returncode != 0:
        return None

    output = (result.stdout or "").strip()

    if not output:
        return None

    return Path(output)


def install_global_command(
    command_name: str,
    entry_path: Path,
    local: bool = False,
) -> None:

    print()
    print("=" * 70)
    print(
        "Local command" if local else "Global command"
    )
    print("=" * 70)

    if os.name != "nt":
        print(
            "[ERROR] Command installation currently supports "
            "Windows PowerShell only."
        )
        return

    if local:
        install_local_command_windows(command_name, entry_path)
    else:
        install_global_command_windows(command_name, entry_path)


def install_local_command_windows(
    command_name: str,
    entry_path: Path,
) -> None:

    project_dir = Path.cwd().resolve()
    target = project_dir / f"{command_name}.local.ps1"

    if target.exists():
        backup_file(
            target,
            prefix=target.stem,
        )

    script_path = str(entry_path)

    content = LOCAL_COMMAND_TEMPLATE % {
        "project_dir": str(project_dir),
        "local_filename": target.name,
        "command_name": command_name,
        "script_path": script_path,
    }

    target.write_text(
        content,
        encoding="utf-8",
    )

    print(
        f"[OK] Local command '{command_name}' created at:"
    )
    print(
        f"     {target}"
    )
    print()
    print(
        "Load it in your current PowerShell session with:"
    )
    print(
        f"    . .\\{target.name}"
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


def install_global_command_windows(
    command_name: str,
    entry_path: Path,
) -> None:

    profile_path = resolve_powershell_profile()

    if profile_path is None:
        print(
            "[ERROR] Could not resolve the PowerShell "
            "$PROFILE path."
        )
        return

    profile_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if profile_path.exists():
        backup_file(
            profile_path,
            prefix=profile_path.stem,
        )
        existing = profile_path.read_text(
            encoding="utf-8",
            errors="replace",
        )
    else:
        existing = ""

    script_path = str(entry_path)

    block = GLOBAL_COMMAND_TEMPLATE % (
        command_name,
        script_path,
    )
    block = block.strip("\n") + "\n"

    if (
        COMMAND_MARKER_START in existing
        and COMMAND_MARKER_END in existing
    ):
        start_index = existing.index(COMMAND_MARKER_START)
        end_index = existing.index(
            COMMAND_MARKER_END
        ) + len(COMMAND_MARKER_END)

        updated = (
            existing[:start_index]
            + block
            + existing[end_index:].lstrip("\n")
        )
    else:
        separator = "\n\n" if existing.strip() else ""
        updated = (
            existing.rstrip("\n") + separator + block
            if existing.strip()
            else block
        )

    profile_path.write_text(
        updated,
        encoding="utf-8",
    )

    print(
        f"[OK] Global command '{command_name}' installed in:"
    )
    print(
        f"     {profile_path}"
    )
    print()
    print(
        "Reload your PowerShell session to use it now:"
    )
    print(
        "    . $PROFILE"
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
