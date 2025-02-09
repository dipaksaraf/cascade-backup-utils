# Cascade Conversation Backup Utility

This utility helps you back up and consolidate your Cascade conversations from the Windsurf IDE as markdown files. It may also work with other AI coding platforms, though this has not been tested. Backing up conversations from AI coding sessions is crucial, especially as AI models can sometimes produce unexpected results. In particular, when using Windsurf, large conversations can lead to issues such as the IDE failing to start with the message "windsurf failed to start."

## Why This Utility?

When the Windsurf IDE encounters issues with large conversations, the common solutions are:

1. Continuously press `Ctrl + Shift + P` (Command Palette) and select "Developer: Reload Window."
2. Delete the Cascade cache folder:
   - **Windows**: `C:\Users\<YOUR_USERNAME>\.codeium\windsurf\cascade`
   - **Linux/Mac**: `~/.codeium/windsurf/cascade`

However, deleting the cache folder will remove your conversation history. This utility ensures your valuable conversations are preserved and accessible even if you need to clear the cache.

## Features

### Backup Features
- Manual text selection and copying with retry mechanism
- Automatic timestamp addition
- Clipboard management and content verification
- Clear user instructions and feedback
- Fail-safe mechanism (move mouse to corner to abort)

### Consolidation Features
- Combines multiple backup files into a single conversation
- Removes duplicate content automatically
- Chronological sorting (newest conversations first)
- Cleans up UI messages and system text
- Preserves conversation context and readability

## Setup

1. Make sure you have Python installed on your system
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Backing Up Conversations

1. Open your Cascade conversation
2. Run the backup script:
   ```bash
   python backup_conversation.py
   ```
3. Follow the on-screen instructions:
   - Clear any existing text selection
   - Select the conversation text you want to backup
   - Copy using Ctrl+C
   - Press Enter to continue

The script will:
- Clear the clipboard before starting
- Verify the content was copied successfully
- Allow multiple retry attempts if needed
- Save the backup with timestamp

### Consolidating Backups

1. Run the consolidate script:
   ```bash
   python consolidate_backups.py
   ```

The script will:
- Process all backup files in the `backups` directory
- Remove duplicate content
- Sort conversations chronologically (newest first)
- Clean up UI messages and system text
- Save everything to `consolidated_conversation.md`

## Backup Location

All files are stored in the `backups` directory:
```
backups/
  ├── cascade_backup_20250209_200618.md  # Individual backups
  ├── cascade_backup_20250210_001059.md
  ├── consolidated_conversation.md        # Combined conversations
  └── ...
```

## UI Messages Removed

The consolidation process automatically removes common UI elements and system messages:
- "DoneFeedback has been submitted"
- "Start with History Ctrl + ⏎"
- "Press Enter again to interrupt and send a new message"
- Various UI mode indicators (Image, Write, Chat, etc.)
- System status messages

## Troubleshooting

If you encounter issues:
1. Make sure all required packages are installed
2. Ensure Cascade window is active when copying
3. Try the retry option if clipboard content is not captured
4. Check console output for error messages
5. Move mouse to corner to abort if needed

## Safety Features

- Fail-safe enabled (move mouse to corner to abort)
- Multiple retry attempts for clipboard operations
- Error handling for common issues
- UTF-8 encoding support
- Backup verification before saving
