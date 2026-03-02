from app import app, db, User

with app.app_context():
    user = User.query.filter_by(username='testuser').first()
    if user:
        print(f"User: {user.username}, Role: {user.role}")
    else:
        print("User not found")
