from app import app, db
from models import Product

def verify_products():
    with app.app_context():
        product_names = [
            "Chinor Rice", "Wild Honey", "Mango Seed Butter", 
            "Grape Seed Powder", "Banana Fiber Basket", 
            "Handloom Textile", "Tribal Textile Art"
        ]
        
        print(f"{'Product Name':<25} | {'District':<15} | {'Price':<10} | {'Status'}")
        print("-" * 65)
        
        found_count = 0
        for name in product_names:
            product = Product.query.filter_by(name=name).first()
            if product:
                status = "FOUND"
                found_count += 1
                print(f"{product.name:<25} | {product.district:<15} | {product.price:<10} | {status}")
            else:
                print(f"{name:<25} | {'---':<15} | {'---':<10} | MISSING")
        
        print("-" * 65)
        print(f"Total Found: {found_count}/{len(product_names)}")

if __name__ == "__main__":
    verify_products()
