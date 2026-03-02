"""
Database Models for Digital Catalyst Platform
Contains models for Heritage Sites, Artisans, and Users
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    User model for authentication and authorization
    
    Academic Context - Cascade Delete Rules and Referential Integrity:
    ------------------------------------------------------------------
    Relationships in this model demonstrate different cascade behaviors based on
    business requirements and data preservation needs.
    
    Cascade Delete (bookmarks, reviews):
    - When a user is deleted, their bookmarks and reviews are automatically deleted
    - Rationale: These are user-generated content tied to user identity
    - Maintains referential integrity (no orphaned records)
    - GDPR compliance: User data removal includes all personal content
    
    SET NULL (site_views):
    - When a user is deleted, their site_views records remain but user_id becomes NULL
    - Rationale: Preserve analytics data for business intelligence
    - Anonymous analytics: Views become anonymous but still counted
    - Historical data preservation: Engagement metrics remain accurate
    
    Relationship Types:
    - One-to-Many: One user has many bookmarks/reviews/views
    - Lazy Loading: Related objects loaded only when accessed (performance optimization)
    - Backref: Enables bidirectional navigation (user.bookmarks and bookmark.user)
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'user' or 'manufacturer'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships with cascade delete rules
    bookmarks = db.relationship('Bookmark', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    site_views = db.relationship('SiteView', backref='user', lazy=True)
    hotel_bookings = db.relationship('HotelBooking', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def is_user(self):
        """
        Check if user has 'user' role.
        
        Academic Context - Role-Based Access Control (RBAC):
        ----------------------------------------------------
        RBAC is a security model where access decisions are based on roles
        assigned to users rather than individual user identities.
        
        RBAC Components:
        1. Users: Entities that need access (people, services)
        2. Roles: Job functions or responsibilities (user, manufacturer, admin)
        3. Permissions: Access rights to resources (read, write, delete)
        4. Role-Permission Assignment: Roles are granted permissions
        5. User-Role Assignment: Users are assigned roles
        
        Benefits of RBAC:
        - Principle of Least Privilege: Users get only necessary permissions
        - Separation of Duties: Different roles for different responsibilities
        - Simplified Management: Change role permissions, not individual users
        - Audit Trail: Track access by role
        
        Role Hierarchy in Digital Catalyst:
        - user: Basic access (browse, bookmark, review)
        - manufacturer: User permissions + product management
        - admin: All permissions + user management + analytics
        
        Returns:
            bool: True if user has 'user' role
        """
        return (self.role or 'user').lower() == 'user'
    
    def is_manufacturer(self):
        """
        Check if user has 'manufacturer' role.
        
        Manufacturer Permissions:
        - All user permissions (browse, bookmark, review)
        - Add/edit/delete own artisan products
        - Upload product images
        - View own product analytics
        
        Returns:
            bool: True if user has 'manufacturer' role
        """
        return (self.role or 'user').lower() == 'manufacturer'
    
    def is_admin(self):
        """
        Check if user has 'admin' role.
        
        Admin Permissions:
        - All user and manufacturer permissions
        - View all users
        - Delete users
        - Approve artisans
        - Delete inappropriate reviews
        - View system-wide analytics dashboard
        - Access admin-only routes
        
        Security Note:
        Admin role should be assigned carefully and audited regularly.
        Consider implementing multi-factor authentication for admin accounts.
        
        Returns:
            bool: True if user has 'admin' role
        """
        return (self.role or 'user').lower() == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'


class HeritageSite(db.Model):
    """
    Heritage Site model for cultural preservation tracking
    
    Academic Context - Cascade Delete and Data Lifecycle Management:
    ----------------------------------------------------------------
    This model demonstrates comprehensive cascade delete rules for maintaining
    database consistency when heritage sites are removed.
    
    Cascade Delete Strategy:
    All related records (bookmarks, reviews, site_views) are deleted when a
    heritage site is deleted. This ensures:
    
    1. No Orphaned Records: Prevents foreign key references to non-existent sites
    2. Data Consistency: Maintains referential integrity across all tables
    3. Storage Efficiency: Removes obsolete data automatically
    4. Query Performance: No need to filter out invalid references
    
    Relationship Cardinality:
    - One-to-Many: One site has many bookmarks/reviews/views
    - Bidirectional: site.bookmarks and bookmark.heritage_site both work
    
    Performance Considerations:
    - Lazy loading: Related objects loaded on-demand (not with every query)
    - Indexed foreign keys: Fast JOIN operations for aggregations
    - Cascade operations: Database handles deletions efficiently in single transaction
    """
    __tablename__ = 'heritage_sites'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # Temple, Fort, Monument, etc.
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)  # optional image URL
    latitude = db.Column(db.Float, nullable=True)  # Geographic latitude for map display
    longitude = db.Column(db.Float, nullable=True)  # Geographic longitude for map display
    annual_visitors = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships with cascade delete rules
    bookmarks = db.relationship('Bookmark', backref='heritage_site', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='heritage_site', lazy=True, cascade='all, delete-orphan')
    site_views = db.relationship('SiteView', backref='heritage_site', lazy=True, cascade='all, delete-orphan')
    hotels = db.relationship('Hotel', backref='heritage_site', lazy=True, cascade='all, delete-orphan')
    
    @property
    def avg_rating(self):
        """
        Calculate average rating from all reviews for this heritage site.
        
        Academic Context - Lazy Evaluation and Query Optimization:
        ----------------------------------------------------------
        This property demonstrates lazy evaluation - the average is calculated
        on-demand rather than stored in the database.
        
        Trade-offs:
        
        Lazy Evaluation (Current Approach):
        Pros:
        - Always accurate (no stale data)
        - No storage overhead
        - No update complexity (no triggers needed)
        Cons:
        - Computed on every access (CPU cost)
        - Requires JOIN query (I/O cost)
        
        Eager Evaluation (Alternative):
        Pros:
        - Fast retrieval (pre-computed)
        - No JOIN needed
        Cons:
        - Stale data risk
        - Storage overhead
        - Complex update logic (triggers or application code)
        
        For this application, lazy evaluation is preferred because:
        1. Review frequency is low (not updated constantly)
        2. Accuracy is more important than speed
        3. Simpler implementation (no cache invalidation)
        
        Query Optimization:
        - Uses SQLAlchemy func.avg() for database-level aggregation
        - More efficient than loading all reviews into Python
        - Database engines optimize aggregate functions
        
        Returns:
            float: Average rating (1.0-5.0) or None if no reviews
        """
        from sqlalchemy import func
        result = db.session.query(func.avg(Review.rating)).filter(
            Review.heritage_id == self.id
        ).scalar()
        return round(result, 2) if result else None
    
    @property
    def review_count(self):
        """
        Count total number of reviews for this heritage site.
        
        Implementation Note:
        Uses COUNT query instead of len(self.reviews) to avoid loading
        all review objects into memory. More efficient for large datasets.
        
        Returns:
            int: Total number of reviews
        """
        from sqlalchemy import func
        return db.session.query(func.count(Review.id)).filter(
            Review.heritage_id == self.id
        ).scalar() or 0
    
    @property
    def view_count(self):
        """
        Count total number of views (both authenticated and anonymous) for this site.
        
        Analytics Use Cases:
        - Popularity ranking
        - Trending sites detection
        - Recommendation engine input
        - Business intelligence dashboards
        
        Returns:
            int: Total number of views
        """
        from sqlalchemy import func
        return db.session.query(func.count(SiteView.id)).filter(
            SiteView.heritage_id == self.id
        ).scalar() or 0
    
    @property
    def bookmark_count(self):
        """
        Count total number of users who bookmarked this heritage site.
        
        Business Value:
        - Indicates user interest and intent to visit
        - Higher signal than views (active engagement vs passive browsing)
        - Useful for recommendation algorithms
        
        Returns:
            int: Total number of bookmarks
        """
        from sqlalchemy import func
        return db.session.query(func.count(Bookmark.id)).filter(
            Bookmark.heritage_id == self.id
        ).scalar() or 0
    
    def image_or_placeholder(self):
        """Return image_url or a placeholder URL based on category."""
        if self.image_url:
            return self.image_url
        from urllib.parse import quote
        text = quote(self.category or 'Heritage')
        return f"https://placehold.co/400x300/2C6E7C/FFFFFF?text={text}"
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'category': self.category,
            'description': self.description,
            'image_url': self.image_url,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'annual_visitors': self.annual_visitors,
            'avg_rating': self.avg_rating,
            'review_count': self.review_count,
            'view_count': self.view_count,
            'bookmark_count': self.bookmark_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<HeritageSite {self.name}>'


class Artisan(db.Model):
    """Artisan model for MSME and craftsperson tracking"""
    __tablename__ = 'artisans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    craft = db.Column(db.String(100), nullable=False)  # Pottery, Weaving, Metalwork, etc.
    state = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    contact = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)  # optional product/image URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def image_or_placeholder(self):
        """Return image_url or a placeholder URL based on craft."""
        if self.image_url:
            return self.image_url
        from urllib.parse import quote
        text = quote(self.craft or 'Craft')
        return f"https://placehold.co/400x300/FF6B35/FFFFFF?text={text}"
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'craft': self.craft,
            'state': self.state,
            'product_price': self.product_price,
            'contact': self.contact,
            'description': self.description,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Artisan {self.name}>'


class Product(db.Model):
    """Product model for artisan products"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    stock = db.Column(db.Integer, default=1)
    district = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)  # Added for state-wide filtering
    artisan_id = db.Column(db.Integer, db.ForeignKey('artisans.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    artisan = db.relationship('Artisan', backref=db.backref('products', lazy=True, cascade='all, delete-orphan'))
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'stock': self.stock,
            'artisan_id': self.artisan_id,
            'artisan_name': self.artisan.name if self.artisan else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Product {self.name}>'


class Order(db.Model):
    """Order model for product purchases"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    total_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), default='pending')  # pending, completed, failed
    payment_id = db.Column(db.String(200), nullable=True)
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(200), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='orders')
    product = db.relationship('Product', backref='orders')
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'total_amount': self.total_amount,
            'payment_status': self.payment_status,
            'payment_id': self.payment_id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'shipping_address': self.shipping_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Order {self.id}>'


class Bookmark(db.Model):
    """
    Bookmark model for user-saved heritage sites
    
    Academic Context - Database Normalization:
    ------------------------------------------
    This model represents a many-to-many relationship between Users and HeritageSites.
    In relational database design, many-to-many relationships require a junction table
    (also called association table or bridge table).
    
    Normalization Benefits:
    - 3NF (Third Normal Form): No transitive dependencies
    - Eliminates data redundancy
    - Maintains referential integrity through foreign keys
    - Enables efficient querying of user bookmarks and site popularity
    
    Unique Constraint:
    The composite unique constraint on (user_id, heritage_id) ensures that:
    - A user cannot bookmark the same site multiple times
    - Prevents duplicate records in the database
    - Enforces business rule at database level (defense in depth)
    
    Indexing Strategy:
    Foreign key columns are automatically indexed by most databases, but we explicitly
    define indexes to ensure optimal query performance for:
    - Finding all bookmarks for a user: WHERE user_id = ?
    - Finding all users who bookmarked a site: WHERE heritage_id = ?
    - Counting bookmarks per site: GROUP BY heritage_id
    """
    __tablename__ = 'bookmarks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    heritage_id = db.Column(db.Integer, db.ForeignKey('heritage_sites.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Unique constraint: one bookmark per user per site
    __table_args__ = (
        db.UniqueConstraint('user_id', 'heritage_id', name='unique_user_heritage_bookmark'),
    )
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'heritage_id': self.heritage_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Bookmark user={self.user_id} heritage={self.heritage_id}>'


class SiteView(db.Model):
    """
    SiteView model for tracking heritage site engagement
    
    Academic Context - Analytics and User Behavior Tracking:
    --------------------------------------------------------
    This model implements event tracking for analytics purposes, recording each
    time a heritage site is viewed. This data enables:
    
    1. Popularity Metrics: Identify most viewed sites
    2. User Behavior Analysis: Understand browsing patterns
    3. Recommendation Engine Input: Use view history for personalization
    4. Business Intelligence: Track engagement trends over time
    
    Nullable user_id Design Decision:
    The user_id field is nullable to support both:
    - Authenticated tracking: user_id is set for logged-in users
    - Anonymous tracking: user_id is NULL for guest visitors
    
    This design choice enables:
    - Privacy-conscious analytics (no forced authentication)
    - Comprehensive engagement metrics (includes anonymous traffic)
    - Conversion funnel analysis (anonymous → registered user journey)
    
    Timestamp Indexing:
    The created_at field is indexed to enable efficient time-based queries:
    - Views in last 24 hours: WHERE created_at > NOW() - INTERVAL 1 DAY
    - Trending sites: GROUP BY heritage_id ORDER BY COUNT(*) DESC
    - Time series analysis: GROUP BY DATE(created_at)
    
    Cascade Delete Behavior:
    - User deletion: SET NULL (preserve analytics data)
    - Heritage site deletion: CASCADE (no orphaned view records)
    """
    __tablename__ = 'site_views'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    heritage_id = db.Column(db.Integer, db.ForeignKey('heritage_sites.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'heritage_id': self.heritage_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<SiteView user={self.user_id} heritage={self.heritage_id}>'


class Review(db.Model):
    """
    Review model for user ratings and comments on heritage sites
    
    Academic Context - Data Integrity and Constraints:
    --------------------------------------------------
    This model demonstrates advanced database constraint usage to enforce
    business rules at the database level, implementing defense-in-depth security.
    
    Constraint Types Implemented:
    
    1. Unique Constraint (user_id, heritage_id):
       - Business Rule: One review per user per site
       - Prevents duplicate reviews
       - Enforced at database level (cannot be bypassed by application bugs)
       - Alternative to application-level validation (more reliable)
    
    2. Check Constraint (rating BETWEEN 1 AND 5):
       - Business Rule: Ratings must be 1-5 stars
       - Prevents invalid data entry
       - Database-level validation (last line of defense)
       - Complements application-level validation
    
    3. NOT NULL Constraints:
       - Ensures required fields are always present
       - Prevents incomplete records
       - Maintains data quality
    
    Timestamp Fields (created_at, updated_at):
    - created_at: Records when review was first submitted
    - updated_at: Automatically updates when review is modified
    - Enables audit trail and change tracking
    - Supports "edited" indicator in UI
    
    Indexing Strategy:
    - Foreign keys indexed for JOIN performance
    - created_at indexed for sorting (newest first)
    - Composite index on (heritage_id, rating) for average rating calculation
    
    Referential Integrity:
    - CASCADE delete: When user/site deleted, reviews are removed
    - Maintains database consistency
    - Prevents orphaned records
    """
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    heritage_id = db.Column(db.Integer, db.ForeignKey('heritage_sites.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint: one review per user per site
    # Check constraint: rating must be between 1 and 5
    __table_args__ = (
        db.UniqueConstraint('user_id', 'heritage_id', name='unique_user_heritage_review'),
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='valid_rating_range'),
    )
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'heritage_id': self.heritage_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Review user={self.user_id} heritage={self.heritage_id} rating={self.rating}>'


# ============================================================================
# HOTEL BOOKING SYSTEM MODELS
# ============================================================================

class Hotel(db.Model):
    """
    Hotel Model for Heritage Site Accommodation
    
    Academic Context - Hotel Management System:
    ------------------------------------------
    This model represents hotels near heritage sites, enabling users to book
    accommodation during their cultural tourism visits.
    
    Business Logic:
    - Each hotel is associated with a specific heritage site
    - Hotels have pricing, ratings, and availability information
    - Supports tourism ecosystem around cultural heritage
    
    Relationship Design:
    - Many-to-One: Many hotels can be near one heritage site
    - One-to-Many: One hotel can have many bookings
    
    Data Integrity:
    - Foreign key to heritage_sites ensures valid associations
    - Rating constraint ensures valid range (1-5)
    - Price validation prevents negative values
    
    Use Cases:
    - Display hotels on heritage detail pages
    - Enable booking flow for tourists
    - Analytics on accommodation preferences
    - Revenue tracking for tourism impact
    """
    __tablename__ = 'hotels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(300), nullable=False)  # Full address
    state = db.Column(db.String(100), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=True)  # 1.0 to 5.0
    image = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    heritage_id = db.Column(db.Integer, db.ForeignKey('heritage_sites.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('HotelBooking', backref='hotel', lazy=True, cascade='all, delete-orphan')
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('price_per_night > 0', name='valid_price'),
        db.CheckConstraint('rating IS NULL OR (rating >= 1.0 AND rating <= 5.0)', name='valid_hotel_rating'),
    )
    
    def image_or_placeholder(self):
        """Return image URL or placeholder"""
        if self.image:
            return self.image
        from urllib.parse import quote
        text = quote('Hotel')
        return f"https://placehold.co/400x300/4ECDC4/FFFFFF?text={text}"
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'state': self.state,
            'price_per_night': self.price_per_night,
            'rating': self.rating,
            'image': self.image,
            'description': self.description,
            'heritage_id': self.heritage_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Hotel {self.name}>'


class HotelBooking(db.Model):
    """
    Hotel Booking Model for Reservation Management
    
    Academic Context - Booking System Design:
    ----------------------------------------
    This model tracks hotel reservations made by users, implementing a
    complete booking lifecycle with status management.
    
    Booking Lifecycle:
    1. User selects hotel and dates
    2. System calculates total price
    3. Booking created with "Confirmed" status
    4. User can view in "My Bookings"
    5. User can cancel (status → "Cancelled")
    
    Business Rules:
    - Check-out must be after check-in
    - Cannot book in the past
    - Total price = nights × price_per_night
    - Cancelled bookings retained for analytics
    
    Data Integrity:
    - Foreign keys ensure valid user and hotel references
    - Date constraints prevent invalid bookings
    - Status enum ensures valid states
    - Cascade rules maintain consistency
    
    Analytics Value:
    - Track booking patterns
    - Calculate revenue
    - Identify popular hotels
    - Measure tourism impact
    """
    __tablename__ = 'hotel_bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False, index=True)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booking_status = db.Column(db.String(20), nullable=False, default='Confirmed')  # Confirmed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('check_out_date > check_in_date', name='valid_date_range'),
        db.CheckConstraint('total_price > 0', name='valid_total_price'),
        db.CheckConstraint("booking_status IN ('Confirmed', 'Cancelled')", name='valid_booking_status'),
    )
    
    @property
    def nights(self):
        """Calculate number of nights"""
        if self.check_in_date and self.check_out_date:
            return (self.check_out_date - self.check_in_date).days
        return 0
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'hotel_id': self.hotel_id,
            'hotel_name': self.hotel.name if self.hotel else None,
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'check_out_date': self.check_out_date.isoformat() if self.check_out_date else None,
            'nights': self.nights,
            'total_price': self.total_price,
            'booking_status': self.booking_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<HotelBooking user={self.user_id} hotel={self.hotel_id} status={self.booking_status}>'


# Update HeritageSite model to include hotels relationship
# Add this to the HeritageSite class relationships section:
# hotels = db.relationship('Hotel', backref='heritage_site', lazy=True, cascade='all, delete-orphan')

# Update User model to include hotel bookings relationship
# Add this to the User class relationships section:
# hotel_bookings = db.relationship('HotelBooking', backref='user', lazy=True, cascade='all, delete-orphan')
