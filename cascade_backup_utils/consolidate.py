"""Module for consolidating multiple backup files.

This script consolidates multiple backup files of Cascade conversations into a
single markdown file. It handles duplicate removal, chronological sorting, and
cleanup of UI elements and system messages.

Features:
- Removes duplicate conversations
- Sorts conversations chronologically
- Cleans up UI elements and system messages
"""

import os
import re
from datetime import datetime


class BackupConsolidator:
    def __init__(self, backup_dir=None):
        """Initialize the consolidator.

        Args:
            backup_dir: Directory containing backup files.
                       If None, uses default location.
        """
        if backup_dir is None:
            self.backup_dir = os.path.join(os.path.dirname(__file__), "backups")
        else:
            self.backup_dir = backup_dir
        self.consolidated_file = os.path.join(
            self.backup_dir, "consolidated_conversation.md"
        )
        self.ui_messages = [
            "DoneFeedback has been submitted",
            "Start with History Ctrl+Enter",  # Fixed pattern
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

    def clean_content(self, content):
        """Clean up the content by removing UI messages and duplicates.

        Args:
            content: Raw content string to clean.

        Returns:
            Cleaned content string.
        """
        ui_messages = [
            "DoneFeedback has been submitted",
            "Start with History Ctrl+Enter",
            "Press Enter again to interrupt and send a new message",
            "Image",
            "Claude 3.5 Sonnet",
            "Write",
            "Chat",
        ]

        lines = content.split("\n")
        cleaned = []

        for line in lines:
            if any(msg in line for msg in ui_messages):
                continue
            if not line.strip():
                continue
            cleaned.append(line)

        result = "\n".join(cleaned)
        result = re.sub(r"\n{3,}", "\n\n", result)
        return result.strip()

    def _get_backup_files(self):
        """Get list of backup files in the backup directory."""
        if not os.path.exists(self.backup_dir):
            print(f"Backup directory not found: {self.backup_dir}")
            return []

        consolidated_name = "consolidated_conversation.md"
        backup_dir = self.backup_dir
        files = os.listdir(backup_dir)

        md_files = [f for f in files if f.endswith(".md")]
        return [
            os.path.join(backup_dir, f)
            for f in md_files
            if f != consolidated_name
        ]

    def _extract_timestamp(self, filename):
        """Extract timestamp from backup filename."""
        match = re.search(r"backup_(\d{8}_\d{6})", filename)
        if match:
            timestamp_str = match.group(1)
            try:
                return datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            except ValueError:
                pass
        return None

    def _sort_files_by_timestamp(self, files):
        """Sort backup files by their timestamp."""
        file_times = []
        for f in files:
            timestamp = self._extract_timestamp(f)
            if timestamp:
                file_times.append((f, timestamp))

        file_times.sort(key=lambda x: x[1])
        return [f[0] for f in file_times]

    def consolidate(self):
        """Consolidate all backup files into a single file."""
        backup_files = self._get_backup_files()
        if not backup_files:
            print("No backup files found to consolidate.")
            return

        sorted_files = self._sort_files_by_timestamp(backup_files)

        consolidated_content = []
        seen_content = set()

        for file_path in sorted_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()

                cleaned = self.clean_content(content)

                if cleaned in seen_content:
                    continue

                consolidated_content.append(cleaned)
                seen_content.add(cleaned)

            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

        if consolidated_content:
            try:
                with open(self.consolidated_file, "w", encoding="utf-8") as f:
                    f.write("\n\n---\n\n".join(consolidated_content))
                print(f"Consolidated file saved to: {self.consolidated_file}")
            except Exception as e:
                print(f"Error saving consolidated file: {str(e)}")
        else:
            print("No valid content found to consolidate.")


if __name__ == "__main__":
    consolidator = BackupConsolidator()
    consolidator.consolidate()
