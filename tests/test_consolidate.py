import os
from cascade_backup_utils.consolidate import BackupConsolidator


def test_consolidate_backups(tmp_path, monkeypatch):
    # Create backup directory
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    # Create some test backup files
    test_files = [
        (
            "backup_2024-01-01_10-00-00.md",
            "*Backup created on: 2024-01-01 10:00:00*\nConversation 1\n",
        ),
        (
            "backup_2024-01-01_11-00-00.md",
            "*Backup created on: 2024-01-01 11:00:00*\nConversation 2\n",
        ),
        (
            "backup_2024-01-01_12-00-00.md",
            "*Backup created on: 2024-01-01 12:00:00*\nConversation 3\n",
        ),
    ]

    for filename, content in test_files:
        (backup_dir / filename).write_text(content)

    # Initialize consolidator and patch the backup directory
    consolidator = BackupConsolidator()
    monkeypatch.setattr(consolidator, "backup_dir", str(backup_dir))
    monkeypatch.setattr(
        consolidator,
        "consolidated_file",
        str(backup_dir / "consolidated_conversation.md"),
    )

    # Consolidate backups
    consolidator.consolidate()

    # Check if consolidated file exists and contains expected content
    consolidated_file = backup_dir / "consolidated_conversation.md"
    assert consolidated_file.exists()
    consolidated_content = consolidated_file.read_text()

    # Check if content is in chronological order
    assert "*Backup created on: 2024-01-01 10:00:00*" in consolidated_content
    assert "*Backup created on: 2024-01-01 11:00:00*" in consolidated_content
    assert "*Backup created on: 2024-01-01 12:00:00*" in consolidated_content


def test_consolidate_no_backups(tmp_path, monkeypatch):
    # Create empty backup directory
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    # Initialize consolidator and patch the backup directory
    consolidator = BackupConsolidator()
    monkeypatch.setattr(consolidator, "backup_dir", str(backup_dir))
    monkeypatch.setattr(
        consolidator,
        "consolidated_file",
        str(backup_dir / "consolidated_conversation.md"),
    )

    # Consolidate backups
    consolidator.consolidate()

    # Check that no consolidated file was created
    consolidated_file = backup_dir / "consolidated_conversation.md"
    assert not consolidated_file.exists()


def test_consolidate_duplicate_content(tmp_path, monkeypatch):
    # Create backup directory
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    # Create backup files with duplicate content
    test_files = [
        (
            "backup_2024-01-01_10-00-00.md",
            "*Backup created on: 2024-01-01 10:00:00*\nDuplicate content",
        ),
        (
            "backup_2024-01-01_11-00-00.md",
            "*Backup created on: 2024-01-01 11:00:00*\nDuplicate content",
        ),
        (
            "backup_2024-01-01_12-00-00.md",
            "*Backup created on: 2024-01-01 12:00:00*\nUnique content",
        ),
    ]

    for filename, content in test_files:
        (backup_dir / filename).write_text(content)

    # Initialize consolidator and patch the backup directory
    consolidator = BackupConsolidator()
    monkeypatch.setattr(consolidator, "backup_dir", str(backup_dir))
    monkeypatch.setattr(
        consolidator,
        "consolidated_file",
        str(backup_dir / "consolidated_conversation.md"),
    )

    # Consolidate backups
    consolidator.consolidate()

    # Check if consolidated file exists and contains expected content
    consolidated_file = backup_dir / "consolidated_conversation.md"
    assert consolidated_file.exists()
    consolidated_content = consolidated_file.read_text()

    # Check content - duplicates should only appear once
    assert consolidated_content.count("Duplicate content") == 1
    assert "Unique content" in consolidated_content


