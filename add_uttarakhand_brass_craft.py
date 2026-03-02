from app import app, db, mongo
from models import Product, Artisan

def add_uttarakhand_brass_product():
    with app.app_context():
        # 1. Get Artisan
        artisan = Artisan.query.filter_by(name='Uttarakhand Crafts', state='Uttarakhand').first()
        if not artisan:
            # Fallback
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

        # 2. Product Details
        product_data = {
            "name": "Brass Craft",
            "description": "Traditional Brass metal work from Bageshwar, Uttarakhand. Ideal for home décor, providing a highly durable traditional touch.",
            "price": 2500.0, 
            "stock": 15,
            "district": "Bageshwar",
            "state": "Uttarakhand",
            # Image given from product4 folder
            "image_url": "/static/img/product4/temple_imitiation_f8cb6a78a4.webp",
            "artisan_id": artisan.id
        }

        # 3. Add to SQL
        existing = Product.query.filter_by(name=product_data['name'], state=product_data['state']).first()
        if existing:
             print(f"Product {product_data['name']} already exists in SQL. Updating details...")
             existing.price = product_data['price']
             existing.image_url = product_data['image_url']
             existing.description = product_data['description']
             existing.district = product_data['district']
             db.session.commit()
             sql_id = existing.id
        else:
            new_product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                stock=product_data['stock'],
                image_url=product_data['image_url'],
                district=product_data['district'],
                state=product_data['state'],
                artisan_id=product_data['artisan_id']
            )
            db.session.add(new_product)
            db.session.commit()
            sql_id = new_product.id
            print(f"Added {product_data['name']} to SQL (ID: {sql_id}).")

        # 4. Add to Mongo (Atlas)
        mongo_existing = mongo.db.products.find_one({"sql_id": sql_id})
        
        if mongo_existing:
             print(f"Product {product_data['name']} already exists in MongoDB. Updating...")
             mongo.db.products.update_one(
                 {"sql_id": sql_id},
                 {"$set": {
                     "image_url": product_data['image_url'],
                     "price": product_data['price'],
                     "district": product_data['district'],
                     "description": product_data['description'],
                     "state": product_data['state']
                 }}
             )
        else:
            mongo_product = product_data.copy()
            mongo_product['sql_id'] = sql_id
            mongo_product['artisan_name'] = artisan.name
            mongo.db.products.insert_one(mongo_product)
            print(f"Added {product_data['name']} to MongoDB Atlas.")

if __name__ == "__main__":
    add_uttarakhand_brass_product()
