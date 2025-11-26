# Session Management Test Checklist

## Pre-Test Setup
- [ ] Change timeout to 2 minutes in config.py (line 26)
- [ ] Change timeout to 2 minutes in app.py (line 125)
- [ ] Start app: `python3 app.py`

## Test 1: Parent Session Timeout
- [ ] Login as parent user
- [ ] Wait 2 minutes without activity
- [ ] Click any page
- [ ] Expected: "Your session has expired" message + redirect to login

## Test 2: Parent Activity Refresh
- [ ] Login as parent user
- [ ] Click pages every 30 seconds for 5 minutes
- [ ] Expected: Stay logged in (no timeout)

## Test 3: Admin No Timeout
- [ ] Login as admin user
- [ ] Wait 5+ minutes without activity
- [ ] Click any admin page
- [ ] Expected: Stay logged in (no timeout)

## Test 4: Session Regeneration
- [ ] Open DevTools → Application → Cookies
- [ ] Note session cookie value before login
- [ ] Login (parent or admin)
- [ ] Note session cookie value after login
- [ ] Expected: Cookie value changed

## Test 5: Secure Cookie Flags
- [ ] Check DevTools → Cookies
- [ ] Expected: HttpOnly ✓, SameSite = Lax

## Test 6: Logout Cleanup
- [ ] Login as any user
- [ ] Click Logout
- [ ] Check DevTools → Cookies
- [ ] Expected: Session cookie deleted
- [ ] Try accessing /dashboard directly
- [ ] Expected: Redirect to login

## Post-Test Cleanup
- [ ] Change timeout back to 30 minutes in config.py
- [ ] Change timeout back to 30 minutes in app.py
- [ ] Commit changes if needed

## Test Results
Parent Timeout: ____
Admin No Timeout: ____
Session Security: ____
Logout Cleanup: ____
