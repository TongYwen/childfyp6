# Session Management & Timeout Features

## Overview
This application now includes comprehensive session management and timeout features to ensure secure authentication.

## Features Implemented

### 1. **Session Timeout**
- **Default Timeout**: 30 minutes of inactivity
- Users are automatically logged out after 30 minutes of no activity
- Configurable via environment variable `SESSION_TIMEOUT_MINUTES`

### 2. **Remember Me Functionality**
- Users can choose to stay logged in for 30 days
- Checkbox available on the login page
- If unchecked, session expires when browser closes

### 3. **Session Security**
- **Strong Session Protection**: Prevents session hijacking
- **HTTP-Only Cookies**: Prevents XSS attacks from stealing session cookies
- **SameSite Cookies**: Prevents CSRF attacks
- **Secure Cookies**: Can be enabled for HTTPS in production

### 4. **Activity Tracking**
- Last activity timestamp tracked for each user
- Automatic session refresh on user activity
- Clear session timeout message when session expires

## Configuration

### Environment Variables (.env file)

Add these optional configurations to your `.env` file:

```bash
# Session timeout in minutes (default: 30)
SESSION_TIMEOUT_MINUTES=30

# Enable secure cookies in production (requires HTTPS)
SESSION_COOKIE_SECURE=False  # Set to True in production with HTTPS
```

### Default Settings (config.py)

```python
# Session timeout: 30 minutes by default
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

# Cookie security settings
SESSION_COOKIE_SECURE = False  # Set True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
```

## How It Works

### Login Process
1. User enters credentials
2. Optionally checks "Remember me for 30 days"
3. If Remember Me is checked:
   - Session persists for 30 days
4. If Remember Me is NOT checked:
   - Session expires when browser closes
   - Still subject to 30-minute inactivity timeout

### Session Timeout
1. Each user request updates the `last_activity` timestamp
2. Before each request, the system checks:
   - If user is authenticated
   - Time since last activity
3. If inactivity exceeds 30 minutes:
   - User is automatically logged out
   - Session is cleared
   - User sees: "Your session has expired due to inactivity. Please log in again."

### Logout Process
1. User clicks logout
2. User session is terminated
3. All session data is cleared
4. User is redirected to login page

## Testing the Features

### Test Inactivity Timeout
1. Log in to the application
2. Wait for 30 minutes without any activity
3. Try to navigate to any page
4. You should be automatically logged out with a timeout message

### Test Remember Me
1. Log in and check the "Remember me" checkbox
2. Close the browser completely
3. Reopen the browser and navigate to the app
4. You should still be logged in (valid for 30 days)

### Test Normal Login
1. Log in WITHOUT checking "Remember me"
2. Close the browser completely
3. Reopen the browser and navigate to the app
4. You should be logged out

### Test Manual Logout
1. Log in to the application
2. Click the logout button
3. Verify you're redirected to the login page
4. Try to go back to a protected page
5. You should be redirected to login

## Security Best Practices

### For Development
- `SESSION_COOKIE_SECURE = False` (allows HTTP)
- Keep `SESSION_COOKIE_HTTPONLY = True`
- Keep `SESSION_COOKIE_SAMESITE = "Lax"`

### For Production
- `SESSION_COOKIE_SECURE = True` (requires HTTPS)
- Keep `SESSION_COOKIE_HTTPONLY = True`
- Consider `SESSION_COOKIE_SAMESITE = "Strict"` for extra security

## Customization

### Change Timeout Duration
Edit your `.env` file:
```bash
# Set timeout to 60 minutes
SESSION_TIMEOUT_MINUTES=60

# Set timeout to 15 minutes
SESSION_TIMEOUT_MINUTES=15
```

### Change Remember Me Duration
Edit `app.py` - look for the `login_user()` call:
```python
# Default is 30 days, change the duration in config.py
# or by setting REMEMBER_COOKIE_DURATION
```

## Files Modified

1. **config.py** - Added session configuration
2. **app.py** - Added:
   - Session timeout middleware (`manage_session()`)
   - Remember me functionality
   - Enhanced login/logout routes
3. **templates/login.html** - Added "Remember Me" checkbox

## Troubleshooting

### Sessions Expiring Too Quickly
- Check `SESSION_TIMEOUT_MINUTES` in your `.env` file
- Ensure the value is in minutes (e.g., 30 for 30 minutes)

### Remember Me Not Working
- Ensure the checkbox is checked during login
- Check browser cookie settings (cookies must be enabled)
- Clear browser cookies and try again

### Getting Logged Out Unexpectedly
- This is normal if inactive for 30+ minutes
- Check your activity - the timeout resets with each request
- Consider increasing `SESSION_TIMEOUT_MINUTES` if needed
