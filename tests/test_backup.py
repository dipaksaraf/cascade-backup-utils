"""Tests for the backup module."""
import os
import sys
import pytest
import pyperclip
import pyautogui
# from pathlib import Path
from cascade_backup_utils.backup import CascadeBackup
# from datetime import datetime
# import time


# Mock pyautogui functions to avoid actual mouse movement
@pytest.fixture(autouse=True)
def mock_pyautogui(monkeypatch):
    def mock_moveTo(*args, **kwargs):
        pass

    def mock_position():
        return (0, 0)

    monkeypatch.setattr(pyautogui, "moveTo", mock_moveTo)
    monkeypatch.setattr(pyautogui, "position", mock_position)


@pytest.fixture
def backup_dir(tmp_path):
    """Create a backup directory."""
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


@pytest.mark.skipif(
    sys.platform == "win32" and sys.version_info >= (3, 12),
    reason="pyautogui has issues with Python 3.12 on Windows",
)
def test_backup_creation(backup_dir, monkeypatch):
    """Test successful backup creation."""
    # Initialize backup utility
    backup = CascadeBackup()
    monkeypatch.setattr(backup, "backup_dir", str(backup_dir))

    # Set clipboard content
    pyperclip.copy("Test conversation\nLine 2\nLine 3")

    # Mock input to skip user prompt
    monkeypatch.setattr("builtins.input", lambda _: "")

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


@pytest.mark.skipif(
    sys.platform == "win32" and sys.version_info >= (3, 12),
    reason="pyautogui has issues with Python 3.12 on Windows",
)
def test_backup_empty_clipboard(backup_dir, monkeypatch):
    """Test handling of empty clipboard."""
    backup = CascadeBackup()
    monkeypatch.setattr(backup, "backup_dir", str(backup_dir))

    # Set empty clipboard
    pyperclip.copy("")

    # Mock input
    monkeypatch.setattr("builtins.input", lambda _: "")

    # Run backup
    backup.backup()

    # Check that no backup was created
    backup_files = list(backup_dir.glob("*.md"))
    assert len(backup_files) == 0


@pytest.mark.skipif(
    sys.platform == "win32" and sys.version_info >= (3, 12),
    reason="pyautogui has issues with Python 3.12 on Windows",
)
def test_backup_failsafe(backup_dir, monkeypatch):
    """Test handling of FailSafeException."""
    backup = CascadeBackup()
    monkeypatch.setattr(backup, "backup_dir", str(backup_dir))

    # Mock clipboard to raise FailSafeException
    def mock_copy_failsafe(_):
        raise pyautogui.FailSafeException("Test failsafe")

    monkeypatch.setattr(pyperclip, "copy", mock_copy_failsafe)
    monkeypatch.setattr("builtins.input", lambda _: "")

    # Run backup
    backup.backup()

    # Check that no backup was created
    backup_files = list(backup_dir.glob("*.md"))
    assert len(backup_files) == 0


@pytest.mark.skipif(
    sys.platform == "win32" and sys.version_info >= (3, 12),
    reason="pyautogui has issues with Python 3.12 on Windows",
)
def test_backup_save_error(backup_dir, monkeypatch):
    """Test handling of save errors."""
    backup = CascadeBackup()
    monkeypatch.setattr(backup, "backup_dir", str(backup_dir))

    # Set clipboard content
    pyperclip.copy("Test conversation")

    # Mock open to raise an error
    def mock_open(*args, **kwargs):
        raise IOError("Test save error")

    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr("builtins.input", lambda _: "")

    # Run backup
    backup.backup()

    # Check that no backup was created
    backup_files = list(backup_dir.glob("*.md"))
    assert len(backup_files) == 0


@pytest.mark.skipif(
    sys.platform == "win32" and sys.version_info >= (3, 12),
    reason="pyautogui has issues with Python 3.12 on Windows",
)
def test_backup_retry_success(backup_dir, monkeypatch):
    """Test successful backup after retry."""
    backup = CascadeBackup()
    monkeypatch.setattr(backup, "backup_dir", str(backup_dir))

    # Set up mock for clipboard content
    clipboard_content = ["", "", "Test conversation"]
    current_attempt = [0]

    def mock_paste():
        content = clipboard_content[current_attempt[0]]
        current_attempt[0] += 1
        return content

    monkeypatch.setattr(pyperclip, "paste", mock_paste)
    monkeypatch.setattr("builtins.input", lambda _: "y")

    # Run backup
    backup.backup()

    # Check if backup was created
    backup_files = list(backup_dir.glob("*.md"))
    assert len(backup_files) == 1

    # Check content
    backup_content = backup_files[0].read_text()
    assert "Test conversation" in backup_content
