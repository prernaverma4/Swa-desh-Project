from app import app, db, mongo
from models import Product, Artisan

def add_uttarakhand_more_products():
    with app.app_context():
        # Get Artisan
        artisan = Artisan.query.filter_by(name='Uttarakhand Crafts', state='Uttarakhand').first()
        if not artisan:
            artisan = Artisan(
                name='Uttarakhand Crafts',
                craft='Handicraft',
                state='Uttarakhand',
                product_price=1500.0,
                contact='9876543221',
                description='Authentic highly-durable products from Uttarakhand.'
            )
            db.session.add(artisan)
            db.session.commit()
            print("Created new artisan: Uttarakhand Crafts")
        else:
            print("Using existing artisan: Uttarakhand Crafts")

        products = [
            {
                "name": "Brass Craft",
                "description": "Traditional Brass metal work. Ideal for home décor with a highly durable traditional touch.",
                "price": 2500.0,
                "stock": 15,
                "district": "Bageshwar",
                "state": "Uttarakhand",
                "image_url": "/static/img/product4/temple_imitiation_f8cb6a78a4.webp"
            },
            {
                "name": "Herbal Products",
                "description": "Local medicinal and Ayurvedic herbal products sourced from the Himalayas.",
                "price": 600.0,
                "stock": 40,
                "district": "Chamoli",
                "state": "Uttarakhand",
                "image_url": "/static/img/product4/herbal_products_44ad6b6d8a.jpg"
            },
            {
                "name": "Bakery Products",
                "description": "Traditional flour and sugar baked goods, popular for domestic consumption.",
                "price": 300.0,
                "stock": 100,
                "district": "Dehradun",
                "state": "Uttarakhand",
                "image_url": "/static/img/product4/bakery_fe7febc4d3.jpg"
            },
            {
                "name": "Jaggery & Products",
                "description": "Organic sugarcane jaggery products, perfect for health-conscious consumers.",
                "price": 250.0,
                "stock": 80,
                "district": "Haridwar",
                "state": "Uttarakhand",
                "image_url": "/static/img/product4/jaggery_b177aacb9a.jpg"
            }
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
    add_uttarakhand_more_products()
