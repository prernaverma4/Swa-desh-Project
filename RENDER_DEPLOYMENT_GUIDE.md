# Render Deployment Guide - Digital Catalyst

## 🚀 Quick Deploy to Render

### Prerequisites
- GitHub account with your code pushed
- Render account (free tier available)

---

## Step 1: Prepare Your Repository

### Files Created for Deployment:
1. ✅ `render.yaml` - Render configuration
2. ✅ `Procfile` - Process file for Gunicorn
3. ✅ `build.sh` - Build script to initialize database
4. ✅ `requirements.txt` - Updated with all dependencies

### Push to GitHub:
```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

---

## Step 2: Deploy on Render

### Method 1: Using render.yaml (Recommended)

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → **"Blueprint"**
3. **Connect your GitHub repository**: `pankajrajbhar19/trial`
4. **Select branch**: `main`
5. **Render will detect** `render.yaml` automatically
6. **Click "Apply"**
7. **Wait for deployment** (5-10 minutes)

### Method 2: Manual Setup

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → **"Web Service"**
3. **Connect GitHub repository**: `pankajrajbhar19/trial`
4. **Configure**:
   - **Name**: `digital-catalyst`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. **Add Environment Variables**:
   - `PYTHON_VERSION`: `3.11.0`
   - `SECRET_KEY`: (auto-generate)
   - `DATABASE_URL`: `sqlite:///instance/database.db`

6. **Click "Create Web Service"**

---

## Step 3: Monitor Deployment

### Check Logs:
1. Go to your service dashboard
2. Click "Logs" tab
3. Watch for:
   ```
   ==> Building...
   ==> Installing dependencies
   ==> Running build.sh
   ==> Database initialized successfully
   ==> Starting gunicorn
   ==> Listening on port 10000
   ```

### Common Build Messages:
- ✅ "Build successful" - Good!
- ✅ "Admin user created" - Database initialized
- ✅ "Listening on 0.0.0.0:10000" - Server running
- ❌ "Build failed" - Check error logs

---

## Step 4: Access Your Application

### Your URL:
```
https://digital-catalyst.onrender.com
```
(Or whatever name you chose)

### Test It:
1. Open the URL in browser
2. You should see the landing page
3. Login with:
   - **Username**: `admin`
   - **Password**: `admin123`

---

## 🔧 Troubleshooting

### Issue 1: "Internal Server Error"

**Cause**: Database not initialized or missing dependencies

**Fix**:
1. Check logs for specific error
2. Redeploy with "Clear build cache"
3. Verify `build.sh` ran successfully

### Issue 2: "Application failed to respond"

**Cause**: Wrong port or host configuration

**Fix**: Already fixed in `app.py`:
```python
port = int(os.environ.get('PORT', 5002))
app.run(host='0.0.0.0', port=port)
```

### Issue 3: "Module not found"

**Cause**: Missing dependency in requirements.txt

**Fix**: Already added all dependencies:
```
Flask==3.0.0
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
beautifulsoup4==4.14.3
gunicorn==23.0.0
Werkzeug==3.0.1
scikit-learn==1.3.2
numpy==1.26.2
pandas==2.1.3
```

### Issue 4: "Database locked"

**Cause**: SQLite doesn't work well with multiple workers

**Fix**: Use single worker in Procfile:
```
web: gunicorn app:app --workers 1
```

### Issue 5: "Static files not loading"

**Cause**: Render needs explicit static file configuration

**Fix**: Already configured in Flask:
```python
app = Flask(__name__)
# Static files served automatically from /static
```

---

## 📊 Deployment Checklist

Before deploying, verify:

- [x] `requirements.txt` has all dependencies
- [x] `Procfile` exists with gunicorn command
- [x] `build.sh` is executable (`chmod +x build.sh`)
- [x] `render.yaml` is configured correctly
- [x] `app.py` uses `0.0.0.0` as host
- [x] `app.py` uses `PORT` environment variable
- [x] Database path uses absolute path
- [x] `SECRET_KEY` uses environment variable
- [x] All code pushed to GitHub

