# Hotel Booking Feature - Testing Guide

## Overview
The Digital Catalyst platform now includes a complete hotel booking system integrated with the heritage sites map. Users can view hotels on a map, browse a list of all available hotels, and book rooms.

## Features Implemented

### 1. Map View with Hotel Toggle
- **Location**: Navigate to Heritage Sites Map (click "Heritage Sites" → "View on Map")
- **Toggle Button**: Switch between "Map View" and "Hotels List"
- **Map View**: Shows heritage sites on an interactive Leaflet map
- **Hotels List View**: Shows all available hotels in card format

### 2. Hotel Listing
Each hotel card displays:
- Hotel image
- Hotel name
- Location address
- State
- Price per night (₹)
- Rating (if available)
- Short description
- Associated heritage site name
- "Book Now" button
- "View Heritage Site" button

### 3. Hotel Booking Flow
1. User clicks "Book Now" on any hotel
2. Redirected to booking form with:
   - Check-in date picker
   - Check-out date picker
   - Real-time price calculation
   - Hotel details sidebar
3. System validates:
   - Check-in date not in past
   - Check-out date after check-in
   - Calculates total price automatically
4. On submission:
   - Booking saved with "Confirmed" status
   - User redirected to "My Bookings" page
   - Success message displayed

### 4. My Bookings Page
- Shows all user's hotel bookings
- Displays booking details:
  - Hotel name and location
  - Check-in and check-out dates
  - Number of nights
  - Total price
  - Booking status (Confirmed/Cancelled)
  - Booking date
- Actions available:
  - Cancel confirmed bookings
  - View associated heritage site

## Testing Steps

### Step 1: View Hotels on Map
1. Start the application: `python3 app.py`
2. Login to the application
3. Navigate to: **Heritage Sites** → **View on Map**
4. You should see the map with heritage site markers

### Step 2: Switch to Hotels List
1. On the map page, click the **"Hotels List"** button
2. The view should switch from map to hotel cards
3. You should see all available hotels displayed in a grid layout
4. Each hotel card shows complete information

### Step 3: Book a Hotel
1. Click **"Book Now"** on any hotel card
2. You'll be redirected to the booking form
3. Select a check-in date (today or future)
4. Select a check-out date (after check-in)
5. Watch the price calculation update automatically
6. Click **"Confirm Booking"**
7. You should see a success message and be redirected to "My Bookings"

### Step 4: View Your Bookings
1. Navigate to **"My Bookings"** from the top navigation
2. You should see your confirmed booking
3. Booking details should be displayed correctly
4. Try clicking **"Cancel Booking"** to test cancellation
5. Confirm the cancellation
6. Booking status should change to "Cancelled"

### Step 5: Book from Heritage Detail Page
1. Navigate to any heritage site detail page
2. Scroll down to the "Hotels Near This Heritage Site" section
3. Click **"Book Now"** on any hotel
4. Complete the booking process
5. Verify booking appears in "My Bookings"

## API Endpoints

### Get All Hotels
```bash
curl http://localhost:5002/api/hotels/all
```

Response:
```json
{
  "hotel_count": 9,
  "hotels": [
    {
      "id": 1,
      "name": "Oberoi Amarvilas",
      "location": "Taj East Gate Road, Agra",
      "state": "Uttar Pradesh",
      "price_per_night": 45000.0,
      "rating": 4.9,
      "heritage_id": 1,
      "heritage_name": "Taj Mahal",
      "description": "Luxury hotel with Taj Mahal views..."
    }
  ]
}
```

### Get Hotels by Heritage Site
```bash
curl http://localhost:5002/api/hotels/1
```

### Get User Bookings
```bash
curl http://localhost:5002/api/bookings/1
```

## Database Schema

### Hotel Table
- `id`: Primary key
- `name`: Hotel name
- `location`: Full address
- `state`: State name
- `price_per_night`: Price in rupees
- `rating`: Rating (1.0-5.0)
- `image`: Image URL
- `description`: Hotel description
- `heritage_id`: Foreign key to heritage_sites
- `created_at`: Timestamp

