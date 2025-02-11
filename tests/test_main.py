import os
import sys
import pytest
from unittest.mock import patch
from cascade_backup_utils.__main__ import main
from cascade_backup_utils.backup import CascadeBackup
from cascade_backup_utils.consolidate import BackupConsolidator


def test_main_backup(tmp_path, monkeypatch):
    # Create backup directory
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    # Mock clipboard content
    monkeypatch.setattr("pyperclip.paste", lambda: "Test conversation")
    monkeypatch.setattr("pyperclip.copy", lambda _: None)
    monkeypatch.setattr("time.sleep", lambda _: None)

    # Mock user input
    monkeypatch.setattr("builtins.input", lambda _: "")

    # Mock backup directory initialization
    def mock_init(self):
        self.backup_dir = str(backup_dir)
        self.max_retries = 3
        self.retry_delay = 1

    monkeypatch.setattr(CascadeBackup, "__init__", mock_init)

    # Run main with backup command
    with patch.object(sys, "argv", ["cascade_backup_utils", "backup"]):
        main()

    # Check if backup was created
    backup_files = list(backup_dir.glob("*.md"))
    assert len(backup_files) == 1
    assert "Test conversation" in backup_files[0].read_text()


def test_main_consolidate(tmp_path, monkeypatch):
    # Create backup directory
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    # Create some test backup files
    test_files = [
        (
            "backup_2024-01-01_10-00-00.md",
            "*Backup created on: 2024-01-01 10:00:00*\nTest content 1",
        ),
        (
            "backup_2024-01-01_11-00-00.md",
            "*Backup created on: 2024-01-01 11:00:00*\nTest content 2",
        ),
    ]

    for filename, content in test_files:
        (backup_dir / filename).write_text(content)

    # Mock backup directory initialization
    def mock_init(self):
        self.backup_dir = str(backup_dir)
        self.consolidated_file = str(backup_dir / "consolidated_conversation.md")
        self.ui_messages = [
            "DoneFeedback has been submitted",
            "Start with History Ctrl+Enter",
            "Press Enter again to interrupt and send a new message",
            "Image",
            "Claude 3.5 Sonnet",
            "Write",
            "Chat",
            "ChatWriteLegacy",
            "Legacy",
            "Changes overview (0 files need review)",
            "GPT-4o",
            "Cascade |  mode (Ctrl + .)",
        ]

    monkeypatch.setattr(BackupConsolidator, "__init__", mock_init)

    # Run main with consolidate command
    with patch.object(sys, "argv", ["cascade_backup_utils", "consolidate"]):
        main()

    # Check if consolidated file was created
    consolidated_file = backup_dir / "consolidated_conversation.md"
    assert consolidated_file.exists()
    consolidated_content = consolidated_file.read_text()

    # Check content
    assert "*Backup created on: 2024-01-01 10:00:00*" in consolidated_content
    assert "*Backup created on: 2024-01-01 11:00:00*" in consolidated_content
    assert "Test content 1" in consolidated_content
    assert "Test content 2" in consolidated_content


def test_main_invalid_command(capsys):
    # Run main with invalid command
    with patch.object(sys, "argv", ["cascade_backup_utils", "invalid"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
    assert exc_info.value.code == 1

    # Check error message
    captured = capsys.readouterr()
    assert "Invalid command" in captured.out


def test_main_no_command(capsys):
    # Run main without command
    with patch.object(sys, "argv", ["cascade_backup_utils"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
    assert exc_info.value.code == 1

    # Check error message
    captured = capsys.readouterr()
    assert "Usage:" in captured.out
