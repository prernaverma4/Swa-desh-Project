# 📋 Complete Pre-Deployment Checklist for Render

## Overview

This guide covers everything you need to do BEFORE deploying to Render.

---

## 🔍 Project Analysis

### Database Used
- **Development:** SQLite (local file-based database)
- **Production (Render):** PostgreSQL (cloud database)
- **Auto-switching:** App automatically uses PostgreSQL when DATABASE_URL is set

### Chatbot
- **Type:** Rule-based chatbot (no external API)
- **Location:** `chatbot.py`
- **API Keys Needed:** ❌ None! It's a simple pattern-matching chatbot
- **Works offline:** ✅ Yes, no internet API calls

### External Services
- **None required!** Your app is self-contained
- No OpenAI, no external APIs, no third-party services

---

## ✅ Pre-Deployment Checklist

### Step 1: Verify Local Setup Works

```bash
# 1. Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run locally
python app.py

# 4. Test in browser
# Visit: http://localhost:5002
# Login: admin / admin123
# Test all features
```

**Verify:**
- [ ] App starts without errors
- [ ] Login works
- [ ] Heritage sites display
- [ ] Artisans display
- [ ] Chatbot responds
- [ ] Dashboard loads
- [ ] All pages accessible

---

### Step 2: Environment Variables Setup

#### For Local Development (.env file)

Create a `.env` file (optional for local):
```bash
SECRET_KEY=your-local-secret-key-change-this
DATABASE_URL=sqlite:///instance/database.db
FLASK_ENV=development
PORT=5002
```

**Note:** The app works without .env file locally (uses defaults)

#### For Render Production

You'll set these in Render Dashboard (NOT in code):

| Variable | Value | Required | Notes |
|----------|-------|----------|-------|
| `SECRET_KEY` | Auto-generated | ✅ Yes | Render generates this automatically |
| `DATABASE_URL` | Auto-set | ✅ Yes | Comes from PostgreSQL database |
| `PYTHON_VERSION` | 3.11.9 | ✅ Yes | Set in render.yaml |
| `PORT` | Auto-set | ✅ Yes | Render sets this automatically |

**Important:** 
- ❌ Don't hardcode secrets in code
- ❌ Don't commit .env to git (already in .gitignore)
- ✅ Use Render's environment variables UI

---

### Step 3: Database Configuration

#### Local Database (SQLite)
- **File:** `instance/database.db`
- **Auto-created:** Yes, when you run the app
- **Location:** Local filesystem
- **Backup:** Copy the file

#### Production Database (PostgreSQL on Render)

**Setup in Render:**

1. **Create PostgreSQL Database:**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Settings:
     - Name: `digital-catalyst-db`
     - Database: `digital_catalyst`
     - User: `digital_catalyst_user`
     - Region: Same as your web service
     - Plan: Free (or paid for production)

2. **Connection Details:**
   - Render provides these automatically:
     - Internal Database URL (for your app)
     - External Database URL (for external tools)
   - Your app uses Internal Database URL automatically

3. **Database Initialization:**
   - Happens automatically on first app start
   - Creates all tables
   - Inserts default users and sample data

**No manual SQL needed!** The app handles everything.

---

### Step 4: Files to Check Before Deployment

#### ✅ Required Files (Already Present)

1. **requirements.txt** - Python dependencies
   ```
   Flask==3.0.0
   Flask-Login==0.6.3
   Flask-SQLAlchemy==3.1.1
   gunicorn==21.2.0
   Werkzeug==3.0.1
   psycopg2-binary==2.9.9
   ```

2. **runtime.txt** - Python version
   ```
   python-3.11.9
   ```

3. **Procfile** - How to start the app
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

4. **render.yaml** - Render configuration
   ```yaml
   services:
     - type: web
       name: digital-catalyst
       env: python
       buildCommand: pip install --upgrade pip && pip install -r requirements.txt
       startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --log-level info
       envVars:
         - key: PYTHON_VERSION
           value: 3.11.9
         - key: SECRET_KEY
           generateValue: true
         - key: DATABASE_URL
           fromDatabase:
             name: digital-catalyst-db
             property: connectionString
   
   databases:
     - name: digital-catalyst-db
       databaseName: digital_catalyst
       user: digital_catalyst_user
   ```

#### ✅ Files to Verify

Check these files exist and are correct:

```bash
# Check all required files
ls -la requirements.txt runtime.txt Procfile render.yaml app.py models.py

# Verify .gitignore excludes sensitive files
cat .gitignore
# Should include: .env, *.db, instance/, __pycache__/
```

---

### Step 5: Git Repository Setup

#### Verify Git Status

