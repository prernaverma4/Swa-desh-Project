from app import app, db
from models import Artisan, Product

with app.app_context():
    # Check if Maharashtra artisan exists
    mah_artisan = Artisan.query.filter_by(state='Maharashtra').first()
    
    if not mah_artisan:
        print("Creating Maharashtra Artisan...")
        mah_artisan = Artisan(
            name="Ganesh Patil",
            craft="Paithani Saree Weaving",
            state="Maharashtra",
            product_price=15000.0,
            contact="ganesh.patil@example.com",
            description="Traditional Paithani sarees from Yeola.",
            image_url="https://placehold.co/400x300?text=Paithani+Weaver"
        )
        db.session.add(mah_artisan)
        db.session.commit()
        print(f"Created Artisan: {mah_artisan.name} (ID: {mah_artisan.id})")
    else:
        print(f"Using existing Maharashtra Artisan: {mah_artisan.name}")

    # Add products for this artisan
    products_data = [
        {
            "name": "Royal Blue Paithani Saree",
            "description": "Handwoven silk saree with peacock motifs.",
            "price": 18000.0,
            "image_url": "https://placehold.co/400x300?text=Blue+Paithani",
            "state": "Maharashtra",
            "district": "Aurangabad"
        },
        {
            "name": "Green Paithani Dupatta",
            "description": "Pure silk dupatta with golden zari border.",
            "price": 5000.0,
            "image_url": "https://placehold.co/400x300?text=Green+Dupatta",
            "state": "Maharashtra",
            "district": "Aurangabad"
        },
        {
            "name": "Kolhapuri Chappals",
            "description": "Traditional handcrafted leather footwear from Kolhapur.",
            "price": 1200.0,
            "image_url": "https://placehold.co/400x300?text=Kolhapuri+Chappals",
            "state": "Maharashtra",
            "district": "Kolhapur"
        },
        {
            "name": "Warli Painting",
            "description": "Tribal art form from the North Sahyadri Range in Maharashtra.",
            "price": 3500.0,
            "image_url": "https://placehold.co/400x300?text=Warli+Painting",
            "state": "Maharashtra",
            "district": "Palghar"
        },
        {
            "name": "Solapuri Chaddar",
            "description": "Famous cotton bed sheets from Solapur, known for their durability.",
            "price": 850.0,
            "image_url": "https://placehold.co/400x300?text=Solapuri+Chaddar",
            "state": "Maharashtra",
            "district": "Solapur"
        },
        {
            "name": "Nashik Grapes (Box)",
            "description": "Fresh, export-quality grapes from Nashik, the wine capital of India.",
            "price": 400.0,
            "image_url": "https://placehold.co/400x300?text=Nashik+Grapes",
            "state": "Maharashtra",
            "district": "Nashik"
        }
    ]

    for p_data in products_data:
        existing_p = Product.query.filter_by(name=p_data["name"], artisan_id=mah_artisan.id).first()
        if not existing_p:
            new_p = Product(
                name=p_data["name"],
                description=p_data["description"],
                price=p_data["price"],
                image_url=p_data["image_url"],
                stock=5,
                artisan_id=mah_artisan.id,
                state=p_data.get("state", "Maharashtra"),
                district=p_data.get("district")
            )
            db.session.add(new_p)
            print(f"Added Product: {new_p.name}")
        else:
            print(f"Product already exists: {existing_p.name}")
            # Optional: Update missing state/district if needed
            if not existing_p.state:
                 existing_p.state = p_data.get("state", "Maharashtra")
                 existing_p.district = p_data.get("district")
                 print(f"Updated state for: {existing_p.name}")

    # Add a non-Maharashtra product for contrast (if artisan 1 exists)
    other_artisan = Artisan.query.get(1)
    if other_artisan:
        other_p_data = {
            "name": "Rajasthani Blue Pottery Vase",
            "description": "Hand-painted ceramic vase.",
            "price": 1200.0,
            "image_url": "https://placehold.co/400x300?text=Blue+Pottery"
        }
        existing_other = Product.query.filter_by(name=other_p_data["name"], artisan_id=other_artisan.id).first()
        if not existing_other:
            other_p = Product(
                name=other_p_data["name"],
                description=other_p_data["description"],
                price=other_p_data["price"],
                image_url=other_p_data["image_url"],
                stock=10,
                artisan_id=other_artisan.id
            )
            db.session.add(other_p)
            print(f"Added Non-Maharashtra Product: {other_p.name}")

    db.session.commit()
    print("Seeding complete.")
