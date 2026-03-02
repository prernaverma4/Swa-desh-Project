from app import app, db, mongo
from models import Product

def update_images():
    with app.app_context():
        # Map product names (partial match) to keywords
        keyword_map = {
            "Paithani": "saree,silk",
            "Warli": "tribal,painting",
            "Kolhapuri": "sandals,leather",
            "Chinor Rice": "rice,grain",
            "Honey": "honey,jar",
            "Mango": "mango,fruit",
            "Grape": "grapes,powder",
            "Banana Fiber": "basket,craft",
            "Textile": "fabric,textile",
            "Bronze": "bronze,metal",
            "Kasuti": "embroidery,cloth",
            "Coriander": "spices,seeds",
            "Bone": "jewelry,necklace",
            "Ghongadi": "blanket,wool",
            "Banana Powder": "banana,powder",
            "Tuljapur": "saree,traditional",
            "Pottery": "pottery,clay",
            "Blue Pottery": "blue,pottery",
            "Chaddar": "bedsheet,textile"
        }

        products = Product.query.all()
        print(f"Updating images for {len(products)} products...")
        
        count = 0
        for p in products:
            # Find best keyword
            keyword = "craft,india" # Default
            for key, val in keyword_map.items():
                if key.lower() in p.name.lower():
                    keyword = val
                    break
            
            # Generate URL (adding random param to avoid caching same image for same keywords if possible, 
            # though loremflickr might give same. We'll use ID to randomize)
            new_url = f"https://loremflickr.com/600/400/{keyword}?lock={p.id}"
            
            # Update SQL
            p.image_url = new_url
            
            # Update Mongo
            mongo.db.products.update_one(
                {"sql_id": p.id},
                {"$set": {"image_url": new_url}}
            )
            
            count += 1
            print(f"Updated {p.name} -> {keyword}")
            
        db.session.commit()
        print(f"\nSuccessfully updated {count} product images.")

if __name__ == "__main__":
    update_images()
