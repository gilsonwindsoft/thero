from __future__ import annotations

import os
from pathlib import Path

from thero.claude_md.claude_client import call_claude
from thero.claude_md.merge_prompt import MERGE_PROMPT
from thero.domain.engineering_system import ENGINEERING_SYSTEM
from thero.settings import BACKUP_PREFIX, GLOBAL_CLAUDE_MD
from thero.system.backup import backup_file
from thero.system.environment import ensure_claude_dir
from thero.system.process import timestamp


def validate_merged_claude_md(
    content: str,
) -> bool:

    stripped = content.strip()

    if len(stripped) < 500:
        print(
            "[ERROR] Generated CLAUDE.md is suspiciously small."
        )
        return False

    # Evita que uma resposta acidental venha embrulhada em
    # markdown fence.
    if stripped.startswith("```"):
        print(
            "[ERROR] Generated CLAUDE.md contains "
            "unexpected markdown fences."
        )
        return False

    return True


def merge_claude_md(
    claude_md_path: Path = GLOBAL_CLAUDE_MD,
) -> None:

    ensure_claude_dir(
        claude_md_path.parent
    )

    if not claude_md_path.exists():

        print()
        print(
            f"[INFO] No existing CLAUDE.md found at "
            f"{claude_md_path}."
        )

        claude_md_path.write_text(
            ENGINEERING_SYSTEM.strip()
            + "\n",
            encoding="utf-8",
        )

        print(
            f"[OK] Created {claude_md_path}"
        )

        return

    # --------------------------------------------------------
    # Backup
    # --------------------------------------------------------

    backup_file(
        claude_md_path,
        prefix=BACKUP_PREFIX,
    )

    existing = claude_md_path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    print()
    print("=" * 70)
    print("Consolidating CLAUDE.md with Claude")
    print("=" * 70)

    prompt = MERGE_PROMPT.format(
        existing=existing,
        new_rules=ENGINEERING_SYSTEM,
    )

    merged = call_claude(
        prompt
    )

    if merged is None:

        print(
            "[WARN] Merge failed."
        )
        print(
            "[WARN] Existing CLAUDE.md was NOT changed."
        )

        return

    if not validate_merged_claude_md(
        merged
    ):

        print(
            "[WARN] Validation failed."
        )
        print(
            "[WARN] Existing CLAUDE.md was NOT changed."
        )

        return

    # --------------------------------------------------------
    # Atomic-ish replacement:
    #
    # escreve primeiro um arquivo temporário no mesmo diretório
    # e depois substitui.
    # --------------------------------------------------------

    temporary = claude_md_path.with_name(
        f".CLAUDE.md.tmp_{timestamp()}"
    )

    try:

        temporary.write_text(
            merged.rstrip()
            + "\n",
            encoding="utf-8",
        )

        os.replace(
            temporary,
            claude_md_path,
        )

    except Exception as exc:

        print(
            f"[ERROR] Could not replace CLAUDE.md: {exc}"
        )

        if temporary.exists():
            temporary.unlink()

        print(
            "[WARN] Original CLAUDE.md remains unchanged."
        )

        return

    print(
        "[OK] CLAUDE.md successfully consolidated."
    )
