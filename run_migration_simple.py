#!/usr/bin/env python3
"""Simple migration runner using app's database connection"""
from app import get_db_conn
import sys

def run_migration():
    """Execute the grade level migration"""
    migration_file = "db/migrations/add_grade_level_system.sql"

    try:
        # Read migration file
        with open(migration_file, 'r') as f:
            sql_content = f.read()

        # Connect using app's connection function
        conn = get_db_conn()
        cursor = conn.cursor()

        # Split into statements
        statements = []
        current_statement = []

        for line in sql_content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('--') or not stripped:
                continue

            current_statement.append(line)

            if stripped.endswith(';'):
                statement = '\n'.join(current_statement)
                if statement.strip():
                    statements.append(statement)
                current_statement = []

        print(f"Found {len(statements)} SQL statements to execute\n")

        # Execute statements
        success = 0
        skipped = 0
        errors = 0

        for i, stmt in enumerate(statements, 1):
            stmt = stmt.strip()
            if not stmt:
                continue

            try:
                cursor.execute(stmt)
                conn.commit()
                success += 1
                # Print first 60 chars of statement
                preview = stmt[:60].replace('\n', ' ')
                print(f"✓ [{i}/{len(statements)}] {preview}...")

            except Exception as e:
                error_str = str(e)
                if 'already exists' in error_str.lower() or 'duplicate' in error_str.lower():
                    skipped += 1
                    print(f"⊘ [{i}/{len(statements)}] Already exists (skipped)")
                else:
                    errors += 1
                    print(f"✗ [{i}/{len(statements)}] ERROR: {error_str}")

        cursor.close()
        conn.close()

        print(f"\n{'='*60}")
        print(f"Migration Summary:")
        print(f"  ✓ Successful: {success}")
        print(f"  ⊘ Skipped:    {skipped}")
        print(f"  ✗ Errors:     {errors}")
        print(f"{'='*60}")

        return errors == 0

    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("Running Grade Level Migration")
    print("="*60 + "\n")

    success = run_migration()
    sys.exit(0 if success else 1)
