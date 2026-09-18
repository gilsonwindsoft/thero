from __future__ import annotations

from unittest.mock import patch

from thero.system.environment import ensure_claude_dir, validate_environment


def _which(available):
    def fake_command_exists(name):
        return name in available

    return fake_command_exists


def test_validate_environment_all_present():
    with patch(
        "thero.system.environment.command_exists",
        side_effect=_which({"node", "npx", "claude"}),
    ):
        assert validate_environment() is True


def test_validate_environment_missing_node_is_invalid():
    with patch(
        "thero.system.environment.command_exists",
        side_effect=_which({"npx", "claude"}),
    ):
        assert validate_environment() is False


def test_validate_environment_missing_claude_ok_when_not_required():
    with patch(
        "thero.system.environment.command_exists",
        side_effect=_which({"node", "npx"}),
    ):
        assert validate_environment(require_claude=False) is True


def test_validate_environment_missing_npx_is_invalid():
    with patch(
        "thero.system.environment.command_exists",
        side_effect=_which({"node", "claude"}),
    ):
        assert validate_environment() is False


def test_validate_environment_missing_claude_invalid_when_required():
    with patch(
        "thero.system.environment.command_exists",
        side_effect=_which({"node", "npx"}),
    ):
        assert validate_environment(require_claude=True) is False


def test_ensure_claude_dir_creates_directory(tmp_path):
    claude_dir = tmp_path / "sub" / ".claude"

    ensure_claude_dir(claude_dir)

    assert claude_dir.is_dir()


def test_ensure_claude_dir_idempotent_when_already_exists(tmp_path):
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()

    ensure_claude_dir(claude_dir)

    assert claude_dir.is_dir()
