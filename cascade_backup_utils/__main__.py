"""Command-line interface for Cascade Backup Utils."""

import sys
from cascade_backup_utils.backup import CascadeBackup
from cascade_backup_utils.consolidate import BackupConsolidator


def backup_main():
    """Entry point for backup command."""
    backup = CascadeBackup()
    backup.backup()


def consolidate_main():
    """Entry point for consolidate command."""
    consolidator = BackupConsolidator()
    consolidator.consolidate()


def main():
    """Main entry point for the cascade-backup-utils command-line interface."""
    if len(sys.argv) < 2:
        print("Usage: cascade-backup-utils <command>")
        print("Commands:")
        print("  backup      Create a new backup of the current conversation")
        print("  consolidate Consolidate all backup files into a single file")
        sys.exit(1)

    command = sys.argv[1]

    if command == "backup":
        backup = CascadeBackup()
        backup.backup()
    elif command == "consolidate":
        consolidator = BackupConsolidator()
        consolidator.consolidate()
    else:
        print(f"Invalid command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
