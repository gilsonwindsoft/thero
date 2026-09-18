from __future__ import annotations

import shutil
import subprocess
from unittest.mock import patch

import pytest

from thero.settings import COMMAND_MARKER_END, COMMAND_MARKER_START
from thero.shell_command.posix import (
    install_global_command_posix,
    install_local_command_posix,
    resolve_shell_rc_file,
)


@pytest.mark.parametrize(
    "shell_value,expected_name",
    [
        ("/bin/zsh", ".zshrc"),
        ("/usr/bin/zsh", ".zshrc"),
        ("/bin/bash", ".bashrc"),
        ("", ".profile"),
        ("/bin/fish", ".profile"),
    ],
)
def test_resolve_shell_rc_file_by_shell_env(shell_value, expected_name, monkeypatch):
    monkeypatch.setenv("SHELL", shell_value)

    result = resolve_shell_rc_file()

    assert result.name == expected_name


def test_install_local_command_posix_writes_script(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    install_local_command_posix("mycmd", tmp_path / "thero.py")

    target = tmp_path / "mycmd.local.sh"
    assert target.exists()
    content = target.read_text(encoding="utf-8")
    assert "mycmd() {" in content
    assert str(tmp_path) in content


def test_install_local_command_posix_backs_up_existing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    target = tmp_path / "mycmd.local.sh"
    target.write_text("old content", encoding="utf-8")

    with patch("thero.shell_command.posix.backup_file") as mock_backup:
        install_local_command_posix("mycmd", tmp_path / "thero.py")

    mock_backup.assert_called_once()


def test_install_global_command_posix_creates_fresh_rc_file(tmp_path):
    rc_path = tmp_path / "sub" / ".zshrc"

    with patch(
        "thero.shell_command.posix.resolve_shell_rc_file", return_value=rc_path
    ):
        install_global_command_posix("mycmd", tmp_path / "thero.py")

    assert rc_path.exists()
    content = rc_path.read_text(encoding="utf-8")
    assert COMMAND_MARKER_START in content
    assert COMMAND_MARKER_END in content
    assert "mycmd() {" in content


def test_install_global_command_posix_backs_up_existing_rc_file(tmp_path):
    rc_path = tmp_path / ".zshrc"
    rc_path.write_text("existing stuff", encoding="utf-8")

    with patch(
        "thero.shell_command.posix.resolve_shell_rc_file", return_value=rc_path
    ):
        install_global_command_posix("mycmd", tmp_path / "thero.py")

    content = rc_path.read_text(encoding="utf-8")
    assert "existing stuff" in content
    assert "mycmd() {" in content
    backups = list(tmp_path.glob(".zshrc.backup_*"))
    assert len(backups) == 1


def test_install_global_command_posix_reinstall_does_not_duplicate(tmp_path):
    rc_path = tmp_path / ".zshrc"

    with patch(
        "thero.shell_command.posix.resolve_shell_rc_file", return_value=rc_path
    ):
        install_global_command_posix("mycmd", tmp_path / "thero.py")
        install_global_command_posix("mycmd", tmp_path / "thero.py")

    content = rc_path.read_text(encoding="utf-8")
    assert content.count(COMMAND_MARKER_START) == 1
    assert content.count(COMMAND_MARKER_END) == 1


bash_missing = shutil.which("bash") is None


@pytest.mark.skipif(bash_missing, reason="bash not available on this runner")
def test_generated_local_script_has_valid_bash_syntax(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    install_local_command_posix("mycmd", tmp_path / "thero.py")

    target = tmp_path / "mycmd.local.sh"
    result = subprocess.run(
        ["bash", "-n", str(target)], capture_output=True, text=True
    )

    assert result.returncode == 0, result.stderr


@pytest.mark.skipif(bash_missing, reason="bash not available on this runner")
def test_generated_local_script_function_runs_in_real_bash(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    install_local_command_posix("mycmd", tmp_path / "thero.py")

    target = tmp_path / "mycmd.local.sh"
    result = subprocess.run(
        ["bash", "-c", f"source ./{target.name} && type mycmd"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )

    assert result.returncode == 0, result.stderr
    assert "mycmd" in result.stdout


@pytest.mark.skipif(bash_missing, reason="bash not available on this runner")
def test_generated_global_rc_block_has_valid_bash_syntax(tmp_path):
    rc_path = tmp_path / ".zshrc"

    with patch(
        "thero.shell_command.posix.resolve_shell_rc_file", return_value=rc_path
    ):
        install_global_command_posix("mycmd", tmp_path / "thero.py")

    result = subprocess.run(
        ["bash", "-n", str(rc_path)], capture_output=True, text=True
    )

    assert result.returncode == 0, result.stderr
