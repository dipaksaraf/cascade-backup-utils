"""Common test fixtures for cascade-backup-utils."""
import os
import time
import pytest
import pyperclip
import pyautogui
# from pathlib import Path
from unittest.mock import MagicMock


@pytest.fixture(autouse=True)
def mock_clipboard(monkeypatch):
    """Mock clipboard operations for all tests."""
    clipboard_content = [""]

    def mock_copy(text):
        clipboard_content[0] = text

    def mock_paste():
        return clipboard_content[0]

    monkeypatch.setattr(pyperclip, "copy", mock_copy)
    monkeypatch.setattr(pyperclip, "paste", mock_paste)


@pytest.fixture(autouse=True)
def mock_gui(monkeypatch):
    """Mock GUI operations for all tests."""

    def mock_move_to(*args, **kwargs):
        pass

    def mock_position():
        return (0, 0)

    def mock_sleep(*args):
        pass

    def mock_screenshot(*args, **kwargs):
        from PIL import Image

        return Image.new("RGB", (1, 1))

    def mock_click(*args, **kwargs):
        pass

    def mock_hotkey(*args, **kwargs):
        pass

    monkeypatch.setattr(pyautogui, "moveTo", mock_move_to)
    monkeypatch.setattr(pyautogui, "position", mock_position)
    monkeypatch.setattr(pyautogui, "screenshot", mock_screenshot)
    monkeypatch.setattr(pyautogui, "click", mock_click)
    monkeypatch.setattr(pyautogui, "hotkey", mock_hotkey)
    monkeypatch.setattr(time, "sleep", MagicMock())


@pytest.fixture
def backup_dir(tmp_path):
    """Create a temporary backup directory."""
    path = tmp_path / "backups"
    os.makedirs(path, exist_ok=True)
    return path
