from app import app, db
from models import Artisan, Product

def add_products():
    with app.app_context():
        # 1. Find or Create a General Maharashtra Artisan 
        # (Using the existing one "Ganesh Patil" or creating a generic one if needed)
        mah_artisan = Artisan.query.filter_by(state='Maharashtra').first()
        
        if not mah_artisan:
            print("Creating General Maharashtra Artisan...")
            mah_artisan = Artisan(
                name="Maharashtra ODOP Artisan",
                craft="Various",
                state="Maharashtra",
                product_price=0,
                contact="contact@maharashtra.odop.in",
                description="Promoting One District One Product from Maharashtra.",
                image_url="https://placehold.co/400x300?text=MH+Artisan"
            )
            db.session.add(mah_artisan)
            db.session.commit()
        else:
            print(f"Using existing artisan: {mah_artisan.name} (ID: {mah_artisan.id})")

        # 2. Define New Products
        # 1.Bhandara:chinor rice 2.Gadchiroli:honey 3.Ratnagiri:Mango seed butter 4.Nashik:grape seed powder 5.jalgaon:banana fiber product 6.dhule:textile 7.nandubar:textile
        new_products = [
            {
                "name": "Chinor Rice",
                "district": "Bhandara",
                "state": "Maharashtra",
                "description": "Premium aromatic Chinor rice from Bhandara district, known for its distinct fragrance and taste.",
                "price": 120.0,
                "image_url": "https://placehold.co/400x300?text=Chinor+Rice",
                "stock": 50
            },
            {
                "name": "Wild Honey",
                "district": "Gadchiroli",
                "state": "Maharashtra",
                "description": "Pure, organic wild honey collected from the dense forests of Gadchiroli.",
                "price": 350.0,
                "image_url": "https://placehold.co/400x300?text=Gadchiroli+Honey",
                "stock": 30
            },
            {
                "name": "Mango Seed Butter",
                "district": "Ratnagiri",
                "state": "Maharashtra",
                "description": "Rich and moisturizing butter extracted from premium Ratnagiri mango seeds. Excellent for skincare.",
                "price": 450.0,
                "image_url": "https://placehold.co/400x300?text=Mango+Butter",
                "stock": 20
            },
            {
                "name": "Grape Seed Powder",
                "district": "Nashik",
                "state": "Maharashtra",
                "description": "Antioxidant-rich powder made from Nashik's finest grape seeds. A healthy dietary supplement.",
                "price": 250.0,
                "image_url": "https://placehold.co/400x300?text=Grape+Seed+Powder",
                "stock": 40
            },
            {
                "name": "Banana Fiber Basket",
                "district": "Jalgaon",
                "state": "Maharashtra",
                "description": "Eco-friendly handcrafted basket woven from banana production waste fibers in Jalgaon.",
                "price": 300.0,
                "image_url": "https://placehold.co/400x300?text=Banana+Fiber+Product",
                "stock": 15
            },
            {
                "name": "Handloom Textile",
                "district": "Dhule",
                "state": "Maharashtra",
                "description": "Traditional handloom textile fabric from Dhule, known for its quality and durability.",
                "price": 600.0,
                "image_url": "https://placehold.co/400x300?text=Dhule+Textile",
                "stock": 25
            },
            {
                "name": "Tribal Textile Art",
                "district": "Nandurbar",
                "state": "Maharashtra",
                "description": "Unique textile art reflecting the rich tribal culture of Nandurbar district.",
                "price": 850.0,
                "image_url": "https://placehold.co/400x300?text=Nandurbar+Textile",
                "stock": 10
            }
        ]

        # 3. Insert Products
        count = 0
        for p_data in new_products:
            # Check if exists (by name and district to be safe)
            existing = Product.query.filter_by(name=p_data['name']).first()
            if not existing:
                new_product = Product(
                    name=p_data['name'],
                    description=p_data['description'],
                    price=p_data['price'],
                    image_url=p_data['image_url'],
                    stock=p_data['stock'],
                    state=p_data['state'],
                    district=p_data['district'],
                    artisan_id=mah_artisan.id
                )
                db.session.add(new_product)
                print(f"Adding: {p_data['name']} ({p_data['district']})")
                count += 1
            else:
                print(f"Skipping: {p_data['name']} (Already exists)")
                # Optional: Update district if missing
                if not existing.district:
                     existing.district = p_data['district']
                     existing.state = p_data['state']
                     print(f"  -> Updated location info for {p_data['name']}")

        db.session.commit()
        print(f"\nSuccess! Added {count} new products.")

if __name__ == "__main__":
    add_products()
