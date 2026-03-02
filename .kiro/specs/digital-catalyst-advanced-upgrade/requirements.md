# Requirements Document

## Introduction

This document specifies the requirements for upgrading the Digital Catalyst platform into a distinction-level final year project. The upgrade transforms the existing heritage preservation and artisan marketplace platform by adding advanced features including AI-based recommendations, comprehensive role-based access control, analytics dashboard, bookmark and engagement tracking, review and rating system, advanced search and filtering, REST API layer, image upload capabilities, security enhancements, and academic documentation.

The system currently supports basic user authentication, heritage site management, artisan profiles, product listings, and simple ML-based recommendations. This upgrade will add sophisticated user engagement features, multi-role access control, comprehensive analytics, and production-ready security measures suitable for academic evaluation at the distinction level.

## Glossary

- **System**: The Digital Catalyst web application platform
- **User**: A registered platform user with 'user' role who can browse, bookmark, rate, and review content
- **Manufacturer**: A registered platform user with 'manufacturer' role who can manage artisan products
- **Admin**: A registered platform user with 'admin' role who has system-wide management capabilities
- **Heritage_Site**: A cultural or historical location tracked in the system
- **Artisan**: A craftsperson or MSME tracked in the system
- **Product**: An item created by an artisan and listed for sale
- **Bookmark**: A saved reference by a user to a heritage site
- **Review**: A user-submitted rating and comment for a heritage site
- **Site_View**: A tracking record of when a heritage site was viewed
- **Recommendation_Engine**: The AI/ML component that suggests heritage sites and artisans
- **Blueprint**: A Flask modular component for organizing routes
- **Route_Protection**: Authentication and authorization checks on endpoints
- **Analytics_Dashboard**: A view displaying aggregated system metrics
- **REST_API**: JSON-based HTTP endpoints for programmatic access

## Requirements

### Requirement 1: Architecture Refactoring

**User Story:** As a developer, I want the codebase organized into Flask Blueprints with clear separation of concerns, so that the project is maintainable and demonstrates professional software architecture.

#### Acceptance Criteria

1. THE System SHALL organize routes into four Flask Blueprints: auth, main, api, and dashboard
2. THE System SHALL maintain all database models in a single models.py file
3. THE System SHALL maintain all ML logic in ml/recommendation_engine.py
4. THE System SHALL define proper SQLAlchemy relationships with foreign keys and cascade deletes
5. THE System SHALL include academic comments explaining architectural decisions and design patterns

### Requirement 2: Role-Based Access Control

**User Story:** As a system administrator, I want three distinct user roles with different permissions, so that users have appropriate access levels for their responsibilities.

#### Acceptance Criteria

1. THE System SHALL support three roles: user, manufacturer, and admin
2. WHEN a user with 'user' role is authenticated, THE System SHALL allow browsing, searching, filtering, bookmarking, rating, reviewing, and viewing recommendations
3. WHEN a user with 'manufacturer' role is authenticated, THE System SHALL allow adding, editing, and deleting artisan products and uploading images
4. WHEN a user with 'admin' role is authenticated, THE System SHALL allow managing users, approving artisans, deleting reviews, and viewing system-wide analytics
5. THE System SHALL implement route protection using Flask decorators that verify user roles
6. WHEN an unauthorized user attempts to access a protected route, THE System SHALL redirect to login with an appropriate error message

### Requirement 3: Bookmark System

**User Story:** As a user, I want to bookmark heritage sites I'm interested in, so that I can easily find them later and the system can personalize recommendations.

#### Acceptance Criteria

1. THE System SHALL create a Bookmark model with user_id, heritage_id, and timestamp fields
2. WHEN a user bookmarks a heritage site, THE System SHALL create a bookmark record with the current timestamp
3. WHEN a user views their bookmarks, THE System SHALL display all bookmarked heritage sites ordered by most recent first
4. WHEN a user unbookmarks a heritage site, THE System SHALL delete the bookmark record
5. THE System SHALL prevent duplicate bookmarks for the same user and heritage site combination
6. THE System SHALL use bookmark data in the recommendation engine

