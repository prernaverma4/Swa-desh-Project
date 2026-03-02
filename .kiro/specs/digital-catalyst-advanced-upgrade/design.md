# Design Document: Digital Catalyst Advanced Upgrade

## Overview

This design document outlines the architecture and implementation approach for upgrading the Digital Catalyst platform into a distinction-level final year project. The upgrade transforms the existing monolithic Flask application into a modular, production-ready system with advanced features including AI-based recommendations, role-based access control, analytics, and comprehensive user engagement tracking.

The design follows Flask best practices using Blueprints for modular organization, implements a hybrid AI recommendation system combining content-based and collaborative filtering approaches, and provides comprehensive security measures suitable for production deployment. The architecture emphasizes maintainability, scalability, and academic rigor with detailed documentation suitable for viva examination.

## Architecture

### High-Level Architecture

The system follows a three-tier architecture:

1. **Presentation Layer**: Flask templates with Jinja2, Bootstrap for responsive UI
2. **Application Layer**: Flask application with Blueprint-based modular organization
3. **Data Layer**: SQLite database with SQLAlchemy ORM

### Blueprint Organization

The application will be refactored into four Flask Blueprints:

1. **auth** (`blueprints/auth.py`): Authentication routes (login, register, logout)
2. **main** (`blueprints/main.py`): Core application routes (dashboard, heritage sites, artisans, products)
3. **api** (`blueprints/api.py`): REST API endpoints returning JSON
4. **dashboard** (`blueprints/dashboard.py`): Analytics and admin dashboard routes

Each Blueprint will be registered with the main Flask app with appropriate URL prefixes:
- auth: `/auth`
- main: `/` (no prefix)
- api: `/api`
- dashboard: `/dashboard`

### Directory Structure

```
digital-catalyst/
├── app.py                          # Main Flask application entry point
├── models.py                       # All database models
├── config.py                       # Configuration settings
├── blueprints/
│   ├── __init__.py
│   ├── auth.py                     # Authentication Blueprint
│   ├── main.py                     # Main application Blueprint
│   ├── api.py                      # REST API Blueprint
│   └── dashboard.py                # Analytics Dashboard Blueprint
├── ml/
│   └── recommendation_engine.py    # AI/ML recommendation logic
├── utils/
│   ├── __init__.py
│   ├── decorators.py               # Role-based access decorators
│   ├── validators.py               # Input validation functions
│   └── file_upload.py              # Image upload utilities
├── static/
│   ├── uploads/                    # User-uploaded images
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── auth/                       # Authentication templates
│   ├── main/                       # Main application templates
│   ├── dashboard/                  # Dashboard templates
│   └── base.html                   # Base template
└── instance/
    └── database.db                 # SQLite database
```

## Components and Interfaces

### 1. Authentication System

**Component**: `blueprints/auth.py`

**Routes**:
- `GET/POST /auth/login`: User login with role selection
- `GET/POST /auth/register`: User registration with role assignment
- `GET /auth/logout`: User logout

**Functions**:
- `login()`: Authenticates user, validates role, creates session
- `register()`: Creates new user with hashed password and assigned role
- `logout()`: Clears session and redirects to landing page

### 2. Role-Based Access Control

**Component**: `utils/decorators.py`

**Decorators**:
- `@role_required('user')`: Requires user role or higher
- `@role_required('manufacturer')`: Requires manufacturer role or higher
- `@role_required('admin')`: Requires admin role

