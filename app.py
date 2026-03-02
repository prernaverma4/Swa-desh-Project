"""
Digital Catalyst: AI-Driven Platform for Indian Economic Growth & Heritage Preservation
Main Flask Application with REST APIs and Dashboard
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, HeritageSite, Artisan, Product, Order, Hotel, HotelBooking, Bookmark, SiteView
import json
from ml.recommendation_engine import RecommendationEngine
import os
import csv
from io import StringIO
from datetime import datetime
from functools import lru_cache
from types import SimpleNamespace

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'digital-catalyst-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb+srv://prernaIIT:prernaIIT1104@cluster0.1e9vauw.mongodb.net/test?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'landing'

# Initialize ML engine
ml_engine = RecommendationEngine()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def _ensure_schema_columns():
    """Add missing columns for existing DBs (role, image_url). Run once per process."""
    from sqlalchemy import text
    migrations = [
        ("users", "role", "VARCHAR(20) DEFAULT 'user'"),
        ("heritage_sites", "image_url", "VARCHAR(500)"),
        ("artisans", "image_url", "VARCHAR(500)"),
        ("products", "district", "VARCHAR(100)"),
        ("products", "state", "VARCHAR(100)"),
    ]
    for table, column, col_type in migrations:
        try:
            db.session.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            if "duplicate column name" not in str(e).lower():
                raise


_role_migration_done = False


@app.before_request
def run_schema_migration_once():
    global _role_migration_done
    if _role_migration_done:
        return
    try:
        _ensure_schema_columns()
    except Exception:
        pass
    _role_migration_done = True


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/')
def landing():
    """Landing page – show when not logged in, else redirect to dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Full login page: Sign in + Login as Manufacturer"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        login_type = request.form.get('login_type', 'user')  # 'user' or 'manufacturer'
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            if login_type == 'manufacturer' and not user.is_manufacturer:
                flash('This account is not registered as a manufacturer. Sign in as a regular user or register as manufacturer.', 'warning')
                return redirect(url_for('login'))
            login_user(user)
            session['login_as_manufacturer'] = (login_type == 'manufacturer')
            flash('Login successful!', 'success')
            if login_type == 'manufacturer':
                return redirect(url_for('product_list_2'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.before_request
def restrict_manufacturer_access():
    """Restrict manufacturer access to allowed routes only"""
    # print(f"DEBUG: Endpoint: {request.endpoint}, User: {current_user}, Is Mfg: {current_user.is_authenticated and current_user.is_manufacturer()}")
    if current_user.is_authenticated and current_user.is_manufacturer():
        allowed_endpoints = [
            'product_list_2', 'static', 'logout', 'login', 'register',
            'product_detail', 'add_product_2', 'edit_product_2', 'delete_product_2'
        ]
        
        if request.endpoint and request.endpoint not in allowed_endpoints:
            # print(f"DEBUG: Redirecting restricted access from {request.endpoint} to product_list_2")
            return redirect(url_for('product_list_2'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        role = request.form.get('role', 'user')
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    session.pop('login_as_manufacturer', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('landing'))


# ============================================================================
# DASHBOARD ROUTES
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with analytics"""
    # Get all data with optimized queries
    heritage_sites = HeritageSite.query.with_entities(
        HeritageSite.id, HeritageSite.name, HeritageSite.state, 
        HeritageSite.category, HeritageSite.annual_visitors
    ).all()
    
    artisans = Artisan.query.with_entities(
        Artisan.id, Artisan.name, Artisan.craft, 
        Artisan.state, Artisan.product_price
    ).all()
    
    # Convert to dict for ML engine
    sites_data = [{'id': s.id, 'name': s.name, 'state': s.state, 
                   'category': s.category, 'annual_visitors': s.annual_visitors} 
                  for s in heritage_sites]
    artisans_data = [{'id': a.id, 'name': a.name, 'craft': a.craft, 
                      'state': a.state, 'product_price': a.product_price} 
                     for a in artisans]
    
    # Get recommendations (list of dicts with id)
    recommended_sites_data = ml_engine.recommend_heritage_sites(sites_data, top_n=5)
    recommended_site_ids = [s['id'] for s in recommended_sites_data if s.get('id')]
    recommended_sites = HeritageSite.query.filter(HeritageSite.id.in_(recommended_site_ids)).all() if recommended_site_ids else []
    # Keep order by visitor count (same as ML order)
    recommended_sites.sort(key=lambda s: s.annual_visitors or 0, reverse=True)
    
    state_distribution = ml_engine.get_state_wise_distribution(artisans_data)
    visitor_trends = ml_engine.get_visitor_trends(sites_data)
    economic_impact = ml_engine.calculate_economic_impact(sites_data, artisans_data)
    
    # Calculate statistics
    stats = {
        'total_heritage_sites': len(heritage_sites),
        'total_artisans': len(artisans),
        'total_states': len(set([s.state for s in heritage_sites] + [a.state for a in artisans])),
        'total_visitors': sum([s.annual_visitors for s in heritage_sites])
    }
    
    # Get full objects for display
    full_sites = HeritageSite.query.limit(10).all()
    full_artisans = Artisan.query.limit(10).all()
    
    return render_template('dashboard.html',
                         stats=stats,
                         heritage_sites=full_sites,
                         artisans=full_artisans,
                         recommended_sites=recommended_sites,
                         state_distribution=state_distribution,
                         visitor_trends=visitor_trends,
                         economic_impact=economic_impact)


# ============================================================================
# HERITAGE SITE ROUTES
# ============================================================================

@app.route('/heritage')
@login_required
def heritage_list():
    """List all heritage sites"""
    search = request.args.get('search', '')
    state_filter = request.args.get('state', '')
    category_filter = request.args.get('category', '')
    
    query = HeritageSite.query
    
    if search:
        query = query.filter(HeritageSite.name.ilike(f'%{search}%'))
    if state_filter:
        query = query.filter(HeritageSite.state == state_filter)
    if category_filter:
        query = query.filter(HeritageSite.category == category_filter)
    
    sites = query.limit(100).all()
    
    # Get unique states and categories for filters
    all_states = db.session.query(HeritageSite.state).distinct().limit(50).all()
    all_categories = db.session.query(HeritageSite.category).distinct().limit(50).all()
    
    return render_template('heritage.html',
                         sites=sites,
                         states=[s[0] for s in all_states],
                         categories=[c[0] for c in all_categories])


@app.route('/heritage/add', methods=['GET', 'POST'])
@login_required
def add_heritage():
    """Add new heritage site"""
    if request.method == 'POST':
        name = request.form.get('name')
        state = request.form.get('state')
        category = request.form.get('category')
        description = request.form.get('description')
        annual_visitors = int(request.form.get('annual_visitors', 0))
        
        image_url = request.form.get('image_url') or None
        new_site = HeritageSite(
            name=name,
            state=state,
            category=category,
            description=description,
            image_url=image_url,
            annual_visitors=annual_visitors
        )
        
        db.session.add(new_site)
        db.session.commit()
        
        flash('Heritage site added successfully!', 'success')
        return redirect(url_for('heritage_list'))
    
    return render_template('add_heritage.html')


@app.route('/heritage/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_heritage(id):
    """Edit heritage site"""
    site = HeritageSite.query.get_or_404(id)
    
    if request.method == 'POST':
        site.name = request.form.get('name')
        site.state = request.form.get('state')
        site.category = request.form.get('category')
        site.description = request.form.get('description')
        site.image_url = request.form.get('image_url') or None
        site.annual_visitors = int(request.form.get('annual_visitors', 0))
        
        db.session.commit()
        
        flash('Heritage site updated successfully!', 'success')
        return redirect(url_for('heritage_list'))
    
    return render_template('edit_heritage.html', site=site)


@app.route('/heritage/delete/<int:id>', methods=['POST'])
@login_required
def delete_heritage(id):
    """Delete heritage site"""
    site = HeritageSite.query.get_or_404(id)
    db.session.delete(site)
    db.session.commit()
    
    flash('Heritage site deleted successfully!', 'info')
    return redirect(url_for('heritage_list'))


@app.route('/heritage/<int:id>')
@login_required
def heritage_detail(id):
    """Heritage site detail page with image and full description"""
    site = HeritageSite.query.get_or_404(id)
    return render_template('heritage_detail.html', site=site)


# ============================================================================
# ARTISAN ROUTES
# ============================================================================

@app.route('/artisans')
@login_required
def artisan_list():
    """List all artisans"""
    search = request.args.get('search', '')
    state_filter = request.args.get('state', '')
    craft_filter = request.args.get('craft', '')
    
    query = Artisan.query
    
    if search:
        query = query.filter(Artisan.name.ilike(f'%{search}%'))
    if state_filter:
        query = query.filter(Artisan.state == state_filter)
    if craft_filter:
        query = query.filter(Artisan.craft == craft_filter)
    
    artisans = query.limit(100).all()
    
    # Get unique states and crafts for filters
    all_states = db.session.query(Artisan.state).distinct().limit(50).all()
    all_crafts = db.session.query(Artisan.craft).distinct().limit(50).all()
    
    return render_template('artisans.html',
                         artisans=artisans,
                         states=[s[0] for s in all_states],
                         crafts=[c[0] for c in all_crafts])


@app.route('/artisans/add', methods=['GET', 'POST'])
@login_required
def add_artisan():
    """Add new artisan"""
    if request.method == 'POST':
        name = request.form.get('name')
        craft = request.form.get('craft')
        state = request.form.get('state')
        product_price = float(request.form.get('product_price', 0))
        contact = request.form.get('contact')
        description = request.form.get('description')
        
        image_url = request.form.get('image_url') or None
        new_artisan = Artisan(
            name=name,
            craft=craft,
            state=state,
            product_price=product_price,
            contact=contact,
            description=description,
            image_url=image_url
        )
        
        db.session.add(new_artisan)
        db.session.commit()
        
        flash('Artisan added successfully!', 'success')
        return redirect(url_for('artisan_list'))
    
    return render_template('add_artisan.html')


@app.route('/artisans/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_artisan(id):
    """Edit artisan"""
    artisan = Artisan.query.get_or_404(id)
    
    if request.method == 'POST':
        artisan.name = request.form.get('name')
        artisan.craft = request.form.get('craft')
        artisan.state = request.form.get('state')
        artisan.product_price = float(request.form.get('product_price', 0))
        artisan.contact = request.form.get('contact')
        artisan.description = request.form.get('description')
        artisan.image_url = request.form.get('image_url') or None
        
        db.session.commit()
        
        flash('Artisan updated successfully!', 'success')
        return redirect(url_for('artisan_list'))
    
    return render_template('edit_artisan.html', artisan=artisan)


@app.route('/artisans/delete/<int:id>', methods=['POST'])
@login_required
def delete_artisan(id):
    """Delete artisan"""
    artisan = Artisan.query.get_or_404(id)
    db.session.delete(artisan)
    db.session.commit()
    
    flash('Artisan deleted successfully!', 'info')
    return redirect(url_for('artisan_list'))


@app.route('/artisans/<int:id>')
@login_required
def artisan_detail(id):
    """Artisan detail page with image and full description"""
    artisan = Artisan.query.get_or_404(id)
    return render_template('artisan_detail.html', artisan=artisan)


# ============================================================================
# PRODUCT ROUTES
# ============================================================================

@app.route('/Products2')
@login_required
def product_list_2():
    """List products for manufacturers (Version 2) - Airbnb Style Grid with State Filtering"""
    state_filter = request.args.get('state')
    
    # Fetch from MongoDB
    query = {}
    if state_filter:
        query['state'] = state_filter
        
    # Get products from Mongo
    products_cursor = mongo.db.products.find(query)
    products = list(products_cursor)
    
    # MongoDB returns dicts. Jinja2 allows dot notation for dicts in recent versions, 
    # but to be safe and consistent with SQLAlchemy objects, we can wrap them or just use them as is.
    # We'll assume the template can handle dicts or we patch it if needed.
    
    return render_template('products2.html', products=products, selected_state=state_filter)

@app.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product_2():
    """Add new product (Manufacturer Only)"""
    if not current_user.is_manufacturer():
        flash('Access denied.', 'danger')
        return redirect(url_for('product_list_2'))
        
    if request.method == 'POST':
        artisan_name = request.form.get('artisan_name')
        name = request.form.get('name')
        state = request.form.get('state')
        district = request.form.get('district')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        image_url = request.form.get('image_url')
        
        # 1. SQL Write (Maintain Integrity)
        username = current_user.username
        artisan = Artisan.query.filter_by(name=username).first()
        
        if not artisan:
            artisan = Artisan(
                name=artisan_name or username,
                craft='Regional Specialties',
                state=state or 'Maharashtra',
                product_price=0,
                contact=current_user.email,
                description=f"Authentic products from {district}, {state}",
                image_url="https://placehold.co/400x300?text=Artisan"
            )
            db.session.add(artisan)
        else:
             if artisan_name: artisan.name = artisan_name
             if state: artisan.state = state
        
        db.session.commit()
            
        new_product = Product(
            name=name, description=description, price=price, stock=stock,
            image_url=image_url, district=district, state=state, artisan_id=artisan.id
        )
        db.session.add(new_product)
        db.session.commit()
        
        # 2. MongoDB Write
        mongo_product = {
            "name": name,
            "description": description,
            "price": price,
            "stock": stock,
            "image_url": image_url,
            "district": district,
            "state": state,
            "artisan_id": artisan.id,
            "artisan_name": artisan.name,
            "sql_id": new_product.id
        }
        mongo.db.products.insert_one(mongo_product)
        
        flash('Product listed successfully!', 'success')
        return redirect(url_for('product_list_2'))

    return render_template('manage_product.html', product=None)

@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product_2(id):
    """Edit product (Manufacturer Only)"""
    if not current_user.is_manufacturer():
        flash('Access denied.', 'danger')
        return redirect(url_for('product_list_2'))
        
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        # SQL Update
        artisan_name = request.form.get('artisan_name')
        if artisan_name and product.artisan.name != artisan_name:
             product.artisan.name = artisan_name

        product.name = request.form.get('name')
        product.state = request.form.get('state')
        product.district = request.form.get('district')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.image_url = request.form.get('image_url')
        
        db.session.commit()
        
        # MongoDB Update
        mongo.db.products.update_one(
            {"sql_id": id},
            {"$set": {
                "name": product.name,
                "state": product.state,
                "district": product.district,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "image_url": product.image_url,
                "artisan_name": product.artisan.name
            }}
        )
        
        flash('Product updated successfully.', 'success')
        return redirect(url_for('product_list_2'))
        
    return render_template('manage_product.html', product=product)

@app.route('/product/delete/<int:id>', methods=['POST'])
@login_required
def delete_product_2(id):
    """Delete product (Manufacturer Only)"""
    if not current_user.is_manufacturer():
        flash('Access denied.', 'danger')
        return redirect(url_for('product_list_2'))
        
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    
    # MongoDB Delete
    mongo.db.products.delete_one({"sql_id": id})
    
    flash('Product removed from listing.', 'success')
    return redirect(url_for('product_list_2'))

class MongoProductWrapper:
    """Wrapper to make MongoDB dictionaries look like SQLAlchemy Product objects for the template"""
    
    # Mapping to fix incorrect loremflickr links dumped in the DB
    IMAGE_MAP = {
        "Bal Mithai": "/static/img/product4/bal_mithai_f11e625e7e.jpg",
        "Tweed": "/static/img/product4/natural_fibre_a69c9fc2ca.jpg",
        "Temple Imitation": "/static/img/product4/temple_imitiation_f8cb6a78a4.webp",
        "Red Rice": "/static/img/product4/red_rice_46e7cfcf95.jpg",
        "Herbal Products": "/static/img/product4/herbal_products_44ad6b6d8a.jpg",
        "Bakery Products": "/static/img/product4/bakery_fe7febc4d3.jpg",
        "Jaggery & Products": "/static/img/product4/jaggery_b177aacb9a.jpg",
        "Brass Craft": "/static/img/product4/temple_imitiation_f8cb6a78a4.webp",
        "Brass Utensil Work": "/static/img/product4/temple_imitiation_f8cb6a78a4.webp",
        "Tilkut (Gaya)": "/static/img/products/40367.jpg",
        "Tilkut": "/static/img/products/40367.jpg",
        "Locks": "/static/img/product2/lock2.jpg",
        "Black Pottery": "/static/img/product2/black-pottery.jpg",
        "Zari Zardozi": "/static/img/product2/lucknow4.jpg",
        "Carpets": "/static/img/product2/bhadoi4.jpg",
        "Glass Bangles": "/static/img/products/lac_bangles_d2df1cb8b3.jpg",
        "Hing": "/static/img/product2/61NEmftqOmL.jpg",
        "Perfume (Attar)": "/static/img/products/lemon_grass_8439d7a9d0.jpg",
        "Saddlery": "/static/img/product2/61NEmftqOmL.jpg",
        "Chikankari": "/static/img/product2/lucknow4.jpg",
        "Tarkashi (Brass Inlay)": "/static/img/product2/moradabad.jpg",
        "Kalanamak Rice": "/static/img/products/75151.jpg"
    }

    def __init__(self, data):
        self.id = str(data.get('_id'))
        self.name = data.get('name', '')
        self.description = data.get('description', '')
        self.price = data.get('price', 0)
        self.stock = data.get('stock', 0)
        
        # Override corrupted database image URLs with known local paths if available
        base_url = data.get('image_url', '')
        if self.name in self.IMAGE_MAP:
            self.image_url = self.IMAGE_MAP[self.name]
        else:
            self.image_url = base_url
            
        # Mock artisan relationship
        class MockArtisan:
            def __init__(self, name):
                self.name = name
        self.artisan = MockArtisan(data.get('artisan_name', 'Unknown Artisan'))

@app.route('/products')
@login_required
def product_list():
    """List all products from MongoDB"""
    # Fetch from Mongo instead of SQL
    products_cursor = mongo.db.products.find()
    products = [MongoProductWrapper(p) for p in products_cursor]
    
    return render_template('products.html', products=products)


@app.route('/artisan/<int:artisan_id>/products')
@login_required
def artisan_products(artisan_id):
    """View products by specific artisan"""
    artisan = Artisan.query.get_or_404(artisan_id)
    products = Product.query.filter_by(artisan_id=artisan_id).all()
    return render_template('artisan_products.html', artisan=artisan, products=products)


@app.route('/product/add/<int:artisan_id>', methods=['GET', 'POST'])
@login_required
def add_product(artisan_id):
    """Add new product for an artisan"""
    artisan = Artisan.query.get_or_404(artisan_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price', 0))
        image_url = request.form.get('image_url')
        stock = int(request.form.get('stock', 1))
        
        new_product = Product(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            stock=stock,
            artisan_id=artisan_id
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('artisan_products', artisan_id=artisan_id))
    
    return render_template('add_product.html', artisan=artisan)


@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """Edit product"""
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price', 0))
        product.image_url = request.form.get('image_url')
        product.stock = int(request.form.get('stock', 1))
        
        db.session.commit()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('artisan_products', artisan_id=product.artisan_id))
    
    return render_template('edit_product.html', product=product)


@app.route('/product/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    """Delete product"""
    product = Product.query.get_or_404(id)
    artisan_id = product.artisan_id
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'info')
    return redirect(url_for('artisan_products', artisan_id=artisan_id))


@app.route('/product/<id>')
@login_required
def product_detail(id):
    """Product detail page with buy option"""
    # Try fetching from MongoDB first (if ID looks like a Mongo string)
    from bson.objectid import ObjectId
    try:
        mongo_id = ObjectId(id)
        product_data = mongo.db.products.find_one({"_id": mongo_id})
        if product_data:
            product = MongoProductWrapper(product_data)
            return render_template('product_detail.html', product=product)
    except Exception:
        pass
    
    # Fallback to SQL (for legacy links or other places using SQL integer IDs)
    product = Product.query.get_or_404(int(id))
    return render_template('product_detail.html', product=product)


@app.route('/product/<int:id>/checkout', methods=['GET', 'POST'])
@login_required
def checkout(id):
    """Checkout page for product purchase"""
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        customer_phone = request.form.get('customer_phone')
        shipping_address = request.form.get('shipping_address')
        
        total_amount = product.price * quantity
        
        # Create order
        new_order = Order(
            user_id=current_user.id,
            product_id=product.id,
            quantity=quantity,
            total_amount=total_amount,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            shipping_address=shipping_address,
            payment_status='pending'
        )
        
        db.session.add(new_order)
        db.session.commit()
        
        # Redirect to payment
        return redirect(url_for('payment', order_id=new_order.id))
    
    return render_template('checkout.html', product=product)


@app.route('/payment/<int:order_id>')
@login_required
def payment(order_id):
    """Payment gateway page"""
    order = Order.query.get_or_404(order_id)
    return render_template('payment.html', order=order)


@app.route('/payment/<int:order_id>/process', methods=['POST'])
@login_required
def process_payment(order_id):
    """Process payment (demo - integrate with real payment gateway)"""
    order = Order.query.get_or_404(order_id)
    
    # Simulate payment processing
    payment_method = request.form.get('payment_method')
    
    # In production, integrate with Razorpay, Stripe, PayPal, etc.
    # For demo, we'll mark as completed
    order.payment_status = 'completed'
    order.payment_id = f'PAY_{order_id}_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
    
    # Update product stock
    product = Product.query.get(order.product_id)
    if product:
        product.stock = max(0, product.stock - order.quantity)
    
    db.session.commit()
    
    flash('Payment successful! Order confirmed.', 'success')
    return redirect(url_for('order_success', order_id=order.id))


@app.route('/order/<int:order_id>/success')
@login_required
def order_success(order_id):
    """Order success page"""
    order = Order.query.get_or_404(order_id)
    return render_template('order_success.html', order=order)


@app.route('/my-orders')
@login_required
def my_orders():
    """View user's orders"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)


# ============================================================================
# NEW ROUTES (Fixing Missing Templates)
# ============================================================================

@app.route('/analytics')
@login_required
def analytics():
    # Generate stats for dashboard
    users_count = User.query.count()
    manufacturers_count = User.query.filter_by(role='manufacturer').count()
    sites_count = HeritageSite.query.count()
    artisans_count = Artisan.query.count()
    
    # Heritage Stats
    most_visited = HeritageSite.query.order_by(HeritageSite.annual_visitors.desc()).first()
    
    from sqlalchemy import func
    
    # Most viewed
    most_viewed_id = db.session.query(SiteView.heritage_id, func.count(SiteView.id).label('count'))\
        .group_by(SiteView.heritage_id).order_by(func.count(SiteView.id).desc()).first()
    most_viewed_site = HeritageSite.query.get(most_viewed_id[0]) if most_viewed_id else most_visited
    if most_viewed_site:
        most_viewed_site.view_count_temp = most_viewed_id[1] if most_viewed_id else 0
        
    # Most bookmarked
    most_bookmarked_id = db.session.query(Bookmark.heritage_id, func.count(Bookmark.id).label('count'))\
        .group_by(Bookmark.heritage_id).order_by(func.count(Bookmark.id).desc()).first()
    most_bookmarked_ref = HeritageSite.query.get(most_bookmarked_id[0]) if most_bookmarked_id else most_visited
    if most_bookmarked_ref:
        most_bookmarked_ref.bookmark_count = most_bookmarked_id[1] if most_bookmarked_id else 0
    else:
        most_bookmarked_ref = most_visited # Fallback
        
    # Highest rated
    all_sites = HeritageSite.query.all()
    highest_rated_site = max(all_sites, key=lambda s: s.avg_rating or 0) if all_sites else most_visited
    
    # State distribution
    state_counts = db.session.query(HeritageSite.state, func.count(HeritageSite.id)).group_by(HeritageSite.state).all()
    state_dist = [{'state': s[0], 'count': s[1]} for s in state_counts]
    most_active_state_name = max(state_dist, key=lambda x: x['count'])['state'] if state_dist else 'N/A'
    most_active_state = {'name': most_active_state_name, 'site_count': max(state_dist, key=lambda x: x['count'])['count'] if state_dist else 0}
    
    # Artisan Stats
    craft_counts = db.session.query(Artisan.craft, func.count(Artisan.id)).group_by(Artisan.craft).all()
    most_popular_craft_data = max(craft_counts, key=lambda x: x[1]) if craft_counts else ('N/A', 0)
    most_popular_craft = {'name': most_popular_craft_data[0], 'artisan_count': most_popular_craft_data[1]}
    
    # Product Stats
    total_products = Product.query.count()
    avg_price = db.session.query(func.avg(Product.price)).scalar() or 0
    total_inventory_value = db.session.query(func.sum(Product.price * Product.stock)).scalar() or 0
    
    # Avg price by craft
    avg_price_craft = db.session.query(Artisan.craft, func.avg(Product.price))\
        .join(Product).group_by(Artisan.craft).all()
    avg_price_by_craft = [{'craft': c[0], 'avg_price': c[1]} for c in avg_price_craft]
    
    # Hotel Stats
    total_hotels = Hotel.query.count()
    total_bookings = HotelBooking.query.count()
    confirmed_bookings = HotelBooking.query.filter_by(booking_status='Confirmed').count()
    total_revenue = db.session.query(func.sum(HotelBooking.total_price)).filter_by(booking_status='Confirmed').scalar() or 0
    
    most_booked_hotel_id = db.session.query(HotelBooking.hotel_id, func.count(HotelBooking.id))\
        .group_by(HotelBooking.hotel_id).order_by(func.count(HotelBooking.id).desc()).first()
    most_booked_hotel = Hotel.query.get(most_booked_hotel_id[0]) if most_booked_hotel_id else None
    if most_booked_hotel:
        most_booked_hotel.booking_count = most_booked_hotel_id[1]
    else:
        most_booked_hotel = SimpleNamespace(name='N/A', booking_count=0)
        
    analytics_data = {
        'total_users': users_count,
        'total_manufacturers': manufacturers_count,
        'total_heritage_sites': sites_count,
        'total_artisans': artisans_count,
        'most_visited_site': most_visited,
        'most_viewed_site': most_viewed_site,
        'most_bookmarked_site': most_bookmarked_ref,
        'highest_rated_site': highest_rated_site,
        'most_active_state': most_active_state,
        'state_distribution': state_dist,
        'most_popular_craft': most_popular_craft,
        'total_products': total_products,
        'avg_product_price': avg_price,
        'total_inventory_value': total_inventory_value,
        'avg_price_by_craft': avg_price_by_craft,
        'total_hotels': total_hotels,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_revenue': total_revenue,
        'most_booked_hotel': most_booked_hotel
    }
    
    return render_template('dashboard/analytics.html', analytics=analytics_data)

@app.route('/heritage/map')
def heritage_map():
    sites = HeritageSite.query.all()
    states = sorted(list(set(s.state for s in sites)))
    categories = sorted(list(set(s.category for s in sites)))
    sites_json = json.dumps([site.to_dict() for site in sites])
    return render_template('heritage_map.html', sites=sites, states=states, categories=categories, sites_json=sites_json)

@app.route('/my-bookmarks')
@login_required
def my_bookmarks():
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
    bookmarked_site_ids = [b.heritage_id for b in bookmarks]
    bookmarked_sites = HeritageSite.query.filter(HeritageSite.id.in_(bookmarked_site_ids)).all()
    return render_template('my_bookmarks.html', bookmarks=bookmarks, bookmarked_sites=bookmarked_sites)

@app.route('/bookmark/remove/<int:heritage_id>', methods=['POST'])
@login_required
def remove_bookmark(heritage_id):
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, heritage_id=heritage_id).first_or_404()
    db.session.delete(bookmark)
    db.session.commit()
    flash('Bookmark removed successfully.', 'success')
    return redirect(url_for('my_bookmarks'))

@app.route('/my-bookings')
@login_required
def my_bookings():
    bookings = HotelBooking.query.filter_by(user_id=current_user.id).order_by(HotelBooking.created_at.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/booking/cancel/<int:id>', methods=['POST'])
@login_required
def cancel_booking(id):
    booking = HotelBooking.query.get_or_404(id)
    if booking.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('my_bookings'))
        
    booking.booking_status = 'Cancelled'
    db.session.commit()
    flash('Booking cancelled successfully.', 'info')
    return redirect(url_for('my_bookings'))

@app.route('/api/hotels/all')
def api_hotels_all():
    hotels = Hotel.query.all()
    hotels_data = []
    for hotel in hotels:
        h_dict = hotel.to_dict()
        h_dict['heritage_name'] = hotel.heritage_site.name if hotel.heritage_site else 'Unknown'
        hotels_data.append(h_dict)
    return jsonify({'hotels': hotels_data})

# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.route('/api/heritage', methods=['GET'])
def api_heritage():
    """API endpoint for heritage sites"""
    sites = HeritageSite.query.all()
    return jsonify([site.to_dict() for site in sites])


@app.route('/api/artisans', methods=['GET'])
def api_artisans():
    """API endpoint for artisans"""
    artisans = Artisan.query.all()
    return jsonify([artisan.to_dict() for artisan in artisans])


@app.route('/api/recommendations', methods=['GET'])
def api_recommendations():
    """API endpoint for AI recommendations"""
    recommendation_type = request.args.get('type', 'heritage')
    state = request.args.get('state', None)
    top_n = int(request.args.get('top_n', 5))
    
    if recommendation_type == 'heritage':
        sites = HeritageSite.query.all()
        sites_data = [site.to_dict() for site in sites]
        recommendations = ml_engine.recommend_heritage_sites(sites_data, top_n)
        return jsonify(recommendations)
    
    elif recommendation_type == 'artisans':
        artisans = Artisan.query.all()
        artisans_data = [artisan.to_dict() for artisan in artisans]
        recommendations = ml_engine.recommend_artisans_by_state(artisans_data, state, top_n)
        return jsonify(recommendations)
    
    else:
        return jsonify({'error': 'Invalid recommendation type'}), 400


@app.route('/api/analytics', methods=['GET'])
def api_analytics():
    """API endpoint for analytics data"""
    heritage_sites = HeritageSite.query.all()
    artisans = Artisan.query.all()
    
    sites_data = [site.to_dict() for site in heritage_sites]
    artisans_data = [artisan.to_dict() for artisan in artisans]
    
    economic_impact = ml_engine.calculate_economic_impact(sites_data, artisans_data)
    visitor_trends = ml_engine.get_visitor_trends(sites_data)
    state_distribution = ml_engine.get_state_wise_distribution(artisans_data)
    
    return jsonify({
        'economic_impact': economic_impact,
        'visitor_trends': visitor_trends,
        'state_distribution': state_distribution
    })


@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chatbot API for customer support"""
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'success': False, 'response': 'Please enter a message.'}), 400

    from chatbot import get_chat_response
    response = get_chat_response(
        message=message,
        get_heritage_sites=lambda: HeritageSite.query.all(),
        get_artisans=lambda: Artisan.query.all(),
        is_authenticated=current_user.is_authenticated
    )
    # Convert **bold** to HTML for display
    import re
    response_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', response)
    response_html = response_html.replace('\n', '<br>')
    return jsonify({'success': True, 'response': response_html})


# ============================================================================
# EXPORT ROUTES
# ============================================================================

@app.route('/export/heritage')
@login_required
def export_heritage():
    """Export heritage sites to CSV"""
    sites = HeritageSite.query.all()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Name', 'State', 'Category', 'Description', 'Annual Visitors', 'Created At'])
    
    # Write data
    for site in sites:
        writer.writerow([
            site.id,
            site.name,
            site.state,
            site.category,
            site.description,
            site.annual_visitors,
            site.created_at.strftime('%Y-%m-%d %H:%M:%S') if site.created_at else ''
        ])
    
    output.seek(0)
    
    # from flask import Response # Removed
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=heritage_sites.csv'}
    )


@app.route('/export/artisans')
@login_required
def export_artisans():
    """Export artisans to CSV"""
    artisans = Artisan.query.all()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Name', 'Craft', 'State', 'Product Price', 'Contact', 'Description', 'Created At'])
    
    # Write data
    for artisan in artisans:
        writer.writerow([
            artisan.id,
            artisan.name,
            artisan.craft,
            artisan.state,
            artisan.product_price,
            artisan.contact,
            artisan.description,
            artisan.created_at.strftime('%Y-%m-%d %H:%M:%S') if artisan.created_at else ''
        ])
    
    output.seek(0)
    
    # from flask import Response # Removed
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=artisans.csv'}
    )


# ============================================================================
# INITIALIZATION & SAMPLE DATA
# ============================================================================

def init_database():
    """Initialize database with tables and sample data"""
    with app.app_context():
        # Create tables and add any missing columns (role, image_url)
        db.create_all()
        try:
            _ensure_schema_columns()
        except Exception:
            pass
        
        # Check if data already exists
        if User.query.first() is None:
            # Create default user (regular)
            default_user = User(
                username='admin',
                email='admin@digitalcatalyst.in',
                password=generate_password_hash('admin123'),
                role='user'
            )
            db.session.add(default_user)
            # Create manufacturer demo user
            manufacturer_user = User(
                username='manufacturer',
                email='manufacturer@digitalcatalyst.in',
                password=generate_password_hash('manufacturer123'),
                role='manufacturer'
            )
            db.session.add(manufacturer_user)
            
            # Sample Heritage Sites
            heritage_sites = [
                HeritageSite(name='Taj Mahal', state='Uttar Pradesh', category='Monument', 
                           description='Iconic white marble mausoleum', annual_visitors=7000000),
                HeritageSite(name='Red Fort', state='Delhi', category='Fort', 
                           description='Historic fortified palace', annual_visitors=2500000),
                HeritageSite(name='Ajanta Caves', state='Maharashtra', category='Cave Temple', 
                           description='Ancient Buddhist rock-cut caves', annual_visitors=600000),
                HeritageSite(name='Hampi', state='Karnataka', category='Archaeological Site', 
                           description='Ruins of Vijayanagara Empire', annual_visitors=500000),
                HeritageSite(name='Golden Temple', state='Punjab', category='Temple', 
                           description='Holiest Gurdwara of Sikhism', annual_visitors=100000),
                HeritageSite(name='Konark Sun Temple', state='Odisha', category='Temple', 
                           description='13th-century Sun Temple', annual_visitors=400000),
                HeritageSite(name='Khajuraho Temples', state='Madhya Pradesh', category='Temple', 
                           description='Medieval Hindu and Jain temples', annual_visitors=300000),
                HeritageSite(name='Mysore Palace', state='Karnataka', category='Palace', 
                           description='Historical palace in Mysore', annual_visitors=2800000),
            ]
            
            # Sample Artisans
            artisans = [
                Artisan(name='Ramesh Kumar', craft='Pottery', state='Rajasthan', 
                       product_price=1500, contact='9876543210', 
                       description='Traditional blue pottery artisan'),
                Artisan(name='Lakshmi Devi', craft='Weaving', state='West Bengal', 
                       product_price=3500, contact='9876543211', 
                       description='Handloom saree weaver'),
                Artisan(name='Mohammed Ali', craft='Metalwork', state='Uttar Pradesh', 
                       product_price=2500, contact='9876543212', 
                       description='Brass and copper craftsman'),
                Artisan(name='Priya Sharma', craft='Embroidery', state='Gujarat', 
                       product_price=2000, contact='9876543213', 
                       description='Kutch embroidery specialist'),
                Artisan(name='Suresh Babu', craft='Wood Carving', state='Kerala', 
                       product_price=4000, contact='9876543214', 
                       description='Traditional temple wood carver'),
                Artisan(name='Anjali Patel', craft='Painting', state='Madhya Pradesh', 
                       product_price=1200, contact='9876543215', 
                       description='Gond art painter'),
                Artisan(name='Vijay Singh', craft='Jewelry Making', state='Rajasthan', 
                       product_price=5000, contact='9876543216', 
                       description='Kundan jewelry craftsman'),
                Artisan(name='Geeta Rani', craft='Basket Weaving', state='Assam', 
                       product_price=800, contact='9876543217', 
                       description='Bamboo basket weaver'),
            ]
            
            # Add sample data
            for site in heritage_sites:
                db.session.add(site)
            
            for artisan in artisans:
                db.session.add(artisan)
            
            db.session.commit()
            print("Database initialized with sample data!")


if __name__ == "__main__":
    init_database()
    # Optimized for speed
    app.run(debug=False, host='127.0.0.1', port=5002, threaded=True, use_reloader=False)
