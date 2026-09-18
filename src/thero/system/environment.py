from __future__ import annotations

from pathlib import Path

from thero.settings import CLAUDE_DIR
from thero.system.process import command_exists


def validate_environment(
    require_claude: bool = False,
) -> bool:

    print()
    print("=" * 70)
    print("Environment")
    print("=" * 70)

    valid = True

    if command_exists("node"):
        print("[OK] node")
    else:
        print("[ERROR] node was not found")
        valid = False

    if command_exists("npx"):
        print("[OK] npx")
    else:
        print("[ERROR] npx was not found")
        valid = False

    if command_exists("claude"):
        print("[OK] claude")
    else:
        if require_claude:
            print("[ERROR] claude was not found")
            valid = False
        else:
            print(
                "[WARN] claude was not found."
                "\n       Skill installation may still work."
            )

    return valid


def ensure_claude_dir(
    claude_dir: Path = CLAUDE_DIR,
) -> None:

    claude_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"[OK] Claude directory: {claude_dir}"
    )
