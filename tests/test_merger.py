from __future__ import annotations

from unittest.mock import patch

from thero.claude_md.merger import merge_claude_md, validate_merged_claude_md


def test_validate_rejects_too_short():
    assert validate_merged_claude_md("short") is False


def test_validate_rejects_markdown_fence():
    assert validate_merged_claude_md("```\n" + "x" * 600) is False


def test_validate_accepts_normal_content():
    assert validate_merged_claude_md("# CLAUDE.md\n\n" + "x" * 600) is True


def test_merge_creates_fresh_file_when_none_exists(tmp_path):
    claude_md_path = tmp_path / ".claude" / "CLAUDE.md"

    with patch("thero.claude_md.merger.call_claude") as mock_claude:
        merge_claude_md(claude_md_path)

    assert claude_md_path.exists()
    mock_claude.assert_not_called()
    content = claude_md_path.read_text(encoding="utf-8")
    assert "Engineering Operating System" in content


def test_merge_with_existing_file_backs_up_and_replaces(tmp_path):
    claude_md_path = tmp_path / "CLAUDE.md"
    claude_md_path.write_text("old rules", encoding="utf-8")
    new_content = "# Merged\n\n" + "x" * 600

    with patch(
        "thero.claude_md.merger.call_claude", return_value=new_content
    ):
        merge_claude_md(claude_md_path)

    assert claude_md_path.read_text(encoding="utf-8") == new_content.rstrip() + "\n"
    backups = list(tmp_path.glob("CLAUDE.md.backup*"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "old rules"


def test_merge_claude_failure_leaves_original_untouched(tmp_path):
    claude_md_path = tmp_path / "CLAUDE.md"
    claude_md_path.write_text("old rules", encoding="utf-8")

    with patch("thero.claude_md.merger.call_claude", return_value=None):
        merge_claude_md(claude_md_path)

    assert claude_md_path.read_text(encoding="utf-8") == "old rules"


def test_merge_validation_failure_leaves_original_untouched(tmp_path):
    claude_md_path = tmp_path / "CLAUDE.md"
    claude_md_path.write_text("old rules", encoding="utf-8")

    with patch(
        "thero.claude_md.merger.call_claude", return_value="too short"
    ):
        merge_claude_md(claude_md_path)

    assert claude_md_path.read_text(encoding="utf-8") == "old rules"


def test_merge_write_failure_keeps_original_and_cleans_temp(tmp_path):
    claude_md_path = tmp_path / "CLAUDE.md"
    claude_md_path.write_text("old rules", encoding="utf-8")
    new_content = "# Merged\n\n" + "x" * 600

    with patch(
        "thero.claude_md.merger.call_claude", return_value=new_content
    ), patch(
        "thero.claude_md.merger.os.replace", side_effect=OSError("disk full")
    ):
        merge_claude_md(claude_md_path)

    assert claude_md_path.read_text(encoding="utf-8") == "old rules"
    leftover_temp_files = list(tmp_path.glob(".CLAUDE.md.tmp_*"))
    assert leftover_temp_files == []
