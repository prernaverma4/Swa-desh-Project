# Digital Catalyst: AI-Driven Platform for Indian Economic Growth & Heritage Preservation

![Digital Catalyst](https://img.shields.io/badge/Version-1.0.0-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## 🌟 Overview

**Digital Catalyst** is a comprehensive full-stack AI-powered platform designed to support and accelerate India's economic growth through heritage preservation and artisan empowerment. The platform combines modern web technologies with machine learning to provide intelligent recommendations and analytics for cultural heritage sites and traditional craftspeople.

### 🎯 Key Features

- **Heritage Management Module**: Comprehensive CRUD operations for heritage sites across India
- **Artisan & MSME Module**: Track and support traditional artisans and their crafts
- **AI Hybrid Recommendation System**: Content-based, collaborative, and popularity-based filtering
- **Bookmark System**: Save favorite heritage sites for later
- **Review & Rating System**: User reviews with 1-5 star ratings
- **Engagement Tracking**: Track views, bookmarks, and user interactions
- **Advanced Search & Filtering**: Multi-criteria search with rating filters and sorting
- **Analytics Dashboard**: Real-time insights with engagement metrics (admin-only)
- **Role-Based Access Control**: User, Manufacturer, and Admin roles
- **User Authentication**: Secure login/registration with password hashing
- **Image Upload System**: Secure file uploads for heritage sites and products
- **RESTful APIs**: Comprehensive API endpoints for programmatic access
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5

## 🏗️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **SQLite** - Lightweight database

### Frontend
- **HTML5/CSS3**
- **Bootstrap 5.3.0** - Responsive framework
- **JavaScript (ES6+)**
- **Chart.js** - Data visualization
- **Bootstrap Icons** - Icon library
- **Google Fonts** (Playfair Display, Work Sans)

### AI/ML
- **Custom Hybrid Recommendation Engine** - Pure Python implementation
- **Content-Based Filtering** - User preference analysis
- **Collaborative Filtering** - Jaccard similarity for user matching
- **Popularity-Based Filtering** - Engagement score calculation

## 📁 Project Structure

```
digital_catalyst/
│
├── app.py                          # Main Flask application with security config
├── models.py                       # Database models (User, HeritageSite, Artisan, Bookmark, Review, SiteView)
├── requirements.txt                # Python dependencies
├── migrate_database.py             # Database migration script
├── database.db                     # SQLite database (auto-generated)
│
├── blueprints/                     # Modular Blueprint architecture
│   ├── __init__.py
│   ├── auth.py                     # Authentication routes
│   ├── main.py                     # Core application routes
│   ├── api.py                      # REST API endpoints
│   └── dashboard.py                # Analytics dashboard (admin)
│
├── ml/
│   └── recommendation_engine.py    # Hybrid AI recommendation system
│
├── utils/                          # Utility modules
│   ├── decorators.py               # Role-based access control decorators
│   ├── validators.py               # Input validation functions
│   └── file_upload.py              # Secure file upload utilities
│
├── templates/
│   ├── base.html                   # Base template with navigation
│   ├── landing.html                # Landing page
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── dashboard.html              # Main dashboard
│   ├── heritage.html               # Heritage sites listing
│   ├── heritage_detail.html        # Heritage site details with reviews
│   ├── add_heritage.html           # Add heritage site form
│   ├── edit_heritage.html          # Edit heritage site form
│   ├── my_bookmarks.html           # User's bookmarked sites
│   ├── reviews.html                # All reviews for a site
│   ├── artisans.html               # Artisans listing
│   ├── products.html               # Products listing
│   ├── my_orders.html              # User's orders
│   └── dashboard/
│       └── analytics.html          # Admin analytics dashboard
│
└── static/
    ├── css/
    │   └── style.css               # Custom styles (Indian-inspired design)
    ├── js/
    │   └── main.js                 # Custom JavaScript
    └── uploads/                    # User-uploaded images
        ├── heritage/               # Heritage site images
        └── products/               # Product images
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step-by-Step Installation

1. **Navigate to the project directory:**
   ```bash
   cd digital_catalyst
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   If you get an SSL certificate error, use:
   ```bash
   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Run the application:**
   ```bash
   python app.py
   ```
   Or use the run script (installs dependencies if needed):
   ```bash
   chmod +x run.sh && ./run.sh
   ```

6. **Access the application:**
   Open your web browser and navigate to:
   ```
   http://localhost:5001
   ```

### Default Credentials

- **Username**: `admin`
- **Password**: `admin123`

## 📊 Sample Data

The application comes pre-loaded with sample data including:

### Heritage Sites (8 sites)
- Taj Mahal (Uttar Pradesh)
- Red Fort (Delhi)
- Ajanta Caves (Maharashtra)
- Hampi (Karnataka)
- Golden Temple (Punjab)
- Konark Sun Temple (Odisha)
- Khajuraho Temples (Madhya Pradesh)
- Mysore Palace (Karnataka)

### Artisans (8 artisans)
- Pottery experts from Rajasthan
- Weaving specialists from West Bengal
- Metalwork craftsmen from Uttar Pradesh
- Embroidery artists from Gujarat
- Wood carvers from Kerala
- Painters from Madhya Pradesh
- Jewelry makers from Rajasthan
- Basket weavers from Assam

## 🔌 REST API Endpoints

### Heritage Sites API

**GET /api/heritage**
- Returns all heritage sites in JSON format
- No authentication required

**GET /api/heritage/<id>**
- Returns specific heritage site details
- No authentication required

### Artisans API

**GET /api/artisans**
- Returns all artisans in JSON format

**GET /api/artisan/<id>**
- Returns specific artisan details

### Products API

**GET /api/products**
- Returns all products in JSON format

**GET /api/product/<id>**
- Returns specific product details

### Recommendations API

**GET /api/recommendations?type=heritage&top_n=5**
- Returns AI-recommended heritage sites
- Parameters:
  - `type`: 'heritage' or 'artisans'
  - `top_n`: Number of recommendations (default: 5)
  - `state`: State filter for artisans (optional)

**GET /api/recommendations/<user_id>**
- Returns personalized recommendations for a specific user
- Uses hybrid approach (content-based + collaborative + popularity)
- Parameters:
  - `top_n`: Number of recommendations (default: 10)

### Reviews API

**GET /api/reviews/<heritage_id>**
- Returns all reviews for a specific heritage site
- Includes average rating and review count

### Analytics API

**GET /api/analytics**
- Returns comprehensive analytics data including:
  - Economic impact metrics
  - Visitor trends
  - State-wise distribution

### Error Responses

All API endpoints return consistent error responses:

**404 Not Found:**
```json
{
  "error": "Heritage site not found",
  "message": "No heritage site with id 999"
}
```

**400 Bad Request:**
```json
{
  "error": "Invalid input",
  "message": "top_n must be between 1 and 50"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal server error",
  "message": "Database connection failed"
}
```

## 🎨 Design Philosophy

The platform features a distinctive **Indian-inspired modern design** with:

- **Color Palette**: Navy, teal, saffron, gold, and coral
- **Typography**: Playfair Display (headings) + Work Sans (body)
- **Animations**: Smooth transitions and micro-interactions
- **Responsive**: Mobile-first design approach
- **Accessibility**: WCAG 2.1 compliant color contrasts

## 🧠 AI/ML Features

### Hybrid Recommendation Engine

The platform uses a sophisticated hybrid recommendation system combining three filtering strategies:

#### 1. Content-Based Filtering (40% weight)
- Analyzes user's preferred categories and states
- Matches heritage sites to user preferences
- Provides personalized recommendations based on browsing history

#### 2. Collaborative Filtering (30% weight)
- Finds similar users using Jaccard similarity
- Recommends sites liked by users with similar tastes
- Discovers unexpected items through community preferences

#### 3. Popularity-Based Filtering (30% weight)
- Calculates engagement scores from:
  - Average rating (40%)
  - View count (30%)
  - Bookmark count (30%)
- Recommends trending and highly-rated sites

#### Cold Start Solution
- New users: Rely on popularity-based recommendations
- New items: Use content-based filtering with attributes
- Gradually incorporate user preferences as they interact

### Engagement Metrics

The system tracks:
- **Views**: Every heritage site visit (authenticated and anonymous)
- **Bookmarks**: User-saved sites for later
- **Reviews**: Ratings (1-5 stars) and comments
- **Computed Properties**: Average rating, view count, bookmark count

### Economic Impact Analysis
- Tourism revenue estimates
- Artisan revenue projections
- Total economic impact calculations
- State-wise distribution analysis

## 📈 Features Breakdown

### 1. Heritage Management Module
- ✅ Add new heritage sites with image upload
- ✅ Edit existing sites
- ✅ Delete sites
- ✅ Advanced search and filter (name, state, category, rating)
- ✅ Sort by views, rating, bookmarks, or name
- ✅ View detailed statistics (views, bookmarks, reviews)
- ✅ Export to CSV

### 2. Bookmark System
- ✅ Save favorite heritage sites
- ✅ View all bookmarked sites
- ✅ Remove bookmarks
- ✅ Bookmark count tracking

### 3. Review & Rating System
- ✅ Submit reviews with 1-5 star ratings
- ✅ Add optional comments
- ✅ Edit own reviews
- ✅ Delete own reviews
- ✅ Admin moderation (delete any review)
- ✅ Average rating calculation
- ✅ Review count display

### 4. Engagement Tracking
- ✅ Track site views (authenticated and anonymous)
- ✅ View count display
- ✅ Most viewed sites analytics
- ✅ User browsing history

### 5. Artisan & MSME Module
- ✅ Add new artisans
- ✅ Edit artisan profiles
- ✅ Delete artisans
- ✅ Search and filter by name, state, craft
- ✅ Track product pricing
- ✅ Export to CSV

### 6. Product Management
- ✅ Add products with image upload
- ✅ Edit products (manufacturer only)
- ✅ Delete products (manufacturer only)
- ✅ Product listing and details
- ✅ Stock management

### 7. Analytics Dashboard (Admin Only)
- ✅ Total counts (users, manufacturers, sites, artisans, products)
- ✅ Most visited heritage site
- ✅ Most viewed heritage site
- ✅ Most bookmarked site
- ✅ Highest rated site
- ✅ Most active state
- ✅ State-wise distribution
- ✅ Craft analytics
- ✅ Product analytics

### 8. Authentication & Authorization
- ✅ User registration with role selection
- ✅ Secure login (user/manufacturer)
- ✅ Password hashing (PBKDF2-SHA256)
- ✅ Session management
- ✅ Role-based access control (User, Manufacturer, Admin)
- ✅ Protected routes with decorators

### 9. Security Features
- ✅ Password hashing with salt
- ✅ Session security (HttpOnly, SameSite)
- ✅ Input validation and sanitization
- ✅ XSS prevention
- ✅ SQL injection prevention (ORM)
- ✅ Secure file uploads (type and size validation)
- ✅ CSRF protection ready

## 🔒 Security Features

### Authentication & Authorization
- **Password Hashing**: PBKDF2-SHA256 with salt using Werkzeug security
- **Role-Based Access Control (RBAC)**: Three roles (User, Manufacturer, Admin)
- **Session Management**: Flask-Login with secure session configuration
- **Protected Routes**: Decorators for role-based access control

### Session Security
- **HttpOnly Cookies**: Prevents XSS attacks on session cookies
- **SameSite Policy**: Set to 'Lax' to prevent CSRF attacks
- **Session Timeout**: 24-hour permanent session lifetime
- **Secure Flag**: Ready for HTTPS deployment

### Input Validation & Sanitization
- **Rating Validation**: 1-5 range check for reviews
- **Email Validation**: Regex pattern matching
- **Text Sanitization**: HTML tag removal from user input
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries

### File Upload Security
- **File Type Validation**: Only allowed extensions (jpg, jpeg, png, gif, webp)
- **File Size Limit**: 5MB maximum upload size
- **Secure Filenames**: Werkzeug secure_filename() for path traversal prevention
- **Upload Directory Isolation**: Separate folders for heritage and product images

## 🌐 Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

## 📱 Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## 🐛 Troubleshooting

### Common Issues

1. **Import Error: No module named 'flask'**
   - Solution: Run `pip install -r requirements.txt`
   - If you get an SSL certificate error, run:
     ```bash
     pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
     ```

2. **Database locked error**
   - Solution: Close any other instances of the app and restart

3. **Port 5001 already in use**
   - Solution: Change the port in `app.py` (last line), e.g. to `port=5002`

4. **Charts not displaying**
   - Solution: Ensure internet connection (Chart.js loaded from CDN)

## 🚀 Deployment

### Production Deployment

For production deployment, follow these steps:

1. **Database Migration**
   ```bash
   python migrate_database.py
   ```

2. **Environment Variables**
   Create a `.env` file with:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///instance/database.db
   FLASK_ENV=production
   SESSION_COOKIE_SECURE=True
   ```

3. **Use Production Server**
   Install Gunicorn:
   ```bash
   pip install gunicorn
   ```
   
   Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

4. **Nginx Configuration** (optional)
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static {
           alias /path/to/digital_catalyst/static;
       }
   }
   ```

5. **Database Upgrade** (for PostgreSQL)
   Update `app.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
   ```

### Cloud Deployment Options

- **Heroku**: Use Procfile with `web: gunicorn app:app`
- **AWS EC2**: Deploy with Nginx + Gunicorn
- **Google Cloud Run**: Containerize with Docker
- **DigitalOcean App Platform**: Direct GitHub integration

## 🔮 Future Enhancements

### Technical Improvements
- [ ] **PostgreSQL Migration**: Scale beyond SQLite for production
- [ ] **Redis Caching**: Cache recommendations and analytics queries
- [ ] **Elasticsearch Integration**: Full-text search with fuzzy matching
- [ ] **WebSocket Support**: Real-time notifications and updates
- [ ] **API Rate Limiting**: Prevent abuse with Flask-Limiter
- [ ] **CDN Integration**: Serve static assets and images faster

### Feature Additions
- [ ] **Multi-language Support**: Hindi and regional languages (i18n)
- [ ] **Advanced ML Models**: Deep learning for image recognition
- [ ] **Payment Gateway**: Razorpay/Stripe integration for artisan products
- [ ] **Mobile App**: React Native or Flutter mobile version
- [ ] **Social Features**: Share sites, follow artisans, user profiles
- [ ] **Email Notifications**: Review responses, bookmark reminders
- [ ] **Export Features**: PDF reports, data exports for analytics
- [ ] **Chatbot Integration**: AI assistant for heritage information
- [ ] **Virtual Tours**: 360° images and video integration
- [ ] **Gamification**: Badges, points for engagement

### Analytics Enhancements
- [ ] **Predictive Analytics**: Forecast tourism trends
- [ ] **A/B Testing**: Optimize recommendation algorithms
- [ ] **User Segmentation**: Cluster analysis for targeted recommendations
- [ ] **Sentiment Analysis**: Analyze review text for insights

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ for India's Heritage & Economic Growth

## 📞 Support

For issues and questions, please create an issue in the repository.

---

**Made with passion to empower India's cultural heritage and artisan economy! 🇮🇳**
