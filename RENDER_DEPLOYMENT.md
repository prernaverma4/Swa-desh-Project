# Render Deployment Guide for Digital Catalyst

## Prerequisites
- GitHub account with your code pushed
- Render account (free tier available at https://render.com)

## Quick Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create New Web Service on Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and set up both web service and database

3. **Wait for deployment** (5-10 minutes)
   - Render will install dependencies and start your app
   - You'll get a URL like: `https://digital-catalyst.onrender.com`

### Option 2: Manual Setup

1. **Create PostgreSQL Database**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Name: `digital-catalyst-db`
   - Database: `digital_catalyst`
   - User: `digital_catalyst_user`
   - Plan: Free
   - Click "Create Database"
   - Copy the "Internal Database URL"

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: `digital-catalyst`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
     - Plan: Free

3. **Add Environment Variables**
   - In your web service settings, go to "Environment"
   - Add these variables:
     ```
     SECRET_KEY=<generate-random-string>
     DATABASE_URL=<paste-internal-database-url>
     PYTHON_VERSION=3.11.0
     ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

## Important Notes

### Database Migration
- On first deployment, the app will automatically create tables
- Sample data will be initialized if database is empty

### Free Tier Limitations
- Web service spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Database has 90-day expiration on free tier
- 750 hours/month of runtime

### Environment Variables
- `SECRET_KEY`: Used for session encryption (generate a strong random string)
- `DATABASE_URL`: PostgreSQL connection string (provided by Render)
- `PORT`: Automatically set by Render (don't override)

### Static Files
- Static files are served by Flask (works on free tier)
- For production, consider using a CDN

### Uploads Directory
- User uploads are stored in `/static/uploads/`
- On Render free tier, files are ephemeral (lost on restart)
- For persistent storage, use Render Disks or external storage (S3, Cloudinary)

## Troubleshooting

### Build Fails
- Check Python version in `runtime.txt` matches requirements
- Verify all dependencies in `requirements.txt` are compatible
- Check build logs in Render dashboard

### Database Connection Error
- Verify `DATABASE_URL` environment variable is set
- Check database is running and accessible
- Ensure `psycopg2-binary` is in requirements.txt

### App Crashes on Start
- Check logs in Render dashboard
- Verify `gunicorn` is in requirements.txt
- Ensure `Procfile` has correct command

### Slow First Load
- This is normal on free tier (cold start)
- Consider upgrading to paid tier for always-on service

## Post-Deployment

### Test Your Deployment
1. Visit your Render URL
2. Try logging in with default credentials:
   - Username: `admin`
   - Password: `admin123`
3. Test key features:
   - Browse heritage sites
   - Add bookmarks
   - Submit reviews
   - Check analytics dashboard

### Update Default Credentials
- Log in as admin
- Change the default password immediately
- Create new admin users if needed

### Monitor Your App
- Check Render dashboard for:
  - Request logs
  - Error logs
  - Resource usage
  - Uptime status

## Updating Your App

To deploy updates:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically detect the push and redeploy.

## Upgrading from Free Tier

For production use, consider:
- Starter plan ($7/month) - Always-on, no cold starts
- PostgreSQL paid plan - No 90-day limit
- Render Disks - Persistent file storage

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Project Issues: Check your GitHub repository

---

**Ready to deploy? Follow the steps above and your app will be live in minutes!**
