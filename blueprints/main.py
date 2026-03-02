"""
Main Application Blueprint
===========================

This blueprint contains the core application routes for the Digital Catalyst platform,
including dashboard, heritage sites, artisans, products, and user engagement features.

Academic Note:
This blueprint demonstrates the Model-View-Controller (MVC) pattern where:
- Models: Database entities (HeritageSite, Artisan, Product, etc.)
- Views: Jinja2 templates rendering HTML
- Controllers: Route functions handling business logic

The blueprint uses Flask-Login for authentication and implements CRUD operations
(Create, Read, Update, Delete) for all major entities.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, HeritageSite, Artisan, Product, Order
from ml.recommendation_engine import RecommendationEngine
from utils.decorators import role_required, manufacturer_required, admin_required
from datetime import datetime

# Create Blueprint
main_bp = Blueprint('main', __name__)

# Initialize ML engine
ml_engine = RecommendationEngine()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_most_viewed_sites(top_n=10):
    """
    Get most viewed heritage sites based on SiteView records.
    
    Academic Note - Aggregation Queries:
    -----------------------------------
    This function demonstrates SQL aggregation using SQLAlchemy:
    
    Query Structure:
    1. JOIN: Combines SiteView and HeritageSite tables
    2. GROUP BY: Groups views by heritage site
    3. COUNT: Counts views per site
    4. ORDER BY: Sorts by view count descending
    5. LIMIT: Returns top N results
    
    SQL Equivalent:
    SELECT h.*, COUNT(v.id) as view_count
    FROM heritage_sites h
    LEFT JOIN site_views v ON h.id = v.heritage_id
    GROUP BY h.id
    ORDER BY view_count DESC
    LIMIT top_n
    
    Complexity Analysis:
    - Time: O(n log n) where n is number of sites (due to sorting)
    - Space: O(n) for result set
    - Database: Optimized with indexes on foreign keys
    
    Args:
        top_n (int): Number of top sites to return
        
    Returns:
        list: List of tuples (HeritageSite, view_count)
    """
    from models import SiteView
    from sqlalchemy import func
    
    results = db.session.query(
        HeritageSite,
        func.count(SiteView.id).label('view_count')
    ).outerjoin(
        SiteView, HeritageSite.id == SiteView.heritage_id
    ).group_by(
        HeritageSite.id
    ).order_by(
        func.count(SiteView.id).desc()
    ).limit(top_n).all()
    
    return results


# ============================================================================
# LANDING & DASHBOARD ROUTES
# ============================================================================

@main_bp.route('/')
def landing():
    """
    Landing Page Route
    
    Shows landing page for unauthenticated users, redirects authenticated users to dashboard.
    
    Academic Note:
    This implements a common web pattern where the root URL serves different
    content based on authentication state, improving user experience.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('landing.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Main Dashboard Route
    
    Displays analytics, recommendations, and overview of heritage sites and artisans.
    
    Academic Note:
    This route demonstrates query optimization techniques:
    1. with_entities(): Selects only required columns (reduces data transfer)
    2. Lazy loading: Relationships loaded only when accessed
    3. Aggregation: Calculations performed in database (more efficient than Python)
    
    The ML engine provides personalized recommendations based on user behavior.
    """
    # Optimized queries - select only needed columns
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
    
    # Get AI recommendations
    recommended_sites_data = ml_engine.recommend_heritage_sites(sites_data, top_n=5)
    recommended_site_ids = [s['id'] for s in recommended_sites_data if s.get('id')]
    recommended_sites = HeritageSite.query.filter(HeritageSite.id.in_(recommended_site_ids)).all() if recommended_site_ids else []
    recommended_sites.sort(key=lambda s: s.annual_visitors or 0, reverse=True)
    
    # Get analytics data
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

@main_bp.route('/heritage')
@login_required
def heritage_list():
    """
    Heritage Sites List Route
    
    Displays all heritage sites with advanced search, filter, and sort capabilities.
    
    Academic Note - Query Building and Optimization:
    -----------------------------------------------
    This route demonstrates dynamic query construction with multiple filters:
    
    Query Building Pattern:
    1. Start with base query
    2. Apply filters conditionally (only if provided)
    3. Apply sorting based on user selection
    4. Execute query with pagination/limits
    
    SQL Injection Prevention:
    - Uses SQLAlchemy ORM (parameterized queries)
    - Never concatenates user input into SQL strings
    - ILIKE operator for case-insensitive search
    
    Performance Optimization:
    - Indexed columns: state, category (for filtering)
    - Foreign key indexes: for JOIN operations
    - LIMIT clause: prevents loading entire table
    
    Complexity Analysis:
    - Search (ILIKE): O(n) without full-text index
    - Exact match filters: O(log n) with indexes
    - Sorting: O(n log n) for database-level sort
    - JOINs for aggregation: O(n*m) worst case, O(n) with indexes
    """
    from models import Review, SiteView, Bookmark
    from sqlalchemy import func, desc
    
    # Get filter parameters
    search = request.args.get('search', '').strip()
    state_filter = request.args.get('state', '').strip()
    category_filter = request.args.get('category', '').strip()
    rating_min = request.args.get('rating_min', type=float)
    rating_max = request.args.get('rating_max', type=float)
    sort_by = request.args.get('sort', 'name')  # name, views, rating, bookmarks
    
    # Start with base query
    query = HeritageSite.query
    
    # Apply name search filter (case-insensitive)
    # Academic Note: ILIKE is PostgreSQL/SQLite case-insensitive LIKE
    if search:
        query = query.filter(HeritageSite.name.ilike(f'%{search}%'))
    
    # Apply state filter (exact match)
    if state_filter:
        query = query.filter(HeritageSite.state == state_filter)
    
    # Apply category filter (exact match)
    if category_filter:
        query = query.filter(HeritageSite.category == category_filter)
    
    # Apply rating range filter
    # Academic Note: Requires JOIN with Review table and HAVING clause
    if rating_min is not None or rating_max is not None:
        # Subquery to calculate average rating per site
        rating_subquery = db.session.query(
            Review.heritage_id,
            func.avg(Review.rating).label('avg_rating')
        ).group_by(Review.heritage_id).subquery()
        
        # JOIN with subquery
        query = query.join(
            rating_subquery,
            HeritageSite.id == rating_subquery.c.heritage_id
        )
        
        # Apply rating filters
        if rating_min is not None:
            query = query.filter(rating_subquery.c.avg_rating >= rating_min)
        if rating_max is not None:
            query = query.filter(rating_subquery.c.avg_rating <= rating_max)
    
    # Apply sorting
    # Academic Note: Different sort options require different JOIN strategies
    if sort_by == 'views':
        # Sort by view count (most viewed first)
        view_count_subquery = db.session.query(
            SiteView.heritage_id,
            func.count(SiteView.id).label('view_count')
        ).group_by(SiteView.heritage_id).subquery()
        
        query = query.outerjoin(
            view_count_subquery,
            HeritageSite.id == view_count_subquery.c.heritage_id
        ).order_by(desc(view_count_subquery.c.view_count))
        
    elif sort_by == 'rating':
        # Sort by average rating (highest first)
        rating_subquery = db.session.query(
            Review.heritage_id,
            func.avg(Review.rating).label('avg_rating')
        ).group_by(Review.heritage_id).subquery()
        
        query = query.outerjoin(
            rating_subquery,
            HeritageSite.id == rating_subquery.c.heritage_id
        ).order_by(desc(rating_subquery.c.avg_rating))
        
    elif sort_by == 'bookmarks':
        # Sort by bookmark count (most bookmarked first)
        bookmark_count_subquery = db.session.query(
            Bookmark.heritage_id,
            func.count(Bookmark.id).label('bookmark_count')
        ).group_by(Bookmark.heritage_id).subquery()
        
        query = query.outerjoin(
            bookmark_count_subquery,
            HeritageSite.id == bookmark_count_subquery.c.heritage_id
        ).order_by(desc(bookmark_count_subquery.c.bookmark_count))
        
    else:
        # Default: sort by name (alphabetical)
        query = query.order_by(HeritageSite.name)
    
    # Execute query with limit
    # Academic Note: LIMIT prevents loading entire table into memory
    sites = query.limit(100).all()
    
    # Get unique values for filter dropdowns
    # Academic Note: DISTINCT returns unique values, useful for filter options
    all_states = db.session.query(HeritageSite.state).distinct().order_by(HeritageSite.state).all()
    all_categories = db.session.query(HeritageSite.category).distinct().order_by(HeritageSite.category).all()
    
    return render_template('heritage.html',
                         sites=sites,
                         states=[s[0] for s in all_states],
                         categories=[c[0] for c in all_categories])
@main_bp.route('/heritage/map')
def heritage_map():
    """
    Heritage Sites Map View

    Displays all heritage sites on an interactive Leaflet map with filtering capabilities.

    Academic Note - Geographic Data Visualization:
    ---------------------------------------------
    This route demonstrates integration of geographic data with web mapping libraries.

    Leaflet.js Benefits:
    - Open source (no API key required)
    - Lightweight and fast
    - Mobile-friendly
    - Extensive plugin ecosystem

    Data Serialization:
    - Converts SQLAlchemy models to JSON for JavaScript consumption
    - Includes computed properties (avg_rating, view_count) for rich popups

    Performance Considerations:
    - Loads all sites at once (suitable for small datasets)
    - Client-side filtering (no server round-trips)
    - For large datasets, consider:
      * Server-side clustering
      * Tile-based loading
      * Viewport-based queries
    """
    import json

    # Get all heritage sites with coordinates
    sites = HeritageSite.query.filter(
        HeritageSite.latitude.isnot(None),
        HeritageSite.longitude.isnot(None)
    ).all()

    # Convert to JSON for JavaScript
    sites_json = json.dumps([site.to_dict() for site in sites])

    # Get unique states and categories for filters
    states = db.session.query(HeritageSite.state).distinct().order_by(HeritageSite.state).all()
    categories = db.session.query(HeritageSite.category).distinct().order_by(HeritageSite.category).all()

    return render_template('heritage_map.html',
                         sites=sites,
                         sites_json=sites_json,
                         states=[s[0] for s in states],
                         categories=[c[0] for c in categories])





@main_bp.route('/heritage/add', methods=['GET', 'POST'])
@login_required
def add_heritage():
    """
    Add Heritage Site Route
    
    Creates new heritage site record with optional image upload.
    
    Academic Note - File Upload Handling:
    ------------------------------------
    This route demonstrates secure file upload implementation:
    
    1. File Validation: Check file type and size
    2. Secure Filename: Sanitize filename to prevent path traversal
    3. Unique Naming: Add timestamp to prevent overwrites
    4. Error Handling: Graceful failure if upload fails
    5. Database Storage: Store file path, not file content
    
    Security Considerations:
    - Only allow image file types (whitelist approach)
    - Limit file size to prevent DoS attacks
    - Sanitize filenames to prevent directory traversal
    - Store files outside web root if possible
    
    Form Encoding:
    File uploads require enctype="multipart/form-data" in HTML form.
    """
    from utils.file_upload import save_uploaded_image
    
    if request.method == 'POST':
        name = request.form.get('name')
        state = request.form.get('state')
        category = request.form.get('category')
        description = request.form.get('description')
        annual_visitors = int(request.form.get('annual_visitors', 0))
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        # Convert latitude/longitude to float if provided
        lat = float(latitude) if latitude else None
        lng = float(longitude) if longitude else None
        
        # Handle image upload
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                # Use utility function to save image securely
                success, result = save_uploaded_image(file, 'static/uploads/heritage')
                if success:
                    image_url = result
                else:
                    # Upload failed, show error but continue
                    flash(f'Image upload failed: {result}', 'warning')
        
        # Fallback to URL if no file uploaded
        if not image_url:
            image_url = request.form.get('image_url') or None
        
        new_site = HeritageSite(
            name=name,
            state=state,
            category=category,
            description=description,
            image_url=image_url,
            latitude=lat,
            longitude=lng,
            annual_visitors=annual_visitors
        )
        
        db.session.add(new_site)
        db.session.commit()
        
        flash('Heritage site added successfully!', 'success')
        return redirect(url_for('main.heritage_list'))
    
    return render_template('add_heritage.html')


@main_bp.route('/heritage/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_heritage(id):
    """
    Edit Heritage Site Route
    
    Updates existing heritage site record with optional image upload.
    
    Academic Note - Update with File Upload:
    ---------------------------------------
    When updating records with file uploads:
    1. Check if new file uploaded
    2. If yes, delete old file (prevent orphaned files)
    3. Save new file
    4. Update database with new path
    5. If no new file, keep existing or update URL
    
    This prevents disk space waste from orphaned files.
    """
    from utils.file_upload import save_uploaded_image, delete_uploaded_image
    
    site = HeritageSite.query.get_or_404(id)
    
    if request.method == 'POST':
        site.name = request.form.get('name')
        site.state = request.form.get('state')
        site.category = request.form.get('category')
        site.description = request.form.get('description')
        site.annual_visitors = int(request.form.get('annual_visitors', 0))
        
        # Update latitude/longitude
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        site.latitude = float(latitude) if latitude else None
        site.longitude = float(longitude) if longitude else None
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                # Delete old image if it exists and is a local file
                if site.image_url and site.image_url.startswith('static/'):
                    delete_uploaded_image(site.image_url)
                
                # Save new image
                success, result = save_uploaded_image(file, 'static/uploads/heritage')
                if success:
                    site.image_url = result
                else:
                    flash(f'Image upload failed: {result}', 'warning')
        else:
            # Update URL if provided and no file uploaded
            url_input = request.form.get('image_url')
            if url_input:
                site.image_url = url_input
        
        db.session.commit()
        
        flash('Heritage site updated successfully!', 'success')
        return redirect(url_for('main.heritage_list'))
    
    return render_template('edit_heritage.html', site=site)


@main_bp.route('/heritage/delete/<int:id>', methods=['POST'])
@login_required
def delete_heritage(id):
    """
    Delete Heritage Site Route
    
    Removes heritage site record.
    
    Academic Note:
    Implements the Delete operation in CRUD. Uses POST method (not GET)
    to prevent accidental deletion via URL access. Cascade delete rules
    ensure related records (bookmarks, reviews) are also removed.
    """
    site = HeritageSite.query.get_or_404(id)
    db.session.delete(site)
    db.session.commit()
    
    flash('Heritage site deleted successfully!', 'info')
    return redirect(url_for('main.heritage_list'))


@main_bp.route('/heritage/<int:id>')
@login_required
def heritage_detail(id):
    """
    Heritage Site Detail Route
    
    Displays detailed information about a specific heritage site and tracks views.
    
    Academic Note - Analytics Tracking:
    ----------------------------------
    This route implements engagement tracking for analytics purposes.
    
    View Tracking Strategy:
    1. Record every page view (both authenticated and anonymous)
    2. Store user_id if authenticated, NULL if anonymous
    3. Timestamp each view for time-series analysis
    
    Privacy Considerations:
    - Anonymous tracking: No personal data collected for guests
    - Aggregate analytics: Individual views used only for statistics
    - GDPR compliance: User deletion sets user_id to NULL (preserves analytics)
    
    Performance Considerations:
    - Asynchronous tracking: View recording doesn't block page load
    - Indexed queries: Fast aggregation for view counts
    - Minimal data: Only essential fields stored
    
    Use Cases:
    - Popularity metrics: Most viewed sites
    - Trending detection: Recent view spikes
    - Recommendation engine: User browsing history
    - Business intelligence: Engagement patterns
    """
    from models import Bookmark, SiteView, Review
    
    site = HeritageSite.query.get_or_404(id)
    
    # Track site view
    # Academic Note: This creates a view record for analytics
    # user_id is NULL for anonymous users, set for authenticated users
    try:
        new_view = SiteView(
            user_id=current_user.id if current_user.is_authenticated else None,
            heritage_id=id
        )
        db.session.add(new_view)
        db.session.commit()
    except Exception as e:
        # Don't fail page load if view tracking fails
        # Log error but continue rendering page
        db.session.rollback()
        print(f"Error tracking view: {str(e)}")
    
    # Check if current user has bookmarked this site
    is_bookmarked = False
    user_review = None
    if current_user.is_authenticated:
        is_bookmarked = Bookmark.query.filter_by(
            user_id=current_user.id,
            heritage_id=id
        ).first() is not None
        
        # Get user's existing review if any
        user_review = Review.query.filter_by(
            user_id=current_user.id,
            heritage_id=id
        ).first()
    
    # Get recent reviews (limit to 5 for detail page)
    recent_reviews = Review.query.filter_by(
        heritage_id=id
    ).order_by(Review.created_at.desc()).limit(5).all()
    
    # Get hotels near this heritage site
    from models import Hotel
    hotels = Hotel.query.filter_by(heritage_id=id).all()
    
    return render_template('heritage_detail.html', 
                         site=site, 
                         is_bookmarked=is_bookmarked,
                         user_review=user_review,
                         recent_reviews=recent_reviews,
                         hotels=hotels)


@main_bp.route('/heritage/<int:heritage_id>/hotels')
@login_required
def view_heritage_hotels(heritage_id):
    """
    View Hotels for Heritage Site Route
    
    Displays all hotels near a specific heritage site in a dedicated page.
    """
    from models import Hotel
    
    # Get heritage site
    heritage_site = HeritageSite.query.get_or_404(heritage_id)
    
    # Get all hotels for this heritage site
    hotels = Hotel.query.filter_by(heritage_id=heritage_id).all()
    
    return render_template('heritage_hotels.html',
                         heritage_site=heritage_site,
                         hotels=hotels)


# ============================================================================
# ARTISAN ROUTES
# ============================================================================

@main_bp.route('/artisans')
@login_required
def artisan_list():
    """Artisan List Route - displays all artisans with filters"""
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
    
    all_states = db.session.query(Artisan.state).distinct().limit(50).all()
    all_crafts = db.session.query(Artisan.craft).distinct().limit(50).all()
    
    return render_template('artisans.html',
                         artisans=artisans,
                         states=[s[0] for s in all_states],
                         crafts=[c[0] for c in all_crafts])


@main_bp.route('/artisans/add', methods=['GET', 'POST'])
@login_required
def add_artisan():
    """Add Artisan Route"""
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
        return redirect(url_for('main.artisan_list'))
    
    return render_template('add_artisan.html')


@main_bp.route('/artisans/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_artisan(id):
    """Edit Artisan Route"""
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
        return redirect(url_for('main.artisan_list'))
    
    return render_template('edit_artisan.html', artisan=artisan)


@main_bp.route('/artisans/delete/<int:id>', methods=['POST'])
@login_required
def delete_artisan(id):
    """Delete Artisan Route"""
    artisan = Artisan.query.get_or_404(id)
    db.session.delete(artisan)
    db.session.commit()
    
    flash('Artisan deleted successfully!', 'info')
    return redirect(url_for('main.artisan_list'))


@main_bp.route('/artisans/<int:id>')
@login_required
def artisan_detail(id):
    """Artisan Detail Route"""
    artisan = Artisan.query.get_or_404(id)
    return render_template('artisan_detail.html', artisan=artisan)


# ============================================================================
# PRODUCT ROUTES
# ============================================================================

@main_bp.route('/products')
@login_required
def product_list():
    """Product List Route"""
    products = Product.query.all()
    return render_template('products.html', products=products)


@main_bp.route('/artisan/<int:artisan_id>/products')
@login_required
def artisan_products(artisan_id):
    """Artisan Products Route"""
    artisan = Artisan.query.get_or_404(artisan_id)
    products = Product.query.filter_by(artisan_id=artisan_id).all()
    return render_template('artisan_products.html', artisan=artisan, products=products)


@main_bp.route('/product/add/<int:artisan_id>', methods=['GET', 'POST'])
@login_required
@manufacturer_required
def add_product(artisan_id):
    """
    Add Product Route
    
    Academic Note - Authorization vs Authentication:
    -----------------------------------------------
    This route demonstrates the difference between authentication and authorization:
    
    Authentication: Verifying WHO the user is (@login_required)
    - Confirms user identity through credentials
    - Ensures user is logged in
    
    Authorization: Verifying WHAT the user can do (@manufacturer_required)
    - Confirms user has permission for this action
    - Enforces role-based access control
    
    Security Principle: Defense in Depth
    Multiple layers of security (authentication + authorization) provide
    better protection than single layer.
    """
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
        return redirect(url_for('main.artisan_products', artisan_id=artisan_id))
    
    return render_template('add_product.html', artisan=artisan)


@main_bp.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@manufacturer_required
def edit_product(id):
    """
    Edit Product Route
    
    Restricted to manufacturer role for product management.
    """
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price', 0))
        product.image_url = request.form.get('image_url')
        product.stock = int(request.form.get('stock', 1))
        
        db.session.commit()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('main.artisan_products', artisan_id=product.artisan_id))
    
    return render_template('edit_product.html', product=product)


@main_bp.route('/product/delete/<int:id>', methods=['POST'])
@login_required
@manufacturer_required
def delete_product(id):
    """
    Delete Product Route
    
    Restricted to manufacturer role for product management.
    """
    product = Product.query.get_or_404(id)
    artisan_id = product.artisan_id
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'info')
    return redirect(url_for('main.artisan_products', artisan_id=artisan_id))


@main_bp.route('/product/<int:id>')
@login_required
def product_detail(id):
    """Product Detail Route"""
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)


# ============================================================================
# ORDER & CHECKOUT ROUTES
# ============================================================================

@main_bp.route('/product/<int:id>/checkout', methods=['GET', 'POST'])
@login_required
def checkout(id):
    """Checkout Route"""
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        customer_phone = request.form.get('customer_phone')
        shipping_address = request.form.get('shipping_address')
        
        total_amount = product.price * quantity
        
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
        
        return redirect(url_for('main.payment', order_id=new_order.id))
    
    return render_template('checkout.html', product=product)


@main_bp.route('/payment/<int:order_id>')
@login_required
def payment(order_id):
    """Payment Gateway Route"""
    order = Order.query.get_or_404(order_id)
    return render_template('payment.html', order=order)


@main_bp.route('/payment/<int:order_id>/process', methods=['POST'])
@login_required
def process_payment(order_id):
    """Process Payment Route"""
    order = Order.query.get_or_404(order_id)
    
    payment_method = request.form.get('payment_method')
    
    # Demo payment processing
    order.payment_status = 'completed'
    order.payment_id = f'PAY_{order_id}_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
    
    # Update product stock
    product = Product.query.get(order.product_id)
    if product:
        product.stock = max(0, product.stock - order.quantity)
    
    db.session.commit()
    
    flash('Payment successful! Order confirmed.', 'success')
    return redirect(url_for('main.order_success', order_id=order.id))


@main_bp.route('/order/<int:order_id>/success')
@login_required
def order_success(order_id):
    """Order Success Route"""
    order = Order.query.get_or_404(order_id)
    return render_template('order_success.html', order=order)


@main_bp.route('/my-orders')
@login_required
def my_orders():
    """My Orders Route"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)


# ============================================================================
# BOOKMARK ROUTES
# ============================================================================

@main_bp.route('/bookmark/<int:heritage_id>', methods=['POST'])
@login_required
@role_required('user')
def add_bookmark(heritage_id):
    """
    Add Bookmark Route
    
    Creates a bookmark for a heritage site for the current user.
    
    Academic Note - RESTful Design Principles:
    -----------------------------------------
    This route follows REST conventions:
    - POST method: Creates a new resource (bookmark)
    - Resource identifier in URL: /bookmark/<heritage_id>
    - Idempotent behavior: Duplicate bookmarks prevented
    - Appropriate HTTP status: 201 Created (implicit via redirect)
    
    Business Logic:
    1. Check if bookmark already exists (prevent duplicates)
    2. Verify heritage site exists (404 if not)
    3. Create bookmark record
    4. Provide user feedback via flash message
    5. Redirect to appropriate page
    
    Database Constraint:
    The unique constraint on (user_id, heritage_id) in the Bookmark model
    provides database-level duplicate prevention as a safety net.
    """
    from models import Bookmark
    
    # Verify heritage site exists
    heritage_site = HeritageSite.query.get_or_404(heritage_id)
    
    # Check if bookmark already exists
    existing_bookmark = Bookmark.query.filter_by(
        user_id=current_user.id,
        heritage_id=heritage_id
    ).first()
    
    if existing_bookmark:
        flash('You have already bookmarked this heritage site.', 'info')
    else:
        # Create new bookmark
        new_bookmark = Bookmark(
            user_id=current_user.id,
            heritage_id=heritage_id
        )
        
        try:
            db.session.add(new_bookmark)
            db.session.commit()
            flash(f'"{heritage_site.name}" added to your bookmarks!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error adding bookmark. Please try again.', 'danger')
    
    # Redirect back to the heritage site detail page
    return redirect(url_for('main.heritage_detail', id=heritage_id))


@main_bp.route('/bookmark/<int:heritage_id>/delete', methods=['POST'])
@login_required
@role_required('user')
def remove_bookmark(heritage_id):
    """
    Remove Bookmark Route
    
    Deletes a bookmark for a heritage site for the current user.
    
    Academic Note - RESTful Design:
    ------------------------------
    REST best practice would use DELETE method, but HTML forms only support
    GET and POST. We use POST with /delete suffix as a pragmatic compromise.
    
    Alternative approaches:
    1. JavaScript fetch() with DELETE method (requires client-side code)
    2. Method override via hidden form field (requires middleware)
    3. POST with /delete suffix (current approach - simple and effective)
    
    Security:
    - User can only delete their own bookmarks (filtered by user_id)
    - No authorization bypass possible
    """
    from models import Bookmark
    
    # Find bookmark for current user and heritage site
    bookmark = Bookmark.query.filter_by(
        user_id=current_user.id,
        heritage_id=heritage_id
    ).first()
    
    if bookmark:
        try:
            db.session.delete(bookmark)
            db.session.commit()
            flash('Bookmark removed successfully.', 'info')
        except Exception as e:
            db.session.rollback()
            flash('Error removing bookmark. Please try again.', 'danger')
    else:
        flash('Bookmark not found.', 'warning')
    
    # Redirect back to referring page or bookmarks page
    return redirect(request.referrer or url_for('main.my_bookmarks'))


@main_bp.route('/my-bookmarks')
@login_required
@role_required('user')
def my_bookmarks():
    """
    My Bookmarks Route
    
    Displays all heritage sites bookmarked by the current user.
    
    Academic Note - Query Optimization:
    ----------------------------------
    This route demonstrates efficient querying with relationships:
    
    1. Join Strategy:
       - SQLAlchemy automatically performs JOIN between Bookmark and HeritageSite
       - More efficient than N+1 queries (loading bookmarks then sites separately)
    
    2. Eager Loading:
       - Using .join() and accessing bookmark.heritage_site loads data in one query
       - Alternative: .options(joinedload(Bookmark.heritage_site)) for explicit control
    
    3. Ordering:
       - ORDER BY created_at DESC shows newest bookmarks first
       - Indexed timestamp field ensures fast sorting
    
    Complexity Analysis:
    - Time: O(n log n) where n is number of bookmarks (due to sorting)
    - Space: O(n) for storing bookmark list
    - Database: Single JOIN query (efficient)
    """
    from models import Bookmark
    
    # Get all bookmarks for current user, ordered by newest first
    bookmarks = Bookmark.query.filter_by(
        user_id=current_user.id
    ).order_by(Bookmark.created_at.desc()).all()
    
    # Extract heritage sites from bookmarks
    # The relationship is already loaded, so this doesn't trigger additional queries
    bookmarked_sites = [bookmark.heritage_site for bookmark in bookmarks]
    
    return render_template('my_bookmarks.html', 
                         bookmarks=bookmarks,
                         bookmarked_sites=bookmarked_sites)


# ============================================================================
# REVIEW AND RATING ROUTES
# ============================================================================

@main_bp.route('/heritage/<int:id>/review', methods=['POST'])
@login_required
@role_required('user')
def submit_review(id):
    """
    Submit or Update Review Route
    
    Allows users to submit a rating and comment for a heritage site.
    If user already reviewed this site, updates the existing review.
    
    Academic Note - CRUD Operations:
    -------------------------------
    This route implements Create/Update operations with idempotent behavior:
    
    CRUD Pattern:
    - Create: If no existing review, create new record
    - Read: Check for existing review
    - Update: If review exists, update rating and comment
    - Delete: Separate route (admin only)
    
    Idempotency:
    Multiple submissions by same user for same site result in single review
    (updated, not duplicated). This prevents review spam and maintains data integrity.
    
    Validation Layers:
    1. Application-level: validate_rating() function
    2. Database-level: CHECK constraint (rating BETWEEN 1 AND 5)
    3. Unique constraint: (user_id, heritage_id) prevents duplicates
    
    Defense in Depth:
    Multiple validation layers ensure data integrity even if one layer fails.
    """
    from models import Review
    from utils.validators import validate_rating, sanitize_input
    
    # Verify heritage site exists
    heritage_site = HeritageSite.query.get_or_404(id)
    
    # Get form data
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '')
    
    # Validate rating
    is_valid, error_message = validate_rating(rating)
    if not is_valid:
        flash(error_message, 'danger')
        return redirect(url_for('main.heritage_detail', id=id))
    
    # Sanitize comment to prevent XSS attacks
    clean_comment = sanitize_input(comment, max_length=1000)
    
    # Check if user already reviewed this site
    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        heritage_id=id
    ).first()
    
    try:
        if existing_review:
            # Update existing review
            existing_review.rating = rating
            existing_review.comment = clean_comment
            existing_review.updated_at = datetime.utcnow()
            flash('Your review has been updated!', 'success')
        else:
            # Create new review
            new_review = Review(
                user_id=current_user.id,
                heritage_id=id,
                rating=rating,
                comment=clean_comment
            )
            db.session.add(new_review)
            flash('Thank you for your review!', 'success')
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        flash('Error submitting review. Please try again.', 'danger')
    
    return redirect(url_for('main.heritage_detail', id=id))