---

## 🎯 Post-Deployment

### 1. Test All Features:
- [ ] Login/Register
- [ ] Heritage Sites listing
- [ ] Heritage Map
- [ ] Hotels List
- [ ] Book Hotel
- [ ] My Bookings
- [ ] Admin Panel

### 2. Add Sample Data:
Run migrations to add sample heritage sites and hotels:
```bash
# In Render shell (if available) or locally then push database
python3 migrate_hotel_booking.py
```

### 3. Configure Custom Domain (Optional):
1. Go to service settings
2. Add custom domain
3. Update DNS records
4. Enable HTTPS

### 4. Monitor Performance:
- Check response times
- Monitor error rates
- Watch resource usage
- Set up alerts

---

## 🔒 Security Recommendations

### For Production:

1. **Change Default Credentials**:
   ```python
   # Don't use admin/admin123 in production!
   # Create strong password
   ```

2. **Use Environment Variables**:
   ```bash
   SECRET_KEY=your-super-secret-key-here
   ADMIN_PASSWORD=strong-password-here
   ```

3. **Enable HTTPS**:
   - Render provides free SSL
   - Already enabled by default

4. **Set Secure Cookies**:
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
   ```

5. **Add Rate Limiting**:
   ```bash
   pip install Flask-Limiter
   ```

---

## 📈 Scaling Options

### Free Tier Limitations:
- Spins down after 15 minutes of inactivity
- 750 hours/month free
- Shared CPU/RAM
- SQLite database (not persistent across deploys)

### Upgrade Options:
1. **Starter Plan** ($7/month):
   - Always on
   - More resources
   - Better performance

2. **Use PostgreSQL**:
   - Add PostgreSQL database on Render
   - Update `DATABASE_URL`
   - More reliable for production

3. **Add Redis**:
   - For caching
   - Session storage
   - Better performance

---

## 🐛 Debug Mode

### Enable Debug Logs:
In Render dashboard:
1. Go to Environment
2. Add: `FLASK_DEBUG=1`
3. Redeploy

**Warning**: Never enable debug in production!

---

## 📝 Deployment Commands

### Redeploy:
```bash
# Push changes to GitHub
git add .
git commit -m "Update application"
git push origin main

# Render auto-deploys on push
```

### Manual Deploy:
1. Go to Render dashboard
2. Click "Manual Deploy"
3. Select branch
4. Click "Deploy"

### Clear Build Cache:
1. Go to service settings
2. Click "Clear build cache"
3. Redeploy

---

## ✅ Success Indicators

Your deployment is successful when:

1. ✅ Build completes without errors
2. ✅ Service shows "Live" status
3. ✅ URL opens the landing page
4. ✅ Can login with admin credentials
5. ✅ All pages load correctly
6. ✅ Database queries work
7. ✅ Static files load (CSS, JS, images)
8. ✅ No errors in logs

---

## 🆘 Getting Help

### If deployment fails:

1. **Check Render Logs**:
   - Build logs
   - Deploy logs
   - Runtime logs

2. **Common Error Messages**:
   - "No module named 'X'" → Add to requirements.txt
   - "Database locked" → Use single worker
   - "Port already in use" → Render handles this
   - "Permission denied" → Check file permissions

3. **Test Locally First**:
   ```bash
   # Test with gunicorn locally
   gunicorn app:app
   
   # Should work on http://localhost:8000
   ```

4. **Render Support**:
   - Community forum: https://community.render.com
   - Documentation: https://render.com/docs
   - Status page: https://status.render.com

---

## 🎉 You're Done!

Your Digital Catalyst application should now be live on Render!

**Your URL**: https://digital-catalyst.onrender.com

**Default Login**:
- Username: `admin`
- Password: `admin123`

**Remember to**:
1. Change default password
2. Add your data
3. Test all features
4. Share with users!

---

**Happy Deploying! 🚀**
