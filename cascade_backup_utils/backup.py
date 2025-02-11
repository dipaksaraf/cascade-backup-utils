"""
Module for backing up Cascade conversations.

This module handles the backup of conversations by copying them from the
clipboard and saving them as markdown files. It includes retry mechanisms
and error handling for clipboard operations.
"""

import os
import time
from datetime import datetime
import pyperclip
import pyautogui


class CascadeBackup:
    def __init__(self):
        # Set up backup directory in the same location as the script
        self.backup_dir = os.path.join(os.path.dirname(__file__), "backups")
        os.makedirs(self.backup_dir, exist_ok=True)
        # Enable fail-safe - moving mouse to corner will abort
        pyautogui.FAILSAFE = True
        # Maximum number of retry attempts for clipboard operations
        self.max_retries = 3

    def clear_clipboard(self):
        """
        Clear the clipboard before starting the backup process.
        Adds a small delay to ensure the system processes the clear operation.
        """
        print("Clearing clipboard...")
        pyperclip.copy("")
        time.sleep(1)  # Give system time to clear clipboard

    def get_clipboard_content(self, max_attempts=3):
        """
        Try to get clipboard content with multiple retry attempts.

        Args:
            max_attempts (int): Maximum number of attempts to read clipboard

        Returns:
            str or None: Clipboard content if found, None if clipboard is empty
        """
        for attempt in range(max_attempts):
            content = pyperclip.paste()
            if content.strip():
                return content
            print(f"Attempt {attempt + 1}: No content found in clipboard, waiting...")
            time.sleep(2)  # Wait before next attempt
        return None

    def copy_conversation(self):
        """
        Guide the user through the process of copying conversation text.
        Includes multiple retry attempts and user confirmation.

        Returns:
            str or None: Copied conversation text if successful, None otherwise
        """
        try:
            print("\nBefore copying the conversation:")
            print("1. Clear any existing text selection")
            print("2. Make sure no other content is in clipboard")
            input("Press Enter when ready to proceed...")

            self.clear_clipboard()

            for attempt in range(self.max_retries):
                print(f"\nAttempt {attempt + 1} of {self.max_retries}")
                print("In the Cascade window:")
                print("1. Select the conversation text you want to backup")
                print("2. Copy the text using Ctrl+C")
                input("Press Enter after you have copied the text...")

                content = self.get_clipboard_content()

                if content:
                    print("Successfully copied conversation text!")
                    return content

                if attempt < self.max_retries - 1:
                    retry = input("Would you like to try again? (y/n): ").lower()
                    if retry != "y":
                        break

            print("Failed to copy conversation text after multiple attempts")
            return None

        except pyautogui.FailSafeException:
            print("Operation aborted by moving mouse to corner")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def _save_backup(self, content):
        """Save backup content to a markdown file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{timestamp}.md"
        filepath = os.path.join(self.backup_dir, filename)

        # Format timestamp for content header
        header = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content_with_ts = (
            f"*Backup created on: {header}*\n\n{content}"
        )

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content_with_ts)
            print(f"\nBackup saved to: {filepath}")
        except Exception as e:
            err_msg = str(e)
            print("Error:", err_msg)
            print("Backup creation failed.")

    def backup(self):
        """Backup the current conversation.

        This method copies the conversation text from the clipboard
        and saves it as a markdown file with a timestamp.
        """
        print("Starting Cascade conversation backup...")
        content = self.copy_conversation()
        if content:
            self._save_backup(content)
            print("Backup completed successfully!")
        else:
            print("Backup failed! Please try again.")


if __name__ == "__main__":
    # Create requirements.txt if it doesn't exist
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if not os.path.exists(requirements_path):
        with open(requirements_path, "w") as f:
            f.write("pyautogui\npyperclip\n")
        print("Created requirements.txt")

    print("=== Cascade Conversation Backup Utility ===")
    print("\nMake sure you have installed the required packages:")
    print("pip install -r requirements.txt")
    print("\nInstructions:")
    print("1. Open your Cascade conversation window")
    print("2. Manually select the conversation text")
    print("3. Copy the text using Ctrl+C")
    print("4. Run this script and follow the prompts")
    print("5. Move mouse to any corner to abort the operation")
    print("\nStarting in 3 seconds...")
    time.sleep(3)

    backup = CascadeBackup()
    backup.backup()