```bash
# Check current status
git status

# Should show: "nothing to commit, working tree clean"
# If not, commit changes:
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### Verify GitHub Repository

1. Go to: https://github.com/pankajrajbhar19/trial
2. Check:
   - [ ] All files are pushed
   - [ ] Latest commit is visible
   - [ ] No .env or database files committed
   - [ ] render.yaml is present

---

### Step 6: Security Checklist

#### ✅ Verify These Security Measures

- [ ] No hardcoded passwords in code
- [ ] No API keys in code (none needed!)
- [ ] .env file in .gitignore
- [ ] Database files in .gitignore
- [ ] SECRET_KEY uses environment variable
- [ ] Passwords are hashed (using werkzeug)
- [ ] SQL injection protected (using SQLAlchemy ORM)

#### ⚠️ Change Default Credentials After Deployment

Default users created:
- Username: `admin` / Password: `admin123`
- Username: `manufacturer` / Password: `manufacturer123`

**Action:** Change these passwords immediately after first login!

---

## 🚀 Deployment Steps (On Render)

### Option 1: Blueprint Deployment (Recommended)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign in or create account

2. **Create New Blueprint**
   - Click "New +" → "Blueprint"
   - Connect GitHub account (if not connected)
   - Select repository: `pankajrajbhar19/trial`
   - Branch: `main`

3. **Review Configuration**
   - Render reads `render.yaml` automatically
   - Shows: 1 Web Service + 1 PostgreSQL Database
   - Click "Apply"

4. **Wait for Deployment**
   - Build time: 3-5 minutes
   - Database creation: 1-2 minutes
   - Total: ~5-7 minutes

5. **Get Your URL**
   - Format: `https://digital-catalyst-xxxx.onrender.com`
   - Or custom domain if configured

### Option 2: Manual Deployment

If Blueprint doesn't work:

1. **Create PostgreSQL Database First**
   - New + → PostgreSQL
   - Name: `digital-catalyst-db`
   - Plan: Free
   - Create Database
   - Copy "Internal Database URL"

2. **Create Web Service**
   - New + → Web Service
   - Connect repository: `pankajrajbhar19/trial`
   - Name: `digital-catalyst`
   - Environment: Python 3
   - Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`
   - Plan: Free

3. **Set Environment Variables**
   - Go to Environment tab
   - Add:
     - `DATABASE_URL`: Paste Internal Database URL
     - `SECRET_KEY`: Generate random string (or let Render auto-generate)
     - `PYTHON_VERSION`: 3.11.9

4. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete

---

## 🔧 Post-Deployment Verification

### Step 1: Check Health Endpoint

Visit: `https://your-app.onrender.com/api/health`

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "users": 2,
  "message": "Application is running correctly"
}
```

### Step 2: Check Logs

In Render Dashboard:
1. Click your service
2. Go to "Logs" tab
3. Look for:
   ```
   ✓ Database connection successful
   ✓ Database tables created/verified
   ✓ Database already initialized
   ```

### Step 3: Test Login

1. Visit your app URL
2. Click "Sign In"
3. Enter: `admin` / `admin123`
4. Should redirect to dashboard

### Step 4: Test Features

- [ ] Browse heritage sites
- [ ] View site details
- [ ] Add bookmark
- [ ] Submit review
- [ ] Chat with chatbot
- [ ] View analytics (admin)
- [ ] Browse artisans
- [ ] View products

---

## 🐛 Troubleshooting

### If Health Check Fails

```bash
# In Render Shell, run:
python force_init_db.py
```

This will:
- Test database connection
- Create tables
- Insert default users
- Show detailed errors

### If Login Fails

1. Check health endpoint shows users > 0
2. Check logs for initialization errors
3. Run `force_init_db.py` in Shell
4. Restart service

### If Database Connection Fails

1. Verify DATABASE_URL is set
2. Check PostgreSQL database is running
3. Ensure database hasn't expired (free tier: 90 days)
4. Try restarting both services

---

## 📊 Environment Variables Summary

### Required (Auto-set by Render)

| Variable | Source | Example |
|----------|--------|---------|
| DATABASE_URL | PostgreSQL database | `postgresql://user:pass@host/db` |
| SECRET_KEY | Auto-generated | Random string |
| PORT | Render platform | `10000` |

### Optional (Already in render.yaml)

| Variable | Value | Purpose |
|----------|-------|---------|
| PYTHON_VERSION | 3.11.9 | Python runtime version |

### NOT Needed

- ❌ No OpenAI API key
- ❌ No external API keys
- ❌ No email service keys
- ❌ No payment gateway keys
- ❌ No cloud storage keys

**Your app is completely self-contained!**

---

## 🎯 Quick Reference

### Chatbot Details
- **Type:** Rule-based (pattern matching)
- **File:** `chatbot.py`
- **API:** None (works offline)
- **Features:**
  - Answers questions about heritage sites
  - Helps find artisans by state
  - Explains how to use the platform
  - Provides registration/login help

### Database Details
- **Local:** SQLite (file: `instance/database.db`)
- **Production:** PostgreSQL (Render managed)
- **Tables:** User, HeritageSite, Artisan, Product, Order, Bookmark, SiteView, Review, Hotel, HotelBooking
- **Auto-migration:** Yes (creates tables automatically)

### Default Data
- **Users:** 2 (admin, manufacturer)
- **Heritage Sites:** 8 (Taj Mahal, Red Fort, etc.)
- **Artisans:** 8 (various crafts from different states)

---

## ✅ Final Checklist Before Deployment

- [ ] Local app runs without errors
- [ ] All features tested locally
- [ ] Git repository is up to date
- [ ] No sensitive data in code
- [ ] .gitignore is correct
- [ ] requirements.txt is complete
- [ ] runtime.txt has Python 3.11.9
- [ ] Procfile is correct
- [ ] render.yaml is configured
- [ ] GitHub repository is accessible
- [ ] Render account is created
- [ ] Ready to deploy!

---

## 🎉 You're Ready to Deploy!

Your project is **100% ready** for Render deployment. No additional configuration needed!

**Next Step:** Follow the "Deployment Steps" section above.

**Support:** Check `RENDER_TROUBLESHOOTING.md` if you encounter issues.

---

**Good luck with your deployment!** 🚀