### Requirement 4: Engagement Tracking System

**User Story:** As a system analyst, I want to track which heritage sites are being viewed, so that I can identify popular content and improve recommendations.

#### Acceptance Criteria

1. THE System SHALL create a SiteView model with user_id (nullable), heritage_id, and timestamp fields
2. WHEN a heritage site detail page is viewed, THE System SHALL create a site view record with the current timestamp
3. WHEN an anonymous user views a heritage site, THE System SHALL create a site view record with null user_id
4. THE System SHALL calculate most viewed sites using aggregation queries on the SiteView model
5. THE System SHALL use view count data in the recommendation engine

### Requirement 5: Review and Rating System

**User Story:** As a user, I want to rate and review heritage sites, so that I can share my experience and help others make informed decisions.

#### Acceptance Criteria

1. THE System SHALL create a Review model with user_id, heritage_id, rating (1-5), comment, and created_at fields
2. WHEN a user submits a review, THE System SHALL validate that the rating is between 1 and 5 inclusive
3. THE System SHALL enforce one review per user per heritage site
4. WHEN a user attempts to submit a duplicate review, THE System SHALL update the existing review instead of creating a new one
5. THE System SHALL calculate average rating dynamically using SQLAlchemy aggregation functions
6. THE System SHALL display review count and average star rating on heritage site pages
7. WHEN an admin deletes a review, THE System SHALL remove the review record and recalculate the average rating

### Requirement 6: Advanced Search and Filtering Engine

**User Story:** As a user, I want to search and filter heritage sites by multiple criteria, so that I can quickly find sites that match my interests.

#### Acceptance Criteria

1. WHEN a user searches by name, THE System SHALL return heritage sites with names containing the search term (case-insensitive)
2. WHEN a user filters by state, THE System SHALL return only heritage sites in the selected state
3. WHEN a user filters by category, THE System SHALL return only heritage sites in the selected category
4. WHEN a user filters by rating range, THE System SHALL return only heritage sites with average ratings within the specified range
5. THE System SHALL support combining multiple filters simultaneously
6. WHEN a user sorts by most viewed, THE System SHALL order results by view count descending
7. WHEN a user sorts by highest rated, THE System SHALL order results by average rating descending
8. WHEN a user sorts by most bookmarked, THE System SHALL order results by bookmark count descending
9. THE System SHALL use optimized SQLAlchemy queries with proper joins and indexing

### Requirement 7: AI-Based Recommendation System

**User Story:** As a user, I want personalized recommendations for heritage sites, so that I can discover new places aligned with my interests.

#### Acceptance Criteria

1. WHEN a user has bookmark history, THE System SHALL recommend heritage sites based on the categories and states of bookmarked sites
2. WHEN a user has view history, THE System SHALL recommend heritage sites similar to previously viewed sites
3. WHEN a user has no history (cold start), THE System SHALL recommend top-rated and most popular heritage sites
4. THE Recommendation_Engine SHALL implement content-based filtering using category and state attributes
5. THE Recommendation_Engine SHALL implement popularity-based filtering using view counts, ratings, and bookmark counts
6. THE Recommendation_Engine SHALL combine multiple filtering strategies into a hybrid recommendation algorithm
7. THE System SHALL include academic comments in recommendation_engine.py explaining each algorithm and its complexity
8. THE System SHALL provide viva-ready documentation explaining the recommendation approach

### Requirement 8: Analytics Dashboard

**User Story:** As an admin, I want to view comprehensive system analytics, so that I can understand platform usage and make data-driven decisions.

#### Acceptance Criteria

1. WHEN an admin accesses the analytics dashboard, THE System SHALL display total counts of users, manufacturers, and heritage sites
2. THE System SHALL display the most viewed heritage site with its view count
3. THE System SHALL display the most bookmarked heritage site with its bookmark count
4. THE System SHALL display the highest rated heritage site with its average rating
5. THE System SHALL display the most active state by number of heritage sites
6. THE System SHALL calculate all metrics using SQLAlchemy aggregation queries (func.count, func.avg, func.sum, group_by)
7. THE System SHALL make the analytics dashboard accessible at /dashboard/analytics
8. WHEN a non-admin user attempts to access the analytics dashboard, THE System SHALL deny access

