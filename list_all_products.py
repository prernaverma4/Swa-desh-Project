from app import app, db, Product

with app.app_context():
    products = Product.query.all()
    print(f"{'ID':<5} {'Name':<30} {'State':<20} {'Price':<10}")
    print("-" * 70)
    for p in products:
        state = p.state or 'N/A'
        price = str(p.price) if p.price is not None else 'N/A'
        print(f"{p.id:<5} {p.name:<30} {state:<20} {price:<10}")