def test_consolidate_ui_message_cleanup(tmp_path, monkeypatch):
    # Create test backup files
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    # Create backup file with UI messages
    content = """*Backup created on: 2024-01-01 10:00:00*
DoneFeedback has been submitted
Start with History Ctrl+Enter
Important content
Press Enter again to interrupt and send a new message
Image
Claude 3.5 Sonnet
More content
Write
Chat
Final content"""

    (backup_dir / "backup1.md").write_text(content, encoding="utf-8")

    # Initialize consolidator and patch the backup directory
    consolidator = BackupConsolidator()
    monkeypatch.setattr(consolidator, "backup_dir", str(backup_dir))
    monkeypatch.setattr(
        consolidator,
        "consolidated_file",
        str(backup_dir / "consolidated_conversation.md"),
    )

    # Consolidate backups
    consolidator.consolidate()

    # Check that UI messages were removed
    consolidated_file = backup_dir / "consolidated_conversation.md"
    consolidated_content = consolidated_file.read_text(encoding="utf-8")
    assert "Important content" in consolidated_content
    assert "More content" in consolidated_content
    assert "Final content" in consolidated_content
    assert "DoneFeedback has been submitted" not in consolidated_content
    assert "Start with History Ctrl+Enter" not in consolidated_content
    assert "Press Enter again to interrupt" not in consolidated_content
    assert "Image" not in consolidated_content
    assert "Claude 3.5 Sonnet" not in consolidated_content
    assert "Write" not in consolidated_content
    assert "Chat" not in consolidated_content


def test_consolidate_invalid_timestamp(tmp_path, monkeypatch):
    # Create test backup files
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    # Create backup file with invalid timestamp
    content = """*Backup created on: 2024-13-32 25:61:99*
Test content with invalid timestamp"""

    (backup_dir / "backup1.md").write_text(content)

    # Initialize consolidator and patch the backup directory
    consolidator = BackupConsolidator()
    monkeypatch.setattr(consolidator, "backup_dir", str(backup_dir))
    monkeypatch.setattr(
        consolidator,
        "consolidated_file",
        str(backup_dir / "consolidated_conversation.md"),
    )

    # Consolidate backups
    consolidator.consolidate()

    # Check that file was created but content was handled gracefully
    consolidated_file = backup_dir / "consolidated_conversation.md"
    assert consolidated_file.exists()
    consolidated_content = consolidated_file.read_text()
    assert "Test content with invalid timestamp" not in consolidated_content


def test_consolidate_filename_timestamp(tmp_path, monkeypatch):
    # Create backup directory
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    # Create backup file with timestamp in filename
    timestamp = "2024-02-10_19-31-01"
    content = (
        "*Backup created on: 2024-02-10 19:31:01*\nTest content with filename timestamp"
    )
    filename = f"backup_{timestamp}.md"
    (backup_dir / filename).write_text(content)

    # Initialize consolidator and patch the backup directory
    consolidator = BackupConsolidator()
    monkeypatch.setattr(consolidator, "backup_dir", str(backup_dir))
    monkeypatch.setattr(
        consolidator,
        "consolidated_file",
        str(backup_dir / "consolidated_conversation.md"),
    )

    # Consolidate backups
    consolidator.consolidate()

    # Check if consolidated file exists and contains expected content
    consolidated_file = backup_dir / "consolidated_conversation.md"
    assert consolidated_file.exists()
    consolidated_content = consolidated_file.read_text()

    # Check if timestamp was extracted from filename
    assert "*Backup created on: 2024-02-10 19:31:01*" in consolidated_content
    assert "Test content with filename timestamp" in consolidated_content


def test_consolidate_read_error(tmp_path, monkeypatch):
    """Test handling of file read errors during consolidation."""
    # Create test backup files
    backup_dir = tmp_path / "backups"
    os.makedirs(backup_dir, exist_ok=True)

    # Create a backup file
    (backup_dir / "backup1.md").write_text("Test content")

    # Initialize consolidator and patch the backup directory
    consolidator = BackupConsolidator()
    monkeypatch.setattr(consolidator, "backup_dir", str(backup_dir))
    monkeypatch.setattr(
        consolidator,
        "consolidated_file",
        str(backup_dir / "consolidated_conversation.md"),
    )

    # Mock file read to raise error
    def mock_open(*args, **kwargs):
        raise PermissionError("Test permission error")

    monkeypatch.setattr("builtins.open", mock_open)

    # Consolidate backups - should handle error gracefully
    consolidator.consolidate()

    # Verify the consolidated file was not created
    assert not os.path.exists(consolidator.consolidated_file)
