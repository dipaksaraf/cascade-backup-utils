import os
import time
import pytest
import pyperclip
import pyautogui
from datetime import datetime
from cascade_backup_utils.backup import CascadeBackup

# Mock pyautogui functions to avoid actual mouse movement
@pytest.fixture(autouse=True)
def mock_pyautogui(monkeypatch):
    def mock_moveTo(*args, **kwargs):
        pass
    
    def mock_position():
        return (0, 0)
    
    monkeypatch.setattr(pyautogui, "moveTo", mock_moveTo)
    monkeypatch.setattr(pyautogui, "position", mock_position)


def test_backup_creation(tmp_path, monkeypatch):
    # Create a backup directory
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    # Initialize backup utility and patch the backup directory
    backup = CascadeBackup()
    monkeypatch.setattr(backup, "backup_dir", str(backup_dir))

    # Mock clipboard functions
    clipboard_content = [""]  # Use a list to allow modification in the closure

    def mock_copy(text):
        clipboard_content[0] = text

    def mock_paste():
        return (
            clipboard_content[0]
            if clipboard_content[0]
            else "Test conversation\nLine 2\nLine 3"
        )

    monkeypatch.setattr(pyperclip, "copy", mock_copy)
    monkeypatch.setattr(pyperclip, "paste", mock_paste)

    # Mock input to skip user prompt
    monkeypatch.setattr("builtins.input", lambda _: "")

    # Mock time.sleep to speed up tests
    monkeypatch.setattr(time, "sleep", lambda _: None)

    # Run backup
    backup.backup()

    # Check if backup was created
    backup_files = list(backup_dir.glob("*.md"))
    assert len(backup_files) == 1

    # Check content
    backup_content = backup_files[0].read_text()
    assert "Test conversation" in backup_content
    assert "Line 2" in backup_content
    assert "Line 3" in backup_content


def test_backup_empty_clipboard(tmp_path, monkeypatch):
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    backup = CascadeBackup()
    monkeypatch.setattr(backup, "backup_dir", str(backup_dir))

    # Mock empty clipboard
    monkeypatch.setattr(pyperclip, "copy", lambda _: None)
    monkeypatch.setattr(pyperclip, "paste", lambda: "")

    # Mock input
    monkeypatch.setattr("builtins.input", lambda _: "")
    monkeypatch.setattr(time, "sleep", lambda _: None)

    # Run backup
    backup.backup()

    # Check that no backup was created
    backup_files = list(backup_dir.glob("*.md"))
    assert len(backup_files) == 0


def test_backup_failsafe(tmp_path, monkeypatch):
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    backup = CascadeBackup()
    monkeypatch.setattr(backup, "backup_dir", str(backup_dir))

    # Mock clipboard to raise FailSafeException
    def mock_copy_failsafe(_):
        raise pyautogui.FailSafeException("Test failsafe")

    monkeypatch.setattr(pyperclip, "copy", mock_copy_failsafe)
    monkeypatch.setattr(pyperclip, "paste", lambda: "")

    # Mock input
    monkeypatch.setattr("builtins.input", lambda _: "")
    monkeypatch.setattr(time, "sleep", lambda _: None)

    # Run backup
    backup.backup()

    # Check that no backup was created
    backup_files = list(backup_dir.glob("*.md"))
    assert len(backup_files) == 0


def test_backup_save_error(tmp_path, monkeypatch):
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    backup = CascadeBackup()
    monkeypatch.setattr(backup, "backup_dir", str(backup_dir))

    # Mock clipboard
    monkeypatch.setattr(pyperclip, "copy", lambda _: None)
    monkeypatch.setattr(pyperclip, "paste", lambda: "Test content")

    # Mock input
    monkeypatch.setattr("builtins.input", lambda _: "")
    monkeypatch.setattr(time, "sleep", lambda _: None)

    # Mock save_backup to simulate error
    def mock_save_backup(_):
        return False

    monkeypatch.setattr(backup, "_save_backup", mock_save_backup)

    # Run backup
    backup.backup()

    # Check that no backup was created
    backup_files = list(backup_dir.glob("*.md"))
    assert len(backup_files) == 0


def test_backup_retry_success(tmp_path, monkeypatch):
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    backup = CascadeBackup()
    monkeypatch.setattr(backup, "backup_dir", str(backup_dir))

    # Mock clipboard to fail twice then succeed
    attempts = [0]

    def mock_paste():
        attempts[0] += 1
        return "" if attempts[0] < 3 else "Test content after retry"

    monkeypatch.setattr(pyperclip, "copy", lambda _: None)
    monkeypatch.setattr(pyperclip, "paste", mock_paste)

    # Mock input to always continue
    monkeypatch.setattr("builtins.input", lambda _: "y")
    monkeypatch.setattr(time, "sleep", lambda _: None)

    # Run backup
    backup.backup()

    # Check that backup was created after retries
    backup_files = list(backup_dir.glob("*.md"))
    assert len(backup_files) == 1
    assert "Test content after retry" in backup_files[0].read_text()
