from app import app, db, mongo
from models import Product

def migrate():
    with app.app_context():
        # Check connection
        try:
            # Ping to check connection
            mongo.cx.server_info()
            print("Connected to MongoDB.")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            return

        # Clear collection
        mongo.db.products.delete_many({})
        print("Cleared MongoDB 'products' collection.")

        # Fetch from SQL
        products = Product.query.all()
        print(f"Found {len(products)} products in SQL database.")

        count = 0
        for p in products:
            p_dict = p.to_dict()
            
            # Enrich with fields that might be missing in to_dict or useful for NoSQL
            p_dict['state'] = p.state
            p_dict['district'] = p.district
            p_dict['sql_id'] = p.id
            
            # Ensure price is float
            if p_dict.get('price'):
                 p_dict['price'] = float(p_dict['price'])

            mongo.db.products.insert_one(p_dict)
            count += 1
            print(f"Migrated: {p.name}")
            
        print(f"\nMigration Complete. {count} products moved to MongoDB.")

if __name__ == "__main__":
    migrate()
