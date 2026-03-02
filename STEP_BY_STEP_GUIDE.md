# Step-by-Step Guide: How to View Hotels and Book

## ✅ Prerequisites

1. **Server must be running**:
   ```bash
   python3 app.py
   ```
   You should see: `Running on http://0.0.0.0:5002`

2. **You must be logged in** to the application

---

## 📍 Step 1: Navigate to Heritage Map

### What to do:
1. Open browser: `http://localhost:5002`
2. Login with your credentials
3. Look at the top navigation bar
4. Click on **"Heritage Sites"**
5. You'll see a dropdown or page with heritage sites
6. Click the **"View on Map"** button (usually at the top of the page)

### What you should see:
- A page with an interactive map
- Heritage site markers on the map
- Filter options on the left side
- Two buttons at the top center:
  - **"Map View"** (active/blue)
  - **"Hotels List"** (inactive/outline)

---

## 📍 Step 2: Switch to Hotels List

### What to do:
1. Look for the toggle buttons at the top of the map
2. You'll see two buttons side by side:
   ```
   [🗺️ Map View]  [🏨 Hotels List]
   ```
3. Click the **"Hotels List"** button (the second one)

### What should happen:
- The "Hotels List" button becomes blue/active
- The "Map View" button becomes outline/inactive
- The map disappears
- A loading spinner appears briefly
- Hotel cards start appearing

### What you should see:
- Grid of hotel cards (2 columns on desktop)
- Each card shows:
  - Hotel image at the top
  - Hotel name
  - Location with 📍 icon
  - "Near: [Heritage Site Name]" with 📌 icon
  - Rating badge (⭐ 4.5)
  - State badge
  - Price in large text (₹45,000 / night)
  - Short description
  - Two buttons:
    - **"Book Now"** (blue button)
    - **"View Heritage Site"** (gray button)

---

## 📍 Step 3: Browse Hotels

### What you can do:
- Scroll down to see all 9 hotels
- Read hotel descriptions
- Compare prices
- Check ratings
- See which heritage site each hotel is near

### Hotels you should see:
1. **Oberoi Amarvilas** - ₹45,000/night (near Taj Mahal)
2. **The Gateway Hotel** - ₹8,500/night (near Taj Mahal)
3. **Hotel Taj Resorts** - ₹3,500/night (near Taj Mahal)
4. **The Leela Palace New Delhi** - ₹35,000/night (near Red Fort)
5. **Haveli Dharampura** - ₹12,000/night (near Red Fort)
6. **Hyatt Regency Amritsar** - ₹15,000/night (near Golden Temple)
7. **Hotel Golden Tulip** - ₹5,500/night (near Golden Temple)
8. **Lalitha Mahal Palace Hotel** - ₹18,000/night (near Mysore Palace)
9. **Hotel Pai Vista** - ₹6,500/night (near Mysore Palace)

---

## 📍 Step 4: Book a Hotel

### What to do:
1. Choose a hotel you like
2. Click the **"Book Now"** button on that hotel card

### What should happen:
- You're redirected to a new page
- URL changes to: `http://localhost:5002/hotel/book/[hotel_id]`
- Booking form appears

### What you should see on booking page:
- **Left side**: Booking form with:
  - Check-in date picker
  - Check-out date picker
  - Price information box
  - Booking summary (appears after selecting dates)
  - "Confirm Booking" button (blue)
  - "Cancel" button (gray)

- **Right side**: Hotel details card with:
  - Hotel image
  - Hotel name
  - Rating
  - Location
  - Description
  - Price per night

---

## 📍 Step 5: Select Dates

### What to do:
1. Click on **"Check-in Date"** field
2. A calendar appears
3. Select a date (today or any future date)
4. Click on **"Check-out Date"** field
5. Select a date (must be after check-in date)

### What should happen:
- After selecting both dates, a green box appears showing:
  ```
  Booking Summary
  Number of Nights: 2
  Total Price: ₹90,000
  ```
- Price is calculated automatically: nights × price_per_night

### Example:
- Check-in: March 1, 2026
- Check-out: March 3, 2026
- Nights: 2
- Price per night: ₹45,000
- **Total: ₹90,000**

---

## 📍 Step 6: Confirm Booking

