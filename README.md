# Cascade Conversation Backup Utility

[![Test Package](https://github.com/dipaksaraf/cascade-backup-utils/actions/workflows/test.yml/badge.svg)](https://github.com/dipaksaraf/cascade-backup-utils/actions/workflows/test.yml)
[![Publish to PyPI](https://github.com/dipaksaraf/cascade-backup-utils/actions/workflows/publish.yml/badge.svg)](https://github.com/dipaksaraf/cascade-backup-utils/actions/workflows/publish.yml)
[![PyPI version](https://badge.fury.io/py/cascade-backup-utils.svg)](https://badge.fury.io/py/cascade-backup-utils)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Coverage](https://codecov.io/gh/dipaksaraf/cascade-backup-utils/branch/main/graph/badge.svg)](https://codecov.io/gh/dipaksaraf/cascade-backup-utils)
[![GitHub Actions Build Status](https://github.com/dipaksaraf/cascade-backup-utils/actions/workflows/build.yml/badge.svg)](https://github.com/dipaksaraf/cascade-backup-utils/actions/workflows/build.yml)
[![GitHub Actions Lint Status](https://github.com/dipaksaraf/cascade-backup-utils/actions/workflows/lint.yml/badge.svg)](https://github.com/dipaksaraf/cascade-backup-utils/actions/workflows/lint.yml)

This utility helps you back up and consolidate your Cascade conversations from the Windsurf IDE as markdown files. It may also work with other AI coding platforms, though this has not been tested. Backing up conversations from AI coding sessions is crucial, especially as AI models can sometimes produce unexpected results. In particular, when using Windsurf, large conversations can lead to issues such as the IDE failing to start with the message "windsurf failed to start."

## Quick Start

### Installation

You can install the package directly from PyPI:

```bash
pip install cascade-backup-utils
```

Or install from source:

```bash
git clone https://github.com/dipaksaraf/cascade-backup-utils.git
cd cascade-backup-utils
pip install -e .
```

### Basic Usage

After installation, you can use the command-line tools:

```bash
# To backup a conversation:
cascade-backup

# To consolidate all backups:
cascade-consolidate
```

## Why This Utility?

When the Windsurf IDE encounters issues with large conversations, the common solutions are:

1. Continuously press `Ctrl + Shift + P` (Command Palette) and select "Developer: Reload Window."
2. Delete the Cascade cache folder:
   - **Windows**: `C:\Users\<YOUR_USERNAME>\.codeium\windsurf\cascade`
   - **Linux/Mac**: `~/.codeium/windsurf\cascade`

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

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/dipaksaraf/cascade-backup-utils.git
   cd cascade-backup-utils
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Usage

### Backing Up Conversations

1. Open your Cascade conversation
2. Run the backup command:
   ```bash
   cascade-backup
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

1. Run the consolidate command:
   ```bash
   cascade-consolidate
   ```

The script will:
- Process all backup files in the `backups` directory
- Remove duplicate content
- Sort conversations chronologically (newest first)
- Clean up UI messages and system text
- Save everything to `consolidated_conversation.md`

## Advanced Usage

### Custom Backup Directory
By default, backups are stored in your home directory under `.cascade_backups`. You can specify a custom directory:

```bash
cascade-backup --dir /path/to/backup/directory
```

### Consolidation Options
The consolidate command supports several options:

```bash
# Consolidate with custom output file
cascade-consolidate --output combined_conversations.md

# Keep original timestamps
cascade-consolidate --preserve-timestamps

# Sort by oldest first
cascade-consolidate --sort ascending
```

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

### Common Issues

1. **Mouse Movement Issues**
   - Ensure no other applications are controlling the mouse
   - Try increasing the delay: `cascade-backup --delay 2`

2. **Clipboard Problems**
   - Clear your clipboard before starting
   - Check if other applications are monitoring the clipboard

3. **File Permission Errors**
   - Ensure you have write permissions in the backup directory
   - Try running with elevated privileges if necessary

### Error Messages

- `Failed to capture clipboard`: Clear your clipboard and try again
- `Timeout waiting for selection`: Increase the timeout with `--timeout 60`
- `Invalid backup file format`: Ensure the backup files haven't been modified manually

## Security Considerations

1. **Clipboard Security**
   - The utility temporarily stores conversation data in your system clipboard
   - Clear sensitive information from your clipboard after use

2. **File Permissions**
   - Backup files are created with user-only read/write permissions
   - Consider encrypting sensitive backups

3. **Data Privacy**
   - Review conversations before backup to exclude sensitive information
   - Be cautious when sharing consolidated backup files

## Best Practices

1. **Regular Backups**
   - Back up important conversations immediately
   - Consider scheduling regular backups

2. **Backup Organization**
   - Use descriptive filenames
   - Maintain separate directories for different projects
   - Document the context of important conversations

3. **Maintenance**
   - Regularly consolidate backups to save space
   - Archive old backups
   - Test backup files periodically

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
