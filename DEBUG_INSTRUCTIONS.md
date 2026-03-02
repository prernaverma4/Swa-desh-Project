# Debug Instructions - Hotels Not Showing

## Step 1: Test the API Directly

Open this URL in your browser:
```
http://localhost:5002/api/hotels/all
```

**What you should see:**
- JSON data with 9 hotels
- Each hotel has: name, location, price_per_night, etc.

**If you see this** → API is working ✅
**If you see error** → Tell me what error

---

## Step 2: Use the Test Page

Open this URL in your browser:
```
http://localhost:5002/static/test_hotels_simple.html
```

**What to do:**
1. Page loads automatically and tests API
2. Click "Load Hotels" button
3. Hotels should appear below

**If hotels appear here** → API works, main page has issue
**If hotels don't appear** → Check the console logs on the page

---

## Step 3: Check Browser Console

On the heritage map page:

1. Press **F12** (opens Developer Tools)
2. Click **"Console"** tab
3. Click the "Hotels List" button
4. Look for messages in console

**Tell me what you see:**
- Any red errors?
- Do you see "Hotels List button clicked!"?
- Do you see "loadHotels() called"?
- Do you see "Hotels data: ..."?
- Any other messages?

---

## Step 4: Check Network Tab

1. Press **F12**
2. Click **"Network"** tab
3. Click "Hotels List" button
4. Look for a request to `/api/hotels/all`

**Tell me:**
- Do you see the request?
- What's the status code? (200, 404, 500?)
- Click on it and check "Response" tab - what does it show?

---

## Quick Commands to Run

```bash
# 1. Check if server is running
ps aux | grep "python.*app.py" | grep -v grep

# 2. Test API from command line
curl http://localhost:5002/api/hotels/all | python3 -m json.tool | head -20

# 3. Check hotels in database
python3 -c "from app import app; from models import Hotel; app.app_context().push(); print(f'Hotels in DB: {Hotel.query.count()}')"

# 4. Restart server
lsof -ti:5002 | xargs kill -9
python3 app.py
```

---

## What to Tell Me

Please provide:

1. **API Test Result:**
   - Go to: `http://localhost:5002/api/hotels/all`
   - Copy what you see (first 20 lines)

2. **Test Page Result:**
   - Go to: `http://localhost:5002/static/test_hotels_simple.html`
   - Click "Load Hotels"
   - Do hotels appear? Yes/No
   - What do the logs say?

3. **Browser Console:**
   - On heritage map page, press F12
   - Click "Hotels List" button
   - Copy any messages from Console tab

4. **Network Tab:**
   - Press F12 → Network tab
   - Click "Hotels List" button
   - Do you see `/api/hotels/all` request?
   - What's the status code?

---

## Common Issues

### Issue 1: API Returns Empty
**Check:**
```bash
python3 -c "from app import app; from models import Hotel; app.app_context().push(); hotels = Hotel.query.all(); print(f'Found {len(hotels)} hotels'); [print(f'  - {h.name}') for h in hotels[:3]]"
```

### Issue 2: CORS Error
**Symptom:** Console shows "CORS policy" error
**Fix:** API should work since it's same domain

### Issue 3: JavaScript Not Running
**Symptom:** No console logs at all
**Fix:** Hard refresh (Ctrl+Shift+R)

### Issue 4: Wrong URL
**Symptom:** 404 error
**Check:** URL should be `/api/hotels/all` not `/api/hotels`

---

## Expected Console Output

When you click "Hotels List", you should see:

```
Hotels List button clicked!
View switched to hotels list
loadHotels() called
hotelsList element: <div id="hotelsList">...</div>
Fetching hotels from /api/hotels/all
API response received: 200
Hotels data: {hotel_count: 9, hotels: Array(9)}
```

**If you see this** → Hotels should load
**If you don't see this** → Tell me what you see instead

---

## Screenshot What You See

If possible, take screenshots of:
1. The heritage map page with "Hotels List" button
2. Browser console (F12 → Console tab)
3. Network tab showing the API request
4. The test page (`test_hotels_simple.html`)

---

**Run the test page first - it will tell us exactly what's wrong!**

URL: `http://localhost:5002/static/test_hotels_simple.html`
