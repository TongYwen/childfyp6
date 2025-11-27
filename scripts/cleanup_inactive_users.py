#!/usr/bin/env python3
"""
Automated Inactive User Cleanup Script
=======================================
This script checks for inactive users and performs automated cleanup:
- Sends warning emails to users inactive for 23+ days
- Sends final warning emails to users inactive for 28+ days
- Deletes accounts inactive for 30+ days (unless protected)

This script should be run daily via cron job.

Usage:
    python3 cleanup_inactive_users.py

Cron job example (runs daily at 2 AM):
    0 2 * * * cd /path/to/childfyp6 && python3 scripts/cleanup_inactive_users.py >> logs/cleanup.log 2>&1
"""

import sys
import os
from datetime import datetime

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app and cleanup function
from app import app, check_inactive_users


def main():
    """Run the inactive user cleanup process"""
    print(f"\n{'='*60}")
    print(f"Inactive User Cleanup - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        # Run cleanup within Flask app context
        with app.app_context():
            stats = check_inactive_users()

        # Print results
        print("Cleanup Results:")
        print(f"  - First warnings sent: {stats['warnings_sent']}")
        print(f"  - Final warnings sent: {stats['final_warnings_sent']}")
        print(f"  - Accounts deleted: {stats['accounts_deleted']}")

        if stats['errors']:
            print(f"\nErrors encountered ({len(stats['errors'])}):")
            for error in stats['errors']:
                print(f"  - {error}")
        else:
            print("\nNo errors encountered.")

        print(f"\n{'='*60}")
        print("Cleanup completed successfully!")
        print(f"{'='*60}\n")

        return 0

    except Exception as e:
        print(f"\nERROR: Cleanup failed!")
        print(f"  {str(e)}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
