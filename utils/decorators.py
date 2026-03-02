"""
Role-Based Access Control Decorators
=====================================

This module provides decorators for implementing role-based access control (RBAC)
in the Digital Catalyst application.

Academic Note:
Role-Based Access Control (RBAC) is a security paradigm where access permissions
are assigned to roles rather than individual users. This provides:

1. Scalability: Easy to manage permissions for many users
2. Flexibility: Users can have multiple roles
3. Security: Principle of least privilege
4. Maintainability: Centralized permission management

Decorator Pattern:
Decorators are a design pattern that allows behavior to be added to functions
without modifying their code. In Python, decorators use the @ syntax and are
implemented as higher-order functions (functions that take functions as arguments).

Implementation:
The @role_required decorator checks if the current user has the required role
before allowing access to a route. If not, it redirects to an appropriate page
with an error message.

Usage Example:
    @app.route('/admin/dashboard')
    @login_required
    @role_required('admin')
    def admin_dashboard():
        return render_template('admin_dashboard.html')

Complexity Analysis:
- Time Complexity: O(1) - Simple role string comparison
- Space Complexity: O(1) - No additional data structures
"""

from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user


def role_required(*roles):
    """
    Decorator to restrict route access based on user roles.
    
    This decorator ensures that only users with specified roles can access
    a route. It should be used after @login_required to ensure user is authenticated.
    
    Args:
        *roles: Variable number of role strings (e.g., 'user', 'manufacturer', 'admin')
    
    Returns:
        Decorated function that checks user role before execution
    
    Raises:
        Redirects to dashboard with error message if user lacks required role
    
    Academic Note:
    This implements the Decorator pattern combined with the Chain of Responsibility
    pattern. Multiple decorators can be chained together:
    
    @login_required          # First: Check if authenticated
    @role_required('admin')  # Second: Check if has admin role
    def admin_only_route():
        pass
    
    The @wraps decorator preserves the original function's metadata (name, docstring)
    which is important for debugging and introspection.
    
    Security Considerations:
    1. Always use with @login_required to ensure authentication
    2. Check role on every request (don't cache role checks)
    3. Use deny-by-default approach (explicit role required)
    4. Log unauthorized access attempts for security monitoring
    
    Example Usage:
        # Single role requirement
        @role_required('admin')
        def admin_route():
            pass
        
        # Multiple roles (user must have at least one)
        @role_required('admin', 'manufacturer')
        def privileged_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated
            # Academic Note: This is a defensive check. In practice, @login_required
            # should be used before @role_required, but we check here for safety.
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Get user role
            user_role = getattr(current_user, 'role', 'user')
            
            # Admin has access to everything (superuser privilege)
            # Academic Note: This implements role hierarchy where admin is the
            # highest privilege level and can access all routes regardless of
            # the required role. This is a common pattern in RBAC systems.
            if user_role == 'admin':
                return f(*args, **kwargs)
            
            # Check if user has required role
            # Academic Note: We use 'in' operator for O(1) average case lookup
            # when roles is converted to a set. For small role lists, this is
            # negligible, but good practice for scalability.
            if user_role not in roles:
                # User doesn't have required role
                # Academic Note: We provide user feedback and redirect rather than
                # raising an exception. This improves user experience and prevents
                # information leakage about system structure.
                flash(f'Access denied. This page requires {" or ".join(roles)} role.', 'danger')
                return redirect(url_for('main.dashboard'))
            
            # User has required role, proceed with original function
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def admin_required(f):
    """
    Convenience decorator for admin-only routes.
    
    This is a specialized version of @role_required('admin') for common use case.
    
    Academic Note:
    This demonstrates the DRY (Don't Repeat Yourself) principle. Rather than
    writing @role_required('admin') everywhere, we create a semantic wrapper
    that makes code more readable and maintainable.
    
    Usage:
        @admin_required
        def admin_dashboard():
            pass
    
    Equivalent to:
        @role_required('admin')
        def admin_dashboard():
            pass
    """
    return role_required('admin')(f)


def manufacturer_required(f):
    """
    Convenience decorator for manufacturer-only routes.
    
    Usage:
        @manufacturer_required
        def manage_products():
            pass
    """
    return role_required('manufacturer')(f)


def user_or_higher(f):
    """
    Decorator for routes accessible to any authenticated user.
    
    This allows access to users, manufacturers, and admins.
    
    Academic Note:
    This implements a hierarchical role system where some roles have
    more privileges than others. In a more complex system, you might
    implement role inheritance or permission-based access control.
    
    Usage:
        @user_or_higher
        def view_heritage_sites():
            pass
    """
    return role_required('user', 'manufacturer', 'admin')(f)


# Academic Note on Access Control Models:
#
# 1. Discretionary Access Control (DAC):
#    - Resource owners control access
#    - Flexible but hard to manage at scale
#    - Example: File permissions in Unix
#
# 2. Mandatory Access Control (MAC):
#    - System-enforced access rules
#    - High security but inflexible
#    - Example: Military classification systems
#
# 3. Role-Based Access Control (RBAC) - Our Implementation:
#    - Access based on user roles
#    - Balance of security and flexibility
#    - Scalable for enterprise applications
#    - Example: Admin, Manager, User roles
#
# 4. Attribute-Based Access Control (ABAC):
#    - Access based on attributes (role, time, location, etc.)
#    - Most flexible but complex to implement
#    - Example: "Allow access if user is manager AND time is business hours"
#
# Our RBAC implementation is suitable for most web applications and provides
# a good balance of security, flexibility, and ease of implementation.
#
# Future Enhancements:
# - Permission-based access (more granular than roles)
# - Role hierarchy (admin inherits manufacturer permissions)
# - Dynamic role assignment
# - Audit logging for access attempts
# - Time-based access restrictions
# - IP-based access restrictions
