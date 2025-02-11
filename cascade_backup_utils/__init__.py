"""Cascade Backup Utils - A package for managing Cascade conversation backups.

This package provides utilities for creating and managing backups of Cascade
conversations. It includes functionality for backup creation and consolidation
of multiple backups.

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
