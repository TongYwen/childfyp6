# Database Migrations

This directory contains SQL migration scripts for the ChildGrowth Insights application.

## How to Apply Migrations

### Migration 001: User Sessions Table

This migration adds session tracking functionality to monitor and manage user logins.

**To apply this migration:**

```bash
# Connect to your MySQL database
mysql -u your_username -p your_database_name

# Run the migration script
source migrations/001_create_user_sessions_table.sql
```

**Or using a single command:**

```bash
mysql -u your_username -p your_database_name < migrations/001_create_user_sessions_table.sql
```

**To rollback (if needed):**

```bash
mysql -u your_username -p your_database_name < migrations/001_rollback_user_sessions_table.sql
```

## What This Migration Does

Creates the `user_sessions` table with the following features:

- **Session Tracking**: Stores active user sessions
- **Security Monitoring**: Records IP address and browser/device information
- **Automatic Cleanup**: Expired sessions are automatically removed
- **Admin Control**: Admins can view and terminate sessions

## Table Structure

```sql
user_sessions
├── id (PRIMARY KEY)
├── user_id (FOREIGN KEY to users.id)
├── session_token (UNIQUE)
├── ip_address
├── user_agent
├── remember_me (BOOLEAN)
├── created_at (DATETIME)
├── last_activity (DATETIME)
└── expires_at (DATETIME)
```

## Features Enabled

After applying this migration, you will have:

✅ **Session Monitoring**: View all active sessions in the admin panel
✅ **Security Tracking**: See who's logged in, from where, and when
✅ **Force Logout**: Terminate specific sessions or all sessions for a user
✅ **Automatic Cleanup**: Expired sessions are removed automatically
✅ **Audit Trail**: Track session duration and activity

## Accessing the Feature

1. Log in as an admin
2. Go to Admin Dashboard
3. Click on "Session Management"

You can now:
- View all active sessions
- See user details, IP addresses, and browser info
- Terminate individual sessions
- Terminate all sessions for a specific user
- Monitor session expiration times
