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
        # Set up paths for backup directory and consolidated file
        if backup_dir is None:
            self.backup_dir = os.path.join(os.path.dirname(__file__), "backups")
        else:
            self.backup_dir = backup_dir
        self.consolidated_file = os.path.join(
            self.backup_dir, "consolidated_conversation.md"
        )
        # Define UI messages to be removed from the content
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
        # Define UI messages to remove
        ui_messages = [
            "DoneFeedback has been submitted",
            "Start with History Ctrl+Enter",
            "Press Enter again to interrupt and send a new message",
            "Image",
            "Claude 3.5 Sonnet",
            "Write",
            "Chat",
        ]

        # Split content into lines
        lines = content.split("\n")
        cleaned = []

        # Process each line
        for line in lines:
            # Skip UI messages
            if any(msg in line for msg in ui_messages):
                continue
            # Skip empty lines after UI messages
            if not line.strip():
                continue
            cleaned.append(line)

        # Join lines and clean up multiple newlines
        result = "\n".join(cleaned)
        result = re.sub(r"\n{3,}", "\n\n", result)
        return result.strip()

    def _get_backup_files(self):
        """Get list of backup files in the backup directory."""
        if not os.path.exists(self.backup_dir):
            print(f"Backup directory not found: {self.backup_dir}")
            return []

        # Get all markdown files except consolidated file
        consolidated_name = "consolidated_conversation.md"
        backup_dir = self.backup_dir
        files = os.listdir(backup_dir)

        # Filter markdown files
        md_files = [f for f in files if f.endswith(".md")]

        # Exclude consolidated file
        return [
            os.path.join(backup_dir, f)
            for f in md_files
            if f != consolidated_name
        ]

    def _read_backups(self, backup_files):
        """Read and process backup files."""
        content = []
        for backup in backup_files:
            try:
                with open(backup, "r", encoding="utf-8") as file:
                    file_content = file.read()
                    # If no timestamp in content, try filename
                    if "*Backup created on:" not in file_content:
                        timestamp = self._extract_timestamp_from_filename(backup)
                        if timestamp:
                            ts_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                            file_content = (
                                f"*Backup created on: {ts_str}*\n{file_content}"
                            )
                    content.append(self.clean_content(file_content))
                print(f"Read file: {backup}")
            except Exception as e:
                print(f"Error reading {backup}: {str(e)}")
                continue
        return content

    def _extract_timestamp_from_filename(self, filename):
        """Extract timestamp from filename if present."""
        pattern = r"backup_(\d{8}_\d{6})\.md"
        match = re.search(pattern, filename)
        if match:
            try:
                return datetime.strptime(match.group(1), "%Y%m%d_%H%M%S")
            except ValueError:
                pass
        return None

    def _extract_timestamp_from_content(self, content):
        """Extract timestamp from content if present."""
        pattern = r"\*Backup created on: ([\d-]+ [\d:]+)\*"
        match = re.search(pattern, content)
        if match:
            try:
                return datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass
        return None

    def parse_interactions(self, content):
        """
        Parse individual interactions from the content based on timestamps.

        Args:
            content (str): Cleaned content from a backup file

        Returns:
            list: List of (timestamp, interaction_text) tuples
        """
        # First, try to find any timestamps in the content
        timestamps = re.findall(
            r"\*Backup created on: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\*", content
        )
        print(f"Found {len(timestamps)} timestamps in content")

        # If no timestamps found, try to extract from filename
        if not timestamps:
            return [
                (
                    self._extract_timestamp_from_content(content),
                    content.strip(),
                )
            ]

        # Split content by timestamp markers
        parts = re.split(
            r"\*Backup created on: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\*", content
        )
        print(f"Split content into {len(parts)} parts")

        parsed_interactions = []
        for i, timestamp_str in enumerate(timestamps):
            if i + 1 < len(parts):
                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    interaction = parts[i + 1].strip()
                    if interaction:  # Only add non-empty interactions
                        parsed_interactions.append((timestamp, interaction))
                        print(f"Added interaction with timestamp: {timestamp_str}")
                except ValueError as e:
                    print(f"Error parsing timestamp {timestamp_str}: {e}")
                    continue

        return parsed_interactions

    def consolidate_content(self, backup_contents):
        """
        Consolidate multiple backup contents into a single chronological conversation.
        Removes duplicates and sorts by timestamp (newest first).

        Args:
            backup_contents (list): List of backup file contents

        Returns:
            str: Consolidated and formatted conversation text
        """
        seen = set()
        consolidated = []

        for content in backup_contents:
            print("\nProcessing new backup content...")
            interactions = self.parse_interactions(content)
            print(f"Found {len(interactions)} interactions in this backup")

            for timestamp, interaction in interactions:
                content_hash = hash(interaction.strip())
                if content_hash not in seen:
                    consolidated.append((timestamp, interaction))
                    seen.add(content_hash)
                    print(f"Added new unique interaction from {timestamp}")

        # Sort by timestamp (reverse order for newest first)
        consolidated.sort(key=lambda x: x[0], reverse=True)
        print(f"\nTotal unique interactions consolidated: {len(consolidated)}")

        result = "\n\n".join(
            [
                f"*Backup created on: {t.strftime('%Y-%m-%d %H:%M:%S')}*\n{c}"
                for t, c in consolidated
            ]
        )
        return result

    def save_consolidated_file(self, content):
        """Save consolidated content to file.

        Args:
            content: Content to save.
        """
        try:
            with open(self.consolidated_file, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"\nConsolidated conversation saved to: {self.consolidated_file}")
            print(f"Content length: {len(content)} characters")
        except Exception as e:
            print(f"\nError saving consolidated file: {str(e)}")

    def consolidate(self):
        """Main consolidation process.

        This method orchestrates the reading, consolidation,
        and saving of backup conversations.
        """
        print("Starting backup consolidation process...")
        backup_files = self._get_backup_files()
        print(f"\nProcessing {len(backup_files)} backup files...")

        # Skip file creation if no backups found
        if not backup_files:
            print("No backup files found. Skipping consolidation.")
            return

        backup_contents = self._read_backups(backup_files)
        consolidated_content = self.consolidate_content(backup_contents)
        self.save_consolidated_file(consolidated_content)


if __name__ == "__main__":
    consolidator = BackupConsolidator()
    consolidator.consolidate()