**Implementation**:
```python
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if current_user.role not in roles:
                flash('Access denied', 'danger')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### 3. Bookmark System

**Component**: `blueprints/main.py`

**Routes**:
- `POST /bookmark/<int:heritage_id>`: Create bookmark
- `DELETE /bookmark/<int:heritage_id>`: Remove bookmark
- `GET /my-bookmarks`: View user's bookmarks

**Functions**:
- `add_bookmark(heritage_id)`: Creates bookmark record, prevents duplicates
- `remove_bookmark(heritage_id)`: Deletes bookmark record
- `view_bookmarks()`: Retrieves user's bookmarks ordered by timestamp

### 4. Engagement Tracking

**Component**: `blueprints/main.py`

**Implementation**:
- Automatically track views in `heritage_detail(id)` route
- Create SiteView record on each heritage site page load
- Support both authenticated and anonymous tracking

**Functions**:
- `track_site_view(heritage_id, user_id=None)`: Creates view record with timestamp

### 5. Review and Rating System

**Component**: `blueprints/main.py`

**Routes**:
- `POST /heritage/<int:id>/review`: Submit or update review
- `GET /heritage/<int:id>/reviews`: View all reviews for a site
- `DELETE /review/<int:id>`: Admin delete review

**Functions**:
- `submit_review(heritage_id)`: Creates or updates review, validates rating 1-5
- `get_reviews(heritage_id)`: Retrieves all reviews with user information
- `delete_review(review_id)`: Admin-only review deletion
- `calculate_average_rating(heritage_id)`: Computes average using SQLAlchemy func.avg

### 6. Advanced Search and Filtering

**Component**: `blueprints/main.py`

**Route**: `GET /heritage?search=&state=&category=&rating_min=&rating_max=&sort=`

**Query Building**:
```python
query = HeritageSite.query
if search:
    query = query.filter(HeritageSite.name.ilike(f'%{search}%'))
if state:
    query = query.filter(HeritageSite.state == state)
if category:
    query = query.filter(HeritageSite.category == category)
if rating_min or rating_max:
    # Join with Review, filter by avg rating
    query = query.join(Review).group_by(HeritageSite.id)
    query = query.having(func.avg(Review.rating).between(rating_min, rating_max))
if sort == 'views':
    query = query.outerjoin(SiteView).group_by(HeritageSite.id)
    query = query.order_by(func.count(SiteView.id).desc())
elif sort == 'rating':
    query = query.outerjoin(Review).group_by(HeritageSite.id)
    query = query.order_by(func.avg(Review.rating).desc())
elif sort == 'bookmarks':
    query = query.outerjoin(Bookmark).group_by(HeritageSite.id)
    query = query.order_by(func.count(Bookmark.id).desc())
```

### 7. AI Recommendation Engine

**Component**: `ml/recommendation_engine.py`

**Hybrid Recommendation Algorithm**:

The recommendation system combines three filtering strategies:

1. **Content-Based Filtering**: Recommends sites similar to user's bookmarked/viewed sites based on category and state
2. **Popularity-Based Filtering**: Recommends highly-rated and frequently viewed sites
3. **User-Based Filtering**: Recommends sites bookmarked by users with similar preferences

**Algorithm Pseudocode**:
```
function recommend_for_user(user_id, top_n):
    user_bookmarks = get_user_bookmarks(user_id)
    user_views = get_user_views(user_id)
    
    if user_bookmarks is empty and user_views is empty:
        # Cold start: return popular sites
        return get_top_rated_sites(top_n) + get_most_viewed_sites(top_n)
    
    # Content-based: find similar sites
    preferred_categories = extract_categories(user_bookmarks)
    preferred_states = extract_states(user_bookmarks)
    content_recommendations = find_sites_by_attributes(preferred_categories, preferred_states)
    
    # Popularity-based: weight by engagement
    for site in content_recommendations:
        site.score = (site.avg_rating * 0.4) + (site.view_count * 0.3) + (site.bookmark_count * 0.3)
    
    # User-based: find similar users
    similar_users = find_users_with_similar_bookmarks(user_id)
    collaborative_recommendations = get_bookmarks_from_users(similar_users)
    
    # Combine and rank
    combined = merge_recommendations(content_recommendations, collaborative_recommendations)
    return top_n_by_score(combined, top_n)
