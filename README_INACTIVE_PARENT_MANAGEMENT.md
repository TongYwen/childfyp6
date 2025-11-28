# Inactive Parent User Management System

## Overview

The Inactive Parent User Management System is an automated feature that identifies, warns, and removes parent accounts that have been inactive for 30 days. This system helps maintain database efficiency, improves security by removing dormant accounts, and encourages user engagement through proactive communication.

**Key Benefits:**
- 📊 Automated database cleanup without manual intervention
- 🔒 Enhanced security by removing inactive accounts
- 📧 Fair warning system with multiple notifications
- ⚙️ Fully automated with manual override capabilities
- 🛡️ Multiple safety mechanisms to prevent accidental deletions

---

## Table of Contents

1. [How It Works](#how-it-works)
2. [Features](#features)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [Usage Guide](#usage-guide)
6. [Technical Details](#technical-details)
7. [Testing Guide](#testing-guide)
8. [Troubleshooting](#troubleshooting)
9. [Safety Features](#safety-features)
10. [Future Enhancements](#future-enhancements)

---

## How It Works

The system operates on a **4-phase timeline**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    INACTIVE ACCOUNT LIFECYCLE                    │
└─────────────────────────────────────────────────────────────────┘

Day 0-22:  ✅ ACTIVE
           └─ No action taken
           └─ User account operates normally

Day 23:    ⚠️  FIRST WARNING
           └─ Warning email sent ("7 days until deletion")
           └─ `inactive_warning_sent` timestamp recorded
           └─ User can log in to reset the clock

Day 28:    🚨 FINAL WARNING
           └─ Final urgent email sent ("2 days until deletion")
           └─ Emphasizes data loss and consequences
           └─ Last chance for user to reactivate

Day 30:    ❌ ACCOUNT DELETED
           └─ Deletion confirmation email sent
           └─ Account and all related data removed
           └─ Permanent and irreversible
```

### Special Case: Never Logged In

Accounts created 30+ days ago that have **never been used** are also deleted automatically. This prevents test accounts and abandoned registrations from cluttering the database.

---

## Features

### 1. Automated Lifecycle Management
- **Daily Automated Checks**: Runs automatically at 2:00 AM UTC every day
- **Smart Detection**: Identifies inactive users based on last login timestamp
- **Progressive Warnings**: Two-stage warning system (Day 23 and Day 28)
- **Automatic Deletion**: Removes accounts at Day 30 with confirmation

### 2. Admin Control Panel
Located at `/admin/inactive-users` (admin access required)

**Dashboard Features:**
- **Summary Cards**: 4 color-coded cards showing account status
  - 🔴 Pending Deletion (30+ days)
  - 🟡 At Risk (23-29 days)
  - 🟢 Active (<23 days)
  - 🔵 Protected (manually exempted)

- **Detailed Tables**: Complete user information with sortable columns
  - User ID, Name, Email, Role
  - Last Login Date, Days Inactive
  - Warning Sent Status
  - Protection Status

- **Admin Actions**:
  - **Protect/Unprotect**: Manually exempt accounts from deletion
  - **Reactivate**: Reset inactivity timer to current date
  - **Run Cleanup Now**: Trigger cleanup process manually

### 3. Email Notification System

Three professionally designed HTML emails:

**First Warning Email (Day 23)**
- Subject: "Your Account Will Be Deleted in 7 Days"
- Yellow theme with warning icon
- Clear call-to-action with login link
- Explains inactivity policy

**Final Warning Email (Day 28)**
- Subject: "URGENT: Account Deletion in 2 Days"
- Red theme emphasizing urgency
- Lists consequences of deletion
- Emphasizes data loss

**Deletion Confirmation Email (Day 30)**
- Subject: "Your Account Has Been Deleted"
- Gray theme for closure
- Confirms permanent deletion
- Provides contact information for questions

### 4. User Dashboard Warnings

When inactive users log in, they see alerts on their profile page:

- **Warning Alert** (23-27 days): Yellow banner showing days until deletion
- **Critical Alert** (28+ days): Red banner emphasizing urgency and data loss
- Alerts are dismissible but reappear until user becomes active

### 5. Safety Mechanisms

- ✅ **Admin Exclusion**: Admin accounts are completely exempt from deletion
- ✅ **Protection Flag**: Admins can manually protect any account
- ✅ **Multiple Warnings**: Users receive 2 emails before deletion
- ✅ **Email Confirmations**: Deletion confirmation sent after account removal
- ✅ **Database Integrity**: Cascade deletes handle related data properly
- ✅ **Transaction Safety**: Rollback on errors to prevent partial deletions

---

## Installation & Setup

### Prerequisites

- Python 3.7+
- Flask application running
- MySQL database
- Mail server (SMTP) configured

### Step 1: Database Schema Update

Run the following SQL to add required columns to your `users` table:

```sql
ALTER TABLE users
ADD COLUMN last_login TIMESTAMP NULL,
ADD COLUMN is_active TINYINT(1) DEFAULT 1,
ADD COLUMN protected_from_deletion TINYINT(1) DEFAULT 0,
ADD COLUMN inactive_warning_sent TIMESTAMP NULL;
```

Or use the complete schema in `db/database_schema.sql`.

### Step 2: Install Dependencies

Ensure Flask-APScheduler is installed:

```bash
pip install Flask-APScheduler
```

Your `requirements.txt` should include:
```
Flask==2.3.0
Flask-Login==0.6.2
Flask-Mail==0.9.1
Flask-APScheduler==1.13.1
PyMySQL==1.1.0
bcrypt==4.0.1
```

### Step 3: Configure Email Settings

In your `config.py` or environment variables:

```python
MAIL_SERVER = 'smtp.gmail.com'  # Your SMTP server
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@example.com'
MAIL_PASSWORD = 'your-app-password'
MAIL_DEFAULT_SENDER = 'your-email@example.com'
```

### Step 4: Verify Scheduler is Running

Check that APScheduler is initialized in `app.py`:

```python
from flask_apscheduler import APScheduler

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
```

The cleanup job should be registered:

```python
@scheduler.task('cron', id='cleanup_inactive_users', hour=2, minute=0)
def scheduled_cleanup():
    with app.app_context():
        stats = check_inactive_users()
        print(f"Cleanup completed: {stats}")
```

### Step 5: Test the Installation

1. Start your Flask application
2. Navigate to `/admin/inactive-users`
3. Verify the dashboard loads correctly
4. Click "Run Cleanup Now" to test manually

---

## Configuration

### Adjusting Inactivity Thresholds

To change the number of days before warnings/deletion, modify these values in `app.py`:

```python
# In check_inactive_users() function (around line 800)

# First warning threshold (default: 23 days)
first_warning_threshold = datetime.now() - timedelta(days=23)

# Final warning threshold (default: 28 days)
final_warning_threshold = datetime.now() - timedelta(days=28)

# Deletion threshold (default: 30 days)
deletion_threshold = datetime.now() - timedelta(days=30)
```

### Changing Cleanup Schedule

Modify the scheduler configuration in `app.py` (around line 928):

```python
# Current: Daily at 2:00 AM UTC
@scheduler.task('cron', id='cleanup_inactive_users', hour=2, minute=0)

# Examples:
# Run every 12 hours at 2 AM and 2 PM:
@scheduler.task('cron', id='cleanup_inactive_users', hour='2,14', minute=0)

# Run every Monday at 3:00 AM:
@scheduler.task('cron', id='cleanup_inactive_users', day_of_week='mon', hour=3, minute=0)

# Run twice daily:
@scheduler.task('interval', id='cleanup_inactive_users', hours=12)
```

### Alternative: Cron Job Setup

If you prefer running cleanup via system cron instead of APScheduler:

1. Make the script executable:
```bash
chmod +x scripts/cleanup_inactive_users.py
```

2. Edit your crontab:
```bash
crontab -e
```

3. Add the cron job (example: daily at 2 AM):
```bash
0 2 * * * cd /path/to/childfyp6 && /usr/bin/python3 scripts/cleanup_inactive_users.py >> logs/cleanup.log 2>&1
```

See `scripts/crontab.example` for more scheduling examples.

---

## Usage Guide

### For Administrators

#### Accessing the Dashboard

1. Log in with an admin account
2. Navigate to `/admin/inactive-users`
3. View the summary cards and user tables

#### Protecting an Account

To prevent a specific account from automatic deletion:

1. Find the user in any of the tables
2. Click the **"Protect"** button next to their name
3. Confirm the action
4. User will appear in the "Protected Accounts" section

**Use Cases for Protection:**
- Important test accounts
- VIP users who travel frequently
- Accounts with special exemptions
- Legacy accounts that must be preserved

#### Reactivating an Account

To reset the inactivity timer for a user:

1. Find the user in the tables
2. Click the **"Reactivate"** button
3. Their `last_login` is set to current date
4. `inactive_warning_sent` flag is cleared
5. User gets another 30-day grace period

#### Running Cleanup Manually

To trigger the cleanup process outside the scheduled time:

1. Click **"Run Cleanup Now"** button at the top
2. Confirm the action in the dialog
3. View the statistics returned:
   - Number of first warnings sent
   - Number of final warnings sent
   - Number of accounts deleted
   - Any errors encountered

#### Monitoring Cleanup Results

After each cleanup (automatic or manual), you'll see statistics:

```
Cleanup Statistics:
✉️  First warnings sent: 5
🚨 Final warnings sent: 3
❌ Accounts deleted: 2
⚠️  Errors: 0
```

### For Parent Users

#### Staying Active

To keep your account active:
- Log in at least once every 30 days
- Any successful login resets the inactivity timer

#### Responding to Warning Emails

**If you receive a warning email:**
1. Read the email carefully
2. Click the "Login Now" link
3. Log in to your account
4. Your account is automatically reactivated
5. No further action needed

**If you don't want to keep the account:**
- Simply ignore the emails
- Account will be deleted automatically at Day 30
- You'll receive a confirmation email

#### Understanding Dashboard Warnings

When you log in after being inactive:

**Yellow Warning (23-27 days):**
```
⚠️ Your account has been inactive for 24 days.
Please log in regularly to keep your account active.
Your account will be deleted in 6 days if you remain inactive.
```

**Red Warning (28+ days):**
```
🚨 URGENT: Your account will be deleted soon!
You have been inactive for 29 days. Your account will be permanently
deleted in 1 day, along with all children's data and assessments.
```

---

## Technical Details

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│           APScheduler / Cron Job                        │
│           (Triggers daily at 2:00 AM)                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│       check_inactive_users() Function                   │
│                                                          │
│  1. Query database for users matching criteria          │
│  2. Calculate days inactive for each user              │
│  3. Send appropriate emails based on threshold          │
│  4. Update database with warning timestamps             │
│  5. Delete accounts meeting deletion criteria           │
│  6. Return statistics                                   │
└─────────┬──────────────┬──────────────┬─────────────────┘
          │              │              │
          ▼              ▼              ▼
    ┌─────────┐    ┌─────────┐    ┌──────────┐
    │ Flask   │    │ MySQL   │    │ Logging  │
    │ Mail    │    │ Updates │    │ & Stats  │
    └─────────┘    └─────────┘    └──────────┘
```

### Key Functions

**`check_inactive_users()` (app.py:797-875)**
- Main cleanup function
- Queries database for inactive users
- Sends appropriate emails
- Deletes accounts when threshold reached
- Returns statistics dictionary

**Email Functions:**
- `send_inactivity_warning_email()` (app.py:595-660) - First warning
- `send_final_warning_email()` (app.py:663-733) - Final warning
- `send_deletion_confirmation_email()` (app.py:736-794) - Deletion notice

**Database Queries:**

```python
# Find users for first warning (23+ days, no warning sent yet)
users = User.query.filter(
    User.role == 'parent',
    User.is_active == True,
    User.protected_from_deletion == False,
    User.last_login <= first_warning_threshold,
    User.inactive_warning_sent == None
).all()

# Find users for final warning (28+ days, warning already sent)
users = User.query.filter(
    User.role == 'parent',
    User.is_active == True,
    User.protected_from_deletion == False,
    User.last_login <= final_warning_threshold,
    User.inactive_warning_sent != None
).all()

# Find users for deletion (30+ days)
users = User.query.filter(
    User.role == 'parent',
    User.protected_from_deletion == False
).filter(
    db.or_(
        User.last_login <= deletion_threshold,
        db.and_(
            User.last_login == None,
            User.created_at <= deletion_threshold
        )
    )
).all()
```

### Database Schema

**Users Table Additions:**

| Column | Type | Default | Description |
|--------|------|---------|-------------|
| `last_login` | TIMESTAMP | NULL | Last successful login timestamp |
| `is_active` | TINYINT(1) | 1 | Active/inactive status flag |
| `protected_from_deletion` | TINYINT(1) | 0 | Manual protection from auto-deletion |
| `inactive_warning_sent` | TIMESTAMP | NULL | When first warning was sent |

### Login Handler Integration

The login route updates `last_login` on successful authentication (app.py:488):

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... authentication logic ...

    # Update last login timestamp
    user.last_login = datetime.now()
    db.session.commit()

    # ... remaining login logic ...
```

### Cascade Deletion

Related data is automatically removed via database constraints:

```sql
-- Children table
FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE CASCADE

-- Assessments table
FOREIGN KEY (child_id) REFERENCES children(id) ON DELETE CASCADE
```

When a parent is deleted:
1. All their children records are deleted
2. All assessments for those children are deleted
3. Any other related data is cleaned up automatically

---

## Testing Guide

### Manual Testing Procedure

#### Test 1: First Warning Email (Day 23)

```sql
-- Create test parent account
INSERT INTO users (name, email, password, role, created_at, last_login)
VALUES ('Test Parent 1', 'test1@example.com', '$2b$12$hashedpassword', 'parent', NOW(), DATE_SUB(NOW(), INTERVAL 23 DAYS));

-- Run cleanup manually from admin dashboard
-- Expected: Warning email sent, inactive_warning_sent timestamp recorded
```

**Verification:**
1. Check email inbox for warning email
2. Query database: `SELECT inactive_warning_sent FROM users WHERE email='test1@example.com'`
3. Should have a timestamp

#### Test 2: Final Warning Email (Day 28)

```sql
-- Update test account to 28 days inactive
UPDATE users
SET last_login = DATE_SUB(NOW(), INTERVAL 28 DAYS),
    inactive_warning_sent = DATE_SUB(NOW(), INTERVAL 5 DAYS)
WHERE email = 'test1@example.com';

-- Run cleanup again
-- Expected: Final warning email sent
```

**Verification:**
1. Check email for final warning (red theme)
2. User should still exist in database

#### Test 3: Account Deletion (Day 30)

```sql
-- Update test account to 30 days inactive
UPDATE users
SET last_login = DATE_SUB(NOW(), INTERVAL 30 DAYS)
WHERE email = 'test1@example.com';

-- Run cleanup
-- Expected: Deletion confirmation email sent, account removed
```

**Verification:**
1. Check email for deletion confirmation
2. Query: `SELECT * FROM users WHERE email='test1@example.com'`
3. Should return 0 rows

#### Test 4: Protection Feature

```sql
-- Create protected account
INSERT INTO users (name, email, password, role, last_login, protected_from_deletion)
VALUES ('Protected User', 'protected@example.com', '$2b$12$hash', 'parent', DATE_SUB(NOW(), INTERVAL 35 DAYS), 1);

-- Run cleanup
-- Expected: Account NOT deleted despite being 35 days inactive
```

**Verification:**
1. User should still exist
2. No emails sent
3. Appears in "Protected Accounts" section

#### Test 5: Admin Exclusion

```sql
-- Create admin account with old last_login
INSERT INTO users (name, email, password, role, last_login)
VALUES ('Test Admin', 'admin@example.com', '$2b$12$hash', 'admin', DATE_SUB(NOW(), INTERVAL 60 DAYS));

-- Run cleanup
-- Expected: Account untouched, no emails sent
```

**Verification:**
1. Admin account still exists
2. No emails sent
3. Does not appear in any inactive user tables

#### Test 6: Reactivation

```sql
-- Create inactive account
INSERT INTO users (name, email, password, role, last_login, inactive_warning_sent)
VALUES ('Reactivate Test', 'reactivate@example.com', '$2b$12$hash', 'parent', DATE_SUB(NOW(), INTERVAL 25 DAYS), DATE_SUB(NOW(), INTERVAL 2 DAYS));

-- Use admin dashboard to click "Reactivate" button
-- Expected: last_login updated to NOW, inactive_warning_sent cleared
```

**Verification:**
```sql
SELECT last_login, inactive_warning_sent
FROM users
WHERE email='reactivate@example.com';
-- last_login should be recent
-- inactive_warning_sent should be NULL
```

#### Test 7: Never Logged In Scenario

```sql
-- Create account that never logged in
INSERT INTO users (name, email, password, role, created_at, last_login)
VALUES ('Never Logged In', 'never@example.com', '$2b$12$hash', 'parent', DATE_SUB(NOW(), INTERVAL 31 DAYS), NULL);

-- Run cleanup
-- Expected: Account deleted
```

### Automated Testing (Optional)

Create a test script `tests/test_inactive_users.py`:

```python
import unittest
from datetime import datetime, timedelta
from app import app, db, User, check_inactive_users

class TestInactiveUsers(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_first_warning_sent(self):
        # Create user 23 days inactive
        user = User(
            name='Test User',
            email='test@example.com',
            password='hash',
            role='parent',
            last_login=datetime.now() - timedelta(days=23)
        )
        db.session.add(user)
        db.session.commit()

        # Run cleanup
        stats = check_inactive_users()

        # Assert warning was sent
        self.assertEqual(stats['warnings_sent'], 1)

        # Verify timestamp recorded
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user.inactive_warning_sent)

    def test_admin_exclusion(self):
        # Create admin 60 days inactive
        admin = User(
            name='Admin',
            email='admin@example.com',
            role='admin',
            last_login=datetime.now() - timedelta(days=60)
        )
        db.session.add(admin)
        db.session.commit()

        # Run cleanup
        stats = check_inactive_users()

        # Assert admin still exists
        admin = User.query.filter_by(email='admin@example.com').first()
        self.assertIsNotNone(admin)

    def test_protection_flag(self):
        # Create protected user 35 days inactive
        user = User(
            name='Protected',
            email='protected@example.com',
            role='parent',
            last_login=datetime.now() - timedelta(days=35),
            protected_from_deletion=True
        )
        db.session.add(user)
        db.session.commit()

        # Run cleanup
        stats = check_inactive_users()

        # Assert user still exists
        user = User.query.filter_by(email='protected@example.com').first()
        self.assertIsNotNone(user)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m pytest tests/test_inactive_users.py -v
```

---

## Troubleshooting

### Problem: Cleanup Not Running Automatically

**Symptoms:**
- Inactive users not being processed
- No emails being sent
- Dashboard shows users should be deleted but aren't

**Solutions:**

1. **Check if APScheduler is running:**
```python
# Look for this message in Flask startup logs:
"✅ APScheduler started - Inactive user cleanup will run daily at 2:00 AM UTC"
```

2. **Verify scheduler initialization:**
```python
# In app.py, ensure these lines exist:
scheduler.init_app(app)
scheduler.start()
```

3. **Check Flask app is running continuously:**
- APScheduler only works while Flask app is running
- Consider using systemd/supervisor for production
- Or use cron job alternative (see Configuration section)

4. **Verify job is registered:**
```bash
# Access Flask shell
flask shell

# Check registered jobs
from app import scheduler
print(scheduler.get_jobs())
```

### Problem: Emails Not Being Sent

**Symptoms:**
- Cleanup runs but no emails received
- No errors in logs

**Solutions:**

1. **Check email configuration:**
```python
# Verify in config.py or environment:
print(app.config['MAIL_SERVER'])
print(app.config['MAIL_PORT'])
print(app.config['MAIL_USERNAME'])
```

2. **Test email manually:**
```python
from flask_mail import Message
from app import mail

msg = Message(
    'Test Email',
    recipients=['test@example.com'],
    body='If you receive this, email is working.'
)
mail.send(msg)
```

3. **Check spam folder:**
- Warning emails may be filtered
- Whitelist your sender email

4. **Enable Flask-Mail debug mode:**
```python
app.config['MAIL_DEBUG'] = True
```

5. **Check firewall/SMTP settings:**
- Port 587 (TLS) or 465 (SSL) must be open
- Some hosting providers block SMTP
- Consider using service like SendGrid, Mailgun, or AWS SES

### Problem: Wrong Users Being Deleted

**Symptoms:**
- Active users receiving warnings
- Admins being flagged

**Solutions:**

1. **Check last_login updates on login:**
```python
# In login route, verify this line exists:
user.last_login = datetime.now()
db.session.commit()
```

2. **Verify admin exclusion logic:**
```python
# In check_inactive_users(), ensure filter includes:
User.role == 'parent'  # Not 'admin'
```

3. **Check database timezones:**
```sql
-- Verify server timezone
SELECT @@global.time_zone, @@session.time_zone;

-- If needed, set timezone:
SET time_zone = '+00:00';  -- UTC
```

4. **Audit the query logic:**
```python
# Add debug logging:
print(f"First warning threshold: {first_warning_threshold}")
print(f"Users found: {len(users_for_first_warning)}")
for user in users_for_first_warning:
    print(f"  - {user.email}: last_login={user.last_login}")
```

### Problem: Dashboard Not Loading

**Symptoms:**
- `/admin/inactive-users` shows error
- 500 Internal Server Error

**Solutions:**

1. **Check admin authentication:**
```python
# Ensure you're logged in as admin
# Verify @admin_required decorator exists on route
```

2. **Verify database connection:**
```python
# Test query manually:
from app import db, User
users = User.query.filter_by(role='parent').all()
print(f"Found {len(users)} parent users")
```

3. **Check template file exists:**
```bash
ls -la templates/admin/inactive_users.html
```

4. **Review error logs:**
```bash
# Check Flask logs for traceback
tail -f /path/to/flask/logs/error.log
```

### Problem: Duplicate Warning Emails

**Symptoms:**
- Users receive multiple first warnings
- Emails sent every day instead of once

**Solutions:**

1. **Verify `inactive_warning_sent` is being set:**
```python
# In check_inactive_users(), after sending email:
user.inactive_warning_sent = datetime.now()
db.session.commit()
```

2. **Check filter logic:**
```python
# First warning query should include:
User.inactive_warning_sent == None  # Only users who haven't been warned
```

3. **Check for database commit:**
```python
# After updating users:
db.session.commit()  # Must be present
```

### Problem: Accounts Not Actually Deleted

**Symptoms:**
- Users past 30 days still in database
- Deletion emails sent but account exists

**Solutions:**

1. **Check for database errors:**
```python
# Wrap deletion in try/except:
try:
    db.session.delete(user)
    db.session.commit()
except Exception as e:
    print(f"Error deleting user: {e}")
    db.session.rollback()
```

2. **Verify foreign key constraints:**
```sql
-- Check if CASCADE is set:
SHOW CREATE TABLE children;
-- Should show: ON DELETE CASCADE
```

3. **Check protection flag:**
```sql
SELECT email, protected_from_deletion
FROM users
WHERE DATEDIFF(NOW(), last_login) > 30;
```

4. **Review deletion query logic:**
```python
# Ensure query doesn't have unintended filters
users_to_delete = User.query.filter(
    User.role == 'parent',
    User.protected_from_deletion == False  # Check this
).filter(...)
```

---

## Safety Features

### 1. Admin Account Protection

**How it works:**
- All queries explicitly filter `WHERE role = 'parent'`
- Admin accounts are never included in inactive user queries
- Admins can be inactive indefinitely without consequences

**Code location:** `app.py:800-875` (check_inactive_users function)

### 2. Manual Protection Override

**How it works:**
- Any account can be marked with `protected_from_deletion = 1`
- Protected accounts are excluded from all cleanup operations
- Protection status visible in admin dashboard

**Use cases:**
- VIP accounts
- Test accounts needed for development
- Special exemptions
- Accounts under investigation

### 3. Multi-Stage Warning System

**How it works:**
- Day 23: First gentle warning
- Day 28: Final urgent warning
- Day 30: Deletion

Users have **7 full days** and **2 separate emails** before any action is taken.

### 4. Easy Reactivation

**How it works:**
- Any login resets the clock
- Admins can manually reactivate from dashboard
- Simple one-click process

### 5. Transparent Communication

**How it works:**
- All emails clearly explain the policy
- Dashboard shows exact days until deletion
- No surprises or hidden actions

### 6. Database Transaction Safety

**How it works:**
- All database operations wrapped in try/except
- Automatic rollback on errors
- Prevents partial deletions

**Code example:**
```python
try:
    db.session.delete(user)
    db.session.commit()
    accounts_deleted += 1
except Exception as e:
    db.session.rollback()
    errors.append(f"Error deleting user {user.email}: {str(e)}")
```

### 7. Comprehensive Logging

**How it works:**
- Statistics returned after each cleanup
- Errors logged and displayed
- Admin can review what happened

**Statistics provided:**
```python
{
    'warnings_sent': 5,
    'final_warnings_sent': 3,
    'accounts_deleted': 2,
    'errors': []
}
```

---

## Future Enhancements

### Potential Improvements

1. **Analytics Dashboard**
   - Charts showing deletion trends over time
   - User engagement metrics
   - Reactivation rate statistics

2. **Customizable Thresholds per User Type**
   - Different timeframes for different parent categories
   - VIP users get 60 days instead of 30
   - Configurable via admin UI

3. **SMS Notifications**
   - Add phone number field to users
   - Send SMS in addition to email
   - Higher engagement rate

4. **Soft Delete Option**
   - Archive instead of permanently delete
   - Allow account recovery within 90 days
   - "Restore Account" feature

5. **Export Reports**
   - CSV export of inactive users
   - Email report to admin before bulk deletion
   - Audit trail of all deletions

6. **Graduated Warning System**
   - More than 2 warnings for high-value accounts
   - Escalating email frequency
   - Different messaging for different scenarios

7. **Re-engagement Campaigns**
   - Personalized reactivation emails
   - Special offers or incentives
   - Surveys to understand why users stopped

8. **API Endpoints**
   - RESTful API for external monitoring
   - Webhook notifications
   - Integration with other systems

9. **Machine Learning Prediction**
   - Predict which users are likely to become inactive
   - Proactive engagement before inactivity
   - Personalized retention strategies

10. **Localization**
    - Multi-language email templates
    - Timezone-aware scheduling
    - Regional policy variations

---

## File Structure

```
childfyp6/
├── app.py                              # Main application with cleanup logic
├── config.py                           # Configuration settings
├── requirements.txt                    # Python dependencies
│
├── db/
│   └── database_schema.sql            # Database schema with new columns
│
├── scripts/
│   ├── cleanup_inactive_users.py      # Standalone cleanup script
│   └── crontab.example                # Example cron configurations
│
├── templates/
│   └── admin/
│       └── inactive_users.html        # Admin dashboard UI
│
└── logs/
    └── cleanup.log                    # Cleanup execution logs (if using cron)
```

---

## API Reference

### Function: `check_inactive_users()`

**Location:** `app.py:797-875`

**Purpose:** Main cleanup function that identifies inactive users, sends warnings, and deletes accounts.

**Parameters:** None

**Returns:** Dictionary with statistics
```python
{
    'warnings_sent': int,           # Number of first warnings sent
    'final_warnings_sent': int,      # Number of final warnings sent
    'accounts_deleted': int,         # Number of accounts deleted
    'errors': [str]                  # List of error messages
}
```

**Usage:**
```python
from app import check_inactive_users

# Run cleanup manually
stats = check_inactive_users()
print(f"Cleanup completed: {stats}")
```

### Function: `send_inactivity_warning_email(user)`

**Location:** `app.py:595-660`

**Purpose:** Send first warning email (Day 23)

**Parameters:**
- `user` (User object): The user to send warning to

**Returns:** None

### Function: `send_final_warning_email(user)`

**Location:** `app.py:663-733`

**Purpose:** Send final warning email (Day 28)

**Parameters:**
- `user` (User object): The user to send final warning to

**Returns:** None

### Function: `send_deletion_confirmation_email(user)`

**Location:** `app.py:736-794`

**Purpose:** Send deletion confirmation email

**Parameters:**
- `user` (User object): The user whose account was deleted

**Returns:** None

---

## Support & Contact

### Getting Help

1. **Check this documentation first**
2. **Review error logs** for specific issues
3. **Test email configuration** manually
4. **Verify database schema** is up to date

### Common Questions

**Q: Can I change the 30-day threshold?**
A: Yes, modify the `timedelta(days=30)` values in `check_inactive_users()` function.

**Q: What happens to children's data when parent is deleted?**
A: All related data (children, assessments) is automatically deleted via CASCADE constraints.

**Q: Can deleted accounts be recovered?**
A: No, deletion is permanent. Implement soft-delete feature if recovery is needed.

**Q: Why aren't emails being sent?**
A: Check SMTP configuration, firewall rules, and spam folders. Enable `MAIL_DEBUG` for detailed logs.

**Q: Can I run cleanup more frequently than daily?**
A: Yes, modify the scheduler cron expression or use interval-based scheduling.

---

## License

This feature is part of the Child Development Tracking System project.

---

## Changelog

### Version 1.0 (2025-01-28)
- ✅ Initial implementation
- ✅ 4-phase lifecycle management
- ✅ Admin dashboard with statistics
- ✅ Email notification system (3 templates)
- ✅ APScheduler integration
- ✅ Protection and reactivation features
- ✅ Admin exclusion logic
- ✅ User dashboard warnings

---

## Credits

Developed as part of the Child Development Tracking System project for managing parent user accounts efficiently and securely.

---

**Last Updated:** 2025-01-28
**Version:** 1.0
**Author:** Child Development Tracking System Team
