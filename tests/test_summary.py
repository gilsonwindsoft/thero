from __future__ import annotations

from pathlib import Path

from thero.reporting.summary import print_summary


def test_print_summary_includes_claude_md_path(capsys):
    fake_path = Path("/fake/CLAUDE.md")

    print_summary(fake_path)

    captured = capsys.readouterr()
    assert str(fake_path) in captured.out


def test_print_summary_does_not_raise_with_default_path(capsys):
    print_summary()

    captured = capsys.readouterr()
    assert "Claude Code Engineering Stack" in captured.out
