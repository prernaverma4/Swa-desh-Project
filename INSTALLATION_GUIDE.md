# Digital Catalyst - Complete Installation Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Detailed Setup Instructions](#detailed-setup-instructions)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [First Run](#first-run)

---

## Prerequisites

Before installing Digital Catalyst, ensure you have the following:

### Required Software
- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Text editor** (VS Code, PyCharm, or any code editor)
- **Web browser** (Chrome, Firefox, Safari, or Edge)

### Verify Prerequisites

Open terminal/command prompt and run:

```bash
python --version
# Should output: Python 3.8.x or higher

pip --version
# Should output: pip 20.x.x or higher
```

---

## Installation Methods

### Method 1: Quick Setup (Recommended)

#### For Windows:
1. Download the project
2. Navigate to the project folder in Command Prompt
3. Double-click `setup.bat`
4. Wait for installation to complete
5. Run `python app.py`

#### For macOS/Linux:
1. Download the project
2. Navigate to the project folder in Terminal
3. Run `chmod +x setup.sh`
4. Run `./setup.sh`
5. Activate virtual environment: `source venv/bin/activate`
6. Run `python app.py`

### Method 2: Manual Installation

Follow the detailed setup instructions below.

---

## Detailed Setup Instructions

### Step 1: Download/Extract the Project

Extract the `digital_catalyst` folder to your desired location.

### Step 2: Open Terminal/Command Prompt

- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **macOS**: Press `Cmd + Space`, type `terminal`, press Enter
- **Linux**: Press `Ctrl + Alt + T`

### Step 3: Navigate to Project Directory

```bash
cd path/to/digital_catalyst
```

Example:
```bash
# Windows
cd C:\Users\YourName\Downloads\digital_catalyst

# macOS/Linux
cd ~/Downloads/digital_catalyst
```

### Step 4: Create Virtual Environment (Recommended)

**Why?** Virtual environments keep project dependencies isolated.

```bash
python -m venv venv
```

This creates a `venv` folder in your project directory.

### Step 5: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 6: Upgrade pip (Optional but Recommended)

```bash
python -m pip install --upgrade pip
```

### Step 7: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- Flask-Login==0.6.3
- scikit-learn==1.3.2
- pandas==2.1.4
- numpy==1.26.2
- Werkzeug==3.0.1

**Note:** Installation may take 2-5 minutes depending on internet speed.

### Step 8: Verify Installation

```bash
pip list
```

You should see all packages listed above.

---

## First Run

### Step 1: Start the Application

```bash
python app.py
```

### Step 2: Wait for Initialization

You should see output like:
```
Database initialized with sample data!
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Step 3: Open Web Browser

Navigate to: **http://localhost:5000**

### Step 4: Login

Use default credentials:
- **Username:** `admin`
- **Password:** `admin123`

### Step 5: Explore the Dashboard

You should see:
- ✅ 8 Heritage Sites
- ✅ 8 Artisans
- ✅ Interactive charts
- ✅ Analytics dashboard

---

## Verification Checklist

After installation, verify everything works:

- [ ] Application starts without errors
- [ ] Login page loads at http://localhost:5000
- [ ] Can login with admin credentials
- [ ] Dashboard shows statistics
- [ ] Charts render properly
- [ ] Can add new heritage site
- [ ] Can add new artisan
- [ ] Search/filter works
- [ ] CSV export works
- [ ] Can logout successfully

---

## Troubleshooting

### Issue 1: "Python is not recognized"

**Problem:** Windows can't find Python

**Solution:**
1. Reinstall Python
2. During installation, check "Add Python to PATH"
3. Restart computer

### Issue 2: "pip is not recognized"

**Solution:**
```bash
python -m ensurepip --upgrade
```

### Issue 3: "Module not found" errors

**Solution:**
```bash
# Deactivate virtual environment
deactivate

# Delete venv folder
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Recreate and reinstall
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue 4: Port 5000 already in use

**Solution:**

Edit `app.py`, change last line:
```python
# From:
app.run(debug=True, host='0.0.0.0', port=5000)

# To:
app.run(debug=True, host='0.0.0.0', port=5001)
```

Then access: http://localhost:5001

### Issue 5: Charts not showing

**Problem:** No internet connection for CDN

**Solution:** Charts require internet to load Chart.js from CDN. Ensure internet connection is available.

### Issue 6: Database locked

**Solution:**
1. Close all instances of the app
2. Delete `database.db` file
3. Restart the application (it will recreate the database)

### Issue 7: CSS not loading

**Solution:**
1. Hard refresh browser: `Ctrl + F5` (Windows) or `Cmd + Shift + R` (Mac)
2. Clear browser cache
3. Try different browser

---

## Stopping the Application

Press `Ctrl + C` in the terminal where the app is running.

To deactivate virtual environment:
```bash
deactivate
```

---

## Restarting the Application

```bash
# Navigate to project folder
cd path/to/digital_catalyst

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run app
python app.py
```

---

## File Structure Explanation

```
digital_catalyst/
│
├── app.py                  # Main application (START HERE)
├── models.py               # Database models
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── API_DOCUMENTATION.md   # API guide
├── setup.sh / setup.bat   # Quick install scripts
│
├── ml/
│   └── recommendation_engine.py  # AI/ML algorithms
│
├── templates/             # HTML files
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   └── ...
│
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── main.js       # JavaScript
│
└── database.db           # SQLite database (auto-created)
```

---

## Development Tips

### Running in Development Mode

The app runs in debug mode by default, which means:
- ✅ Auto-reload on code changes
- ✅ Detailed error messages
- ⚠️ Don't use in production

### Testing APIs

Use tools like:
- **Postman** ([Download](https://www.postman.com/downloads/))
- **cURL** (comes with macOS/Linux, [Windows download](https://curl.se/windows/))
- **Browser** (for GET requests)

Example:
```bash
curl http://localhost:5000/api/heritage
```

### Adding New Features

1. Models: Edit `models.py`
2. Routes: Edit `app.py`
3. Templates: Add to `templates/`
4. Styles: Edit `static/css/style.css`
5. JavaScript: Edit `static/js/main.js`

---

## Production Deployment (Future)

For production deployment, consider:
- Using PostgreSQL instead of SQLite
- Setting `debug=False`
- Using production WSGI server (Gunicorn, uWSGI)
- Adding HTTPS
- Implementing rate limiting
- Using environment variables for secrets

---

## System Requirements

### Minimum:
- OS: Windows 7+, macOS 10.12+, Ubuntu 18.04+
- RAM: 2 GB
- Storage: 500 MB
- Internet: Required for initial setup and charts

### Recommended:
- OS: Windows 10+, macOS 11+, Ubuntu 20.04+
- RAM: 4 GB+
- Storage: 1 GB
- Internet: Broadband connection

---

## Support

If you encounter issues not covered here:

1. Check README.md for general info
2. Check API_DOCUMENTATION.md for API details
3. Review error messages carefully
4. Search error messages online
5. Check Python/Flask documentation

---

## Next Steps

After successful installation:

1. ✅ Explore the dashboard
2. ✅ Add your own heritage sites
3. ✅ Add artisans from your region
4. ✅ Test the API endpoints
5. ✅ Customize the design
6. ✅ Add new features
7. ✅ Share with others!

---

**Happy Coding! 🚀**

Last Updated: February 14, 2026
