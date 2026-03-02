#!/usr/bin/env python3
"""
Force Database Initialization Script
Run this manually on Render if database initialization fails
"""
import os
import sys

print("=" * 60)
print("FORCE DATABASE INITIALIZATION")
print("=" * 60)

# Check if DATABASE_URL is set
if not os.environ.get('DATABASE_URL'):
    print("❌ ERROR: DATABASE_URL environment variable not set")
    print("This script must be run on Render with DATABASE_URL configured")
    sys.exit(1)

print(f"✓ DATABASE_URL found: {os.environ.get('DATABASE_URL')[:30]}...")

# Import app
try:
    from app import app, db
    from models import User, HeritageSite, Artisan
    from werkzeug.security import generate_password_hash
    print("✓ Imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Initialize database
with app.app_context():
    try:
        print("\n1. Testing database connection...")
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        print("✓ Database connection successful")
        
        print("\n2. Creating tables...")
        db.create_all()
        print("✓ Tables created")
        
        print("\n3. Checking existing users...")
        user_count = User.query.count()
        print(f"✓ Found {user_count} existing users")
        
        if user_count == 0:
            print("\n4. Creating default users...")
            
            admin_user = User(
                username='admin',
                email='admin@digitalcatalyst.in',
                password=generate_password_hash('admin123'),
                role='user'
            )
            manufacturer_user = User(
                username='manufacturer',
                email='manufacturer@digitalcatalyst.in',
                password=generate_password_hash('manufacturer123'),
                role='manufacturer'
            )
            
            db.session.add(admin_user)
            db.session.add(manufacturer_user)
            db.session.commit()
            print("✓ Default users created")
            
            print("\n5. Creating sample heritage sites...")
            heritage_sites = [
                HeritageSite(name='Taj Mahal', state='Uttar Pradesh', category='Monument', 
                           description='Iconic white marble mausoleum', annual_visitors=7000000),
                HeritageSite(name='Red Fort', state='Delhi', category='Fort', 
                           description='Historic fortified palace', annual_visitors=2500000),
                HeritageSite(name='Ajanta Caves', state='Maharashtra', category='Cave Temple', 
                           description='Ancient Buddhist rock-cut caves', annual_visitors=600000),
                HeritageSite(name='Hampi', state='Karnataka', category='Archaeological Site', 
                           description='Ruins of Vijayanagara Empire', annual_visitors=500000),
                HeritageSite(name='Golden Temple', state='Punjab', category='Temple', 
                           description='Holiest Gurdwara of Sikhism', annual_visitors=100000),
                HeritageSite(name='Konark Sun Temple', state='Odisha', category='Temple', 
                           description='13th-century Sun Temple', annual_visitors=400000),
                HeritageSite(name='Khajuraho Temples', state='Madhya Pradesh', category='Temple', 
                           description='Medieval Hindu and Jain temples', annual_visitors=300000),
                HeritageSite(name='Mysore Palace', state='Karnataka', category='Palace', 
                           description='Historical palace in Mysore', annual_visitors=2800000),
            ]
            
            for site in heritage_sites:
                db.session.add(site)
            db.session.commit()
            print(f"✓ Created {len(heritage_sites)} heritage sites")
            
            print("\n6. Creating sample artisans...")
            artisans = [
                Artisan(name='Ramesh Kumar', craft='Pottery', state='Rajasthan', 
                       product_price=1500, contact='9876543210', 
                       description='Traditional blue pottery artisan'),
                Artisan(name='Lakshmi Devi', craft='Weaving', state='West Bengal', 
                       product_price=3500, contact='9876543211', 
                       description='Handloom saree weaver'),
                Artisan(name='Mohammed Ali', craft='Metalwork', state='Uttar Pradesh', 
                       product_price=2500, contact='9876543212', 
                       description='Brass and copper craftsman'),
                Artisan(name='Priya Sharma', craft='Embroidery', state='Gujarat', 
                       product_price=2000, contact='9876543213', 
                       description='Kutch embroidery specialist'),
                Artisan(name='Suresh Babu', craft='Wood Carving', state='Kerala', 
                       product_price=4000, contact='9876543214', 
                       description='Traditional temple wood carver'),
                Artisan(name='Anjali Patel', craft='Painting', state='Madhya Pradesh', 
                       product_price=1200, contact='9876543215', 
                       description='Gond art painter'),
                Artisan(name='Vijay Singh', craft='Jewelry Making', state='Rajasthan', 
                       product_price=5000, contact='9876543216', 
                       description='Kundan jewelry craftsman'),
                Artisan(name='Geeta Rani', craft='Basket Weaving', state='Assam', 
                       product_price=800, contact='9876543217', 
                       description='Bamboo basket weaver'),
            ]
            
            for artisan in artisans:
                db.session.add(artisan)
            db.session.commit()
            print(f"✓ Created {len(artisans)} artisans")
            
            print("\n" + "=" * 60)
            print("✅ DATABASE INITIALIZATION COMPLETE!")
            print("=" * 60)
            print("\nDefault Login Credentials:")
            print("  Username: admin")
            print("  Password: admin123")
            print("\n  Username: manufacturer")
            print("  Password: manufacturer123")
            print("=" * 60)
        else:
            print("\n✓ Database already initialized with users")
            print(f"  Total users: {user_count}")
            
    except Exception as e:
        import traceback
        print(f"\n❌ ERROR: {e}")
        print(f"\nFull traceback:")
        print(traceback.format_exc())
        sys.exit(1)
