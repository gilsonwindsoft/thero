from __future__ import annotations

import os
from pathlib import Path

from thero.settings import COMMAND_MARKER_END, COMMAND_MARKER_START


def upsert_marked_block(
    existing: str,
    block: str,
) -> str:
    """
    Insere "block" (delimitado por COMMAND_MARKER_START/END) dentro
    de "existing", substituindo um bloco anterior com os mesmos
    marcadores em vez de duplicar.
    """

    block = block.strip("\n") + "\n"

    if (
        COMMAND_MARKER_START in existing
        and COMMAND_MARKER_END in existing
    ):
        start_index = existing.index(COMMAND_MARKER_START)
        end_index = existing.index(
            COMMAND_MARKER_END
        ) + len(COMMAND_MARKER_END)

        return (
            existing[:start_index]
            + block
            + existing[end_index:].lstrip("\n")
        )

    separator = "\n\n" if existing.strip() else ""

    return (
        existing.rstrip("\n") + separator + block
        if existing.strip()
        else block
    )


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

    if os.name == "nt":
        from thero.shell_command.windows import (
            install_global_command_windows,
            install_local_command_windows,
        )

        if local:
            install_local_command_windows(command_name, entry_path)
        else:
            install_global_command_windows(command_name, entry_path)
    else:
        from thero.shell_command.posix import (
            install_global_command_posix,
            install_local_command_posix,
        )

        if local:
            install_local_command_posix(command_name, entry_path)
        else:
            install_global_command_posix(command_name, entry_path)
