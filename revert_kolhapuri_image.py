from app import app, db, mongo
from models import Product

def revert_kolhapuri():
    with app.app_context():
        # Revert to LoremFlickr pattern
        keyword = "sandals,leather"
        
        # Find product
        product = Product.query.filter(Product.name.ilike('%kolhapuri%')).first()
        
        if product:
            print(f"Found product: {product.name}")
            
            # Reconstruct original LoremFlickr URL
            new_url = f"https://loremflickr.com/600/400/{keyword}?lock={product.id}"
            
            # Update SQL
            product.image_url = new_url
            
            # Update Mongo
            mongo.db.products.update_one(
                {"sql_id": product.id},
                {"$set": {"image_url": new_url}}
            )
            
            db.session.commit()
            print(f"Successfully reverted image to: {new_url}")
        else:
            print("Product 'Kolhapuri' not found!")

if __name__ == "__main__":
    revert_kolhapuri()
