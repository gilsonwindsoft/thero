from __future__ import annotations

from unittest.mock import patch

import pytest

from thero.system.process import command_exists, run_command


def test_command_exists_true_when_which_finds_it():
    with patch("thero.system.process.shutil.which", return_value="/usr/bin/git"):
        assert command_exists("git") is True


def test_command_exists_false_when_which_returns_none():
    with patch("thero.system.process.shutil.which", return_value=None):
        assert command_exists("nope") is False


def test_run_command_raises_on_empty_command():
    with pytest.raises(ValueError):
        run_command([])


@pytest.mark.parametrize(
    "logical,launcher",
    [("npx", "npx.cmd"), ("npm", "npm.cmd"), ("node", "node.exe"), ("claude", "claude.cmd")],
)
@patch("thero.system.process.os.name", "nt")
@patch("thero.system.process.subprocess.run")
def test_run_command_maps_windows_launchers(mock_run, logical, launcher):
    run_command([logical, "--version"])

    called_command = mock_run.call_args.args[0]
    assert called_command[0] == launcher
    assert called_command[1:] == ["--version"]


@patch("thero.system.process.os.name", "nt")
@patch("thero.system.process.subprocess.run")
def test_run_command_leaves_unknown_executable_unmapped_on_windows(mock_run):
    run_command(["python", "-V"])

    called_command = mock_run.call_args.args[0]
    assert called_command[0] == "python"


@patch("thero.system.process.os.name", "posix")
@patch("thero.system.process.subprocess.run")
def test_run_command_does_not_map_launchers_on_posix(mock_run):
    run_command(["claude", "-p"])

    called_command = mock_run.call_args.args[0]
    assert called_command[0] == "claude"


@patch("thero.system.process.subprocess.run")
def test_run_command_passes_utf8_encoding_when_text(mock_run):
    run_command(["echo", "hi"], text=True)

    assert mock_run.call_args.kwargs["encoding"] == "utf-8"


@patch("thero.system.process.subprocess.run")
def test_run_command_no_encoding_when_not_text(mock_run):
    run_command(["echo", "hi"], text=False)

    assert mock_run.call_args.kwargs["encoding"] is None


@patch("thero.system.process.subprocess.run")
def test_run_command_forwards_cwd_check_input(mock_run):
    run_command(
        ["cmd"],
        cwd="/some/dir",
        check=True,
        capture=False,
        input_text="hello",
    )

    kwargs = mock_run.call_args.kwargs
    assert kwargs["cwd"] == "/some/dir"
    assert kwargs["check"] is True
    assert kwargs["capture_output"] is False
    assert kwargs["input"] == "hello"
    assert kwargs["shell"] is False


@patch("thero.system.process.subprocess.run")
def test_run_command_cwd_none_when_not_given(mock_run):
    run_command(["cmd"])

    assert mock_run.call_args.kwargs["cwd"] is None
