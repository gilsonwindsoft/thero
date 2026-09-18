from __future__ import annotations

from unittest.mock import patch

from thero.shell_command.naming import prompt_command_name


def test_returns_default_when_not_a_tty():
    with patch("thero.shell_command.naming.sys.stdin.isatty", return_value=False):
        assert prompt_command_name("thero") == "thero"


def test_returns_default_on_empty_enter():
    with patch(
        "thero.shell_command.naming.sys.stdin.isatty", return_value=True
    ), patch("builtins.input", return_value=""):
        assert prompt_command_name("thero") == "thero"


def test_returns_typed_name():
    with patch(
        "thero.shell_command.naming.sys.stdin.isatty", return_value=True
    ), patch("builtins.input", return_value="mycmd"):
        assert prompt_command_name("thero") == "mycmd"


def test_strips_whitespace_around_typed_name():
    with patch(
        "thero.shell_command.naming.sys.stdin.isatty", return_value=True
    ), patch("builtins.input", return_value="  mycmd  "):
        assert prompt_command_name("thero") == "mycmd"


def test_eof_error_returns_default():
    with patch(
        "thero.shell_command.naming.sys.stdin.isatty", return_value=True
    ), patch("builtins.input", side_effect=EOFError):
        assert prompt_command_name("thero") == "thero"


def test_keyboard_interrupt_returns_default():
    with patch(
        "thero.shell_command.naming.sys.stdin.isatty", return_value=True
    ), patch("builtins.input", side_effect=KeyboardInterrupt):
        assert prompt_command_name("thero") == "thero"
