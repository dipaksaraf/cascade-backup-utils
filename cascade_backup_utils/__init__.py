"""Cascade Backup Utils - A utility to backup and consolidate Cascade AI conversations.

This package provides tools to backup and manage Cascade AI conversations from the Windsurf IDE.
It helps prevent data loss when the IDE needs to be restarted or the cache needs to be cleared.

Main Features:
    - Backup conversations to markdown files
    - Consolidate multiple backups into a single file
    - Preserve conversation context and formatting
    - Handle large conversations efficiently

Example Usage:
    >>> from cascade_backup_utils import backup, consolidate
    >>> backup.create_backup()  # Create a new backup
    >>> consolidate.merge_backups()  # Merge all backups

For command-line usage:
    $ cascade-backup  # Create a new backup
    $ cascade-consolidate  # Merge all backups

See the README.md for detailed usage instructions and best practices.
"""

__version__ = "0.1.0"