```

**Complexity Analysis**:
- Content-based filtering: O(n) where n is number of heritage sites
- Popularity calculation: O(n) for aggregation queries
- User similarity: O(u * b) where u is users and b is average bookmarks per user
- Overall: O(n + u*b) which is acceptable for small to medium datasets

### 8. Analytics Dashboard

**Component**: `blueprints/dashboard.py`

**Route**: `GET /dashboard/analytics` (admin only)

**Metrics Calculated**:
```python
# Total counts
total_users = db.session.query(func.count(User.id)).scalar()
total_manufacturers = db.session.query(func.count(User.id)).filter(User.role == 'manufacturer').scalar()
total_heritage_sites = db.session.query(func.count(HeritageSite.id)).scalar()

# Most viewed site
most_viewed = db.session.query(
    HeritageSite.name, func.count(SiteView.id).label('views')
).join(SiteView).group_by(HeritageSite.id).order_by(desc('views')).first()

# Most bookmarked site
most_bookmarked = db.session.query(
    HeritageSite.name, func.count(Bookmark.id).label('bookmarks')
).join(Bookmark).group_by(HeritageSite.id).order_by(desc('bookmarks')).first()

# Highest rated site
highest_rated = db.session.query(
    HeritageSite.name, func.avg(Review.rating).label('avg_rating')
).join(Review).group_by(HeritageSite.id).order_by(desc('avg_rating')).first()

# Most active state
most_active_state = db.session.query(
    HeritageSite.state, func.count(HeritageSite.id).label('count')
).group_by(HeritageSite.state).order_by(desc('count')).first()
```

### 9. REST API Layer

**Component**: `blueprints/api.py`

**Endpoints**:

1. `GET /api/heritage`: Returns all heritage sites as JSON
   - Response: `[{id, name, state, category, description, image_url, annual_visitors, avg_rating, view_count, bookmark_count}, ...]`

2. `GET /api/artisans`: Returns all artisans as JSON
   - Response: `[{id, name, craft, state, product_price, contact, description, image_url}, ...]`

3. `GET /api/recommendations/<user_id>`: Returns personalized recommendations
   - Response: `{user_id, recommendations: [{id, name, score, reason}, ...]}`

4. `GET /api/reviews/<heritage_id>`: Returns all reviews for a heritage site
   - Response: `{heritage_id, avg_rating, review_count, reviews: [{id, user, rating, comment, created_at}, ...]}`

**Error Handling**:
- 400 Bad Request: Invalid input parameters
- 404 Not Found: Resource does not exist
- 500 Internal Server Error: Server-side error with logged details

### 10. Image Upload System

**Component**: `utils/file_upload.py`

**Functions**:
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_image(file, upload_folder='static/uploads'):
    if not file or not allowed_file(file.filename):
        raise ValueError('Invalid file type')
    
    if file.content_length > MAX_FILE_SIZE:
        raise ValueError('File too large')
    
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{timestamp}_{filename}"
    filepath = os.path.join(upload_folder, unique_filename)
    
    file.save(filepath)
    return filepath
```

**Integration**:
- Add file upload fields to heritage site and product forms
- Validate and save images using `save_uploaded_image()`
- Store relative path in database `image_url` field
- Display images using stored path or placeholder

### 11. Security Components

**Component**: `utils/validators.py`

**Input Validation**:
```python
def validate_rating(rating):
    try:
        rating = int(rating)
        if 1 <= rating <= 5:
            return rating
        raise ValueError('Rating must be between 1 and 5')
    except (ValueError, TypeError):
        raise ValueError('Invalid rating')

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError('Invalid email format')
    return email

def sanitize_input(text, max_length=500):
    if not text:
        return ''
    text = text.strip()
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    return text[:max_length]
```

**CSRF Protection**:
- Use Flask-WTF for form handling with built-in CSRF protection
- Add CSRF tokens to all forms
- Validate tokens on POST requests