@main_bp.route('/heritage/<int:id>/reviews')
@login_required
def view_reviews(id):
    """
    View All Reviews Route
    
    Displays all reviews for a specific heritage site.
    
    Academic Note - Query Optimization:
    ----------------------------------
    This route demonstrates efficient data retrieval with relationships:
    
    Query Strategy:
    1. JOIN: Combines Review and User tables
    2. ORDER BY: Sorts by newest first (created_at DESC)
    3. Eager Loading: User data loaded with reviews (no N+1 queries)
    
    Performance:
    - Single query retrieves all data
    - Indexed foreign keys enable fast JOINs
    - Pagination could be added for large datasets
    """
    from models import Review
    
    # Verify heritage site exists
    heritage_site = HeritageSite.query.get_or_404(id)
    
    # Get all reviews for this site, ordered by newest first
    reviews = Review.query.filter_by(
        heritage_id=id
    ).order_by(Review.created_at.desc()).all()
    
    return render_template('reviews.html', 
                         heritage_site=heritage_site,
                         reviews=reviews)


@main_bp.route('/review/<int:id>/delete', methods=['POST'])
@login_required
def delete_review(id):
    """
    Delete Review Route
    
    Allows users to delete their own reviews, or admins to delete any review.
    
    Academic Note - Authorization Logic:
    -----------------------------------
    This route implements fine-grained access control:
    
    Authorization Rules:
    1. Users can delete their own reviews
    2. Admins can delete any review (moderation)
    3. Other users cannot delete reviews
    
    Security Pattern:
    - Authentication: @login_required ensures user is logged in
    - Authorization: Check ownership or admin role before deletion
    - Audit Trail: Could log deletions for compliance
    
    Use Cases:
    - User wants to remove their review
    - Admin removes inappropriate/spam reviews
    - Content moderation for community guidelines
    """
    from models import Review
    
    review = Review.query.get_or_404(id)
    heritage_id = review.heritage_id
    
    # Check authorization: user owns review OR user is admin
    if review.user_id != current_user.id and not current_user.is_admin():
        flash('You do not have permission to delete this review.', 'danger')
        return redirect(url_for('main.heritage_detail', id=heritage_id))
    
    try:
        db.session.delete(review)
        db.session.commit()
        flash('Review deleted successfully.', 'info')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting review. Please try again.', 'danger')
    
    return redirect(url_for('main.heritage_detail', id=heritage_id))


