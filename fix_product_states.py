from app import app, db
from models import Product, Artisan

with app.app_context():
    # Find all products by Maharashtra artisan and set their state
    mah_artisans = Artisan.query.filter_by(state='Maharashtra').all()
    
    count = 0
    for artisan in mah_artisans:
        products = Product.query.filter_by(artisan_id=artisan.id).all()
        for p in products:
            if not p.state:
                p.state = 'Maharashtra'
                # Also set a default district if missing, based on name mapping
                if "Kolhapuri" in p.name:
                    p.district = "Kolhapur"
                elif "Warli" in p.name:
                    p.district = "Palghar"
                elif "Solapuri" in p.name:
                    p.district = "Solapur"
                elif "Nashik" in p.name:
                    p.district = "Nashik"
                elif "Paithani" in p.name:
                    p.district = "Aurangabad"
                
                print(f"Updating Product: {p.name} -> State: {p.state}, District: {p.district}")
                count += 1
    
    if count > 0:
        db.session.commit()
        print(f"Successfully updated {count} products.")
    else:
        print("No products needed updating.")