**Password Security**:
- Hash passwords using `werkzeug.security.generate_password_hash()`
- Use strong hashing algorithm (pbkdf2:sha256)
- Never store plaintext passwords

## Data Models

### User Model (Extended)

```python
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    role = db.Column(db.String(20), default='user', nullable=False)  # user, manufacturer, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    site_views = db.relationship('SiteView', backref='user', lazy='dynamic', cascade='all, delete-orphan')
```

### Bookmark Model (New)

```python
class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    heritage_id = db.Column(db.Integer, db.ForeignKey('heritage_sites.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Unique constraint: one bookmark per user per site
    __table_args__ = (db.UniqueConstraint('user_id', 'heritage_id', name='unique_user_heritage_bookmark'),)
```

### SiteView Model (New)

```python
class SiteView(db.Model):
    __tablename__ = 'site_views'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    heritage_id = db.Column(db.Integer, db.ForeignKey('heritage_sites.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
```

### Review Model (New)

```python
class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    heritage_id = db.Column(db.Integer, db.ForeignKey('heritage_sites.id', ondelete='CASCADE'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint: one review per user per site
    __table_args__ = (
        db.UniqueConstraint('user_id', 'heritage_id', name='unique_user_heritage_review'),
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range')
    )
```

### HeritageSite Model (Extended)

```python
class HeritageSite(db.Model):
    __tablename__ = 'heritage_sites'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    state = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    annual_visitors = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookmarks = db.relationship('Bookmark', backref='heritage_site', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='heritage_site', lazy='dynamic', cascade='all, delete-orphan')
    site_views = db.relationship('SiteView', backref='heritage_site', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def avg_rating(self):
        result = db.session.query(func.avg(Review.rating)).filter(Review.heritage_id == self.id).scalar()
        return round(result, 2) if result else 0.0
    
    @property
    def review_count(self):
        return self.reviews.count()
    
    @property
    def view_count(self):
        return self.site_views.count()
    
    @property
    def bookmark_count(self):
        return self.bookmarks.count()
```

### Entity Relationship Diagram

```
User (1) ----< (M) Bookmark >---- (M) HeritageSite (1)
User (1) ----< (M) Review >---- (M) HeritageSite (1)
User (1) ----< (M) SiteView >---- (M) HeritageSite (1)
User (1) ----< (M) Order >---- (M) Product (1)
Artisan (1) ----< (M) Product
```

**Cascade Delete Rules**:
- When User is deleted: Delete all Bookmarks, Reviews, Orders (SET NULL on SiteViews)
- When HeritageSite is deleted: Delete all Bookmarks, Reviews, SiteViews
- When Artisan is deleted: Delete all Products
- When Product is deleted: Keep Orders (for historical records)

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After analyzing all acceptance criteria, I've identified the following testable properties and eliminated redundancy:

**Redundancies Identified:**
- 11.5 (prevent duplicate reviews) is identical to 5.3 - will use 5.3 only
- 11.6 (file type validation) is identical to 10.1 - will use 10.1 only
- Several properties about "most viewed/bookmarked/rated" can be combined into a single property about aggregation correctness
- Sort order properties (6.6, 6.7, 6.8) can be combined into one property about sort correctness
- Filter properties (6.2, 6.3, 6.4) follow the same pattern and can be combined

**Properties to Implement:**
1. Cascade delete behavior (1.4)
2. Role-based access control (2.2, 2.3, 2.4, 2.6 combined)
3. Bookmark operations (3.2, 3.3, 3.4, 3.5 combined)
4. Bookmark influence on recommendations (3.6)
5. View tracking (4.2, 4.4 combined)
6. Review validation and uniqueness (5.2, 5.3, 5.4 combined)
7. Rating calculation correctness (5.5, 5.7 combined)
8. Search and filter correctness (6.1, 6.2, 6.3, 6.4, 6.5 combined)
9. Sort order correctness (6.6, 6.7, 6.8 combined)
10. Recommendation personalization (7.1, 7.2 combined)
11. Analytics aggregation correctness (8.1, 8.2, 8.3, 8.4, 8.5 combined)
12. API response format and status codes (9.5, 9.6, 9.7 combined)
13. Image upload validation (10.1, 10.4, 10.5, 10.6 combined)
14. Image display fallback (10.7)
15. Password hashing (11.1)

