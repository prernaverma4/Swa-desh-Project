from app import app, db, mongo
from models import Artisan, Product

def add_products_v2():
    with app.app_context():
        # 1. Find or Create a General Maharashtra Artisan 
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

        # 2. Define New Products (Batch 2)
        # 1.Jalna:Bronze Craft(Geori Bazar) 2.Beed:Kasuti Embroidery 3.Latur:Kasti Coriander 
        # 4.Parbhani:Bone and Horn Jewelry 5.Hingoli:Handloom Blanket (Ghongadi) 
        # 6.Nanded:Banana (Raw Banana Powder) 7.Dharashiv:Tuljapur Handloom Sarees
        new_products = [
            {
                "name": "Bronze Craft (Geori Bazar)",
                "district": "Jalna",
                "state": "Maharashtra",
                "description": "Exquisite traditional bronze metal crafts from Geori Bazar in Jalna district.",
                "price": 1500.0,
                "image_url": "https://placehold.co/400x300?text=Bronze+Craft",
                "stock": 10
            },
            {
                "name": "Kasuti Embroidery",
                "district": "Beed",
                "state": "Maharashtra",
                "description": "Intricate Kasuti embroidery work, a folk embroidery style with geometric patterns.",
                "price": 2200.0,
                "image_url": "https://placehold.co/400x300?text=Kasuti+Embroidery",
                "stock": 15
            },
            {
                "name": "Kasti Coriander",
                "district": "Latur",
                "state": "Maharashtra",
                "description": "Aromatic and flavorful Kasti coriander seeds/powder from Latur.",
                "price": 180.0,
                "image_url": "https://placehold.co/400x300?text=Kasti+Coriander",
                "stock": 50
            },
            {
                "name": "Bone and Horn Jewelry",
                "district": "Parbhani",
                "state": "Maharashtra",
                "description": "Unique handcrafted jewelry made from ethically sourced bone and horn.",
                "price": 650.0,
                "image_url": "https://placehold.co/400x300?text=Bone+Jewelry",
                "stock": 25
            },
            {
                "name": "Handloom Blanket (Ghongadi)",
                "district": "Hingoli",
                "state": "Maharashtra",
                "description": "Traditional rough wool blanket (Ghongadi) known for its durability and warmth.",
                "price": 1200.0,
                "image_url": "https://placehold.co/400x300?text=Ghongadi+Blanket",
                "stock": 20
            },
            {
                "name": "Raw Banana Powder",
                "district": "Nanded",
                "state": "Maharashtra",
                "description": "Nutritious and gluten-free raw banana powder processed from Nanded's banana cultivation.",
                "price": 300.0,
                "image_url": "https://placehold.co/400x300?text=Banana+Powder",
                "stock": 40
            },
            {
                "name": "Tuljapur Handloom Sarees",
                "district": "Dharashiv",
                "state": "Maharashtra",
                "description": "Elegant handloom sarees from the temple town of Tuljapur in Dharashiv district.",
                "price": 2500.0,
                "image_url": "https://placehold.co/400x300?text=Tuljapur+Saree",
                "stock": 12
            }
        ]

        # 3. Insert Products
        count = 0
        for p_data in new_products:
            # Check if exists (by name)
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
                db.session.commit()
                
                # MongoDB Insert
                mongo_product = p_data.copy()
                mongo_product['sql_id'] = new_product.id
                mongo_product['artisan_id'] = mah_artisan.id
                mongo_product['artisan_name'] = mah_artisan.name
                mongo.db.products.insert_one(mongo_product)

                print(f"Adding: {p_data['name']} ({p_data['district']})")
                count += 1
            else:
                print(f"Skipping: {p_data['name']} (Already exists)")
                # Optional: Update info if needed
                if not existing.district or existing.district != p_data['district']:
                     existing.district = p_data['district']
                     existing.state = p_data['state']
                     db.session.commit()
                     print(f"  -> Updated location info for {p_data['name']}")
                
                # Update Mongo
                mongo_existing = mongo.db.products.find_one({"sql_id": existing.id})
                if mongo_existing:
                     mongo.db.products.update_one(
                         {"sql_id": existing.id},
                         {"$set": {
                             "district": p_data['district'],
                             "state": p_data['state'],
                             "price": p_data['price'],
                             "image_url": p_data['image_url']
                         }}
                     )
                else:
                     mongo_product = p_data.copy()
                     mongo_product['sql_id'] = existing.id
                     mongo_product['artisan_id'] = mah_artisan.id
                     mongo_product['artisan_name'] = mah_artisan.name
                     mongo.db.products.insert_one(mongo_product)

        print(f"\nSuccess! Added {count} new products (Batch 2).")

if __name__ == "__main__":
    add_products_v2()
