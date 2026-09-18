from __future__ import annotations

from unittest.mock import patch

from thero.settings import COMMAND_MARKER_END, COMMAND_MARKER_START
from thero.shell_command import install_global_command, upsert_marked_block


def test_upsert_appends_block_when_no_existing_marker():
    result = upsert_marked_block("existing content\n", "new block")

    assert result == "existing content\n\nnew block\n"


def test_upsert_appends_to_empty_existing():
    result = upsert_marked_block("", "new block")

    assert result == "new block\n"


def test_upsert_appends_to_whitespace_only_existing():
    result = upsert_marked_block("   \n\n", "new block")

    assert result == "new block\n"


def test_upsert_strips_trailing_newlines_from_existing_before_appending():
    result = upsert_marked_block("existing\n\n\n", "new block")

    assert result == "existing\n\nnew block\n"


def test_upsert_replaces_existing_marked_block_only():
    block = f"{COMMAND_MARKER_START}\nold content\n{COMMAND_MARKER_END}"
    existing = f"before\n\n{block}\n\nafter"

    result = upsert_marked_block(existing, f"{COMMAND_MARKER_START}\nnew content\n{COMMAND_MARKER_END}")

    assert "before" in result
    assert "after" in result
    assert "new content" in result
    assert "old content" not in result
    # Marker appears exactly once (not duplicated).
    assert result.count(COMMAND_MARKER_START) == 1
    assert result.count(COMMAND_MARKER_END) == 1


def test_upsert_reinstall_does_not_duplicate_marker():
    block = f"{COMMAND_MARKER_START}\ncontent v1\n{COMMAND_MARKER_END}"
    existing = f"prefix\n\n{block}\n"

    once = upsert_marked_block(existing, block)
    twice = upsert_marked_block(once, block)

    assert twice.count(COMMAND_MARKER_START) == 1
    assert twice.count(COMMAND_MARKER_END) == 1


@patch("thero.shell_command.os.name", "nt")
def test_install_global_command_dispatches_to_windows_global():
    with patch(
        "thero.shell_command.windows.install_global_command_windows"
    ) as mock_install:
        install_global_command("mycmd", "/entry.py", local=False)

    mock_install.assert_called_once_with("mycmd", "/entry.py")


@patch("thero.shell_command.os.name", "nt")
def test_install_global_command_dispatches_to_windows_local():
    with patch(
        "thero.shell_command.windows.install_local_command_windows"
    ) as mock_install:
        install_global_command("mycmd", "/entry.py", local=True)

    mock_install.assert_called_once_with("mycmd", "/entry.py")


@patch("thero.shell_command.os.name", "posix")
def test_install_global_command_dispatches_to_posix_global():
    with patch(
        "thero.shell_command.posix.install_global_command_posix"
    ) as mock_install:
        install_global_command("mycmd", "/entry.py", local=False)

    mock_install.assert_called_once_with("mycmd", "/entry.py")


@patch("thero.shell_command.os.name", "posix")
def test_install_global_command_dispatches_to_posix_local():
    with patch(
        "thero.shell_command.posix.install_local_command_posix"
    ) as mock_install:
        install_global_command("mycmd", "/entry.py", local=True)

    mock_install.assert_called_once_with("mycmd", "/entry.py")
