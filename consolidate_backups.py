"""
Cascade Conversation Consolidation Utility

This script consolidates multiple backup files of Cascade conversations into a single markdown file.
It handles duplicate removal, chronological sorting, and cleanup of UI elements and system messages.

Features:
- Removes duplicate conversations
- Sorts conversations by timestamp (newest first)
- Cleans up UI messages and system text
- Maintains conversation context and readability
"""

import os
import re
from datetime import datetime

class BackupConsolidator:
    def __init__(self):
        # Set up paths for backup directory and consolidated file
        self.backup_dir = os.path.join(os.path.dirname(__file__), 'backups')
        self.consolidated_file = os.path.join(self.backup_dir, 'consolidated_conversation.md')
        # Define UI messages to be removed from the content
        self.ui_messages = [
            "DoneFeedback has been submitted",
            "Start with History Ctrl + ⏎",
            "Press Enter again to interrupt and send a new message",
            "Image",
            "Claude 3.5 Sonnet",
            "Write",
            "Chat",
            "ChatWriteLegacy",
            "Legacy",
            "Changes overview (0 files need review)",
            "GPT-4o",
            "Cascade |  mode (Ctrl + .)"
        ]

    def clean_content(self, content):
        """
        Remove UI messages and clean up the content.
        
        Args:
            content (str): Raw content from backup file
            
        Returns:
            str: Cleaned content with UI messages removed
        """
        # Remove UI messages
        cleaned = content
        for msg in self.ui_messages:
            cleaned = cleaned.replace(msg, '')
        
        # Remove combinations of UI elements that might appear together
        ui_pattern = r'(?:Image|Claude 3\.5 Sonnet|Write|Chat|ChatWriteLegacy)(?:\s*(?:Image|Claude 3\.5 Sonnet|Write|Chat|ChatWriteLegacy))*'
        cleaned = re.sub(ui_pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Remove multiple newlines
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        # Strip whitespace from start and end
        cleaned = cleaned.strip()
        
        return cleaned

    def read_backups(self):
        """
        Read all markdown backup files from the backup directory.
        Excludes the consolidated file and processes only .md files.
        
        Returns:
            list: List of cleaned content from each backup file
        """
        backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.md') and f != 'consolidated_conversation.md']
        print(f"Found {len(backups)} backup files to process")
        content = []
        for backup in backups:
            with open(os.path.join(self.backup_dir, backup), 'r', encoding='utf-8') as file:
                content.append(self.clean_content(file.read()))
            print(f"Read file: {backup}")
        return content

    def parse_interactions(self, content):
        """
        Parse individual interactions from the content based on timestamps.
        
        Args:
            content (str): Cleaned content from a backup file
            
        Returns:
            list: List of (timestamp, interaction_text) tuples
        """
        # First, try to find any timestamps in the content
        timestamps = re.findall(r"\*Backup created on: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\*", content)
        print(f"Found {len(timestamps)} timestamps in content")
        
        if not timestamps:
            # If no timestamps found, use the filename timestamp pattern as fallback
            filename_pattern = r"cascade_backup_(\d{8})_(\d{6})"
            matches = re.findall(filename_pattern, content)
            if matches:
                for date, time in matches:
                    timestamp_str = f"{date[:4]}-{date[4:6]}-{date[6:]} {time[:2]}:{time[2:4]}:{time[4:]}"
                    print(f"Using filename timestamp: {timestamp_str}")
                    return [(datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"), content)]
        
        # Split content by timestamp markers
        parts = re.split(r"\*Backup created on: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\*", content)
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
        
        result = '\n\n'.join([f"*Backup created on: {t.strftime('%Y-%m-%d %H:%M:%S')}*\n{c}" for t, c in consolidated])
        return result

    def save_consolidated_file(self, consolidated_content):
        """
        Save the consolidated content to a markdown file.
        
        Args:
            consolidated_content (str): The processed and consolidated conversation text
        """
        with open(self.consolidated_file, 'w', encoding='utf-8') as file:
            file.write(consolidated_content)
        print(f"\nConsolidated conversation saved to: {self.consolidated_file}")
        print(f"Content length: {len(consolidated_content)} characters")

    def consolidate(self):
        """
        Main consolidation process that orchestrates the reading, processing,
        and saving of consolidated conversations.
        """
        print("Starting backup consolidation process...")
        backup_contents = self.read_backups()
        print(f"\nProcessing {len(backup_contents)} backup files...")
        consolidated_content = self.consolidate_content(backup_contents)
        self.save_consolidated_file(consolidated_content)

if __name__ == "__main__":
    consolidator = BackupConsolidator()
    consolidator.consolidate()
