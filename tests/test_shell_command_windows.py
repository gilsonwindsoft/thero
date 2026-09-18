from __future__ import annotations

from unittest.mock import MagicMock, patch

from thero.settings import COMMAND_MARKER_END, COMMAND_MARKER_START
from thero.shell_command.windows import (
    install_global_command_windows,
    install_local_command_windows,
    resolve_powershell_profile,
)


def test_resolve_powershell_profile_returns_path_on_success():
    with patch(
        "thero.shell_command.windows.run_command",
        return_value=MagicMock(returncode=0, stdout="C:\\Users\\x\\profile.ps1\n"),
    ):
        result = resolve_powershell_profile()

    assert str(result) == "C:\\Users\\x\\profile.ps1"


def test_resolve_powershell_profile_returns_none_on_nonzero_returncode():
    with patch(
        "thero.shell_command.windows.run_command",
        return_value=MagicMock(returncode=1, stdout=""),
    ):
        assert resolve_powershell_profile() is None


def test_resolve_powershell_profile_returns_none_on_empty_stdout():
    with patch(
        "thero.shell_command.windows.run_command",
        return_value=MagicMock(returncode=0, stdout="   "),
    ):
        assert resolve_powershell_profile() is None


def test_install_local_command_windows_writes_script(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    install_local_command_windows("mycmd", tmp_path / "thero.py")

    target = tmp_path / "mycmd.local.ps1"
    assert target.exists()
    content = target.read_text(encoding="utf-8")
    assert "function mycmd {" in content
    assert str(tmp_path) in content


def test_install_local_command_windows_backs_up_existing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    target = tmp_path / "mycmd.local.ps1"
    target.write_text("old content", encoding="utf-8")

    with patch(
        "thero.shell_command.windows.backup_file"
    ) as mock_backup:
        install_local_command_windows("mycmd", tmp_path / "thero.py")

    mock_backup.assert_called_once()


def test_install_global_command_windows_errors_when_profile_unresolvable(tmp_path):
    with patch(
        "thero.shell_command.windows.resolve_powershell_profile",
        return_value=None,
    ), patch("thero.shell_command.windows.backup_file") as mock_backup:
        install_global_command_windows("mycmd", tmp_path / "thero.py")

    mock_backup.assert_not_called()


def test_install_global_command_windows_creates_fresh_profile(tmp_path):
    profile_path = tmp_path / "sub" / "profile.ps1"

    with patch(
        "thero.shell_command.windows.resolve_powershell_profile",
        return_value=profile_path,
    ):
        install_global_command_windows("mycmd", tmp_path / "thero.py")

    assert profile_path.exists()
    content = profile_path.read_text(encoding="utf-8")
    assert COMMAND_MARKER_START in content
    assert COMMAND_MARKER_END in content
    assert "function mycmd {" in content


def test_install_global_command_windows_backs_up_existing_profile(tmp_path):
    profile_path = tmp_path / "profile.ps1"
    profile_path.write_text("existing stuff", encoding="utf-8")

    with patch(
        "thero.shell_command.windows.resolve_powershell_profile",
        return_value=profile_path,
    ):
        install_global_command_windows("mycmd", tmp_path / "thero.py")

    content = profile_path.read_text(encoding="utf-8")
    assert "existing stuff" in content
    assert "function mycmd {" in content
    backups = list(tmp_path.glob("profile.backup_*.ps1"))
    assert len(backups) == 1


def test_install_global_command_windows_reinstall_does_not_duplicate(tmp_path):
    profile_path = tmp_path / "profile.ps1"

    with patch(
        "thero.shell_command.windows.resolve_powershell_profile",
        return_value=profile_path,
    ):
        install_global_command_windows("mycmd", tmp_path / "thero.py")
        install_global_command_windows("mycmd", tmp_path / "thero.py")

    content = profile_path.read_text(encoding="utf-8")
    assert content.count(COMMAND_MARKER_START) == 1
    assert content.count(COMMAND_MARKER_END) == 1
