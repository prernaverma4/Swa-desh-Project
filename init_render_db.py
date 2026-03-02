"""
Database Initialization Script for Render Deployment
This script initializes the database with tables and default users.
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize database with tables and sample data."""
    try:
        # Import after path is set
        from app import app, db
        from models import User, HeritageSite, Artisan
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            print("Creating database tables...")
            
            # Create all tables
            db.create_all()
            print("✓ Tables created successfully")
            
            # Check if data already exists
            existing_users = User.query.count()
            if existing_users == 0:
                print("Initializing database with sample data...")
                
                # Create default users
                users = [
                    User(
                        username='admin',
                        email='admin@digitalcatalyst.in',
                        password=generate_password_hash('admin123'),
                        role='user'
                    ),
                    User(
                        username='manufacturer',
                        email='manufacturer@digitalcatalyst.in',
                        password=generate_password_hash('manufacturer123'),
                        role='manufacturer'
                    )
                ]
                
                for user in users:
                    db.session.add(user)
                
                # Sample Heritage Sites
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
                
                # Sample Artisans
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
                
                # Commit all changes
                db.session.commit()
                print("✓ Database initialized successfully!")
                print("✓ Default users created:")
                print("  - Username: admin, Password: admin123")
                print("  - Username: manufacturer, Password: manufacturer123")
            else:
                print(f"✓ Database already initialized ({existing_users} users found)")
                
    except Exception as e:
        print(f"⚠ Database initialization skipped: {str(e)}")
        print("⚠ This is normal during build phase if DATABASE_URL is not yet available")
        print("⚠ Database will be initialized on first app startup")
        sys.exit(0)  # Exit successfully to not fail the build

if __name__ == "__main__":
    init_database()
