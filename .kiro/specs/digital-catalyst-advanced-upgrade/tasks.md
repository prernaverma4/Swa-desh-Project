# Implementation Plan: Digital Catalyst Advanced Upgrade

## Overview

This implementation plan breaks down the Digital Catalyst platform upgrade into discrete, manageable tasks. The approach follows a modular strategy: first refactoring the architecture into Blueprints, then adding new database models and relationships, implementing core features (bookmarks, reviews, engagement tracking), enhancing search and recommendations, adding analytics and API layers, implementing security measures, and finally creating comprehensive documentation.

Each task builds incrementally on previous work, with checkpoints to ensure stability. Testing tasks are marked as optional (*) to allow for faster MVP delivery while maintaining the option for comprehensive test coverage.

## Tasks

- [x] 1. Architecture Refactoring: Create Blueprint Structure
  - Create `blueprints/` directory with `__init__.py`
  - Create `blueprints/auth.py` for authentication routes (login, register, logout)
  - Create `blueprints/main.py` for core application routes (dashboard, heritage, artisans, products)
  - Create `blueprints/api.py` for REST API endpoints
  - Create `blueprints/dashboard.py` for analytics dashboard
  - Move existing routes from `app.py` to appropriate Blueprints
  - Register all Blueprints in `app.py` with appropriate URL prefixes
  - Add academic comments explaining Blueprint organization and modular architecture
  - _Requirements: 1.1_

- [x] 2. Create Utility Modules
  - [x] 2.1 Create `utils/` directory with `__init__.py`
    - Create `utils/decorators.py` for role-based access control decorators
    - Implement `@role_required('user')`, `@role_required('manufacturer')`, `@role_required('admin')` decorators
    - Add academic comments explaining decorator pattern and access control logic
    - _Requirements: 2.5_
  
  - [x] 2.2 Create `utils/validators.py` for input validation
    - Implement `validate_rating(rating)` function (1-5 range check)
    - Implement `validate_email(email)` function with regex pattern
    - Implement `sanitize_input(text, max_length)` function to remove HTML tags
    - Add academic comments explaining validation importance
    - _Requirements: 11.3_
  
  - [x] 2.3 Create `utils/file_upload.py` for image upload handling
    - Define `ALLOWED_EXTENSIONS` constant for image types
    - Implement `allowed_file(filename)` function
    - Implement `save_uploaded_image(file, upload_folder)` function with secure_filename
    - Add file size validation (5MB limit)
    - Add academic comments explaining secure file handling
    - _Requirements: 10.1, 10.2, 10.6_

- [x] 3. Extend Database Models
  - [x] 3.1 Add new models to `models.py`
    - Create `Bookmark` model with user_id, heritage_id, created_at fields
    - Add unique constraint on (user_id, heritage_id)
    - Create `SiteView` model with user_id (nullable), heritage_id, created_at fields
    - Create `Review` model with user_id, heritage_id, rating, comment, created_at, updated_at fields
    - Add unique constraint on (user_id, heritage_id) for Review
    - Add check constraint on rating (1 ≤ rating ≤ 5)
    - Add indexes on foreign keys and timestamp fields
    - Add academic comments explaining normalization and constraints
    - _Requirements: 3.1, 4.1, 5.1_
  
  - [x] 3.2 Add relationships to existing models
    - Add `bookmarks` relationship to User model with cascade delete
    - Add `reviews` relationship to User model with cascade delete
    - Add `site_views` relationship to User model with SET NULL on delete
    - Add `bookmarks` relationship to HeritageSite model with cascade delete
    - Add `reviews` relationship to HeritageSite model with cascade delete
    - Add `site_views` relationship to HeritageSite model with cascade delete
    - Add academic comments explaining cascade delete rules and referential integrity
    - _Requirements: 1.4_
  
  - [x] 3.3 Add computed properties to HeritageSite model
    - Implement `avg_rating` property using SQLAlchemy func.avg
    - Implement `review_count` property
    - Implement `view_count` property
    - Implement `bookmark_count` property
    - Add academic comments explaining lazy evaluation and query optimization
    - _Requirements: 5.5, 4.4_
  
  - [ ]* 3.4 Write property test for cascade delete behavior
    - **Property 1: Cascade Delete Integrity**
    - **Validates: Requirements 1.4**
    - Test that deleting a user cascades to bookmarks and reviews
    - Test that deleting a user sets site_views.user_id to null
    - Test that deleting a heritage site cascades to bookmarks, reviews, and site_views

