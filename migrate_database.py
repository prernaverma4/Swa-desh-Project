"""
Database Migration Script for Digital Catalyst Platform
Adds new tables: Bookmark, SiteView, Review

This script safely migrates the existing database to include new engagement
tracking features while preserving all existing data.

Usage:
    python migrate_database.py
"""

from app import app, db
from models import User, HeritageSite, Artisan, Product, Order, Bookmark, SiteView, Review

def migrate_database():
    """
    Create new tables for bookmarks, site views, and reviews.
    
    Academic Context - Database Migration Strategy:
    -----------------------------------------------
    Database migrations are critical for evolving applications without data loss.
    
    Migration Best Practices:
    1. Backward Compatible: Existing tables/data remain unchanged
    2. Idempotent: Safe to run multiple times (checks if tables exist)
    3. Transactional: All changes succeed or all fail (ACID properties)
    4. Tested: Run on development/staging before production
    5. Reversible: Have rollback plan if issues occur
    
    SQLAlchemy db.create_all() Behavior:
    - Creates only tables that don't exist
    - Does NOT modify existing tables
    - Does NOT delete data
    - Safe for incremental schema changes
    
    For production systems, consider:
    - Alembic for version-controlled migrations
    - Blue-green deployment for zero downtime
    - Database backups before migration
    """
    
    with app.app_context():
        print("Starting database migration...")
        print("=" * 60)
        
        # Create all tables (only creates new ones, doesn't touch existing)
        try:
            db.create_all()
            print("✓ Database tables created successfully")
            print("\nNew tables added:")
            print("  - bookmarks (user bookmarks for heritage sites)")
            print("  - site_views (engagement tracking)")
            print("  - reviews (user ratings and comments)")
            print("\nExisting tables preserved:")
            print("  - users")
            print("  - heritage_sites")
            print("  - artisans")
            print("  - products")
            print("  - orders")
            print("=" * 60)
            print("Migration completed successfully!")
            
        except Exception as e:
            print(f"✗ Migration failed: {str(e)}")
            print("\nPlease check:")
            print("  1. Database file permissions")
            print("  2. Disk space availability")
            print("  3. Database file not locked by another process")
            raise

if __name__ == '__main__':
    migrate_database()
