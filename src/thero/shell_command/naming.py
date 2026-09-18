from __future__ import annotations

import sys


def prompt_command_name(
    default_name: str,
) -> str:

    if not sys.stdin.isatty():
        return default_name

    try:
        answer = input(
            f"Nome do comando global [{default_name}]: "
        ).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return default_name

    return answer or default_name