- [x] 4. Implement Role-Based Access Control
  - [x] 4.1 Update User model with role field
    - Ensure `role` field exists with default 'user'
    - Add helper methods: `is_user()`, `is_manufacturer()`, `is_admin()`
    - Update registration route to accept role parameter
    - Add academic comments explaining role-based security model
    - _Requirements: 2.1_
  
  - [x] 4.2 Apply role decorators to routes
    - Apply `@role_required('user')` to user-specific routes (bookmarks, reviews)
    - Apply `@role_required('manufacturer')` to product management routes
    - Apply `@role_required('admin')` to admin routes (analytics, user management)
    - Add redirect logic for unauthorized access attempts
    - Add academic comments explaining authorization vs authentication
    - _Requirements: 2.2, 2.3, 2.4, 2.6_
  
  - [ ]* 4.3 Write property test for role-based access control
    - **Property 2: Role-Based Access Control**
    - **Validates: Requirements 2.2, 2.3, 2.4, 2.6**
    - Test that users with correct roles can access protected routes
    - Test that users with incorrect roles are denied access
    - Test that unauthenticated users are redirected to login

- [ ] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Implement Bookmark System
  - [x] 6.1 Create bookmark routes in `blueprints/main.py`
    - Implement `POST /bookmark/<int:heritage_id>` to create bookmark
    - Implement `DELETE /bookmark/<int:heritage_id>` to remove bookmark
    - Implement `GET /my-bookmarks` to view user's bookmarks
    - Add duplicate prevention logic (check existing before creating)
    - Add flash messages for user feedback
    - Add academic comments explaining RESTful design
    - _Requirements: 3.2, 3.4, 3.5_
  
  - [x] 6.2 Create bookmark UI templates
    - Add bookmark button to heritage site detail page
    - Create `my_bookmarks.html` template to display bookmarked sites
    - Add bookmark count badge to navigation
    - Style with Bootstrap for responsive design
    - _Requirements: 3.3_
  
  - [ ]* 6.3 Write property test for bookmark operations
    - **Property 3: Bookmark Operations Consistency**
    - **Validates: Requirements 3.2, 3.3, 3.4, 3.5**
    - Test that creating a bookmark creates exactly one record
    - Test that duplicate bookmarks are prevented
    - Test that bookmarks are ordered by timestamp descending
    - Test that deleting a bookmark removes the record

- [x] 7. Implement Engagement Tracking System
  - [x] 7.1 Add view tracking to heritage detail route
    - Modify `heritage_detail(id)` route to create SiteView record
    - Support both authenticated and anonymous tracking
    - Use current_user.id if authenticated, else null
    - Add academic comments explaining analytics tracking
    - _Requirements: 4.2, 4.3_
  
  - [x] 7.2 Create view count aggregation queries
    - Implement helper function `get_most_viewed_sites(top_n)` using func.count
    - Add view count display to heritage site cards
    - Add academic comments explaining aggregation queries
    - _Requirements: 4.4_
  
  - [ ]* 7.3 Write property test for view tracking
    - **Property 5: View Tracking Accuracy**
    - **Validates: Requirements 4.2, 4.4**
    - Test that viewing a site creates a view record
    - Test that view count increases correctly
    - Test that anonymous views are tracked with null user_id

