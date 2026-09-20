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


def _find_usable_bash():
    """Absolute path to a *functional* POSIX bash, or None.

    Two Windows-specific hazards are handled here:

    1. ``shutil.which("bash")`` can resolve to the WSL launcher stub
       (System32\\bash.exe). That stub exists on PATH but, with no installed
       Linux distribution, prints a UTF-16 "Windows Subsystem for Linux has no
       installed distributions" notice and exits non-zero. A mere presence check
       would run the tests against it and fail spuriously, so we execute a probe
       command instead.

    2. The returned *absolute path* is what the tests must invoke. Calling a
       bare ``"bash"`` through ``subprocess`` lets ``CreateProcess`` re-resolve
       the name via a different search order (the WindowsApps alias / System32
       stub can win over Git's bin), so the guard and the subject would target
       different binaries. Pinning to the validated path keeps them consistent:
       either both use a working bash or the tests are skipped.
    """
    exe = shutil.which("bash")
    if exe is None:
        return None
    try:
        probe = subprocess.run(
            [exe, "-c", "printf bash_ok"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    if probe.returncode == 0 and "bash_ok" in (probe.stdout or ""):
        return exe
    return None


BASH_EXE = _find_usable_bash()
requires_bash = pytest.mark.skipif(
    BASH_EXE is None, reason="no functional POSIX bash on this runner"
)


@requires_bash
def test_generated_local_script_has_valid_bash_syntax(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    install_local_command_posix("mycmd", tmp_path / "thero.py")

    target = tmp_path / "mycmd.local.sh"
    # Invoke the validated BASH_EXE (not a bare "bash") with a relative name and
    # cwd set: Git Bash cannot resolve a backslash-qualified absolute path
    # (str(target)) and exits 127.
    result = subprocess.run(
        [BASH_EXE, "-n", target.name],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )

    assert result.returncode == 0, result.stderr


@requires_bash
def test_generated_local_script_function_runs_in_real_bash(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    install_local_command_posix("mycmd", tmp_path / "thero.py")

    target = tmp_path / "mycmd.local.sh"
    result = subprocess.run(
        [BASH_EXE, "-c", f"source ./{target.name} && type mycmd"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )

    assert result.returncode == 0, result.stderr
    assert "mycmd" in result.stdout


@requires_bash
def test_generated_global_rc_block_has_valid_bash_syntax(tmp_path):
    rc_path = tmp_path / ".zshrc"

    with patch(
        "thero.shell_command.posix.resolve_shell_rc_file", return_value=rc_path
    ):
        install_global_command_posix("mycmd", tmp_path / "thero.py")

    result = subprocess.run(
        [BASH_EXE, "-n", rc_path.name],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )

    assert result.returncode == 0, result.stderr
