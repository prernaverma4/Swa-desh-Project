# Troubleshooting Guide - Hotel Booking Feature

## Issue: "Not Working"

Let's diagnose and fix the issue step by step.

---

## Step 1: Check if Server is Running

### Test 1: Check Process
```bash
ps aux | grep "python.*app.py"
```

**Expected**: Should show a running Python process
**If not running**: Start the server:
```bash
python3 app.py
```

### Test 2: Check Port
```bash
lsof -i :5002
```

**Expected**: Should show Python using port 5002
**If port in use**: Kill and restart:
```bash
lsof -ti:5002 | xargs kill -9
python3 app.py
```

---

## Step 2: Test API Endpoint

### Test API Connection
```bash
curl http://localhost:5002/api/hotels/all
```

**Expected Output**: JSON with hotel data
```json
{
  "hotel_count": 9,
  "hotels": [...]
}
```

**If you see this**: ✅ API is working!

**If you get error**:
- `Connection refused`: Server not running
- `404 Not Found`: Route not registered
- `500 Internal Server Error`: Check app.log

---

## Step 3: Test in Browser

### Method A: Direct API Test
1. Open browser
2. Go to: `http://localhost:5002/api/hotels/all`
3. You should see JSON data

### Method B: Use Test Page
1. Open the test file: `test_hotels.html` in your browser
2. Click "Test API Connection"
3. Click "Load Hotels"
4. Hotels should appear

### Method C: Test Heritage Map
1. Go to: `http://localhost:5002`
2. Login
3. Navigate to: Heritage Sites → View on Map
4. Click "Hotels List" button
5. Hotels should load

---

## Step 4: Check Browser Console

### Open Developer Tools
- **Chrome/Edge**: Press F12 or Ctrl+Shift+I (Cmd+Option+I on Mac)
- **Firefox**: Press F12 or Ctrl+Shift+K (Cmd+Option+K on Mac)
- **Safari**: Enable Developer menu, then Cmd+Option+C

### Look for Errors
Check the Console tab for:
- ❌ `Failed to fetch` → Server not running
- ❌ `404 Not Found` → Wrong URL
- ❌ `CORS error` → Cross-origin issue
- ❌ `Syntax error` → JavaScript error

---

## Common Issues & Solutions

### Issue 1: "Hotels List button does nothing"

**Symptoms**: Click button, nothing happens

**Solutions**:
1. Check browser console for JavaScript errors
2. Verify button exists:
   ```bash
   curl -s http://localhost:5002/heritage/map | grep "Hotels List"
   ```
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try different browser

### Issue 2: "API returns empty"

**Symptoms**: API works but no hotels shown

**Check database**:
```bash
python3 -c "from app import app; from models import db, Hotel; app.app_context().push(); print(f'Hotels: {Hotel.query.count()}')"
```

**Expected**: `Hotels: 9`

**If 0 hotels**: Run migration:
```bash
python3 migrate_hotel_booking.py
```

### Issue 3: "Booking form doesn't submit"

**Symptoms**: Click "Confirm Booking", nothing happens

**Solutions**:
1. Check if logged in
2. Verify dates are valid (future dates, check-out after check-in)
3. Check browser console for errors
4. Check app.log:
   ```bash
   tail -f app.log
   ```

### Issue 4: "Page shows but hotels don't load"

**Symptoms**: See loading spinner forever

**Solutions**:
1. Check API endpoint:
   ```bash
   curl http://localhost:5002/api/hotels/all
   ```
2. Check browser Network tab (F12 → Network)
3. Look for failed requests
4. Check if JavaScript is enabled

### Issue 5: "Server won't start"

**Symptoms**: `python3 app.py` fails

**Check for errors**:
```bash
python3 app.py 2>&1 | head -20
```

**Common errors**:
- `Port already in use`: Kill process on port 5002
- `Module not found`: Install requirements
  ```bash
  pip install -r requirements.txt
  ```
