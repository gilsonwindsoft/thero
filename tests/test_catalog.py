from __future__ import annotations

from thero.skills.catalog import SKILL_REPOSITORIES


def test_each_repository_has_expected_shape():
    for repository in SKILL_REPOSITORIES:
        assert set(repository.keys()) == {"name", "repo", "wanted"}
        assert isinstance(repository["name"], str) and repository["name"]
        assert isinstance(repository["repo"], str) and "/" in repository["repo"]
        assert isinstance(repository["wanted"], list) and repository["wanted"]


def test_no_duplicate_skills_within_same_repo():
    for repository in SKILL_REPOSITORIES:
        wanted = repository["wanted"]
        assert len(wanted) == len(set(wanted))


def test_no_duplicate_repository_names():
    names = [repo["name"] for repo in SKILL_REPOSITORIES]
    assert len(names) == len(set(names))
