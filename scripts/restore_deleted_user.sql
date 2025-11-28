-- Emergency Recovery Script for Deleted User
-- WARNING: Only use immediately after accidental deletion
-- This assumes you have the user's data from a recent backup

-- Step 1: Restore user from backup
-- First, get the user data from your backup file and insert it here:

-- Example:
-- INSERT INTO users (id, name, email, password, role, created_at, last_login, is_active, protected_from_deletion)
-- VALUES (123, 'John Doe', 'john@example.com', 'hashed_password', 'parent', '2024-01-15 10:00:00', NOW(), 1, 1);

-- Step 2: Restore their children (if you have backup data)
-- INSERT INTO children (id, parent_id, name, date_of_birth, gender)
-- SELECT * FROM backup_children WHERE parent_id = 123;

-- Step 3: Restore assessments (if you have backup data)
-- INSERT INTO assessments (child_id, assessment_date, ...)
-- SELECT * FROM backup_assessments WHERE child_id IN (SELECT id FROM children WHERE parent_id = 123);

-- Step 4: Protect the account from future deletion
UPDATE users SET protected_from_deletion = 1 WHERE id = 123;

-- Step 5: Reset their inactivity status
UPDATE users SET last_login = NOW(), inactive_warning_sent = NULL WHERE id = 123;

-- Note: This is a manual process and should only be used in emergencies.
-- For production systems, implement soft delete instead.