### Correctness Properties

Property 1: Cascade Delete Integrity
*For any* user with associated bookmarks, reviews, and site views, when the user is deleted, all associated bookmarks and reviews should be deleted, and all site views should have their user_id set to null.
**Validates: Requirements 1.4**

Property 2: Role-Based Access Control
*For any* user and protected route, when the user attempts to access the route, access should be granted if and only if the user's role has the required permissions for that route.
**Validates: Requirements 2.2, 2.3, 2.4, 2.6**

Property 3: Bookmark Operations Consistency
*For any* user and heritage site, the following should hold:
- Creating a bookmark should result in exactly one bookmark record
- Attempting to create a duplicate bookmark should not create additional records
- Viewing bookmarks should return all bookmarked sites ordered by timestamp descending
- Deleting a bookmark should remove the record completely
**Validates: Requirements 3.2, 3.3, 3.4, 3.5**

Property 4: Bookmark-Influenced Recommendations
*For any* user with bookmarks, the recommended heritage sites should include sites that share categories or states with the user's bookmarked sites.
**Validates: Requirements 3.6**

Property 5: View Tracking Accuracy
*For any* heritage site, when the site detail page is viewed, a site view record should be created, and the site's view count should increase by one.
**Validates: Requirements 4.2, 4.4**

Property 6: Review Validation and Uniqueness
*For any* review submission, the following should hold:
- Ratings outside the range [1, 5] should be rejected
- Each user-heritage combination should have at most one review
- Submitting a review for an existing user-heritage combination should update the existing review
**Validates: Requirements 5.2, 5.3, 5.4**

Property 7: Rating Calculation Correctness
*For any* heritage site with reviews, the average rating should equal the sum of all ratings divided by the number of reviews, and deleting a review should update the average accordingly.
**Validates: Requirements 5.5, 5.7**

Property 8: Search and Filter Correctness
*For any* combination of search term, state filter, category filter, and rating range filter, all returned heritage sites should match all specified criteria.
**Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**

Property 9: Sort Order Correctness
*For any* sort criterion (views, rating, bookmarks), the returned heritage sites should be ordered such that each site's sort value is greater than or equal to the next site's sort value.
**Validates: Requirements 6.6, 6.7, 6.8**

Property 10: Recommendation Personalization
*For any* user with bookmark or view history, the recommended sites should be more similar to the user's history than a random selection of sites.
**Validates: Requirements 7.1, 7.2**

Property 11: Analytics Aggregation Correctness
*For any* system state, the analytics dashboard should display:
- Total counts that match the actual number of records
- "Most viewed/bookmarked/rated" sites that have the maximum values for their respective metrics
- "Most active state" that has the maximum number of heritage sites
**Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5**

Property 12: API Response Correctness
*For any* API request, the response should have:
- Status code 200 and valid JSON for successful requests
- Status code 400 and error message for invalid input
- Status code 404 and error message for missing resources
**Validates: Requirements 9.5, 9.6, 9.7**

Property 13: Image Upload Validation
*For any* file upload attempt, the following should hold:
- Files with disallowed extensions should be rejected
- Files exceeding size limit should be rejected
- Valid files should be saved and their paths stored in the database
- Invalid uploads should return error messages
**Validates: Requirements 10.1, 10.4, 10.5, 10.6**

Property 14: Image Display Fallback
*For any* heritage site or product, when displaying an image, if the image_url is null or the file doesn't exist, a placeholder image should be displayed instead.
**Validates: Requirements 10.7**

Property 15: Password Hashing Security
*For any* user registration or password change, the password stored in the database should be a hash, not the plaintext password, and the hash should be verifiable using the check_password_hash function.
**Validates: Requirements 11.1**

