#!/usr/bin/env python3
"""
Script to run database migrations
"""
import mysql.connector
from config import Config
import sys

def run_migration(migration_file):
    """Execute a SQL migration file"""
    try:
        # Read migration file
        with open(migration_file, 'r') as f:
            sql_content = f.read()

        # Connect to database
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASS,
            database=Config.DB_NAME,
        )

        cursor = conn.cursor()

        # Split SQL content by statement (handle multi-statement execution)
        # This is a simple split - won't work for all cases but should work for our migration
        statements = []
        current_statement = []

        for line in sql_content.split('\n'):
            # Skip comments and empty lines
            stripped = line.strip()
            if stripped.startswith('--') or not stripped:
                continue

            current_statement.append(line)

            # Check if this line ends a statement
            if stripped.endswith(';'):
                statement = '\n'.join(current_statement)
                statements.append(statement)
                current_statement = []

        # Execute each statement
        success_count = 0
        error_count = 0

        for i, statement in enumerate(statements, 1):
            statement = statement.strip()
            if not statement:
                continue

            try:
                # Check if it's a multi-result statement (like CREATE VIEW)
                for result in cursor.execute(statement, multi=True):
                    if result.with_rows:
                        result.fetchall()

                conn.commit()
                success_count += 1
                print(f"✓ Statement {i}/{len(statements)} executed successfully")

            except mysql.connector.Error as e:
                # Some errors are acceptable (like table already exists)
                error_msg = str(e)
                if 'already exists' in error_msg.lower():
                    print(f"ℹ Statement {i}/{len(statements)}: {error_msg} (skipped)")
                else:
                    print(f"✗ Statement {i}/{len(statements)} failed: {error_msg}")
                    error_count += 1

        cursor.close()
        conn.close()

        print(f"\n{'='*60}")
        print(f"Migration completed:")
        print(f"  Success: {success_count} statements")
        print(f"  Errors: {error_count} statements")
        print(f"{'='*60}\n")

        return error_count == 0

    except Exception as e:
        print(f"✗ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    migration_file = "db/migrations/add_grade_level_system.sql"

    if len(sys.argv) > 1:
        migration_file = sys.argv[1]

    print(f"Running migration: {migration_file}\n")
    success = run_migration(migration_file)

    sys.exit(0 if success else 1)
