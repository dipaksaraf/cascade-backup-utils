"""Command-line interface for Cascade Backup Utils."""

from .backup import CascadeBackup
from .consolidate import BackupConsolidator

def backup_main():
    """Entry point for backup command."""
    backup = CascadeBackup()
    backup.backup()

def consolidate_main():
    """Entry point for consolidate command."""
    consolidator = BackupConsolidator()
    consolidator.consolidate()

if __name__ == "__main__":
    print("Please use 'cascade-backup' or 'cascade-consolidate' commands.")
