"""
REST API Blueprint
==================

This blueprint provides JSON-based REST API endpoints for programmatic access
to the Digital Catalyst platform.

Academic Note:
REST (Representational State Transfer) is an architectural style for distributed
systems. This API follows REST principles:
1. Stateless: Each request contains all necessary information
2. Resource-based: URLs represent resources (heritage sites, artisans)
3. HTTP methods: GET for retrieval, POST for creation, etc.
4. JSON format: Standard data interchange format

HTTP Status Codes Used:
- 200 OK: Successful request
- 400 Bad Request: Invalid input parameters
- 404 Not Found: Resource doesn't exist
- 500 Internal Server Error: Server-side error

Error Handling:
All endpoints include try-except blocks to catch and handle errors gracefully,
returning appropriate status codes and error messages in JSON format.
"""

from flask import Blueprint, jsonify, request
from models import db, HeritageSite, Artisan, Product, Order, User
from ml.recommendation_engine import RecommendationEngine
from sqlalchemy import text

# Create Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize ML engine
ml_engine = RecommendationEngine()


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    GET /api/health
    
    Health check endpoint to verify database connectivity and app status.
    """
    try:
        # Test database connection
        db.session.execute(text('SELECT 1'))
        
        # Check if users exist
        user_count = User.query.count()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'users': user_count,
            'message': 'Application is running correctly'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'message': 'Database connection failed'
        }), 500


@api_bp.route('/heritage', methods=['GET'])
def api_heritage():
    """
    GET /api/heritage
    
    Returns all heritage sites as JSON array.
    
    Response Format:
    [
        {
            "id": 1,
            "name": "Taj Mahal",
            "state": "Uttar Pradesh",
            "category": "Monument",
            "description": "...",
            "image_url": "...",
            "annual_visitors": 7000000,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        },
        ...
    ]
    
    Academic Note:
    This endpoint demonstrates the Read operation in REST CRUD.
    The to_dict() method serializes SQLAlchemy models to JSON-compatible dictionaries.
    """
    try:
        sites = HeritageSite.query.all()
        return jsonify([site.to_dict() for site in sites]), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@api_bp.route('/artisans', methods=['GET'])
def api_artisans():
    """
    GET /api/artisans
    
    Returns all artisans as JSON array.
    
    Response Format:
    [
        {
            "id": 1,
            "name": "Ramesh Kumar",
            "craft": "Pottery",
            "state": "Rajasthan",
            "product_price": 1500,
            "contact": "9876543210",
            "description": "...",
            "image_url": "...",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        },
        ...
    ]
    """
    try:
        artisans = Artisan.query.all()
        return jsonify([artisan.to_dict() for artisan in artisans]), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@api_bp.route('/recommendations', methods=['GET'])
def api_recommendations():
    """
    GET /api/recommendations?type=heritage&state=&top_n=5
    
    Returns AI-generated recommendations.
    
    Query Parameters:
    - type: 'heritage' or 'artisans' (default: 'heritage')
    - state: Filter by state (optional, for artisans)
    - top_n: Number of recommendations (default: 5)
    
    Response Format:
    [
        {
            "id": 1,
            "name": "Taj Mahal",
            "state": "Uttar Pradesh",
            "category": "Monument",
            "annual_visitors": 7000000
        },
        ...
    ]
    
    Academic Note:
    This endpoint exposes the ML recommendation engine via REST API.
    The recommendation algorithm uses content-based and popularity-based
    filtering to suggest relevant items.
    """
    try:
        recommendation_type = request.args.get('type', 'heritage')
        state = request.args.get('state', None)
        top_n = int(request.args.get('top_n', 5))
        
        if recommendation_type == 'heritage':
            sites = HeritageSite.query.all()
            sites_data = [site.to_dict() for site in sites]
            recommendations = ml_engine.recommend_heritage_sites(sites_data, top_n)
            return jsonify(recommendations), 200
        
        elif recommendation_type == 'artisans':
            artisans = Artisan.query.all()
            artisans_data = [artisan.to_dict() for artisan in artisans]
            recommendations = ml_engine.recommend_artisans_by_state(artisans_data, state, top_n)
            return jsonify(recommendations), 200
        
        else:
            return jsonify({'error': 'Invalid recommendation type', 'message': 'Type must be "heritage" or "artisans"'}), 400
            
    except ValueError as e:
        return jsonify({'error': 'Invalid input', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@api_bp.route('/analytics', methods=['GET'])
def api_analytics():
    """
    GET /api/analytics
    
    Returns analytics data including economic impact, visitor trends, and state distribution.
    
    Response Format:
    {
        "economic_impact": {
            "total_visitors": 15000000,
            "tourism_revenue": 7500000000,
            "artisan_revenue": 10000000,
            "total_economic_impact": 7510000000,
            "avg_product_price": 2500
        },
        "visitor_trends": {
            "labels": ["Taj Mahal", "Red Fort", ...],
            "values": [7000000, 2500000, ...]
        },
        "state_distribution": {
            "Rajasthan": 2,
            "West Bengal": 1,
            ...
        }
    }
    
    Academic Note:
    This endpoint demonstrates data aggregation and analytics.
    The ML engine calculates metrics using statistical methods
    and returns structured data for visualization.
    """
    try:
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
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@api_bp.route('/products', methods=['GET'])
def api_products():
    """
    GET /api/products
    
    Returns all products as JSON array.
    
    Response Format:
    [
        {
            "id": 1,
            "name": "Blue Pottery Vase",
            "description": "...",
            "price": 1500,
            "image_url": "...",
            "stock": 10,
            "artisan_id": 1,
            "artisan_name": "Ramesh Kumar",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        },
        ...
    ]
    """
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@api_bp.route('/heritage/<int:heritage_id>', methods=['GET'])
def api_heritage_detail(heritage_id):
    """
    GET /api/heritage/<heritage_id>
    
    Returns detailed information about a specific heritage site.
    
    Response Format:
    {
        "id": 1,
        "name": "Taj Mahal",
        "state": "Uttar Pradesh",
        "category": "Monument",
        "description": "...",
        "image_url": "...",
        "annual_visitors": 7000000,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    
    Error Response (404):
    {
        "error": "Heritage site not found",
        "message": "No heritage site with id 999"
    }
    """
    try:
        site = HeritageSite.query.get(heritage_id)
        if not site:
            return jsonify({'error': 'Heritage site not found', 'message': f'No heritage site with id {heritage_id}'}), 404
        return jsonify(site.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@api_bp.route('/artisan/<int:artisan_id>', methods=['GET'])
def api_artisan_detail(artisan_id):
    """
    GET /api/artisan/<artisan_id>
    
    Returns detailed information about a specific artisan.
    """
    try:
        artisan = Artisan.query.get(artisan_id)
        if not artisan:
            return jsonify({'error': 'Artisan not found', 'message': f'No artisan with id {artisan_id}'}), 404
        return jsonify(artisan.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@api_bp.route('/product/<int:product_id>', methods=['GET'])
def api_product_detail(product_id):
    """
    GET /api/product/<product_id>
    
    Returns detailed information about a specific product.
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found', 'message': f'No product with id {product_id}'}), 404
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500


@api_bp.route('/recommendations/<int:user_id>', methods=['GET'])
def api_user_recommendations(user_id):
    """
    GET /api/recommendations/<user_id>
    
    Returns personalized recommendations for a specific user using hybrid approach.
    
    Academic Note - Personalized Recommendations API:
    -----------------------------------------------
    This endpoint exposes the hybrid recommendation engine via REST API.
    It combines content-based, collaborative, and popularity-based filtering
    to provide personalized heritage site recommendations.
    
    Query Parameters:
    - top_n: Number of recommendations (default: 10)
    
    Response Format:
    {
        "user_id": 1,
        "recommendations": [
            {
                "id": 5,
                "name": "Qutub Minar",
                "state": "Delhi",
                "category": "Monument",
                "description": "...",
                "annual_visitors": 3500000
            },
            ...
        ],
        "count": 10
    }
    
    Error Responses:
    - 404: User not found
    - 400: Invalid input parameters
    - 500: Internal server error
    """
    from models import User, Bookmark, SiteView, Review
    
    try:
        # Validate user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': f'No user with id {user_id}'
            }), 404
        
        # Get query parameters
        top_n = int(request.args.get('top_n', 10))
        
        if top_n < 1 or top_n > 50:
            return jsonify({
                'error': 'Invalid input',
                'message': 'top_n must be between 1 and 50'
            }), 400
        
        # Get user's bookmarks and views
        user_bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
        user_views = SiteView.query.filter_by(user_id=user_id).all()
        
        # Convert to site dictionaries
        bookmarked_sites = [bookmark.heritage_site.to_dict() for bookmark in user_bookmarks if bookmark.heritage_site]
        viewed_sites = [view.heritage_site.to_dict() for view in user_views if view.heritage_site]
        
        # Get all sites
        all_sites = HeritageSite.query.all()
        all_sites_data = [site.to_dict() for site in all_sites]
        
        # Get all user bookmarks for collaborative filtering
        all_user_bookmarks_query = db.session.query(
            Bookmark.user_id,
            Bookmark.heritage_id
        ).all()
        
        all_user_bookmarks = {}
        for user_id_item, heritage_id in all_user_bookmarks_query:
            if user_id_item not in all_user_bookmarks:
                all_user_bookmarks[user_id_item] = set()
            all_user_bookmarks[user_id_item].add(heritage_id)
        
        # Get engagement data for all sites
        site_engagement_data = {}
        for site in all_sites:
            site_engagement_data[site.id] = {
                'view_count': site.view_count,
                'bookmark_count': site.bookmark_count,
                'avg_rating': site.avg_rating,
                'review_count': site.review_count
            }
        
        # Get recommendations using hybrid approach
        recommendations = ml_engine.recommend_for_user(
            user_id=user_id,
            user_bookmarks=bookmarked_sites,
            user_views=viewed_sites,
            all_sites=all_sites_data,
            all_user_bookmarks=all_user_bookmarks,
            site_engagement_data=site_engagement_data,
            top_n=top_n
        )
        
        return jsonify({
            'user_id': user_id,
            'recommendations': recommendations,
            'count': len(recommendations)
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': 'Invalid input',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@api_bp.route('/reviews/<int:heritage_id>', methods=['GET'])
def api_heritage_reviews(heritage_id):
    """
    GET /api/reviews/<heritage_id>
    
    Returns all reviews for a specific heritage site.
    
    Academic Note - Review API:
    --------------------------
    This endpoint provides access to user-generated content (reviews and ratings).
    Reviews are ordered by creation date (newest first) for relevance.
    
    Response Format:
    {
        "heritage_id": 1,
        "heritage_name": "Taj Mahal",
        "reviews": [
            {
                "id": 1,
                "user_id": 5,
                "username": "john_doe",
                "rating": 5,
                "comment": "Absolutely stunning!",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00"
            },
            ...
        ],
        "average_rating": 4.5,
        "review_count": 25
    }
    
    Error Responses:
    - 404: Heritage site not found
    - 500: Internal server error
    """
    from models import Review
    
    try:
        # Validate heritage site exists
        heritage_site = HeritageSite.query.get(heritage_id)
        if not heritage_site:
            return jsonify({
                'error': 'Heritage site not found',
                'message': f'No heritage site with id {heritage_id}'
            }), 404
        
        # Get all reviews for this site
        reviews = Review.query.filter_by(
            heritage_id=heritage_id
        ).order_by(Review.created_at.desc()).all()
        
        # Convert to dictionaries with username
        reviews_data = []
        for review in reviews:
            review_dict = review.to_dict()
            review_dict['username'] = review.user.username if review.user else 'Unknown'
            reviews_data.append(review_dict)
        
        return jsonify({
            'heritage_id': heritage_id,
            'heritage_name': heritage_site.name,
            'reviews': reviews_data,
            'average_rating': heritage_site.avg_rating,
            'review_count': heritage_site.review_count
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


# Academic Note on API Design:
# This API follows RESTful principles with clear resource naming and HTTP methods.
# Error handling ensures robust operation with meaningful error messages.
# JSON format provides language-agnostic data interchange.
# Future enhancements could include:
# - Authentication (JWT tokens)
# - Rate limiting (prevent abuse)
# - Pagination (for large datasets)
# - Filtering and sorting (query parameters)
# - HATEOAS (hypermedia links)



# ============================================================================
# HOTEL BOOKING API ENDPOINTS
# ============================================================================

@api_bp.route('/api/hotels/<int:heritage_id>')
def get_hotels(heritage_id):
    """
    Get Hotels API Endpoint
    
    Returns all hotels near a specific heritage site in JSON format.
    
    Academic Note - RESTful API Design:
    ----------------------------------
    This endpoint follows REST principles:
    - Resource-based URL: /api/hotels/{id}
    - HTTP GET method for retrieval
    - JSON response format
    - Proper status codes (200, 404, 500)
    
    Use Cases:
    - Mobile app integration
    - Third-party booking platforms
    - JavaScript-based filtering
    - Data export and analysis
    
    Response Format:
    {
        "heritage_site": "Taj Mahal",
        "hotel_count": 3,
        "hotels": [...]
    }
    """
    from models import Hotel, HeritageSite
    
    try:
        # Verify heritage site exists
        heritage_site = HeritageSite.query.get(heritage_id)
        if not heritage_site:
            return jsonify({
                'error': 'Heritage site not found',
                'message': f'No heritage site with id {heritage_id}'
            }), 404
        
        # Get all hotels for this heritage site
        hotels = Hotel.query.filter_by(heritage_id=heritage_id).all()
        
        return jsonify({
            'heritage_site': heritage_site.name,
            'heritage_id': heritage_id,
            'hotel_count': len(hotels),
            'hotels': [hotel.to_dict() for hotel in hotels]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@api_bp.route('/api/bookings/<int:user_id>')
def get_user_bookings(user_id):
    """
    Get User Bookings API Endpoint
    
    Returns all hotel bookings for a specific user in JSON format.
    
    Academic Note - Authorization in APIs:
    -------------------------------------
    In production, this endpoint should verify:
    1. User is authenticated (JWT token, API key)
    2. User can only access their own bookings (unless admin)
    3. Rate limiting to prevent abuse
    
    For this academic implementation, we provide basic functionality
    without authentication to demonstrate API structure.
    
    Security Considerations:
    - Add authentication middleware
    - Implement role-based access control
    - Add rate limiting
    - Log access attempts
    - Sanitize user input
    
    Response Format:
    {
        "user_id": 1,
        "booking_count": 5,
        "bookings": [...]
    }
    """
    from models import HotelBooking, User
    
    try:
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': f'No user with id {user_id}'
            }), 404
        
        # Get all bookings for this user
        bookings = HotelBooking.query.filter_by(user_id=user_id).order_by(
            HotelBooking.created_at.desc()
        ).all()
        
        return jsonify({
            'user_id': user_id,
            'username': user.username,
            'booking_count': len(bookings),
            'bookings': [booking.to_dict() for booking in bookings]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@api_bp.route('/hotels/all')
def get_all_hotels():
    """
    Get All Hotels API Endpoint
    
    Returns all hotels in the system with heritage site information.
    
    Query Parameters:
    - state: Filter by state
    - min_price: Minimum price per night
    - max_price: Maximum price per night
    - min_rating: Minimum rating
    
    Example:
    /api/hotels/all?state=Uttar Pradesh&min_rating=4.0
    """
    from models import Hotel
    
    try:
        query = Hotel.query
        
        # Apply filters
        state = request.args.get('state')
        if state:
            query = query.filter(Hotel.state == state)
        
        min_price = request.args.get('min_price', type=float)
        if min_price:
            query = query.filter(Hotel.price_per_night >= min_price)
        
        max_price = request.args.get('max_price', type=float)
        if max_price:
            query = query.filter(Hotel.price_per_night <= max_price)
        
        min_rating = request.args.get('min_rating', type=float)
        if min_rating:
            query = query.filter(Hotel.rating >= min_rating)
        
        hotels = query.all()
        
        # Add heritage site information to each hotel
        hotels_data = []
        for hotel in hotels:
            hotel_dict = hotel.to_dict()
            hotel_dict['heritage_name'] = hotel.heritage_site.name if hotel.heritage_site else 'Unknown'
            hotels_data.append(hotel_dict)
        
        return jsonify({
            'hotel_count': len(hotels_data),
            'hotels': hotels_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500
