from app import app, db, mongo
from models import Product

def update_mh_images():
    # Mapping based on districts and proximity from product3 folder
    mapping = {
        "Solapuri Chaddar": "solapur.png",
        "Nashik Grapes (Box)": "nashik.jpg",
        "Grape Seed Powder": "nashik.jpg",
        "Chinor Rice": "bhandara_chinoor_rice_148a871fa5.jpg",
        "Handloom Textile": "dhule or nandurbar.jpg",
        "Tribal Textile Art": "dhule or nandurbar.jpg",
        "Bronze Craft (Geori Bazar)": "jalna.png",
        "Kasuti Embroidery": "beed.png",
        "Kasti Coriander": "latur.png",
        "Bone and Horn Jewelry": "parbhani.png",
        "Handloom Blanket (Ghongadi)": "hingoli (2).png",
        "Raw Banana Powder": "nanded.png",
        "Royal Blue Paithani Sarees": "punari pagadi.png",
        "Green Paithani Dupatta": "kolhapur.png",
        "Warli Painting": "sankurti-kala-darpan-ghantali-thane-west-thane-gift-shops-kvvxjafwqa.webp",
        "Wild Honey": "Amravti.jpg",
        "Mango Seed Butter": "sidhurg.png",
        "Banana Fiber Basket": "Akola.jpg",
        "Tuljapur Handloom Sarees": "yavatmal.webp"
    }

    base_path = "/static/img/product3/"
    
    with app.app_context():
        for product_name, img_file in mapping.items():
            img_url = base_path + img_file
            
            # Update SQL
            sql_product = Product.query.filter_by(name=product_name, state="Maharashtra").first()
            if sql_product:
                sql_product.image_url = img_url
                db.session.commit()
                print(f"Updated SQL image for {product_name}")
                
                # Update Mongo
                mongo.db.products.update_one(
                    {"sql_id": sql_product.id},
                    {"$set": {"image_url": img_url}}
                )
                print(f"Updated Mongo image for {product_name}")
            else:
                print(f"Product {product_name} not found in SQL.")

if __name__ == '__main__':
    update_mh_images()
