from __future__ import annotations

from pathlib import Path

from thero.settings import GLOBAL_CLAUDE_MD


def print_summary(
    claude_md_path: Path = GLOBAL_CLAUDE_MD,
) -> None:

    print()
    print("=" * 70)
    print(" Claude Code Engineering Stack")
    print("=" * 70)

    print(
        """
GLOBAL BEHAVIOR
  - request fidelity
  - inspect before editing
  - proportional planning
  - minimal diffs
  - evidence-based debugging
  - security
  - verification
  - final diff review

FRONTEND
  - TypeScript
  - React
  - Next.js
  - Tailwind
  - UI/UX
  - accessibility
  - performance
  - forms
  - validation
  - testing

BACKEND
  - Python
  - Supabase
  - PostgreSQL
  - Firebase
  - Stripe

QUALITY
  - type checking
  - lint
  - unit tests
  - integration tests
  - E2E
  - code review

EXISTING
  - Caveman preserved
  - Impeccable preserved

TOKEN STRATEGY
  - keep CLAUDE.md small
  - technology knowledge lives in skills
  - inspect only relevant context
  - targeted verification
  - avoid speculative refactors
"""
    )

    print(
        f"CLAUDE.md:"
        f"\n  {claude_md_path}"
    )

    print(
        "\nRestart Claude Code before starting a new session."
    )
