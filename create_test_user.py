from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    username = "testuser"
    if not User.query.filter_by(username=username).first():
        hashed_password = generate_password_hash("password123")
        new_user = User(username=username, email="test@example.com", password=hashed_password, role="manufacturer")
        db.session.add(new_user)
        db.session.commit()
        print(f"Created test user: {username}")
    else:
        print(f"User {username} already exists")
