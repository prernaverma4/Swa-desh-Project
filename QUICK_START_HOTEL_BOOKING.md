# Quick Start: Hotel Booking Feature

## 🎯 How to View Hotels and Book a Room

### Method 1: From Heritage Map (Recommended)

#### Step 1: Navigate to Heritage Map
1. Open your browser and go to: `http://localhost:5002`
2. Login with your credentials
3. Click on **"Heritage Sites"** in the navigation menu
4. Click on **"View on Map"** button

#### Step 2: Switch to Hotels List View
1. You'll see the map with heritage site markers
2. Look for the toggle buttons at the top:
   - **"Map View"** (currently active)
   - **"Hotels List"** (click this!)
3. Click the **"Hotels List"** button
4. The page will switch to show all available hotels

#### Step 3: Browse Hotels
You'll now see hotel cards displaying:
- Hotel photo
- Hotel name
- Location and state
- Price per night (₹)
- Rating (⭐)
- Which heritage site it's near
- Description

#### Step 4: Book a Hotel
1. Find a hotel you like
2. Click the **"Book Now"** button on the hotel card
3. You'll be taken to the booking form

#### Step 5: Complete Booking
1. Select **Check-in Date** (today or future date)
2. Select **Check-out Date** (must be after check-in)
3. Watch the price calculate automatically:
   - Number of nights will be shown
   - Total price will be calculated
4. Review the booking summary
5. Click **"Confirm Booking"**
6. Success! You'll be redirected to "My Bookings" page

#### Step 6: View Your Bookings
1. Click **"My Bookings"** in the top navigation menu
2. You'll see all your hotel bookings
3. Each booking shows:
   - Hotel name and location
   - Check-in and check-out dates
   - Number of nights
   - Total price
   - Booking status (Confirmed/Cancelled)
4. You can cancel confirmed bookings by clicking **"Cancel Booking"**

---

### Method 2: From Heritage Site Detail Page

#### Step 1: Go to Any Heritage Site
1. Navigate to **"Heritage Sites"** from the menu
2. Click on any heritage site (e.g., "Taj Mahal")

#### Step 2: Scroll to Hotels Section
1. On the heritage site detail page, scroll down
2. You'll see a section: **"🏨 Book a Hotel Near This Heritage Site"**
3. Hotels near this specific site will be displayed

#### Step 3: Book a Hotel
1. Click **"Book Now"** on any hotel
2. Follow steps 5-6 from Method 1 above

---

## 📱 Quick Navigation

### To View All Hotels:
```
Home → Heritage Sites → View on Map → Click "Hotels List" button
```

### To Book a Hotel:
```
Hotels List → Click "Book Now" → Select dates → Confirm Booking
```

### To View Your Bookings:
```
Top Navigation → My Bookings
```

---

## 🎬 Complete Flow Example

Let's book a hotel near the Taj Mahal:

1. **Start**: Go to `http://localhost:5002` and login
2. **Navigate**: Click "Heritage Sites" → "View on Map"
3. **Switch View**: Click "Hotels List" button
4. **Find Hotel**: Scroll through hotels, find "Oberoi Amarvilas"
5. **Book**: Click "Book Now" on Oberoi Amarvilas
6. **Select Dates**:
   - Check-in: Tomorrow's date
   - Check-out: 3 days from tomorrow
7. **Review**: See "2 nights × ₹45,000 = ₹90,000"
8. **Confirm**: Click "Confirm Booking"
9. **Success**: See your booking in "My Bookings" page!

---

## ✅ What You Can Do

- ✅ View all hotels on a single page
- ✅ See which heritage site each hotel is near
- ✅ Book hotels for any future dates
- ✅ See real-time price calculation
- ✅ View all your bookings in one place
- ✅ Cancel bookings if needed
- ✅ See booking history (confirmed and cancelled)

---

## 🔍 Current Hotels Available

Run the app and check these hotels:

**Near Taj Mahal (Agra):**
- Oberoi Amarvilas - ₹45,000/night ⭐4.9
- The Gateway Hotel - ₹8,500/night ⭐4.5
- Hotel Taj Resorts - ₹3,500/night ⭐4.2

**Near Red Fort (Delhi):**
- The Leela Palace New Delhi - ₹35,000/night ⭐4.8
- Haveli Dharampura - ₹15,000/night ⭐4.6

**Near Victoria Memorial (Kolkata):**
- The Oberoi Grand - ₹25,000/night ⭐4.7
- ITC Royal Bengal - ₹18,000/night ⭐4.6

**Near Mysore Palace:**
- Lalitha Mahal Palace Hotel - ₹12,000/night ⭐4.5
- The Windflower Resort - ₹8,000/night ⭐4.4

---

## 🚀 Start Now!

1. Make sure the server is running:
   ```bash
   python3 app.py
   ```

2. Open your browser:
   ```
   http://localhost:5002
   ```

3. Login and start exploring hotels!

---

## 💡 Tips

- **Best View**: Use the "Hotels List" view to see all hotels at once
- **Price Comparison**: Compare prices across different hotels easily
- **Date Flexibility**: Try different date ranges to see price changes
- **Multiple Bookings**: You can book multiple hotels for different dates
- **Cancellation**: Cancel anytime before check-in (no penalty in this demo)

---

## 🎓 For Admins

If you're logged in as an admin, you can also:
- Add new hotels to any heritage site
- Edit existing hotel details
- Delete hotels
- View all bookings from all users

---

**Enjoy booking your heritage site visits! 🏛️🏨**
