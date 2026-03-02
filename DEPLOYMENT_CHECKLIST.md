# Render Deployment Checklist ✅

## Pre-Deployment (Completed ✓)
- [x] Added `runtime.txt` with Python version
- [x] Added `psycopg2-binary` to requirements.txt for PostgreSQL
- [x] Fixed DATABASE_URL for Render (postgres:// → postgresql://)
- [x] Created `render.yaml` for automated deployment
- [x] Created `.env.example` for environment variables reference
- [x] Updated `.gitignore` to exclude sensitive files
- [x] Committed all changes to Git
- [x] Pushed to GitHub repository

## Render Deployment Steps

### Option A: Blueprint Deployment (Easiest)
1. [ ] Go to https://dashboard.render.com
2. [ ] Click "New +" → "Blueprint"
3. [ ] Connect GitHub repository: `pankajrajbhar19/trial`
4. [ ] Render will detect `render.yaml` automatically
5. [ ] Click "Apply" to create both web service and database
6. [ ] Wait 5-10 minutes for deployment
7. [ ] Visit your app URL (will be shown in dashboard)

### Option B: Manual Deployment
1. [ ] Create PostgreSQL Database
   - Dashboard → New + → PostgreSQL
   - Name: `digital-catalyst-db`
   - Plan: Free
   - Copy "Internal Database URL"

2. [ ] Create Web Service
   - Dashboard → New + → Web Service
   - Connect repository: `pankajrajbhar19/trial`
   - Name: `digital-catalyst`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Plan: Free

3. [ ] Add Environment Variables
   - Go to Environment tab
   - Add `DATABASE_URL` (paste from step 1)
   - Add `SECRET_KEY` (generate random string)
   - Add `PYTHON_VERSION` = `3.11.0`

4. [ ] Deploy
   - Click "Create Web Service"
   - Monitor logs for any errors

## Post-Deployment Testing
1. [ ] Visit your Render URL
2. [ ] Check homepage loads correctly
3. [ ] Test login with default credentials:
   - Username: `admin`
   - Password: `admin123`
4. [ ] Test key features:
   - [ ] Browse heritage sites
   - [ ] View site details
   - [ ] Add bookmark
   - [ ] Submit review
   - [ ] Check analytics dashboard (admin)
5. [ ] Change default admin password

## Troubleshooting

### If Build Fails
- Check Render logs for specific error
- Verify Python version compatibility
- Ensure all dependencies are in requirements.txt

### If Database Connection Fails
- Verify DATABASE_URL is set correctly
- Check database is running in Render dashboard
- Ensure psycopg2-binary is installed

### If App Crashes
- Check application logs in Render
- Verify Procfile command is correct
- Test locally with: `gunicorn app:app`

### If Static Files Don't Load
- Check Flask static file configuration
- Verify paths in templates are correct
- Clear browser cache

## Important URLs
- GitHub Repo: https://github.com/pankajrajbhar19/trial
- Render Dashboard: https://dashboard.render.com
- Your App URL: (will be assigned after deployment)

## Notes
- Free tier spins down after 15 min inactivity
- First request after spin-down takes 30-60 seconds
- Database expires after 90 days on free tier
- Uploaded files are ephemeral on free tier

## Next Steps After Deployment
1. [ ] Update README with live demo URL
2. [ ] Test all features thoroughly
3. [ ] Monitor error logs for issues
4. [ ] Consider upgrading to paid tier for production
5. [ ] Set up custom domain (optional)
6. [ ] Configure environment-specific settings

---

**Your code is ready for Render! Follow the steps above to deploy.** 🚀
