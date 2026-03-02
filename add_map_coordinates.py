"""
Migration Script: Add Map Coordinates to Heritage Sites
========================================================

This script adds latitude and longitude columns to the heritage_sites table
and populates them with approximate coordinates for existing sites.

Academic Note:
This demonstrates database schema evolution and data migration strategies.
"""

from app import app
from models import db, HeritageSite

# Approximate coordinates for Indian heritage sites
HERITAGE_COORDINATES = {
    'Taj Mahal': (27.1751, 78.0421),
    'Red Fort': (28.6562, 77.2410),
    'Ajanta Caves': (20.5519, 75.7033),
    'Hampi': (15.3350, 76.4600),
    'Golden Temple': (31.6200, 74.8765),
    'Konark Sun Temple': (19.8876, 86.0945),
    'Khajuraho Temples': (24.8318, 79.9199),
    'Mysore Palace': (12.3051, 76.6551)
}

def add_coordinates():
    """Add latitude and longitude to existing heritage sites"""
    with app.app_context():
        print("Adding map coordinates to heritage sites...")
        
        # Add columns to existing table
        try:
            db.session.execute(db.text('ALTER TABLE heritage_sites ADD COLUMN latitude REAL'))
            db.session.execute(db.text('ALTER TABLE heritage_sites ADD COLUMN longitude REAL'))
            db.session.commit()
            print("✓ Added latitude and longitude columns")
        except Exception as e:
            if 'duplicate column name' in str(e).lower():
                print("✓ Columns already exist")
            else:
                print(f"Note: {e}")
            db.session.rollback()
        
        # Update existing sites with coordinates
        sites = HeritageSite.query.all()
        updated_count = 0
        
        for site in sites:
            if site.name in HERITAGE_COORDINATES:
                lat, lng = HERITAGE_COORDINATES[site.name]
                site.latitude = lat
                site.longitude = lng
                updated_count += 1
                print(f"✓ Updated {site.name}: ({lat}, {lng})")
            else:
                print(f"⚠ No coordinates for {site.name}")
        
        db.session.commit()
        print(f"\n✅ Successfully updated {updated_count} heritage sites with coordinates")

if __name__ == '__main__':
    add_coordinates()
