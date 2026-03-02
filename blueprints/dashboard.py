"""
Analytics Dashboard Blueprint
==============================

This blueprint provides analytics and admin dashboard functionality for the
Digital Catalyst platform.

Academic Note:
This blueprint demonstrates data analytics using SQL aggregation functions.
The analytics dashboard provides insights into system usage, user engagement,
and content popularity using SQLAlchemy's func module for database-level
aggregation (more efficient than Python-level calculations).

Aggregation Functions Used:
- func.count(): Counts records
- func.avg(): Calculates average values
- func.sum(): Sums numeric values
- group_by(): Groups results by column
- order_by(): Sorts results

Access Control:
This blueprint will be enhanced with role-based access control to restrict
analytics access to admin users only.
"""

from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func, desc
from models import db, User, HeritageSite, Artisan, Product
from utils.decorators import admin_required

# Create Blueprint
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    """
    Analytics Dashboard Route
    
    Displays comprehensive system analytics including:
    - Total counts (users, manufacturers, heritage sites)
    - Most viewed heritage site
    - Most bookmarked heritage site
    - Highest rated heritage site
    - Most active state
    
    Academic Note:
    This route demonstrates advanced SQL aggregation queries using SQLAlchemy.
    All calculations are performed at the database level for optimal performance.
    
    Query Optimization:
    - Uses scalar() for single value queries (more efficient than first())
    - Uses joins for related data (avoids N+1 query problem)
    - Uses group_by() for aggregation (database-level grouping)
    - Uses order_by() with desc() for sorting (database-level sorting)
    
    Complexity Analysis:
    - Total counts: O(1) with database indexes
    - Aggregations: O(n) where n is number of records
    - Joins: O(n*m) worst case, O(n) with proper indexes
    
    Future Enhancement:
    This route will be enhanced to include:
    - View tracking (most viewed sites)
    - Bookmark tracking (most bookmarked sites)
    - Review tracking (highest rated sites)
    """
    
    # ========================================================================
    # TOTAL COUNTS
    # ========================================================================
    
    # Total users (all roles)
    # Academic Note: scalar() returns single value, more efficient than first()[0]
    total_users = db.session.query(func.count(User.id)).scalar() or 0
    
    # Total manufacturers (role = 'manufacturer')
    # Academic Note: filter() adds WHERE clause to query
    total_manufacturers = db.session.query(func.count(User.id)).filter(
        User.role == 'manufacturer'
    ).scalar() or 0
    
    # Total heritage sites
    total_heritage_sites = db.session.query(func.count(HeritageSite.id)).scalar() or 0
    
    # Total artisans
    total_artisans = db.session.query(func.count(Artisan.id)).scalar() or 0
    
    # Total products
    total_products = db.session.query(func.count(Product.id)).scalar() or 0
    
    # ========================================================================
    # TOP HERITAGE SITES
    # ========================================================================
    
    # Most visited heritage site (by annual_visitors)
    # Academic Note: order_by(desc()) sorts in descending order
    most_visited_site = db.session.query(
        HeritageSite.name,
        HeritageSite.annual_visitors
    ).order_by(desc(HeritageSite.annual_visitors)).first()
    
    # Most viewed heritage site (by SiteView count)
    # Academic Note: JOIN with aggregation to count views per site
    from models import SiteView, Bookmark, Review
    
    most_viewed_site = db.session.query(
        HeritageSite.name,
        func.count(SiteView.id).label('view_count')
    ).join(
        SiteView, HeritageSite.id == SiteView.heritage_id
    ).group_by(
        HeritageSite.id, HeritageSite.name
    ).order_by(desc('view_count')).first()
    
    # Most bookmarked heritage site
    # Academic Note: Similar aggregation pattern for bookmarks
    most_bookmarked_site = db.session.query(
        HeritageSite.name,
        func.count(Bookmark.id).label('bookmark_count')
    ).join(
        Bookmark, HeritageSite.id == Bookmark.heritage_id
    ).group_by(
        HeritageSite.id, HeritageSite.name
    ).order_by(desc('bookmark_count')).first()
    
    # Highest rated heritage site
    # Academic Note: Uses AVG aggregation function for average rating
    highest_rated_site = db.session.query(
        HeritageSite.name,
        func.avg(Review.rating).label('avg_rating'),
        func.count(Review.id).label('review_count')
    ).join(
        Review, HeritageSite.id == Review.heritage_id
    ).group_by(
        HeritageSite.id, HeritageSite.name
    ).order_by(desc('avg_rating')).first()
    most_visited_site = db.session.query(
        HeritageSite.name,
        HeritageSite.annual_visitors
    ).order_by(desc(HeritageSite.annual_visitors)).first()
    
    # ========================================================================
    # STATE ANALYTICS
    # ========================================================================
    
    # Most active state (by number of heritage sites)
    # Academic Note: group_by() groups results, func.count() counts per group
    most_active_state = db.session.query(
        HeritageSite.state,
        func.count(HeritageSite.id).label('site_count')
    ).group_by(HeritageSite.state).order_by(desc('site_count')).first()
    
    # State-wise heritage site distribution
    # Returns list of tuples: [(state, count), ...]
    state_distribution = db.session.query(
        HeritageSite.state,
        func.count(HeritageSite.id).label('count')
    ).group_by(HeritageSite.state).order_by(desc('count')).limit(10).all()
    
    # ========================================================================
    # ARTISAN ANALYTICS
    # ========================================================================
    
    # Most popular craft (by number of artisans)
    most_popular_craft = db.session.query(
        Artisan.craft,
        func.count(Artisan.id).label('artisan_count')
    ).group_by(Artisan.craft).order_by(desc('artisan_count')).first()
    
    # Average product price by craft
    avg_price_by_craft = db.session.query(
        Artisan.craft,
        func.avg(Artisan.product_price).label('avg_price')
    ).group_by(Artisan.craft).order_by(desc('avg_price')).limit(10).all()
    
    # ========================================================================
    # PRODUCT ANALYTICS
    # ========================================================================
    
    # Total product inventory value
    # Academic Note: sum() aggregates numeric values
    total_inventory_value = db.session.query(
        func.sum(Product.price * Product.stock)
    ).scalar() or 0
    
    # Average product price
    avg_product_price = db.session.query(
        func.avg(Product.price)
    ).scalar() or 0
    
    # ========================================================================
    # HOTEL BOOKING ANALYTICS
    # ========================================================================
    
    from models import Hotel, HotelBooking
    
    # Total hotels
    total_hotels = db.session.query(func.count(Hotel.id)).scalar() or 0
    
    # Total bookings
    total_bookings = db.session.query(func.count(HotelBooking.id)).scalar() or 0
    
    # Total confirmed bookings
    confirmed_bookings = db.session.query(func.count(HotelBooking.id)).filter(
        HotelBooking.booking_status == 'Confirmed'
    ).scalar() or 0
    
    # Total revenue from bookings
    total_revenue = db.session.query(
        func.sum(HotelBooking.total_price)
    ).filter(HotelBooking.booking_status == 'Confirmed').scalar() or 0
    
    # Most booked hotel
    most_booked_hotel = db.session.query(
        Hotel.name,
        func.count(HotelBooking.id).label('booking_count')
    ).join(
        HotelBooking, Hotel.id == HotelBooking.hotel_id
    ).group_by(
        Hotel.id, Hotel.name
    ).order_by(desc('booking_count')).first()
    
    # ========================================================================
    # PREPARE DATA FOR TEMPLATE
    # ========================================================================
    
    analytics_data = {
        # Total counts
        'total_users': total_users,
        'total_manufacturers': total_manufacturers,
        'total_heritage_sites': total_heritage_sites,
        'total_artisans': total_artisans,
        'total_products': total_products,
        
        # Heritage site analytics
        'most_visited_site': {
            'name': most_visited_site[0] if most_visited_site else 'N/A',
            'visitors': most_visited_site[1] if most_visited_site else 0
        },
        'most_viewed_site': {
            'name': most_viewed_site[0] if most_viewed_site else 'N/A',
            'view_count': most_viewed_site[1] if most_viewed_site else 0
        },
        'most_bookmarked_site': {
            'name': most_bookmarked_site[0] if most_bookmarked_site else 'N/A',
            'bookmark_count': most_bookmarked_site[1] if most_bookmarked_site else 0
        },
        'highest_rated_site': {
            'name': highest_rated_site[0] if highest_rated_site else 'N/A',
            'avg_rating': round(highest_rated_site[1], 2) if highest_rated_site else 0,
            'review_count': highest_rated_site[2] if highest_rated_site else 0
        },
        
        # State analytics
        'most_active_state': {
            'name': most_active_state[0] if most_active_state else 'N/A',
            'site_count': most_active_state[1] if most_active_state else 0
        },
        'state_distribution': [
            {'state': state, 'count': count} 
            for state, count in state_distribution
        ],
        
        # Artisan analytics
        'most_popular_craft': {
            'name': most_popular_craft[0] if most_popular_craft else 'N/A',
            'artisan_count': most_popular_craft[1] if most_popular_craft else 0
        },
        'avg_price_by_craft': [
            {'craft': craft, 'avg_price': round(avg_price, 2)} 
            for craft, avg_price in avg_price_by_craft
        ],
        
        # Product analytics
        'total_inventory_value': round(total_inventory_value, 2),
        'avg_product_price': round(avg_product_price, 2),
        
        # Hotel booking analytics
        'total_hotels': total_hotels,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_revenue': round(total_revenue, 2),
        'most_booked_hotel': {
            'name': most_booked_hotel[0] if most_booked_hotel else 'N/A',
            'booking_count': most_booked_hotel[1] if most_booked_hotel else 0
        }
    }
    
    return render_template('dashboard/analytics.html', analytics=analytics_data)


