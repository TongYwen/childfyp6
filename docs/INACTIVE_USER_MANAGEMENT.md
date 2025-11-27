# Inactive User Management System

## Overview

The Inactive User Management System automatically monitors user login activity and helps maintain a clean user database by removing inactive accounts. The system implements **Option 3: Automatic deletion with admin override**, providing full automation while maintaining administrator control.

## Features

### 🔄 Automated Process
- **Day 23**: System sends first warning email (7 days before deletion)
- **Day 28**: System sends final warning email (2 days before deletion)
- **Day 30**: System automatically deletes inactive accounts
- Users can reactivate their account simply by logging in

### 🛡️ Admin Controls
- **Protect Users**: Mark specific users as "protected" to exempt them from auto-deletion
- **Manual Activation**: Manually reactivate user accounts
- **Manual Cleanup**: Trigger cleanup process manually from admin dashboard
- **Activity Monitoring**: View all users categorized by activity status

### 📧 Email Notifications
- **First Warning** (23 days): Friendly reminder with 7-day notice
- **Final Warning** (28 days): Urgent notification with 2-day notice
- **Deletion Confirmation**: Email sent after account deletion

### 👤 User Experience
- Warning banner appears on user dashboard when at risk
- Login automatically reactivates account
- Clear messaging about account status

## Database Schema Changes

### New Fields in `users` Table
```sql
ALTER TABLE `users`
ADD COLUMN `last_login` timestamp NULL DEFAULT NULL,
ADD COLUMN `is_active` tinyint(1) DEFAULT 1,
ADD COLUMN `protected_from_deletion` tinyint(1) DEFAULT 0,
ADD COLUMN `inactive_warning_sent` timestamp NULL DEFAULT NULL;
```

### Field Descriptions
- **last_login**: Timestamp of user's last successful login
- **is_active**: Boolean flag indicating if account is active (1) or deactivated (0)
- **protected_from_deletion**: Admin-controlled flag to prevent automatic deletion
- **inactive_warning_sent**: Timestamp when first warning email was sent

## Installation & Setup

### 1. Database Migration
Run the migration script to update your database:
```bash
mysql -u username -p database_name < db/migrations/add_inactive_user_management.sql
```

### 2. Install Dependencies
Install the required Python package:
```bash
pip install flask-apscheduler
# OR
pip install -r requirements.txt
```

### 3. Verify Email Configuration
Ensure your `.env` file has proper email settings:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### 4. Automated Cleanup (Built-in Scheduler)

**✅ Default Method: Flask-APScheduler (No Cron Needed!)**

The system now uses Flask-APScheduler to run cleanup automatically. When you start your Flask app, the scheduler starts automatically and runs cleanup daily at 2:00 AM UTC.

```bash
python app.py
# You'll see: ✅ APScheduler started - Inactive user cleanup will run daily at 2:00 AM UTC
```

**That's it!** As long as your Flask app is running, cleanup runs automatically daily.

#### Customizing the Schedule

To change the cleanup time, edit `app.py` line ~923:

```python
# Default: Daily at 2:00 AM UTC
@scheduler.task('cron', id='cleanup_inactive_users', hour=2, minute=0)

# Example: Daily at midnight
@scheduler.task('cron', id='cleanup_inactive_users', hour=0, minute=0)

# Example: Every 12 hours
@scheduler.task('cron', id='cleanup_inactive_users', hour='*/12', minute=0)

# Example: Weekly on Monday at 3 AM
@scheduler.task('cron', id='cleanup_inactive_users', day_of_week='mon', hour=3, minute=0)
```

**Note:** You can still use the manual "Run Cleanup Now" button in the admin dashboard anytime!

#### Alternative: Using crontab (Optional - if you prefer external cron)
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * cd /path/to/childfyp6 && /usr/bin/python3 scripts/cleanup_inactive_users.py >> logs/cleanup.log 2>&1
```

#### Option B: Using systemd timer (Linux)
Create `/etc/systemd/system/cleanup-inactive-users.service`:
```ini
[Unit]
Description=Cleanup Inactive Users
After=network.target

[Service]
Type=oneshot
User=www-data
WorkingDirectory=/path/to/childfyp6
ExecStart=/usr/bin/python3 /path/to/childfyp6/scripts/cleanup_inactive_users.py
StandardOutput=append:/path/to/childfyp6/logs/cleanup.log
StandardError=append:/path/to/childfyp6/logs/cleanup.log
```

Create `/etc/systemd/system/cleanup-inactive-users.timer`:
```ini
[Unit]
Description=Run Cleanup Inactive Users Daily
Requires=cleanup-inactive-users.service

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start the timer:
```bash
sudo systemctl enable cleanup-inactive-users.timer
sudo systemctl start cleanup-inactive-users.timer
```

### 4. Create Logs Directory
```bash
mkdir -p /path/to/childfyp6/logs
chmod 755 /path/to/childfyp6/logs
```

## Admin Dashboard Usage

### Accessing Inactive User Management
1. Log in as admin
2. Go to Admin Dashboard
3. Click "Inactive User Management"

### User Categories
- **🔴 Pending Deletion**: Users inactive for 30+ days (will be deleted on next cleanup)
- **🟡 At Risk**: Users inactive for 23-29 days (receiving warnings)
- **🟢 Active**: Users with recent activity (less than 23 days)
- **🔵 Protected**: Users exempt from automatic deletion

### Admin Actions

#### Protect a User
Click "Protect" button next to any user to exempt them from automatic deletion. Protected users will never be automatically deleted, regardless of inactivity.

#### Unprotect a User
Click "Unprotect" button next to protected users to remove deletion exemption.

