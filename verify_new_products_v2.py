from app import app, db
from models import Product

def verify_products_v2():
    with app.app_context():
        # Batch 2 names
        product_names = [
            "Bronze Craft (Geori Bazar)", "Kasuti Embroidery", "Kasti Coriander",
            "Bone and Horn Jewelry", "Handloom Blanket (Ghongadi)",
            "Raw Banana Powder", "Tuljapur Handloom Sarees"
        ]
        
        print(f"{'Product Name':<30} | {'District':<12} | {'Price':<8} | {'Status'}")
        print("-" * 65)
        
        found_count = 0
        for name in product_names:
            product = Product.query.filter_by(name=name).first()
            if product:
                status = "FOUND"
                found_count += 1
                dist = product.district if product.district else 'N/A'
                print(f"{product.name:<30} | {dist:<12} | {product.price:<8} | {status}")
            else:
                print(f"{name:<30} | {'---':<12} | {'---':<8} | MISSING")
        
        print("-" * 65)
        print(f"Total Found: {found_count}/{len(product_names)}")

if __name__ == "__main__":
    verify_products_v2()