- `Database error`: Check database file exists
  ```bash
  ls -la instance/database.db
  ```

---

## Quick Diagnostic Script

Run this to check everything:

```bash
#!/bin/bash

echo "=== Digital Catalyst Diagnostic ==="
echo ""

echo "1. Checking Python..."
python3 --version

echo ""
echo "2. Checking database..."
ls -lh instance/database.db

echo ""
echo "3. Checking hotels in database..."
python3 -c "from app import app; from models import db, Hotel; app.app_context().push(); hotels = Hotel.query.all(); print(f'Total hotels: {len(hotels)}'); [print(f'  - {h.name}') for h in hotels[:3]]"

echo ""
echo "4. Checking if server is running..."
if lsof -i :5002 > /dev/null 2>&1; then
    echo "✓ Server is running on port 5002"
else
    echo "✗ Server is NOT running"
    echo "  Start with: python3 app.py"
fi

echo ""
echo "5. Testing API..."
if curl -s http://localhost:5002/api/hotels/all > /dev/null 2>&1; then
    echo "✓ API is responding"
    curl -s http://localhost:5002/api/hotels/all | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'  Found {data[\"hotel_count\"]} hotels')"
else
    echo "✗ API is not responding"
fi

echo ""
echo "=== Diagnostic Complete ==="
```

Save as `diagnostic.sh`, make executable, and run:
```bash
chmod +x diagnostic.sh
./diagnostic.sh
```

---

## Manual Testing Checklist

- [ ] Server is running (`python3 app.py`)
- [ ] Can access homepage (`http://localhost:5002`)
- [ ] Can login successfully
- [ ] Can navigate to Heritage Sites
- [ ] Can click "View on Map"
- [ ] Can see map with markers
- [ ] Can click "Hotels List" button
- [ ] Hotels load and display
- [ ] Can click "Book Now" on a hotel
- [ ] Booking form appears
- [ ] Can select dates
- [ ] Price calculates automatically
- [ ] Can submit booking
- [ ] Booking appears in "My Bookings"
- [ ] Can cancel booking

---

## Still Not Working?

### Collect Information

1. **Server logs**:
   ```bash
   tail -50 app.log
   ```

2. **Browser console errors**:
   - Open DevTools (F12)
   - Copy any red errors

3. **API response**:
   ```bash
   curl -v http://localhost:5002/api/hotels/all
   ```

4. **Database state**:
   ```bash
   python3 -c "from app import app; from models import db, Hotel, HotelBooking; app.app_context().push(); print(f'Hotels: {Hotel.query.count()}, Bookings: {HotelBooking.query.count()}')"
   ```

### Reset Everything

If all else fails, reset:

```bash
# 1. Stop server
lsof -ti:5002 | xargs kill -9

# 2. Backup database
cp instance/database.db instance/database.db.backup

# 3. Run migrations
python3 migrate_hotel_booking.py

# 4. Restart server
python3 app.py
```

---

## Contact Information

If you've tried everything and it still doesn't work, provide:
1. Error messages from server logs
2. Browser console errors
3. Output of diagnostic script
4. What specifically is not working (be specific!)

---

## Quick Fixes

### Fix 1: Clear Everything and Restart
```bash
# Kill server
lsof -ti:5002 | xargs kill -9

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Restart
python3 app.py
```

### Fix 2: Test with curl
```bash
# Test API
curl http://localhost:5002/api/hotels/all | python3 -m json.tool

# Test booking (replace IDs)
curl -X POST http://localhost:5002/hotel/book/1 \
  -d "check_in_date=2026-03-01&check_out_date=2026-03-03"
```

### Fix 3: Use Test HTML
Open `test_hotels.html` in browser - this bypasses all Flask templates and tests API directly.

---

**Remember**: Be specific about what "not working" means:
- Button doesn't appear?
- Button doesn't respond to clicks?
- Hotels don't load?
- Booking doesn't save?
- Error message appears?

The more specific you are, the easier it is to fix!
