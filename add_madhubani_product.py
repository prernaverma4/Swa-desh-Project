from app import app, db, mongo
from models import Product, Artisan

def add_madhubani_product():
    with app.app_context():
        # 1. Get Artisan
        artisan = Artisan.query.filter_by(name='Bihar Crafts', state='Bihar').first()
        if not artisan:
            print("Artisan 'Bihar Crafts' not found. Please run add_bihar_product.py first or create it.")
            return

        # 2. Product Details
        product_data = {
            "name": "Madhubani Painting",
            "description": "Traditional Maithili art form from Madhubani district, Bihar. Characterized by eye-catching geometrical patterns.",
            "price": 2500.0, # Representative price logic
            "stock": 20,
            "district": "Madhubani",
            "state": "Bihar",
            "image_url": "/static/img/products/madhubhani_paintings_c43aff0588.jpg",
            "artisan_id": artisan.id
        }

        # 3. Add to SQL
        existing = Product.query.filter_by(name=product_data['name'], state='Bihar').first()
        if existing:
             print(f"Product {product_data['name']} already exists in SQL. Updating...")
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
    add_madhubani_product()