## Error Handling

### Input Validation Errors

1. **Invalid Rating**: Return 400 with message "Rating must be between 1 and 5"
2. **Invalid Email**: Return 400 with message "Invalid email format"
3. **Invalid File Type**: Return 400 with message "Only jpg, jpeg, png, gif files are allowed"
4. **File Too Large**: Return 400 with message "File size exceeds 5MB limit"
5. **Missing Required Fields**: Return 400 with message "Required field missing: {field_name}"

### Authentication Errors

1. **Not Authenticated**: Redirect to login page with message "Please log in to continue"
2. **Insufficient Permissions**: Redirect to dashboard with message "Access denied: insufficient permissions"
3. **Invalid Credentials**: Return to login with message "Invalid username or password"

### Database Errors

1. **Duplicate Entry**: Return 400 with message "Record already exists"
2. **Foreign Key Violation**: Return 400 with message "Referenced record does not exist"
3. **Constraint Violation**: Return 400 with message "Data violates database constraints"

### API Errors

1. **Resource Not Found**: Return 404 with JSON `{"error": "Resource not found"}`
2. **Invalid Request**: Return 400 with JSON `{"error": "Invalid request parameters"}`
3. **Server Error**: Return 500 with JSON `{"error": "Internal server error"}` and log details

### File Upload Errors

1. **No File Selected**: Return 400 with message "No file selected"
2. **Invalid File Type**: Return 400 with message "Invalid file type"
3. **File Too Large**: Return 400 with message "File too large"
4. **Upload Failed**: Return 500 with message "File upload failed" and log error

## Testing Strategy

### Dual Testing Approach

The testing strategy employs both unit tests and property-based tests to ensure comprehensive coverage:

**Unit Tests**: Focus on specific examples, edge cases, and integration points
- Test specific user flows (registration, login, bookmark creation)
- Test edge cases (empty inputs, boundary values, null handling)
- Test error conditions (invalid credentials, missing resources)
- Test integration between components (recommendation engine with database)

**Property-Based Tests**: Verify universal properties across all inputs
- Test with randomized data to catch unexpected edge cases
- Verify invariants hold across all valid inputs
- Test with minimum 100 iterations per property
- Each property test references its design document property

### Property-Based Testing Configuration

**Library Selection**: Use `hypothesis` for Python property-based testing

**Test Configuration**:
```python
from hypothesis import given, settings, strategies as st

@settings(max_examples=100)
@given(
    user_id=st.integers(min_value=1, max_value=1000),
    heritage_id=st.integers(min_value=1, max_value=1000)
)
def test_bookmark_uniqueness(user_id, heritage_id):
    """
    Feature: digital-catalyst-advanced-upgrade, Property 3: Bookmark Operations Consistency
    Validates: Requirements 3.2, 3.3, 3.4, 3.5
    """
    # Test implementation
    pass
```

**Test Organization**:
- `tests/unit/` - Unit tests for specific functionality
- `tests/property/` - Property-based tests for universal properties
- `tests/integration/` - Integration tests for component interaction

### Test Coverage Requirements

1. **Authentication**: Test all role-based access scenarios
2. **Bookmarks**: Test CRUD operations and uniqueness constraints
3. **Reviews**: Test rating validation, uniqueness, and average calculation
4. **Search/Filter**: Test all filter combinations and sort orders
5. **Recommendations**: Test personalization and cold start scenarios
6. **Analytics**: Test aggregation correctness with various data sets
7. **API**: Test all endpoints with valid and invalid inputs
8. **Image Upload**: Test validation, storage, and display
9. **Security**: Test password hashing, input sanitization, access control

### Testing Best Practices

1. Use database transactions and rollback for test isolation
2. Create test fixtures for common data scenarios
3. Mock external dependencies (file system, network)
4. Test both success and failure paths
5. Verify error messages are user-friendly
6. Test cascade deletes and referential integrity
7. Verify performance with realistic data volumes

