from __future__ import annotations

from thero.skills.discovery import discover_repo_skills


def test_discover_repo_skills_always_returns_empty_set():
    assert discover_repo_skills("any/repo") == set()