- [x] 8. Implement Review and Rating System
  - [x] 8.1 Create review routes in `blueprints/main.py`
    - Implement `POST /heritage/<int:id>/review` to submit/update review
    - Implement `GET /heritage/<int:id>/reviews` to view all reviews
    - Implement `DELETE /review/<int:id>` for admin review deletion
    - Add rating validation (1-5 range)
    - Add duplicate check (update existing if found)
    - Add academic comments explaining CRUD operations
    - _Requirements: 5.2, 5.3, 5.4, 5.7_
  
  - [x] 8.2 Create review UI templates
    - Add review form to heritage site detail page
    - Display existing reviews with star ratings
    - Show average rating and review count
    - Add edit/delete buttons for user's own reviews
    - Style with Bootstrap star rating component
    - _Requirements: 5.6_
  
  - [ ]* 8.3 Write property test for review validation
    - **Property 6: Review Validation and Uniqueness**
    - **Validates: Requirements 5.2, 5.3, 5.4**
    - Test that invalid ratings are rejected
    - Test that duplicate reviews are prevented
    - Test that submitting twice updates the existing review
  
  - [ ]* 8.4 Write property test for rating calculation
    - **Property 7: Rating Calculation Correctness**
    - **Validates: Requirements 5.5, 5.7**
    - Test that average rating equals sum/count
    - Test that deleting a review updates the average correctly

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 10. Implement Advanced Search and Filtering
  - [x] 10.1 Enhance heritage list route with filters
    - Add query parameters: search, state, category, rating_min, rating_max, sort
    - Implement name search with case-insensitive ILIKE
    - Implement state filter with exact match
    - Implement category filter with exact match
    - Implement rating range filter with join and having clause
    - Add academic comments explaining query building and optimization
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [x] 10.2 Implement sort functionality
    - Add sort by view count (join SiteView, group by, order by count desc)
    - Add sort by average rating (join Review, group by, order by avg desc)
    - Add sort by bookmark count (join Bookmark, group by, order by count desc)
    - Add academic comments explaining join strategies
    - _Requirements: 6.6, 6.7, 6.8_
  
  - [x] 10.3 Create filter UI in heritage template
    - Add search input field
    - Add state dropdown filter
    - Add category dropdown filter
    - Add rating range slider
    - Add sort dropdown (most viewed, highest rated, most bookmarked)
    - Style with Bootstrap form components
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  
  - [ ]* 10.4 Write property test for search and filter correctness
    - **Property 8: Search and Filter Correctness**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**
    - Test that all returned sites match all specified filters
    - Test filter combinations work correctly
  
  - [ ]* 10.5 Write property test for sort order correctness
    - **Property 9: Sort Order Correctness**
    - **Validates: Requirements 6.6, 6.7, 6.8**
    - Test that results are ordered correctly by each sort criterion

- [x] 11. Enhance AI Recommendation Engine
  - [x] 11.1 Implement content-based filtering
    - Add `get_user_preferred_categories(user_id)` function
    - Add `get_user_preferred_states(user_id)` function
    - Add `find_sites_by_attributes(categories, states)` function
    - Add academic comments explaining content-based filtering algorithm
    - _Requirements: 7.1, 7.2_
  
  - [x] 11.2 Implement popularity-based scoring
    - Add `calculate_engagement_score(site)` function
    - Use formula: (avg_rating × 0.4) + (view_count × 0.3) + (bookmark_count × 0.3)
    - Add academic comments explaining weighted scoring
    - _Requirements: 7.1, 7.2_
  
  - [x] 11.3 Implement user-based collaborative filtering
    - Add `find_similar_users(user_id)` function using Jaccard similarity
    - Add `get_recommendations_from_similar_users(similar_users)` function
    - Add academic comments explaining collaborative filtering
    - _Requirements: 7.1, 7.2_
  
  - [x] 11.4 Implement hybrid recommendation function
    - Add `recommend_for_user(user_id, top_n)` function
    - Combine content-based, popularity-based, and collaborative filtering
    - Implement cold start handling (top-rated + most viewed for new users)
    - Add academic comments explaining hybrid approach and complexity analysis
    - Add viva-ready documentation explaining algorithm choices
    - _Requirements: 3.6, 4.5, 7.1, 7.2, 7.3_
  
  - [ ]* 11.5 Write property test for bookmark-influenced recommendations
    - **Property 4: Bookmark-Influenced Recommendations**
    - **Validates: Requirements 3.6**
    - Test that recommendations include sites similar to bookmarked sites
  
  - [ ]* 11.6 Write property test for recommendation personalization
    - **Property 10: Recommendation Personalization**
    - **Validates: Requirements 7.1, 7.2**
    - Test that personalized recommendations are more similar to user history than random

