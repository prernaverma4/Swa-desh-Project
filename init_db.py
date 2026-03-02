"""
Database Initialization Script for Render Deployment
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with tables and admin user"""
    with app.app_context():
        try:
            print("Creating database tables...")
            db.create_all()
            print("✓ Tables created successfully")
            
            # Check if admin user exists
            admin = User.query.filter_by(username='admin').first()
            
            if not admin:
                print("Creating admin user...")
                admin = User(
                    username='admin',
                    email='admin@digitalcatalyst.com',
                    password=generate_password_hash('admin123'),
                    role='admin'
                )
                db.session.add(admin)
                db.session.commit()
                print("✓ Admin user created")
                print("  Username: admin")
                print("  Password: admin123")
            else:
                print("✓ Admin user already exists")
            
            # Verify
            user_count = User.query.count()
            print(f"✓ Total users in database: {user_count}")
            
            # Test admin login
            admin_test = User.query.filter_by(username='admin').first()
            if admin_test:
                print(f"✓ Admin user verified (ID: {admin_test.id}, Role: {admin_test.role})")
                from werkzeug.security import check_password_hash
                if check_password_hash(admin_test.password, 'admin123'):
                    print("✓ Admin password verified")
                else:
                    print("✗ WARNING: Admin password verification failed!")
            else:
                print("✗ ERROR: Admin user not found!")
                return False
            
            print("\n✓ Database initialization complete!")
            return True
            
        except Exception as e:
            print(f"\n✗ ERROR during database initialization:")
            print(f"  {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
