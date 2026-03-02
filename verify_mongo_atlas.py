from app import app, mongo

def verify_atlas():
    with app.app_context():
        try:
            print("Connecting to MongoDB Atlas...")
            # Ping
            mongo.cx.server_info()
            print("Connected successfully.")
            
            # Count products
            count = mongo.db.products.count_documents({})
            print(f"Total Products in Atlas: {count}")
            
            # List a few
            print("\nSample Products:")
            for p in mongo.db.products.find().limit(5):
                print(f"- {p.get('name')} ({p.get('district', 'N/A')}) - Price: {p.get('price')}")
                
            if count > 0:
                print("\nSUCCESS: Data migrated and accessible.")
            else:
                print("\nWARNING: Connected but no products found.")
                
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    verify_atlas()