- [x] 12. Implement Analytics Dashboard
  - [x] 12.1 Create analytics routes in `blueprints/dashboard.py`
    - Implement `GET /dashboard/analytics` route (admin only)
    - Calculate total users, manufacturers, heritage sites using func.count
    - Calculate most viewed site using join, group by, order by
    - Calculate most bookmarked site using join, group by, order by
    - Calculate highest rated site using join, group by, order by avg
    - Calculate most active state using group by, order by count
    - Add academic comments explaining aggregation queries and group by
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.7_
  
  - [x] 12.2 Create analytics dashboard template
    - Create `templates/dashboard/analytics.html`
    - Display total counts in card components
    - Display top sites in table format
    - Display most active state
    - Style with Bootstrap cards and tables
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  
  - [x] 12.3 Add access control to analytics dashboard
    - Apply `@role_required('admin')` decorator to analytics route
    - Add redirect for non-admin users
    - Add flash message for access denied
    - _Requirements: 8.8_
  
  - [ ]* 12.4 Write property test for analytics aggregation correctness
    - **Property 11: Analytics Aggregation Correctness**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5**
    - Test that total counts match actual record counts
    - Test that "most viewed/bookmarked/rated" sites have maximum values
    - Test that "most active state" has maximum site count

- [ ] 13. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 14. Implement REST API Layer
  - [x] 14.1 Create API endpoints in `blueprints/api.py`
    - Implement `GET /api/heritage` returning all heritage sites as JSON
    - Implement `GET /api/artisans` returning all artisans as JSON
    - Implement `GET /api/recommendations/<user_id>` returning personalized recommendations
    - Implement `GET /api/reviews/<heritage_id>` returning all reviews for a site
    - Add academic comments explaining RESTful API design
    - _Requirements: 9.1, 9.2, 9.3, 9.4_
  
  - [x] 14.2 Add error handling to API endpoints
    - Return 200 with JSON for successful requests
    - Return 400 with error message for invalid input
    - Return 404 with error message for missing resources
    - Return 500 with error message for server errors
    - Add try-except blocks around database queries
    - Add academic comments explaining HTTP status codes
    - _Requirements: 9.5, 9.6, 9.7, 9.8_
  
  - [ ]* 14.3 Write property test for API response correctness
    - **Property 12: API Response Correctness**
    - **Validates: Requirements 9.5, 9.6, 9.7**
    - Test that successful requests return 200 and valid JSON
    - Test that invalid input returns 400 with error message
    - Test that missing resources return 404 with error message

- [x] 15. Implement Image Upload System
  - [x] 15.1 Add image upload to heritage site forms
    - Add file input field to add_heritage.html and edit_heritage.html
    - Modify add_heritage and edit_heritage routes to handle file uploads
    - Use `save_uploaded_image()` utility function
    - Store file path in heritage_site.image_url field
    - Add validation error handling and flash messages
    - _Requirements: 10.3, 10.4_
  
  - [x] 15.2 Add image upload to product forms
    - Add file input field to add_product.html and edit_product.html
    - Modify add_product and edit_product routes to handle file uploads
    - Use `save_uploaded_image()` utility function
    - Store file path in product.image_url field
    - Add validation error handling and flash messages
    - _Requirements: 10.3, 10.4_
  
  - [x] 15.3 Update image display with fallback
    - Modify heritage_detail.html to use image_url or placeholder
    - Modify product_detail.html to use image_url or placeholder
    - Update `image_or_placeholder()` methods in models
    - Add academic comments explaining fallback pattern
    - _Requirements: 10.7_
  
  - [ ]* 15.4 Write property test for image upload validation
    - **Property 13: Image Upload Validation**
    - **Validates: Requirements 10.1, 10.4, 10.5, 10.6**
    - Test that disallowed file types are rejected
    - Test that files exceeding size limit are rejected
    - Test that valid files are saved and paths stored
  
  - [ ]* 15.5 Write property test for image display fallback
    - **Property 14: Image Display Fallback**
    - **Validates: Requirements 10.7**
    - Test that missing images display placeholder

- [x] 16. Implement Security Enhancements
  - [x] 16.1 Verify password hashing implementation
    - Ensure all passwords are hashed using generate_password_hash
    - Ensure password verification uses check_password_hash
    - Add academic comments explaining password security
    - _Requirements: 11.1_
  
  - [x] 16.2 Add CSRF protection
    - Install Flask-WTF if not already installed
    - Add CSRF token to all forms
    - Configure CSRF protection in app configuration
    - Add academic comments explaining CSRF attacks and prevention
    - _Requirements: 11.2_
  
  - [x] 16.3 Add input validation to all forms
    - Apply `validate_rating()` to review submissions
    - Apply `validate_email()` to registration and profile updates
    - Apply `sanitize_input()` to text fields (comments, descriptions)
    - Add academic comments explaining input validation importance
    - _Requirements: 11.3_
  
  - [x] 16.4 Configure secure session settings
    - Set SESSION_COOKIE_SECURE = True for HTTPS
    - Set SESSION_COOKIE_HTTPONLY = True
    - Set SESSION_COOKIE_SAMESITE = 'Lax'
    - Set PERMANENT_SESSION_LIFETIME to appropriate timeout
    - Add academic comments explaining session security
    - _Requirements: 11.8_
  
  - [ ]* 16.5 Write property test for password hashing
    - **Property 15: Password Hashing Security**
    - **Validates: Requirements 11.1**
    - Test that stored passwords are hashed, not plaintext
    - Test that hashes are verifiable with check_password_hash

