"""
Authentication Blueprint
========================

This blueprint handles all authentication-related routes including user login,
registration, and logout functionality.

Academic Note:
Authentication is the process of verifying user identity. This blueprint implements
session-based authentication using Flask-Login, which maintains user sessions via
secure cookies. Password security is ensured through werkzeug's password hashing
functions using PBKDF2-SHA256 algorithm.

Routes:
- GET/POST /auth/login: User login with role selection
- GET/POST /auth/register: User registration with role assignment  
- GET /auth/logout: User logout and session termination
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

# Create Blueprint
# URL prefix '/auth' means all routes will be prefixed with /auth
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User Login Route
    
    Handles user authentication with role-based login support.
    Users can log in as regular users or manufacturers.
    
    Academic Note:
    This implements credential-based authentication where user-provided
    credentials are verified against stored hashed passwords. The role
    system allows different user types to access different features.
    
    Security Measures:
    - Password verification using secure hash comparison
    - Session management via Flask-Login
    - Role validation before granting access
    """
    # Redirect if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            login_type = request.form.get('login_type', 'user')  # 'user' or 'manufacturer'
            
            if not username or not password:
                flash('Please provide both username and password', 'danger')
                return redirect(url_for('auth.login'))
            
            # Query user from database
            user = User.query.filter_by(username=username).first()
            
            # Verify credentials
            if user and check_password_hash(user.password, password):
                # Verify role matches login type
                if login_type == 'manufacturer' and not user.is_manufacturer():
                    flash('This account is not registered as a manufacturer. Sign in as a regular user or register as manufacturer.', 'warning')
                    return redirect(url_for('auth.login'))
                
                # Create session
                login_user(user)
                session['login_as_manufacturer'] = (login_type == 'manufacturer')
                flash('Login successful!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid username or password', 'danger')
        
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Login error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            print(f"Traceback: {error_details}")
            flash('An error occurred during login. Please try again.', 'danger')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User Registration Route
    
    Creates new user accounts with role assignment.
    
    Academic Note:
    Registration implements the following security best practices:
    1. Uniqueness validation (username and email)
    2. Password hashing before storage (never store plaintext)
    3. Role-based access control initialization
    
    Database Constraints:
    - Username: Unique, indexed for fast lookup
    - Email: Unique, indexed, validated format
    - Password: Hashed using PBKDF2-SHA256
    - Role: Defaults to 'user', can be 'manufacturer' or 'admin'
    """
    # Redirect if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')  # Default to 'user' role
        
        # Validate uniqueness
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user with hashed password
        # Academic Note: generate_password_hash uses PBKDF2-SHA256 with salt
        # This prevents rainbow table attacks and ensures password security
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )
        
        # Persist to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    """
    User Logout Route
    
    Terminates user session and clears authentication state.
    
    Academic Note:
    Logout is a critical security operation that:
    1. Invalidates the current session
    2. Clears session cookies
    3. Removes authentication state
    
    This prevents unauthorized access after user explicitly logs out.
    """
    logout_user()
    session.pop('login_as_manufacturer', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('main.landing'))
