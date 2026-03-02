from app import app, db
from models import Product, Artisan

with app.app_context():
    print("--- Artisans ---")
    artisans = Artisan.query.all()
    for a in artisans:
        print(f"ID: {a.id}, Name: {a.name}, State: '{a.state}'")
    
    print("\n--- Products ---")
    products = Product.query.all()
    for p in products:
        print(f"ID: {p.id}, Name: {p.name}, Artisan ID: {p.artisan_id}")

    print("\n--- Query Test (State='Maharashtra') ---")
    maharashtra_products = Product.query.join(Artisan).filter(Artisan.state == 'Maharashtra').all()
    print(f"Count: {len(maharashtra_products)}")
    for p in maharashtra_products:
        print(f"ID: {p.id}, Name: {p.name}")
