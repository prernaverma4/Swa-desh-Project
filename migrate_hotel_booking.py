"""
Database Migration: Add Hotel Booking System
=============================================

This script creates the hotels and hotel_bookings tables and adds sample data.

Academic Note:
This demonstrates database schema evolution and data migration strategies.
"""

from app import app
from models import db, Hotel, HotelBooking, HeritageSite
from datetime import datetime, date, timedelta

def create_tables():
    """Create hotel and hotel_booking tables"""
    with app.app_context():
        print("Creating hotel booking tables...")
        db.create_all()
        print("✓ Tables created successfully")

def add_sample_hotels():
    """Add sample hotels near heritage sites"""
    with app.app_context():
        # Check if hotels already exist
        if Hotel.query.first():
            print("⚠ Hotels already exist, skipping sample data")
            return
        
        print("\nAdding sample hotels...")
        
        # Get heritage sites
        taj_mahal = HeritageSite.query.filter_by(name='Taj Mahal').first()
        red_fort = HeritageSite.query.filter_by(name='Red Fort').first()
        golden_temple = HeritageSite.query.filter_by(name='Golden Temple').first()
        mysore_palace = HeritageSite.query.filter_by(name='Mysore Palace').first()
        
        hotels = []
        
        if taj_mahal:
            hotels.extend([
                Hotel(
                    name='Oberoi Amarvilas',
                    location='Taj East Gate Road, Agra, Uttar Pradesh 282001',
                    state='Uttar Pradesh',
                    price_per_night=45000.00,
                    rating=4.9,
                    image='https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400',
                    description='Luxury hotel with stunning views of the Taj Mahal. Just 600 meters from the monument.',
                    heritage_id=taj_mahal.id
                ),
                Hotel(
                    name='The Gateway Hotel',
                    location='Fatehabad Road, Agra, Uttar Pradesh 282001',
                    state='Uttar Pradesh',
                    price_per_night=8500.00,
                    rating=4.5,
                    image='https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400',
                    description='Comfortable stay with modern amenities. 2 km from Taj Mahal.',
                    heritage_id=taj_mahal.id
                ),
                Hotel(
                    name='Hotel Taj Resorts',
                    location='Eastern Gate, Taj Ganj, Agra, Uttar Pradesh 282001',
                    state='Uttar Pradesh',
                    price_per_night=3500.00,
                    rating=4.2,
                    image='https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400',
                    description='Budget-friendly hotel near Taj Mahal with rooftop restaurant.',
                    heritage_id=taj_mahal.id
                )
            ])
        
        if red_fort:
            hotels.extend([
                Hotel(
                    name='The Leela Palace New Delhi',
                    location='Diplomatic Enclave, Chanakyapuri, New Delhi 110023',
                    state='Delhi',
                    price_per_night=35000.00,
                    rating=4.8,
                    image='https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400',
                    description='Five-star luxury hotel in the heart of Delhi. 5 km from Red Fort.',
                    heritage_id=red_fort.id
                ),
                Hotel(
                    name='Haveli Dharampura',
                    location='2293, Gali Guliyan, Dharampura, Old Delhi 110006',
                    state='Delhi',
                    price_per_night=12000.00,
                    rating=4.6,
                    image='https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400',
                    description='Heritage haveli converted into boutique hotel. Walking distance to Red Fort.',
                    heritage_id=red_fort.id
                )
            ])
        
        if golden_temple:
            hotels.extend([
                Hotel(
                    name='Hyatt Regency Amritsar',
                    location='Opposite Amritsar International Airport, Amritsar, Punjab 143001',
                    state='Punjab',
                    price_per_night=15000.00,
                    rating=4.7,
                    image='https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400',
                    description='Modern luxury hotel near Golden Temple with excellent facilities.',
                    heritage_id=golden_temple.id
                ),
                Hotel(
                    name='Hotel Golden Tulip',
                    location='GT Road, Near Golden Temple, Amritsar, Punjab 143001',
                    state='Punjab',
                    price_per_night=5500.00,
                    rating=4.3,
                    image='https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=400',
                    description='Comfortable hotel with easy access to Golden Temple.',
                    heritage_id=golden_temple.id
                )
            ])
        
        if mysore_palace:
            hotels.extend([
                Hotel(
                    name='Lalitha Mahal Palace Hotel',
                    location='Nazarbad Main Road, Mysore, Karnataka 570010',
                    state='Karnataka',
                    price_per_night=18000.00,
                    rating=4.6,
                    image='https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400',
                    description='Heritage palace hotel with royal ambiance. 3 km from Mysore Palace.',
                    heritage_id=mysore_palace.id
                ),
                Hotel(
                    name='Hotel Pai Vista',
                    location='Nazarbad Main Road, Mysore, Karnataka 570010',
                    state='Karnataka',
                    price_per_night=6500.00,
                    rating=4.4,
                    image='https://images.unsplash.com/photo-1596436889106-be35e843f974?w=400',
                    description='Modern hotel with great amenities near Mysore Palace.',
                    heritage_id=mysore_palace.id
                )
            ])
        
        # Add all hotels
        for hotel in hotels:
            db.session.add(hotel)
        
        db.session.commit()
        print(f"✓ Added {len(hotels)} sample hotels")

def run_migration():
    """Run the complete migration"""
    print("=" * 60)
    print("HOTEL BOOKING SYSTEM MIGRATION")
    print("=" * 60)
    
    create_tables()
    add_sample_hotels()
    
    print("\n" + "=" * 60)
    print("✅ Migration completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    run_migration()