#### Reactivate Account
Click "Reactivate" to manually reset a user's `last_login` to today, giving them a fresh 30-day period.

#### Manual Cleanup
Click "Run Cleanup Now" to immediately trigger the automated cleanup process (useful for testing or emergency cleanup).

## User Experience

### Warning Banner
When users log in after being inactive for 23+ days, they see a warning banner on their dashboard:

- **Yellow Warning** (23-27 days): "Your account will be deleted in X days"
- **Red Critical Warning** (28-30 days): "URGENT: Account deletion in X days!"

The banner also confirms that by logging in, they have reactivated their account.

### Email Notifications

#### First Warning (Day 23)
```
Subject: ChildGrowth Insights - Account Inactivity Warning

Your account will be automatically deleted in 7 days due to inactivity.
To keep your account active, simply log in.
```

#### Final Warning (Day 28)
```
Subject: ChildGrowth Insights - URGENT: Account Deletion in 2 Days

URGENT: Your account will be permanently deleted in 2 days!
Once deleted, all your data will be permanently lost.
Log in now to save your account.
```

#### Deletion Confirmation (Day 30)
```
Subject: ChildGrowth Insights - Account Deleted

Your account has been permanently deleted due to 30 days of inactivity.
All your data has been removed from our system.
```

## Technical Details

### Cleanup Function Logic

```python
def check_inactive_users():
    # 1. Find users inactive 23+ days → Send first warning
    # 2. Find users inactive 28+ days → Send final warning
    # 3. Find users inactive 30+ days → Delete account
    # 4. Check never-logged-in users created 30+ days ago → Delete
```

### Login Handler Updates
On successful login:
1. Update `last_login` to current timestamp
2. Set `is_active = 1`
3. Clear `inactive_warning_sent` (reset warning state)

### Protection Logic
- Protected users (`protected_from_deletion = 1`) are excluded from all cleanup queries
- Admins can toggle protection status at any time
- Protection status is visible in admin dashboard

## Testing

### Manual Testing
1. Create a test user account
2. Manually set `last_login` to 25 days ago:
   ```sql
   UPDATE users SET last_login = DATE_SUB(NOW(), INTERVAL 25 DAY) WHERE email = 'test@example.com';
   ```
3. Run manual cleanup from admin dashboard
4. Check email for warning notification
5. Check user appears in "At Risk" category

### Automated Testing
Run the cleanup script manually:
```bash
cd /path/to/childfyp6
python3 scripts/cleanup_inactive_users.py
```

Check the output for:
- Number of warnings sent
- Number of accounts deleted
- Any errors encountered

## Monitoring & Logs

### Log File Location
```
/path/to/childfyp6/logs/cleanup.log
```

### Log Format
```
============================================================
Inactive User Cleanup - 2025-11-27 02:00:00
============================================================

Cleanup Results:
  - First warnings sent: 3
  - Final warnings sent: 1
  - Accounts deleted: 2

No errors encountered.

============================================================
Cleanup completed successfully!
============================================================
```

### Monitoring Best Practices
1. Check logs weekly to ensure cleanup runs successfully
2. Monitor error rates
3. Review deleted accounts monthly
4. Keep backups before mass deletions

## Troubleshooting

### Issue: Emails not sending
**Solution**:
- Check email configuration in `.env`
- Verify SMTP credentials
- Test email function manually from Python console

### Issue: Cron job not running
**Solution**:
- Check cron logs: `grep CRON /var/log/syslog`
- Verify script permissions: `ls -la scripts/cleanup_inactive_users.py`
- Test script manually: `python3 scripts/cleanup_inactive_users.py`

### Issue: Users not being deleted
**Solution**:
- Check if users are protected
- Verify `last_login` timestamps in database
- Review cleanup logs for errors
- Run manual cleanup from admin dashboard

### Issue: Wrong user deleted
**Solution**:
- Check database backups
- Review deletion criteria (30 days inactive, not protected)
- Consider protecting critical users
- Adjust inactivity threshold if needed

## Security Considerations

1. **Admin Protection**: Recommend protecting all admin accounts
2. **Backup First**: Always backup database before running cleanup
3. **Email Verification**: Ensure emails reach users (check spam folders)
4. **Grace Period**: 30-day period provides ample time for users to respond
5. **Irreversible**: Deletions are permanent; no recovery mechanism

## Customization

### Adjust Inactivity Thresholds
Edit `app.py` function `check_inactive_users()`:
```python
warning_threshold = now - timedelta(days=23)  # Change to desired days
final_warning_threshold = now - timedelta(days=28)
deletion_threshold = now - timedelta(days=30)
```

### Customize Email Templates
Edit email functions in `app.py`:
- `send_inactivity_warning_email()`
- `send_final_warning_email()`
- `send_deletion_confirmation_email()`

### Change Warning Schedule
Modify the query logic to send warnings at different intervals.

## API Endpoints

### Admin Endpoints
- `GET /admin/inactive-users` - View inactive user dashboard
- `POST /admin/users/<id>/toggle-protection` - Toggle user protection status
- `POST /admin/users/<id>/activate` - Manually activate user account
- `POST /admin/run-cleanup` - Manually trigger cleanup process

## Future Enhancements

Potential improvements:
- [ ] Add user preference for email notification frequency
- [ ] Implement "vacation mode" to pause deletion countdown
- [ ] Add data export option before deletion
- [ ] Create audit log of all deletions
- [ ] Add configurable thresholds per user role
- [ ] Implement account suspension before deletion
- [ ] Add SMS notifications as alternative to email

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review application logs
3. Contact system administrator

---

**Last Updated**: 2025-11-27
**Version**: 1.0.0