### HotelBooking Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `hotel_id`: Foreign key to hotels
- `check_in_date`: Date
- `check_out_date`: Date
- `total_price`: Calculated price
- `booking_status`: 'Confirmed' or 'Cancelled'
- `created_at`: Timestamp

## Validation Rules

### Date Validation
- Check-in date cannot be in the past
- Check-out date must be after check-in date
- Both dates are required

### Price Validation
- Total price must be positive
- Calculated as: `(check_out_date - check_in_date).days × price_per_night`

### Authorization
- Users must be logged in to book hotels
- Users can only view/cancel their own bookings
- Admins can manage all hotels and bookings

## Current Hotels in Database

Run this command to see all hotels:
```bash
python3 -c "from models import db, Hotel; from app import app; app.app_context().push(); hotels = Hotel.query.all(); [print(f'{h.name} - ₹{h.price_per_night}/night - Near {h.heritage_site.name}') for h in hotels]"
```

Expected output:
```
Oberoi Amarvilas - ₹45000.0/night - Near Taj Mahal
The Gateway Hotel - ₹8500.0/night - Near Taj Mahal
Hotel Taj Resorts - ₹12000.0/night - Near Taj Mahal
The Leela Palace New Delhi - ₹35000.0/night - Near Red Fort
Haveli Dharampura - ₹15000.0/night - Near Red Fort
...
```

## Troubleshooting

### Hotels Not Loading
1. Check if server is running: `curl http://localhost:5002/api/hotels/all`
2. Check browser console for JavaScript errors
3. Verify hotels exist in database (see command above)

### Booking Not Saving
1. Check if user is logged in
2. Verify dates are valid (future dates, check-out after check-in)
3. Check application logs: `tail -f app.log`

### Price Not Calculating
1. Ensure both dates are selected
2. Check browser console for JavaScript errors
3. Verify check-out date is after check-in date

## Admin Features

### Add New Hotel
1. Login as admin
2. Navigate to any heritage site detail page
3. Scroll to hotels section
4. Click **"Add New Hotel (Admin)"**
5. Fill in hotel details
6. Submit form

### Edit Hotel
1. Login as admin
2. Navigate to heritage site with hotels
3. Click **"Edit"** button on hotel card
4. Update details
5. Submit form

### Delete Hotel
1. Login as admin
2. Navigate to heritage site with hotels
3. Click **"Delete"** button on hotel card
4. Confirm deletion

## Success Criteria

✅ Hotels list loads when clicking "Hotels List" button
✅ Hotel cards display all information correctly
✅ "Book Now" button redirects to booking form
✅ Booking form validates dates correctly
✅ Price calculates automatically
✅ Booking saves successfully
✅ "My Bookings" page shows all user bookings
✅ Booking cancellation works
✅ Admin can add/edit/delete hotels

## Next Steps

To enhance the hotel booking system further, consider:
1. Add payment gateway integration (Razorpay, Stripe)
2. Add email notifications for bookings
3. Add hotel availability calendar
4. Add room types and quantities
5. Add booking modification (change dates)
6. Add reviews and ratings for hotels
7. Add photo gallery for hotels
8. Add amenities and facilities list
9. Add cancellation policy
10. Add booking confirmation PDF download

## Support

If you encounter any issues:
1. Check the application logs: `tail -f app.log`
2. Verify database integrity: `python3 -c "from app import app; from models import db; app.app_context().push(); print('Database OK' if db.engine.connect() else 'Database Error')"`
3. Restart the application: Stop and run `python3 app.py` again
4. Clear browser cache and cookies
5. Try a different browser

---

**Note**: This is an academic project demonstrating full-stack web development with Flask, SQLAlchemy, and modern JavaScript. The booking system is functional but should be enhanced with payment processing and additional security measures for production use.