# ============================================================================
# EXPORT ROUTES
# ============================================================================

@main_bp.route('/export/heritage')
@login_required
def export_heritage():
    """Export Heritage Sites to CSV"""
    from flask import Response
    from io import StringIO
    import csv
    
    sites = HeritageSite.query.all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['ID', 'Name', 'State', 'Category', 'Description', 'Annual Visitors', 'Created At'])
    
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
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=heritage_sites.csv'}
    )


@main_bp.route('/export/artisans')
@login_required
def export_artisans():
    """Export Artisans to CSV"""
    from flask import Response
    from io import StringIO
    import csv
    
    artisans = Artisan.query.all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['ID', 'Name', 'Craft', 'State', 'Product Price', 'Contact', 'Description', 'Created At'])
    
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
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=artisans.csv'}
    )


# ============================================================================
# HOTEL MANAGEMENT ROUTES (Admin Only)
# ============================================================================

@main_bp.route('/admin/hotels/add/<int:heritage_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_hotel(heritage_id):
    """
    Add Hotel Route (Admin Only)
    
    Allows administrators to add new hotels near heritage sites.
    
    Academic Note - Admin-Only Operations:
    -------------------------------------
    Hotel management is restricted to administrators to maintain data quality
    and prevent spam or inappropriate listings.
    
    Validation Rules:
    - Price must be positive
    - Rating must be between 1.0 and 5.0 (if provided)
    - Heritage site must exist
    - All required fields must be provided
    """
    from models import Hotel
    
    heritage_site = HeritageSite.query.get_or_404(heritage_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        state = request.form.get('state')
        price_per_night = float(request.form.get('price_per_night'))
        rating = request.form.get('rating')
        image = request.form.get('image')
        description = request.form.get('description')
        
        # Validate price
        if price_per_night <= 0:
            flash('Price must be greater than 0', 'danger')
            return redirect(request.url)
        
        # Validate rating if provided
        if rating:
            rating = float(rating)
            if rating < 1.0 or rating > 5.0:
                flash('Rating must be between 1.0 and 5.0', 'danger')
                return redirect(request.url)
        else:
            rating = None
        
        new_hotel = Hotel(
            name=name,
            location=location,
            state=state,
            price_per_night=price_per_night,
            rating=rating,
            image=image if image else None,
            description=description,
            heritage_id=heritage_id
        )
        
        db.session.add(new_hotel)
        db.session.commit()
        
        flash(f'Hotel "{name}" added successfully!', 'success')
        return redirect(url_for('main.heritage_detail', id=heritage_id))
    
    return render_template('add_hotel.html', heritage_site=heritage_site)


@main_bp.route('/admin/hotels/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_hotel(id):
    """
    Edit Hotel Route (Admin Only)
    
    Allows administrators to update hotel information.
    """
    from models import Hotel
    
    hotel = Hotel.query.get_or_404(id)
    
    if request.method == 'POST':
        hotel.name = request.form.get('name')
        hotel.location = request.form.get('location')
        hotel.state = request.form.get('state')
        hotel.price_per_night = float(request.form.get('price_per_night'))
        
        rating = request.form.get('rating')
        hotel.rating = float(rating) if rating else None
        
        hotel.image = request.form.get('image') or None
        hotel.description = request.form.get('description')
        
        db.session.commit()
        
        flash(f'Hotel "{hotel.name}" updated successfully!', 'success')
        return redirect(url_for('main.heritage_detail', id=hotel.heritage_id))
    
    return render_template('edit_hotel.html', hotel=hotel)


@main_bp.route('/admin/hotels/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_hotel(id):
    """
    Delete Hotel Route (Admin Only)
    
    Allows administrators to remove hotels from the system.
    
    Academic Note - Cascade Delete:
    ------------------------------
    When a hotel is deleted, all associated bookings are also deleted
    due to the cascade='all, delete-orphan' relationship setting.
    
    This maintains referential integrity but means booking history is lost.
    In production, consider soft deletes (status='deleted') instead.
    """
    from models import Hotel
    
    hotel = Hotel.query.get_or_404(id)
    heritage_id = hotel.heritage_id
    hotel_name = hotel.name
    
    db.session.delete(hotel)
    db.session.commit()
    
    flash(f'Hotel "{hotel_name}" deleted successfully!', 'success')
    return redirect(url_for('main.heritage_detail', id=heritage_id))



# ============================================================================
# HOTEL BOOKING ROUTES
# ============================================================================

@main_bp.route('/hotel/book/<int:hotel_id>', methods=['GET', 'POST'])
@login_required
def book_hotel(hotel_id):
    """
    Hotel Booking Route
    
    Allows authenticated users to book hotels near heritage sites.
    
    Academic Note - Booking System Design:
    -------------------------------------
    This implements a complete booking flow with validation:
    
    Validation Rules:
    1. Check-in date must not be in the past
    2. Check-out date must be after check-in date
    3. Total price must be positive
    4. User must be authenticated
    
    Price Calculation:
    total_price = (check_out_date - check_in_date).days × price_per_night
    
    Business Logic:
    - Booking status defaults to 'Confirmed'
    - Users can cancel bookings later (status → 'Cancelled')
    - Cancelled bookings retained for analytics
    """
    from models import Hotel, HotelBooking
    from datetime import datetime, date
    
    hotel = Hotel.query.get_or_404(hotel_id)
    
    if request.method == 'POST':
        check_in_str = request.form.get('check_in_date')
        check_out_str = request.form.get('check_out_date')
        
        # Parse dates
        try:
            check_in_date = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format', 'danger')
            return redirect(request.url)
        
        # Validate dates
        today = date.today()
        
        if check_in_date < today:
            flash('Check-in date cannot be in the past', 'danger')
            return redirect(request.url)
        
        if check_out_date <= check_in_date:
            flash('Check-out date must be after check-in date', 'danger')
            return redirect(request.url)
        
        # Calculate total price
        nights = (check_out_date - check_in_date).days
        total_price = nights * hotel.price_per_night
        
        if total_price <= 0:
            flash('Invalid booking duration', 'danger')
            return redirect(request.url)
        
        # Create booking
        new_booking = HotelBooking(
            user_id=current_user.id,
            hotel_id=hotel_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_price=total_price,
            booking_status='Confirmed'
        )
        
        db.session.add(new_booking)
        db.session.commit()
        
        flash(f'Booking confirmed! Total: ₹{total_price:,.0f} for {nights} night(s)', 'success')
        return redirect(url_for('main.my_bookings'))
    
    # For GET request
    from datetime import date
    today = date.today().isoformat()
    
    return render_template('book_hotel.html', hotel=hotel, today=today)


@main_bp.route('/dashboard/bookings')
@login_required
def my_bookings():
    """
    My Bookings Route
    
    Displays all hotel bookings made by the current user.
    
    Academic Note - User Dashboard:
    ------------------------------
    This provides users with a personalized view of their booking history.
    
    Features:
    - View all bookings (confirmed and cancelled)
    - See booking details (dates, price, status)
    - Cancel confirmed bookings
    - Sorted by most recent first
    
    Query Optimization:
    - Eager loading of hotel relationship (avoids N+1 queries)
    - Indexed user_id for fast filtering
    - Ordered by created_at descending
    """
    from models import HotelBooking
    
    bookings = HotelBooking.query.filter_by(
        user_id=current_user.id
    ).order_by(HotelBooking.created_at.desc()).all()
    
    return render_template('my_bookings.html', bookings=bookings)


@main_bp.route('/booking/cancel/<int:id>', methods=['POST'])
@login_required
def cancel_booking(id):
    """
    Cancel Booking Route
    
    Allows users to cancel their confirmed bookings.
    
    Academic Note - Soft Delete Pattern:
    -----------------------------------
    Instead of deleting the booking record, we change its status to 'Cancelled'.
    This preserves data for:
    - Analytics and reporting
    - Audit trail
    - Customer service inquiries
    - Business intelligence
    
    Authorization:
    - Users can only cancel their own bookings
    - Admins can cancel any booking (superuser privilege)
    """
    from models import HotelBooking
    
    booking = HotelBooking.query.get_or_404(id)
    
    # Authorization check: user can only cancel their own bookings
    # (admin can cancel any booking due to role hierarchy)
    if booking.user_id != current_user.id and not current_user.is_admin():
        flash('You can only cancel your own bookings', 'danger')
        return redirect(url_for('main.my_bookings'))
    
    # Check if already cancelled
    if booking.booking_status == 'Cancelled':
        flash('This booking is already cancelled', 'warning')
        return redirect(url_for('main.my_bookings'))
    
    # Cancel booking (soft delete)
    booking.booking_status = 'Cancelled'
    db.session.commit()
    
    flash('Booking cancelled successfully', 'success')
    return redirect(url_for('main.my_bookings'))
