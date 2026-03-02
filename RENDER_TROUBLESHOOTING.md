# 🔧 Render Deployment Troubleshooting Guide

## Current Issue: Login Error

If you're seeing "An error occurred during login. Please try again.", follow these steps:

### Step 1: Check Health Endpoint

Visit your app URL + `/api/health`:
```
https://trial-one-nu.onrender.com/api/health
```

**Expected Response (Healthy):**
```json
{
  "status": "healthy",
  "database": "connected",
  "users": 2,
  "message": "Application is running correctly"
}
```

**If Unhealthy:**
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "error": "...",
  "message": "Database connection failed"
}
```

### Step 2: Check Render Logs

1. Go to https://dashboard.render.com
2. Click on your service "trial-1"
3. Click "Logs" tab
4. Look for these messages:

**Success Messages:**
```
✓ Database connection successful
✓ Database tables created/verified
✓ Database already initialized
```

**Error Messages:**
```
❌ Database initialization error: ...
Error type: ...
Traceback: ...
```

### Step 3: Verify Environment Variables

In Render Dashboard → Environment:

1. **DATABASE_URL** - Should be set (from PostgreSQL database)
2. **SECRET_KEY** - Should be auto-generated
3. **PYTHON_VERSION** - Should be 3.11.9

### Step 4: Manual Database Initialization

If automatic initialization failed, run manually:

1. Go to Render Dashboard
2. Click on your service
3. Click "Shell" tab (or use SSH)
4. Run:
```bash
python force_init_db.py
```

This will:
- Test database connection
- Create all tables
- Create default users
- Insert sample data
- Show detailed error messages if it fails

### Step 5: Check PostgreSQL Database

1. Go to Render Dashboard
2. Click on "digital-catalyst-db" (your PostgreSQL database)
3. Verify it's running and not suspended
4. Check "Info" tab for connection details

### Step 6: Restart Service

Sometimes a simple restart helps:

1. Go to Render Dashboard
2. Click on your service
3. Click "Manual Deploy" → "Clear build cache & deploy"

Or use the restart button in the top right.

## Common Issues & Solutions

### Issue 1: Database Not Connected

**Symptoms:**
- Health check shows "disconnected"
- Login fails immediately
- Logs show connection errors

**Solutions:**
1. Verify DATABASE_URL is set correctly
2. Check PostgreSQL database is running
3. Ensure database hasn't expired (free tier: 90 days)
4. Try restarting both database and web service

### Issue 2: Tables Not Created

**Symptoms:**
- Health check shows 0 users
- Login fails with "no such table" error
- Logs show table creation errors

**Solutions:**
1. Run `python force_init_db.py` in Shell
2. Check database permissions
3. Verify SQLAlchemy models are correct
4. Check for migration errors in logs

### Issue 3: Users Not Created

**Symptoms:**
- Health check shows 0 users
- Login fails with "invalid credentials"
- Database connected but empty

**Solutions:**
1. Run `python force_init_db.py` in Shell
2. Check initialization logs for errors
3. Verify password hashing is working
4. Check User model for issues

### Issue 4: Wrong DATABASE_URL Format

**Symptoms:**
- Connection errors mentioning "postgres://"
- SQLAlchemy errors about dialect

**Solutions:**
The app automatically fixes this, but verify:
```python
# In app.py, this should exist:
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
```

### Issue 5: Timeout Errors

**Symptoms:**
- 504 Gateway Timeout
- Gunicorn worker timeout
- Slow responses

**Solutions:**
1. Increase timeout in render.yaml (already set to 120s)
2. Check database query performance
3. Verify no infinite loops in code
4. Check for blocking operations

## Debugging Commands

### In Render Shell:

**Test Database Connection:**
```bash
python -c "from app import app, db; from sqlalchemy import text; app.app_context().push(); db.session.execute(text('SELECT 1')); print('✓ Connected')"
```

**Count Users:**
```bash
python -c "from app import app, db; from models import User; app.app_context().push(); print(f'Users: {User.query.count()}')"
```

**List All Users:**
```bash
python -c "from app import app, db; from models import User; app.app_context().push(); users = User.query.all(); [print(f'{u.username} - {u.role}') for u in users]"
```

**Force Initialize:**
```bash
python force_init_db.py
```

**Check Tables:**
```bash
python -c "from app import app, db; app.app_context().push(); print(db.engine.table_names())"
```

## Manual Database Setup (Last Resort)

If all else fails, manually create the admin user:

```bash
python << EOF
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    
    # Check if admin exists
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@digitalcatalyst.in',
            password=generate_password_hash('admin123'),
            role='user'
        )
        db.session.add(admin)
        db.session.commit()
        print('✓ Admin user created')
    else:
        print('✓ Admin user already exists')
EOF
```

## Verification Checklist

After fixing, verify:

- [ ] Health endpoint returns "healthy"
- [ ] Health endpoint shows users > 0
- [ ] Login page loads
- [ ] Can login with admin/admin123
- [ ] Dashboard loads after login
- [ ] Heritage sites display
- [ ] No errors in Render logs

## Getting Help

If none of these solutions work:

1. **Check Render Logs** - Copy full error messages
2. **Check Health Endpoint** - Note the exact error
3. **Run force_init_db.py** - Copy the output
4. **Check Database Status** - Verify it's running

Then provide:
- Error messages from logs
- Health endpoint response
- force_init_db.py output
- Database status

## Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| Login fails | Run `python force_init_db.py` |
| 0 users | Run `python force_init_db.py` |
| DB disconnected | Check DATABASE_URL, restart service |
| Timeout | Already fixed (120s timeout) |
| Tables missing | Run `python force_init_db.py` |

## Next Steps

1. Try the health endpoint first
2. Check Render logs for errors
3. Run force_init_db.py if needed
4. Verify with health endpoint again
5. Test login

---

**Your app should work after following these steps!** 🎉
