from app import app, db, mongo
from models import Product, Artisan

def add_mushroom_product():
    with app.app_context():
        # 1. Get Artisan
        artisan = Artisan.query.filter_by(name='Bihar Crafts', state='Bihar').first()
        if not artisan:
            # Fallback
            artisan = Artisan(
                name='Bihar Crafts',
                craft='Agriculture',
                state='Bihar',
                product_price=500.0,
                contact='9876543220',
                description='Authentic products from Bihar.'
            )
            db.session.add(artisan)
            db.session.commit()
            print("Created new artisan: Bihar Crafts")
        else:
            print("Using existing artisan: Bihar Crafts")

        # 2. Product Details
        product_data = {
            "name": "Mushroom",
            "description": "Fresh and high-quality mushrooms cultivated in West Champaran, Bihar.",
            "price": 290.0, # Average of 80-500
            "stock": 60,
            "district": "West Champaran",
            "state": "Bihar",
            # Image found: mushroom_0465bc1ecf.jpg
            "image_url": "/static/img/products/mushroom_0465bc1ecf.jpg",
            "artisan_id": artisan.id
        }

        # 3. Add to SQL
        existing = Product.query.filter_by(name=product_data['name'], state='Bihar').first()
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
                     "description": product_data['description']
                 }}
             )
        else:
            mongo_product = product_data.copy()
            mongo_product['sql_id'] = sql_id
            mongo_product['artisan_name'] = artisan.name
            mongo.db.products.insert_one(mongo_product)
            print(f"Added {product_data['name']} to MongoDB Atlas.")

if __name__ == "__main__":
    add_mushroom_product()