### What to do:
1. Review the booking summary
2. Make sure dates are correct
3. Check the total price
4. Click **"Confirm Booking"** button

### What should happen:
- Form submits
- You're redirected to "My Bookings" page
- Green success message appears: "Booking confirmed! Total: ₹90,000 for 2 night(s)"

---

## 📍 Step 7: View Your Bookings

### What you should see:
- Page title: "My Hotel Bookings"
- Your booking card with:
  - Green header: "✓ Confirmed"
  - Hotel name
  - Location
  - Check-in date: "March 01, 2026"
  - Check-out date: "March 03, 2026"
  - Nights: 2
  - Total Price: ₹90,000 (in large blue text)
  - "Booked on: [date]"
  - Red "Cancel Booking" button
  - Link to view heritage site

### What you can do:
- View all your bookings (past and present)
- Cancel confirmed bookings
- Click on heritage site link to see details

---

## 📍 Step 8: Cancel a Booking (Optional)

### What to do:
1. On "My Bookings" page
2. Find the booking you want to cancel
3. Click **"Cancel Booking"** button (red)
4. Confirm the cancellation in the popup

### What should happen:
- Booking status changes from "Confirmed" to "Cancelled"
- Header changes from green to red
- "Cancel Booking" button disappears
- Success message: "Booking cancelled successfully"

---

## 🔍 Troubleshooting

### Problem: "Hotels List button doesn't appear"
**Solution**: 
- Make sure you're on the Heritage Map page
- URL should be: `http://localhost:5002/heritage/map`
- Refresh the page (Ctrl+R or Cmd+R)

### Problem: "Clicking Hotels List does nothing"
**Solution**:
1. Open browser console (F12)
2. Look for errors in red
3. Check if API is working:
   - Open new tab
   - Go to: `http://localhost:5002/api/hotels/all`
   - Should see JSON data

### Problem: "Hotels don't load / Loading spinner forever"
**Solution**:
1. Check server is running: `ps aux | grep app.py`
2. Test API: `curl http://localhost:5002/api/hotels/all`
3. Check browser console for errors
4. Try clearing cache (Ctrl+Shift+Delete)

### Problem: "Can't book hotel / Form doesn't submit"
**Solution**:
1. Make sure you're logged in
2. Check dates are valid:
   - Check-in must be today or future
   - Check-out must be after check-in
3. Look for error messages on the page
4. Check browser console

### Problem: "Booking doesn't appear in My Bookings"
**Solution**:
1. Refresh the page
2. Check if you're logged in as the same user
3. Check database:
   ```bash
   python3 -c "from app import app; from models import HotelBooking; app.app_context().push(); print(f'Bookings: {HotelBooking.query.count()}')"
   ```

---

## 🎯 Quick Test

Run this complete flow in 2 minutes:

1. **Start**: `http://localhost:5002` → Login
2. **Navigate**: Heritage Sites → View on Map
3. **Switch**: Click "Hotels List" button
4. **Browse**: Scroll through hotels
5. **Book**: Click "Book Now" on any hotel
6. **Dates**: Select tomorrow and day after
7. **Confirm**: Click "Confirm Booking"
8. **Verify**: See booking in "My Bookings"

**Expected time**: 1-2 minutes
**Expected result**: Booking confirmed and visible

---

## 📞 Still Having Issues?

If hotels list is not working, run this diagnostic:

```bash
# 1. Check server
curl http://localhost:5002/

# 2. Check API
curl http://localhost:5002/api/hotels/all

# 3. Check hotels in database
python3 -c "from app import app; from models import Hotel; app.app_context().push(); print(f'Hotels: {Hotel.query.count()}')"

# 4. Check page has button
curl -s http://localhost:5002/heritage/map | grep "Hotels List"
```

All four should return data. If any fails, that's where the problem is.

---

## ✅ Success Indicators

You know it's working when:
- ✅ "Hotels List" button is visible on map page
- ✅ Clicking button switches view
- ✅ Hotels load and display in cards
- ✅ "Book Now" button works
- ✅ Booking form appears
- ✅ Dates can be selected
- ✅ Price calculates automatically
- ✅ Booking saves successfully
- ✅ Booking appears in "My Bookings"

---

**Need more help?** Open `test_hotels.html` in your browser to test the API directly without going through the full application flow.
