from app import app, mongo

def list_mh_products():
    with app.app_context():
        products = list(mongo.db.products.find({'state': 'Maharashtra'}))
        for p in products:
            print(f"{p.get('name')} - {p.get('district')}")

if __name__ == '__main__':
    list_mh_products()
