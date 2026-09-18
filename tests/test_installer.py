from __future__ import annotations

from unittest.mock import MagicMock, patch

from thero.skills.installer import (
    build_impeccable_install_command,
    build_skill_install_command,
    build_skills_check_command,
    build_skills_update_command,
    check_skills,
    install_all_skills,
    install_impeccable,
    install_repository_skills,
    install_single_skill,
    update_skills,
    write_failed_skills_report,
)


def test_build_skill_install_command_global():
    command = build_skill_install_command("org/repo", "myskill", global_install=True)

    assert command == [
        "npx", "skills", "add", "org/repo", "--skill", "myskill",
        "--agent", "claude-code", "--global", "--yes",
    ]


def test_build_skill_install_command_project():
    command = build_skill_install_command("org/repo", "myskill", global_install=False)

    assert "--global" not in command
    assert command[-1] == "--yes"


def test_build_impeccable_install_command_global():
    command = build_impeccable_install_command(global_install=True)

    assert command == [
        "npx", "impeccable", "install", "-y", "--force",
        "--providers=claude", "--global",
    ]


def test_build_impeccable_install_command_project():
    command = build_impeccable_install_command(global_install=False)

    assert command[-1] == "--project"


def test_build_skills_check_command():
    assert build_skills_check_command(True) == ["npx", "skills", "check", "--global"]
    assert build_skills_check_command(False) == ["npx", "skills", "check"]


def test_build_skills_update_command():
    assert build_skills_update_command(True) == ["npx", "skills", "update", "--global"]
    assert build_skills_update_command(False) == ["npx", "skills", "update"]


def test_install_single_skill_success():
    with patch(
        "thero.skills.installer.run_command",
        return_value=MagicMock(returncode=0),
    ):
        assert install_single_skill("org/repo", "myskill") is True


def test_install_single_skill_failure():
    with patch(
        "thero.skills.installer.run_command",
        return_value=MagicMock(returncode=1),
    ):
        assert install_single_skill("org/repo", "myskill") is False


def test_install_repository_skills_partial_failure_reports_failed():
    repository = {"name": "Group", "repo": "org/repo", "wanted": ["a", "b"]}

    with patch(
        "thero.skills.installer.run_command",
        side_effect=[
            MagicMock(returncode=0),
            MagicMock(returncode=1),
        ],
    ):
        failed = install_repository_skills(repository)

    assert len(failed) == 1
    assert failed[0]["skill"] == "b"
    assert failed[0]["group"] == "Group"


def test_install_repository_skills_all_succeed():
    repository = {"name": "Group", "repo": "org/repo", "wanted": ["a", "b"]}

    with patch(
        "thero.skills.installer.run_command",
        return_value=MagicMock(returncode=0),
    ):
        failed = install_repository_skills(repository)

    assert failed == []


def test_install_impeccable_success_returns_none():
    with patch(
        "thero.skills.installer.run_command",
        return_value=MagicMock(returncode=0),
    ):
        assert install_impeccable() is None


def test_install_impeccable_failure_returns_failure_dict():
    with patch(
        "thero.skills.installer.run_command",
        return_value=MagicMock(returncode=1),
    ):
        result = install_impeccable()

    assert result is not None
    assert result["skill"] == "impeccable"


def test_write_failed_skills_report_removes_stale_report_when_empty(tmp_path):
    report_path = tmp_path / "SKILLS_INSTALL_FAILED.md"
    report_path.write_text("stale", encoding="utf-8")

    write_failed_skills_report([], tmp_path)

    assert not report_path.exists()


def test_write_failed_skills_report_writes_content_when_failures_exist(tmp_path):
    failed = [
        {"group": "G", "repo": "org/repo", "skill": "s", "command": "npx ..."}
    ]

    write_failed_skills_report(failed, tmp_path)

    report_path = tmp_path / "SKILLS_INSTALL_FAILED.md"
    content = report_path.read_text(encoding="utf-8")
    assert "skill=s" in content
    assert "npx ..." in content


def test_install_all_skills_writes_report_in_entry_dir_when_global(tmp_path):
    entry_path = tmp_path / "sub" / "thero.py"

    with patch(
        "thero.skills.installer.install_repository_skills", return_value=[]
    ), patch(
        "thero.skills.installer.install_impeccable", return_value=None
    ):
        install_all_skills(entry_path, global_install=True)

    assert not (tmp_path / "sub" / "SKILLS_INSTALL_FAILED.md").exists()


def test_install_all_skills_writes_report_in_cwd_when_local(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    entry_path = tmp_path / "sub" / "thero.py"

    failure = {"group": "G", "repo": "r", "skill": "s", "command": "c"}

    with patch(
        "thero.skills.installer.install_repository_skills", return_value=[failure]
    ), patch(
        "thero.skills.installer.install_impeccable", return_value=None
    ):
        install_all_skills(entry_path, global_install=False)

    assert (tmp_path / "SKILLS_INSTALL_FAILED.md").exists()


def test_install_all_skills_includes_impeccable_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    entry_path = tmp_path / "thero.py"
    impeccable_failure = {
        "group": "Impeccable", "repo": "r", "skill": "impeccable", "command": "c",
    }

    with patch(
        "thero.skills.installer.install_repository_skills", return_value=[]
    ), patch(
        "thero.skills.installer.install_impeccable",
        return_value=impeccable_failure,
    ):
        install_all_skills(entry_path, global_install=False)

    content = (tmp_path / "SKILLS_INSTALL_FAILED.md").read_text(encoding="utf-8")
    assert "skill=impeccable" in content


def test_check_skills_true_when_both_succeed():
    with patch(
        "thero.skills.installer.run_command",
        return_value=MagicMock(returncode=0),
    ):
        assert check_skills() is True


def test_check_skills_false_when_either_fails():
    with patch(
        "thero.skills.installer.run_command",
        side_effect=[MagicMock(returncode=0), MagicMock(returncode=1)],
    ):
        assert check_skills() is False


def test_update_skills_true_when_both_succeed():
    with patch(
        "thero.skills.installer.run_command",
        return_value=MagicMock(returncode=0),
    ):
        assert update_skills() is True


def test_update_skills_false_when_either_fails():
    with patch(
        "thero.skills.installer.run_command",
        side_effect=[MagicMock(returncode=1), MagicMock(returncode=0)],
    ):
        assert update_skills() is False
