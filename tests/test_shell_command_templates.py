from __future__ import annotations

import pytest

from thero.settings import COMMAND_MARKER_END, COMMAND_MARKER_START
from thero.shell_command.templates import (
    GLOBAL_COMMAND_TEMPLATE,
    GLOBAL_COMMAND_TEMPLATE_POSIX,
    LOCAL_COMMAND_TEMPLATE,
    LOCAL_COMMAND_TEMPLATE_POSIX,
)


def test_global_templates_wrapped_in_markers():
    for template in (GLOBAL_COMMAND_TEMPLATE, GLOBAL_COMMAND_TEMPLATE_POSIX):
        assert template.startswith(COMMAND_MARKER_START)
        assert COMMAND_MARKER_END in template


@pytest.mark.parametrize(
    "command_name",
    ["mycmd", "my cmd with spaces", "cmd-ção", "日本語", "cmd'quote"],
)
def test_global_template_formats_with_exotic_command_names(command_name):
    result = GLOBAL_COMMAND_TEMPLATE % (command_name, "/path/to/thero.py")

    assert f"function {command_name} {{" in result


@pytest.mark.parametrize(
    "command_name",
    ["mycmd", "my cmd with spaces", "cmd-ção", "日本語"],
)
def test_global_template_posix_formats_with_exotic_command_names(command_name):
    result = GLOBAL_COMMAND_TEMPLATE_POSIX % (command_name, "/path/to/thero.py")

    assert f"{command_name}() {{" in result


@pytest.mark.parametrize(
    "project_dir",
    ["/home/user/proj", "/home/user/my project", "/home/usuário/projeto"],
)
def test_local_template_formats_with_exotic_project_dir(project_dir):
    result = LOCAL_COMMAND_TEMPLATE % {
        "project_dir": project_dir,
        "local_filename": "thero-local.ps1",
        "command_name": "mycmd",
        "script_path": "/path/thero.py",
    }

    assert project_dir in result
    assert "function mycmd {" in result


@pytest.mark.parametrize(
    "project_dir",
    ["/home/user/proj", "/home/user/my project", "/home/usuário/projeto"],
)
def test_local_template_posix_formats_with_exotic_project_dir(project_dir):
    result = LOCAL_COMMAND_TEMPLATE_POSIX % {
        "project_dir": project_dir,
        "local_filename": "thero-local.sh",
        "command_name": "mycmd",
        "script_path": "/path/thero.py",
    }

    assert project_dir in result
    assert "mycmd() {" in result
