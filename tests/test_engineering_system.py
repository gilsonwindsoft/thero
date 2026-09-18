from __future__ import annotations

from thero.domain.engineering_system import ENGINEERING_SYSTEM


def test_contains_expected_top_level_heading():
    assert "# Engineering Operating System" in ENGINEERING_SYSTEM


def test_is_reasonably_sized_content():
    # Light contract check, not a snapshot of the full text (plan
    # explicitly avoids pinning the entire static content).
    assert len(ENGINEERING_SYSTEM.strip()) > 500