## Limitations and Trade-offs

### Current Limitations

1. **Scalability**: SQLite database suitable for development but not production scale
2. **Recommendation Algorithm**: Simple hybrid approach without machine learning models
3. **Image Storage**: Local file system storage not suitable for distributed deployment
4. **Search Performance**: Full-text search limited without dedicated search engine
5. **Real-time Updates**: No WebSocket support for real-time notifications
6. **Caching**: No caching layer for frequently accessed data
7. **Rate Limiting**: No API rate limiting to prevent abuse

### Design Trade-offs

1. **Blueprint Organization**: Chose simplicity over deep nesting for maintainability
2. **ORM vs Raw SQL**: Used SQLAlchemy ORM for safety over raw SQL performance
3. **Synchronous vs Async**: Chose synchronous Flask for simplicity over async performance
4. **Monolithic vs Microservices**: Chose monolithic for academic project simplicity
5. **Client-side vs Server-side Rendering**: Chose server-side for security and simplicity

### Future Enhancements

1. **Database Migration**: Move to PostgreSQL for production deployment
2. **Advanced ML**: Implement collaborative filtering with matrix factorization
3. **Cloud Storage**: Integrate AWS S3 or similar for image storage
4. **Search Engine**: Integrate Elasticsearch for advanced search capabilities
5. **Real-time Features**: Add WebSocket support for notifications
6. **Caching Layer**: Implement Redis for caching frequently accessed data
7. **API Security**: Add JWT authentication and rate limiting
8. **Mobile App**: Develop React Native mobile application
9. **Payment Integration**: Add Razorpay/Stripe for product purchases
10. **Analytics Dashboard**: Add Chart.js visualizations for trends

## Academic Documentation

### Abstract

The Digital Catalyst platform is an AI-driven web application designed to promote Indian economic growth through heritage preservation and artisan marketplace integration. The system implements a hybrid recommendation engine combining content-based and popularity-based filtering to personalize user experiences. Built using Flask with modular Blueprint architecture, the platform features comprehensive role-based access control, advanced search and filtering capabilities, real-time engagement tracking, and RESTful API endpoints. The system demonstrates distinction-level software engineering practices including proper database normalization, cascade delete handling, input validation, security measures, and comprehensive testing strategies. This project showcases the integration of AI/ML techniques with web development, database design, and software architecture principles suitable for final year academic evaluation.

### System Architecture Overview

The Digital Catalyst platform follows a layered architecture pattern:

**Presentation Layer**: 
- Jinja2 templates with Bootstrap for responsive design
- Client-side JavaScript for interactive features
- RESTful API endpoints for programmatic access

**Application Layer**:
- Flask web framework with Blueprint modular organization
- Four Blueprints: auth, main, api, dashboard
- Custom decorators for role-based access control
- Utility modules for validation, file upload, and security

**Business Logic Layer**:
- Recommendation engine implementing hybrid filtering algorithms
- Analytics engine for aggregation and reporting
- Engagement tracking for user behavior analysis

**Data Layer**:
- SQLAlchemy ORM for database abstraction
- SQLite database with proper relationships and constraints
- Cascade delete rules for referential integrity

### Database Schema Explanation

**Core Entities**:
1. **User**: Stores authentication credentials and role information
2. **HeritageSite**: Represents cultural and historical locations
3. **Artisan**: Represents craftspeople and MSME businesses
4. **Product**: Items created by artisans for sale

**Engagement Entities**:
1. **Bookmark**: Many-to-many relationship between users and heritage sites
2. **Review**: User ratings and comments for heritage sites
3. **SiteView**: Tracking table for page views (supports anonymous users)
4. **Order**: Purchase records for artisan products

