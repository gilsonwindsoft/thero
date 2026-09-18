from __future__ import annotations

from pathlib import Path

from thero.audit.audit_prompt import AUDIT_PROMPT
from thero.claude_md.claude_client import call_claude
from thero.settings import AUDIT_FILENAME
from thero.system.backup import backup_file
from thero.system.process import command_exists


def audit_project() -> None:

    if not command_exists("claude"):

        print(
            "[ERROR] Claude Code executable not found."
        )

        return

    project = Path.cwd()

    print()
    print("=" * 70)
    print("PROJECT AUDIT")
    print("=" * 70)

    print(
        f"Project: {project}"
    )

    print()
    print(
        "The first pass is READ-ONLY."
    )

    print(
        "Claude will not modify source code."
    )

    print()

    audit = call_claude(
        AUDIT_PROMPT,
        cwd=project,
    )

    if audit is None:
        return

    audit_path = project / AUDIT_FILENAME

    # --------------------------------------------------------
    # Não sobrescreve auditoria anterior.
    # --------------------------------------------------------

    if audit_path.exists():

        backup_file(
            audit_path,
            prefix="CLAUDE_AUDIT",
        )

    audit_path.write_text(
        audit.rstrip()
        + "\n",
        encoding="utf-8",
    )

    print()
    print(
        "=" * 70
    )

    print(
        f"[OK] Audit saved to:"
    )

    print(
        audit_path
    )

    print(
        "=" * 70
    )


def print_audit_workflow() -> None:

    print(
        """
After reviewing CLAUDE_AUDIT.md, use Claude Code with a controlled
correction request.

Recommended workflow:

    1. Read CLAUDE_AUDIT.md
    2. Correct CRITICAL
    3. Correct BUG
    4. Correct RISK
    5. Re-run typecheck/lint/tests
    6. Review git diff
    7. Only then consider MAINTENANCE
    8. Treat IMPROVEMENT as optional

A useful prompt is:

    "Read CLAUDE_AUDIT.md and correct the CRITICAL, BUG and RISK
    findings that are supported by the current code. Do not perform
    unrelated refactors. Verify every correction."
"""
    )
