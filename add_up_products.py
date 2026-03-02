from app import app, db, mongo
from models import Product, Artisan

def add_up_products():
    with app.app_context():
        # Get Artisan
        artisan = Artisan.query.filter_by(name='UP Crafts', state='Uttar Pradesh').first()
        if not artisan:
            artisan = Artisan(
                name='UP Crafts',
                craft='Handicraft',
                state='Uttar Pradesh',
                product_price=1000.0,
                contact='9876543222',
                description='Authentic ODOP products from Uttar Pradesh.'
            )
            db.session.add(artisan)
            db.session.commit()
            print("Created new artisan: UP Crafts")
        else:
            print("Using existing artisan: UP Crafts")

        products = [
            {"name": "Locks", "description": "Traditional lock industry from Aligarh. High strength and security.", "price": 300.0, "stock": 50, "district": "Aligarh", "state": "Uttar Pradesh", "image_url": "/static/img/product2/lock2.jpg"},
            {"name": "Black Pottery", "description": "GI black clay craft from Azamgarh.", "price": 1500.0, "stock": 20, "district": "Azamgarh", "state": "Uttar Pradesh", "image_url": "/static/img/product2/black-pottery.jpg"},
            {"name": "Zari Zardozi", "description": "Metallic embroidery craft from Bareilly.", "price": 4500.0, "stock": 10, "district": "Bareilly", "state": "Uttar Pradesh", "image_url": "/static/img/product2/lucknow4.jpg"},
            {"name": "Carpets", "description": "Hand-knotted carpets from Bhadohi.", "price": 25000.0, "stock": 5, "district": "Bhadohi", "state": "Uttar Pradesh", "image_url": "/static/img/product2/bhadoi4.jpg"},
            {"name": "Glass Bangles", "description": "Decorative bangles and glass craft from Firozabad.", "price": 350.0, "stock": 100, "district": "Firozabad", "state": "Uttar Pradesh", "image_url": "/static/img/products/lac_bangles_d2df1cb8b3.jpg"},
            {"name": "Hing", "description": "Asafoetida processing from Hathras.", "price": 3000.0, "stock": 15, "district": "Hathras", "state": "Uttar Pradesh", "image_url": "/static/img/product2/61NEmftqOmL.jpg"},
            {"name": "Perfume (Attar)", "description": "Natural essential oils and rose water from Kannauj.", "price": 2500.0, "stock": 30, "district": "Kannauj", "state": "Uttar Pradesh", "image_url": "/static/img/products/lemon_grass_8439d7a9d0.jpg"},
            {"name": "Saddlery", "description": "Horse gear and leather goods from Kanpur Nagar.", "price": 25000.0, "stock": 8, "district": "Kanpur Nagar", "state": "Uttar Pradesh", "image_url": "/static/img/product2/61NEmftqOmL.jpg"},
            {"name": "Chikankari", "description": "Hand embroidery and traditional textile craft from Lucknow.", "price": 1900.0, "stock": 40, "district": "Lucknow", "state": "Uttar Pradesh", "image_url": "/static/img/product2/lucknow4.jpg"},
            {"name": "Tarkashi (Brass Inlay)", "description": "Brass wire inlay craft from Mainpuri.", "price": 5500.0, "stock": 12, "district": "Mainpuri", "state": "Uttar Pradesh", "image_url": "/static/img/product2/moradabad.jpg"},
            {"name": "Peda", "description": "Traditional milk sweet and religious items from Mathura.", "price": 450.0, "stock": 60, "district": "Mathura", "state": "Uttar Pradesh", "image_url": "/static/img/product4/bal_mithai_f11e625e7e.jpg"},
            {"name": "Sports Goods", "description": "Cricket gear and sports equipment from Meerut.", "price": 2750.0, "stock": 25, "district": "Meerut", "state": "Uttar Pradesh", "image_url": "/static/img/product2/meerut.jpg"},
            {"name": "Durries", "description": "Floor rugs and textiles from Mirzapur.", "price": 2900.0, "stock": 18, "district": "Mirzapur", "state": "Uttar Pradesh", "image_url": "/static/img/product2/multicolor-polyester-carpet-abstract-6-ft-x-4-ft-machine-made-carpet-multicolor-polyester-carpet-abs-ldmuo2.webp"},
            {"name": "Brassware", "description": "Decorative metal and brassware from Moradabad.", "price": 10500.0, "stock": 10, "district": "Moradabad", "state": "Uttar Pradesh", "image_url": "/static/img/product2/moradabad.jpg"},
            {"name": "Jaggery", "description": "Agro gur blocks from Muzaffarnagar.", "price": 55.0, "stock": 200, "district": "Muzaffarnagar", "state": "Uttar Pradesh", "image_url": "/static/img/product4/jaggery_b177aacb9a.jpg"},
            {"name": "Patchwork", "description": "Traditional Rampuri knife and patchwork from Rampur.", "price": 2750.0, "stock": 15, "district": "Rampur", "state": "Uttar Pradesh", "image_url": "/static/img/product2/Rampurpro1.jpg"},
            {"name": "Wood Carving", "description": "Carved decor and furniture from Saharanpur.", "price": 25000.0, "stock": 5, "district": "Saharanpur", "state": "Uttar Pradesh", "image_url": "/static/img/product2/uttarakhand_aipan_3c0e862511.webp"},
            {"name": "Kala Namak Rice", "description": "Aromatic rice and agro products from Siddharthnagar.", "price": 90.0, "stock": 150, "district": "Siddharthnagar", "state": "Uttar Pradesh", "image_url": "/static/img/product4/red_rice_46e7cfcf95.jpg"},
            {"name": "Banarasi Saree", "description": "Silk brocade and traditional textile from Varanasi.", "price": 52500.0, "stock": 4, "district": "Varanasi", "state": "Uttar Pradesh", "image_url": "/static/img/product2/lucknow4.jpg"},
            {"name": "Petha", "description": "Ash gourd sweet (GI-tag) from Agra.", "price": 300.0, "stock": 80, "district": "Agra", "state": "Uttar Pradesh", "image_url": "/static/img/product4/bakery_fe7febc4d3.jpg"}
        ]

        for p_data in products:
            existing = Product.query.filter_by(name=p_data['name'], state=p_data['state']).first()
            if existing:
                print(f"Product {p_data['name']} already exists in SQL. Updating details...")
                existing.price = p_data['price']
                existing.image_url = p_data['image_url']
                existing.description = p_data['description']
                existing.district = p_data['district']
                db.session.commit()
                sql_id = existing.id
            else:
                new_product = Product(
                    name=p_data['name'],
                    description=p_data['description'],
                    price=p_data['price'],
                    stock=p_data['stock'],
                    image_url=p_data['image_url'],
                    district=p_data['district'],
                    state=p_data['state'],
                    artisan_id=artisan.id
                )
                db.session.add(new_product)
                db.session.commit()
                sql_id = new_product.id
                print(f"Added {p_data['name']} to SQL (ID: {sql_id}).")

            # Mongo
            mongo_existing = mongo.db.products.find_one({"sql_id": sql_id})
            if mongo_existing:
                print(f"Product {p_data['name']} already exists in MongoDB. Updating...")
                mongo.db.products.update_one(
                    {"sql_id": sql_id},
                    {"$set": {
                        "image_url": p_data['image_url'],
                        "price": p_data['price'],
                        "district": p_data['district'],
                        "description": p_data['description'],
                        "state": p_data['state']
                    }}
                )
            else:
                mongo_product = p_data.copy()
                mongo_product['sql_id'] = sql_id
                mongo_product['artisan_id'] = artisan.id
                mongo_product['artisan_name'] = artisan.name
                mongo.db.products.insert_one(mongo_product)
                print(f"Added {p_data['name']} to MongoDB Atlas.")

if __name__ == "__main__":
    add_up_products()
