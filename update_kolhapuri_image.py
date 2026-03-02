from app import app, db, mongo
from models import Product

def update_kolhapuri():
    with app.app_context():
        # Specific URL found on Wikimedia Commons
        authentic_url = "https://upload.wikimedia.org/wikipedia/commons/e/ea/Kolhapur_chappal.jpg"
        
        # Find product
        # Note: Name might vary slightly, so using 'like'
        product = Product.query.filter(Product.name.ilike('%kolhapuri%')).first()
        
        if product:
            print(f"Found product: {product.name}")
            
            # Update SQL
            product.image_url = authentic_url
            
            # Update Mongo
            mongo.db.products.update_one(
                {"sql_id": product.id},
                {"$set": {"image_url": authentic_url}}
            )
            
            db.session.commit()
            print(f"Successfully updated image to: {authentic_url}")
        else:
            print("Product 'Kolhapuri' not found!")

if __name__ == "__main__":
    update_kolhapuri()