# Academic Note on Analytics Dashboard Design:
# 
# This dashboard demonstrates several important database concepts:
# 
# 1. Aggregation Functions:
#    - COUNT: Counts records (O(n) complexity)
#    - AVG: Calculates average (O(n) complexity)
#    - SUM: Sums values (O(n) complexity)
#    - GROUP BY: Groups results (O(n log n) with sorting)
# 
# 2. Query Optimization:
#    - Database-level calculations (faster than Python)
#    - Proper indexing on foreign keys and frequently queried columns
#    - Limiting results to prevent memory issues
# 
# 3. Data Presentation:
#    - Structured data format for easy template rendering
#    - Null handling (or 0 for missing data)
#    - Rounding for decimal values
# 
# 4. Future Enhancements:
#    - Caching for frequently accessed analytics
#    - Time-based analytics (daily, weekly, monthly trends)
#    - User engagement metrics (views, bookmarks, reviews)
#    - Comparative analytics (year-over-year growth)
#    - Export functionality (PDF, Excel reports)
# 
# 5. Limitations:
#    - Current implementation recalculates on every request
#    - No historical data tracking
#    - Limited to current database state
#    - No real-time updates
# 
# For production deployment, consider:
# - Redis caching for analytics data
# - Background jobs for expensive calculations
# - Materialized views for complex aggregations
# - Time-series database for historical trends
