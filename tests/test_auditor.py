from __future__ import annotations

from unittest.mock import patch

from thero.audit.auditor import audit_project, print_audit_workflow


def test_audit_exits_early_when_claude_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with patch(
        "thero.audit.auditor.command_exists", return_value=False
    ), patch("thero.audit.auditor.call_claude") as mock_claude:
        audit_project()

    mock_claude.assert_not_called()
    assert not (tmp_path / "CLAUDE_AUDIT.md").exists()


def test_print_audit_workflow_prints_recommended_steps(capsys):
    print_audit_workflow()

    captured = capsys.readouterr()
    assert "CLAUDE_AUDIT.md" in captured.out


def test_audit_writes_report_on_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with patch(
        "thero.audit.auditor.command_exists", return_value=True
    ), patch(
        "thero.audit.auditor.call_claude", return_value="  audit findings  "
    ):
        audit_project()

    audit_path = tmp_path / "CLAUDE_AUDIT.md"
    assert audit_path.read_text(encoding="utf-8") == "  audit findings\n"


def test_audit_backs_up_previous_report(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    audit_path = tmp_path / "CLAUDE_AUDIT.md"
    audit_path.write_text("old audit", encoding="utf-8")

    with patch(
        "thero.audit.auditor.command_exists", return_value=True
    ), patch(
        "thero.audit.auditor.call_claude", return_value="new audit"
    ):
        audit_project()

    assert audit_path.read_text(encoding="utf-8") == "new audit\n"
    backups = list(tmp_path.glob("CLAUDE_AUDIT.backup_*.md"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "old audit"


def test_audit_returns_early_when_claude_call_fails(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with patch(
        "thero.audit.auditor.command_exists", return_value=True
    ), patch("thero.audit.auditor.call_claude", return_value=None):
        audit_project()

    assert not (tmp_path / "CLAUDE_AUDIT.md").exists()
