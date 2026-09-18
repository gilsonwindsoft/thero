from __future__ import annotations

import os
import sys
from pathlib import Path

from thero.system.process import run_command

ATHENA_PATH_ENV_VAR = "THERO_ATHENA_PATH"


def find_athena_script(entry_path: Path) -> Path | None:
    """
    Localiza o athena.py. Ordem:

    1. Variável de ambiente THERO_ATHENA_PATH (caminho explícito
       para o athena.py).
    2. Pasta irmã "athena/athena.py", assumindo o layout padrão do
       monorepo myscripts (thero/ e athena/ lado a lado).
    """

    env_path = os.environ.get(ATHENA_PATH_ENV_VAR)

    if env_path:
        candidate = Path(env_path).expanduser()
        return candidate if candidate.is_file() else None

    sibling = entry_path.parent.parent / "athena" / "athena.py"

    return sibling if sibling.is_file() else None


def run_athena_index(entry_path: Path) -> bool:

    print()
    print("=" * 70)
    print("Athena — indexação de arquitetura")
    print("=" * 70)

    athena_script = find_athena_script(entry_path)

    if athena_script is None:
        print(
            "[ERROR] athena.py não encontrado. Instale a Athena "
            "(https://github.com/netovieira/athena) na pasta "
            "irmã de thero (ex.: ~/.myscripts/athena), ou defina "
            f"a variável de ambiente {ATHENA_PATH_ENV_VAR} apontando "
            "para o athena.py."
        )
        return False

    project_dir = str(Path.cwd())

    sys.stdout.flush()

    result = run_command(
        [
            "python",
            str(athena_script),
            "index",
            project_dir,
        ],
        capture=False,
    )

    return result.returncode == 0