### Requirement 9: REST API Layer

**User Story:** As a developer, I want JSON-based REST API endpoints, so that I can integrate the platform with other applications and services.

#### Acceptance Criteria

1. THE System SHALL provide a GET endpoint at /api/heritage returning all heritage sites as JSON
2. THE System SHALL provide a GET endpoint at /api/artisans returning all artisans as JSON
3. THE System SHALL provide a GET endpoint at /api/recommendations/<user_id> returning personalized recommendations as JSON
4. THE System SHALL provide a GET endpoint at /api/reviews/<heritage_id> returning all reviews for a heritage site as JSON
5. WHEN an API request succeeds, THE System SHALL return HTTP status code 200 with properly formatted JSON
6. WHEN an API request fails due to invalid input, THE System SHALL return HTTP status code 400 with an error message
7. WHEN an API request fails due to missing resource, THE System SHALL return HTTP status code 404 with an error message
8. THE System SHALL include proper error handling for all API endpoints

### Requirement 10: Image Upload System

**User Story:** As a manufacturer, I want to upload images for heritage sites and artisan products, so that listings are visually appealing and informative.

#### Acceptance Criteria

1. WHEN a user uploads an image, THE System SHALL validate that the file is an allowed image type (jpg, jpeg, png, gif)
2. WHEN a user uploads an image, THE System SHALL use secure_filename to sanitize the filename
3. THE System SHALL store uploaded images in the static/uploads/ directory
4. THE System SHALL save the file path in the database image_url field
5. WHEN an image upload fails validation, THE System SHALL display an error message and reject the upload
6. THE System SHALL limit uploaded file size to prevent abuse
7. WHEN displaying an image, THE System SHALL use the stored file path or a placeholder if no image exists

### Requirement 11: Security Enhancements

**User Story:** As a security-conscious developer, I want comprehensive security measures, so that the platform protects user data and prevents common vulnerabilities.

#### Acceptance Criteria

1. THE System SHALL hash all passwords using werkzeug.security before storing in the database
2. THE System SHALL implement CSRF protection on all form submissions
3. WHEN a user submits form data, THE System SHALL validate and sanitize all inputs
4. THE System SHALL implement role-based route protection on all sensitive endpoints
5. THE System SHALL prevent duplicate reviews by checking existing user-heritage combinations
6. WHEN a file is uploaded, THE System SHALL validate the file type against an allowlist
7. THE System SHALL use parameterized queries to prevent SQL injection
8. THE System SHALL set secure session configuration with appropriate timeout values

### Requirement 12: Academic Documentation

**User Story:** As a student, I want comprehensive academic documentation, so that I can explain the project architecture and design decisions during viva examination.

#### Acceptance Criteria

1. THE System SHALL include an ER diagram description explaining all entities and relationships
2. THE System SHALL include database schema documentation with table structures and foreign keys
3. THE System SHALL include recommendation algorithm explanation with complexity analysis
4. THE System SHALL include system architecture overview with component diagrams
5. THE System SHALL include a limitations section discussing known constraints and trade-offs
6. THE System SHALL include a future scope section outlining potential enhancements
7. THE System SHALL include an abstract suitable for a project report
8. THE System SHALL include a conclusion section summarizing achievements and learning outcomes
9. THE System SHALL include viva-ready explanations for all major technical decisions

### Requirement 13: Professional README

**User Story:** As a developer or evaluator, I want a comprehensive README file, so that I can understand the project scope, setup, and usage.

#### Acceptance Criteria

1. THE README SHALL include a project title and abstract
2. THE README SHALL list all major features with brief descriptions
3. THE README SHALL document the complete tech stack
4. THE README SHALL provide step-by-step installation instructions
5. THE README SHALL document the folder structure with explanations
6. THE README SHALL include API documentation with endpoint descriptions and example requests
7. THE README SHALL include a future scope section
8. THE README SHALL include deployment instructions for production environments