- [ ] 17. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 18. Create Academic Documentation
  - [x] 18.1 Create ACADEMIC_DOCUMENTATION.md
    - Write ER diagram description with all entities and relationships
    - Document database schema with table structures and foreign keys
    - Explain recommendation algorithm with complexity analysis
    - Create system architecture overview with component descriptions
    - Add Mermaid diagrams for architecture and ER diagram
    - _Requirements: 12.1, 12.2, 12.3, 12.4_
  
  - [x] 18.2 Add limitations and future scope sections
    - Document current limitations (scalability, search, caching)
    - Explain design trade-offs (ORM vs SQL, sync vs async)
    - List future enhancements (PostgreSQL, Elasticsearch, Redis, WebSockets)
    - Add academic comments explaining engineering decisions
    - _Requirements: 12.5, 12.6_
  
  - [x] 18.3 Write abstract and conclusion
    - Write project abstract suitable for report (150-200 words)
    - Write conclusion summarizing achievements and learning outcomes
    - Add viva-ready explanations for major technical decisions
    - _Requirements: 12.7, 12.8, 12.9_

- [x] 19. Create Professional README
  - [x] 19.1 Write comprehensive README.md
    - Add project title and abstract
    - List all major features with descriptions
    - Document complete tech stack (Flask, SQLAlchemy, SQLite, Bootstrap, Hypothesis)
    - Provide step-by-step installation instructions
    - Document folder structure with explanations
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_
  
  - [x] 19.2 Add API documentation to README
    - Document all API endpoints with descriptions
    - Provide example requests and responses
    - Include error response examples
    - Add authentication requirements
    - _Requirements: 13.6_
  
  - [x] 19.3 Add deployment and future scope sections
    - Write deployment instructions for production (Gunicorn, Nginx, PostgreSQL)
    - Add future scope section with potential enhancements
    - Include contribution guidelines
    - _Requirements: 13.7, 13.8_

- [ ] 20. Final Integration and Testing
  - [ ] 20.1 Create database migration script
    - Write script to add new tables (Bookmark, SiteView, Review)
    - Add migration for new columns (role, image_url)
    - Test migration on fresh database
    - Test migration on existing database with data
    - _Requirements: 1.4, 3.1, 4.1, 5.1_
  
  - [ ] 20.2 Update existing templates with new features
    - Add bookmark buttons to heritage site cards
    - Add review sections to heritage detail pages
    - Add filter and sort controls to heritage list page
    - Add analytics link to admin navigation
    - Ensure responsive design with Bootstrap
    - _Requirements: 3.2, 5.6, 6.1_
  
  - [ ] 20.3 Test all user flows end-to-end
    - Test user registration and login with different roles
    - Test bookmark creation, viewing, and deletion
    - Test review submission and display
    - Test search and filtering with various combinations
    - Test image upload for heritage sites and products
    - Test analytics dashboard access control
    - Test API endpoints with various inputs
    - _Requirements: All_

- [ ] 21. Final Checkpoint - Complete System Verification
  - Ensure all tests pass, ask the user if questions arise.
  - Verify all requirements are implemented
  - Verify all documentation is complete
  - Verify system is ready for academic evaluation

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation and stability
- Property tests validate universal correctness properties with 100+ iterations
- Unit tests validate specific examples and edge cases
- Academic comments throughout code explain design decisions for viva preparation
- All database changes include proper migrations to preserve existing data
- Security measures are implemented throughout (password hashing, CSRF, input validation)
- RESTful API design follows best practices with proper status codes
- Recommendation algorithm includes detailed complexity analysis for academic evaluation
