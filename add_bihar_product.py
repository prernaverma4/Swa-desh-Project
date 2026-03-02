from app import app, db, mongo
from models import Product, Artisan

def add_bihar_product():
    with app.app_context():
        # 1. Create or Get Artisan for Bihar
        artisan = Artisan.query.filter_by(name='Bihar Crafts', state='Bihar').first()
        if not artisan:
            artisan = Artisan(
                name='Bihar Crafts',
                craft='Agriculture',
                state='Bihar',
                product_price=400.0,
                contact='9876543220',
                description='Authentic products from Bihar.'
            )
            db.session.add(artisan)
            db.session.commit()
            print("Created new artisan: Bihar Crafts")
        else:
            print("Using existing artisan: Bihar Crafts")

        # 2. Product Details from User Image
        product_data = {
            "name": "Makhana",
            "description": "Premium quality Fox Nuts from Araria, Bihar. Known for their nutritional value.",
            "price": 900.0, # Average of 400-1400
            "stock": 50,
            "district": "Araria",
            "state": "Bihar",
            "image_url": "/static/img/products/makhana_2ae7660066.jpg",
            "artisan_id": artisan.id
        }

        # 3. Add to SQL
        # Check if exists first to avoid duplicates
        existing = Product.query.filter_by(name=product_data['name'], state='Bihar').first()
        if existing:
             print(f"Product {product_data['name']} already exists in SQL. Updating details...")
             existing.image_url = "/static/img/products/makhana_2ae7660066.jpg"  # Direct static path
             existing.price = product_data['price']
             existing.description = product_data['description']
             db.session.commit()
             sql_id = existing.id
        else:
            new_product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                stock=product_data['stock'],
                image_url="/static/img/products/makhana_2ae7660066.jpg", # Direct static path
                district=product_data['district'],
                state=product_data['state'],
                artisan_id=product_data['artisan_id']
            )
            db.session.add(new_product)
            db.session.commit()
            sql_id = new_product.id
            print(f"Added {product_data['name']} to SQL (ID: {sql_id}).")

        # 4. Add to Mongo (Atlas)
        # Check if exists in Mongo
        mongo_existing = mongo.db.products.find_one({"sql_id": sql_id})
        current_image = "/static/img/products/makhana_2ae7660066.jpg"

        if mongo_existing:
             print(f"Product {product_data['name']} already exists in MongoDB. Updating image...")
             mongo.db.products.update_one(
                 {"sql_id": sql_id},
                 {"$set": {
                     "image_url": current_image,
                     "price": product_data['price'],
                     "description": product_data['description']
                 }}
             )
        else:
            mongo_product = product_data.copy()
            mongo_product['sql_id'] = sql_id
            mongo_product['image_url'] = current_image
            mongo_product['artisan_name'] = artisan.name
            
            mongo.db.products.insert_one(mongo_product)
            print(f"Added {product_data['name']} to MongoDB Atlas.")

if __name__ == "__main__":
    add_bihar_product()