**Relationships**:
- User → Bookmark (1:M with cascade delete)
- User → Review (1:M with cascade delete)
- User → SiteView (1:M with SET NULL on delete)
- User → Order (1:M)
- HeritageSite → Bookmark (1:M with cascade delete)
- HeritageSite → Review (1:M with cascade delete)
- HeritageSite → SiteView (1:M with cascade delete)
- Artisan → Product (1:M with cascade delete)
- Product → Order (1:M)

**Constraints**:
- Unique constraint on (user_id, heritage_id) for Bookmark
- Unique constraint on (user_id, heritage_id) for Review
- Check constraint on Review.rating (1 ≤ rating ≤ 5)
- Indexes on foreign keys and frequently queried columns

### Recommendation Algorithm Explanation

**Algorithm Type**: Hybrid Recommendation System

**Components**:

1. **Content-Based Filtering**:
   - Analyzes user's bookmark and view history
   - Extracts preferred categories and states
   - Finds heritage sites matching these preferences
   - Time Complexity: O(n) where n is number of heritage sites
   - Space Complexity: O(k) where k is number of user preferences

2. **Popularity-Based Filtering**:
   - Calculates engagement score for each site
   - Score = (avg_rating × 0.4) + (view_count × 0.3) + (bookmark_count × 0.3)
   - Weights tuned based on importance of each metric
   - Time Complexity: O(n) for score calculation
   - Space Complexity: O(n) for storing scores

3. **Collaborative Filtering (User-Based)**:
   - Finds users with similar bookmark patterns
   - Recommends sites bookmarked by similar users
   - Uses Jaccard similarity for user comparison
   - Time Complexity: O(u × b) where u is users, b is avg bookmarks
   - Space Complexity: O(u) for similarity scores

4. **Cold Start Handling**:
   - For new users without history
   - Returns top-rated sites (avg_rating > 4.0)
   - Combined with most viewed sites
   - Ensures new users see quality content immediately

**Overall Complexity**:
- Time: O(n + u×b) which is acceptable for small to medium datasets
- Space: O(n + u) for storing recommendations and user similarities

**Viva Explanation**:
"The recommendation system uses a hybrid approach combining three strategies. First, content-based filtering analyzes what the user has bookmarked or viewed to find similar heritage sites by category and state. Second, popularity-based filtering ensures we recommend high-quality sites that other users have engaged with. Third, collaborative filtering finds users with similar tastes and recommends sites they've bookmarked. For new users without history, we use a cold start strategy showing top-rated and popular sites. The algorithm runs in linear time relative to the number of sites, making it efficient for our use case."

### Conclusion

The Digital Catalyst Advanced Upgrade successfully transforms a basic heritage preservation platform into a distinction-level final year project. The implementation demonstrates mastery of multiple computer science domains including web development, database design, AI/ML algorithms, software architecture, and security engineering.

**Key Achievements**:
1. Modular architecture using Flask Blueprints for maintainability
2. Comprehensive role-based access control with three distinct user roles
3. Hybrid AI recommendation system combining multiple filtering strategies
4. Advanced search and filtering with optimized database queries
5. Real-time engagement tracking for user behavior analysis
6. RESTful API layer for programmatic access
7. Production-ready security measures including password hashing and input validation
8. Comprehensive testing strategy with both unit and property-based tests

**Learning Outcomes**:
1. Understanding of web application architecture and design patterns
2. Practical experience with ORM and database relationship management
3. Implementation of AI/ML algorithms for personalization
4. Security best practices for web applications
5. API design and RESTful principles
6. Software testing methodologies and quality assurance
7. Academic documentation and technical communication skills

**Project Impact**:
This project demonstrates the potential of technology to preserve cultural heritage while supporting local artisans and MSMEs. The platform provides a scalable foundation for promoting Indian economic growth through digital transformation, showcasing how software engineering can address real-world social and economic challenges.

The comprehensive feature set, clean architecture, and academic rigor make this project suitable for distinction-level evaluation and provide a strong foundation for future enhancements and production deployment.
