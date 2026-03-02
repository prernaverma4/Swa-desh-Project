"""
Input Validation and Sanitization
==================================

This module provides functions for validating and sanitizing user input to prevent
security vulnerabilities and ensure data integrity.

Academic Note:
Input validation is a critical security measure that prevents various attacks:

1. SQL Injection: Malicious SQL code in input
2. Cross-Site Scripting (XSS): Malicious JavaScript in input
3. Command Injection: Shell commands in input
4. Path Traversal: Directory navigation in file paths
5. Buffer Overflow: Excessive input length

Defense in Depth:
We implement multiple layers of validation:
- Client-side: HTML5 validation, JavaScript checks (user experience)
- Server-side: Python validation (security - never trust client)
- Database: Constraints, foreign keys (data integrity)

Validation vs Sanitization:
- Validation: Check if input meets requirements (reject if invalid)
- Sanitization: Clean input to remove dangerous content (modify to make safe)

Both approaches have trade-offs. We use validation for structured data (ratings, emails)
and sanitization for free-text content (comments, descriptions).
"""

import re
from typing import Union, Optional


def validate_rating(rating: Union[int, str, float]) -> tuple[bool, str]:
    """
    Validate that a rating is an integer between 1 and 5 (inclusive).
    
    Args:
        rating: Rating value to validate (can be int, str, or float)
    
    Returns:
        tuple: (is_valid: bool, message: str)
            - (True, "") if valid
            - (False, error_message) if invalid
    
    Academic Note:
    This implements input validation with type coercion. We accept multiple types
    (int, str, float) for flexibility but ensure the output is always an integer
    within the valid range.
    
    Range Validation:
    The range [1, 5] is a common pattern for rating systems (5-star ratings).
    We use inclusive bounds (1 ≤ rating ≤ 5) which is more intuitive for users
    than exclusive bounds.
    
    Error Handling:
    We return a tuple (bool, str) for flexible error handling. The caller can
    check the boolean and display the error message to the user.
    
    Examples:
        >>> validate_rating(3)
        (True, "")
        >>> validate_rating("4")
        (True, "")
        >>> validate_rating(0)
        (False, "Rating must be between 1 and 5")
        >>> validate_rating("invalid")
        (False, "Invalid rating format")
    """
    try:
        # Convert to integer (handles str and float)
        # Academic Note: int() truncates floats (3.7 → 3), doesn't round
        rating_int = int(rating)
        
        # Check range
        if 1 <= rating_int <= 5:
            return (True, "")
        else:
            return (False, 'Rating must be between 1 and 5')
    
    except (ValueError, TypeError):
        # Handle conversion errors or type errors
        return (False, 'Invalid rating format. Must be a number between 1 and 5.')


def validate_email(email: str) -> str:
    """
    Validate email address format using regex pattern.
    
    Args:
        email: Email address string to validate
    
    Returns:
        str: Validated email address (lowercased for consistency)
    
    Raises:
        ValueError: If email format is invalid
    
    Academic Note:
    Email validation is surprisingly complex. The official RFC 5322 specification
    allows many edge cases that are rarely used in practice. We use a simplified
    regex that covers 99% of real-world email addresses.
    
    Regex Pattern Explanation:
    ^[a-zA-Z0-9._%+-]+  : Local part (before @)
                          - Letters, numbers, and special chars (. _ % + -)
                          - At least one character
    @                   : Literal @ symbol
    [a-zA-Z0-9.-]+      : Domain name
                          - Letters, numbers, dots, hyphens
    \.                  : Literal dot before TLD
    [a-zA-Z]{2,}$       : Top-level domain (com, org, etc.)
                          - At least 2 letters
    
    Limitations:
    - Doesn't validate if email actually exists
    - Doesn't check MX records
    - Doesn't handle all RFC 5322 edge cases
    - Doesn't validate internationalized domains (IDN)
    
    For production, consider using a library like email-validator or
    sending a verification email to confirm ownership.
    
    Examples:
        >>> validate_email("user@example.com")
        'user@example.com'
        >>> validate_email("User@Example.COM")
        'user@example.com'
        >>> validate_email("invalid.email")
        ValueError: Invalid email format
    """
    if not email or not isinstance(email, str):
        raise ValueError('Email is required and must be a string')
    
    # Convert to lowercase for consistency
    # Academic Note: Email local parts are technically case-sensitive per RFC,
    # but most email providers treat them as case-insensitive. We normalize
    # to lowercase to prevent duplicate accounts (user@example.com vs User@example.com)
    email = email.strip().lower()
    
    # Regex pattern for email validation
    # Academic Note: This is a simplified pattern. For production, consider
    # using a dedicated email validation library.
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'$'
    
    if not re.match(pattern, email):
        raise ValueError('Invalid email format. Please enter a valid email address.')
    
    # Additional length check
    # Academic Note: RFC 5321 specifies maximum lengths:
    # - Local part: 64 characters
    # - Domain: 255 characters
    # - Total: 320 characters
    if len(email) > 320:
        raise ValueError('Email address is too long (maximum 320 characters)')
    
    return email


def sanitize_input(text: Optional[str], max_length: int = 500) -> str:
    """
    Sanitize text input by removing HTML tags and limiting length.
    
    Args:
        text: Text string to sanitize
        max_length: Maximum allowed length (default: 500)
    
    Returns:
        str: Sanitized text (empty string if input is None)
    
    Academic Note:
    Sanitization is crucial for preventing Cross-Site Scripting (XSS) attacks.
    XSS occurs when malicious JavaScript is injected into web pages and executed
    in other users' browsers.
    
    Defense Strategies:
    1. Remove HTML tags (our approach)
    2. Escape HTML entities (< becomes &lt;)
    3. Use Content Security Policy (CSP) headers
    4. Use templating engines with auto-escaping (Jinja2 does this)
    
    Our Approach:
    We remove HTML tags entirely rather than escaping them. This is appropriate
    for fields where HTML is not expected (names, comments, descriptions).
    
    For rich text editors where HTML is desired, use a whitelist-based HTML
    sanitizer like Bleach or DOMPurify.
    
    Regex Pattern Explanation:
    <[^>]+>  : Matches HTML tags
    <        : Opening angle bracket
    [^>]+    : One or more characters that are not >
    >        : Closing angle bracket
    
    This removes tags like <script>, <img>, <a>, etc.
    
    Limitations:
    - Doesn't handle malformed HTML
    - Doesn't remove JavaScript event handlers in attributes
    - Doesn't handle CSS injection
    
    For production, use a dedicated HTML sanitization library.
    
    Examples:
        >>> sanitize_input("Hello <script>alert('XSS')</script> World")
        'Hello  World'
        >>> sanitize_input("Normal text", max_length=10)
        'Normal tex'
        >>> sanitize_input(None)
        ''
    """
    # Handle None or empty input
    if not text:
        return ''
    
    # Convert to string if not already
    text = str(text)
    
    # Strip leading/trailing whitespace
    # Academic Note: strip() removes spaces, tabs, newlines from both ends
    text = text.strip()
    
    # Remove HTML tags using regex
    # Academic Note: This is a simple approach. For production, use a library
    # like Bleach that handles edge cases and malformed HTML.
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove multiple consecutive spaces
    # Academic Note: \s+ matches one or more whitespace characters
    text = re.sub(r'\s+', ' ', text)
    
    # Limit length
    # Academic Note: Slicing in Python is safe - doesn't raise error if
    # length is less than max_length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_phone(phone: str) -> str:
    """
    Validate and format phone number (Indian format).
    
    Args:
        phone: Phone number string
    
    Returns:
        str: Validated phone number (digits only)
    
    Raises:
        ValueError: If phone number format is invalid
    
    Academic Note:
    Phone number validation is country-specific. This implementation focuses
    on Indian phone numbers (10 digits, starting with 6-9).
    
    Indian Phone Number Format:
    - Mobile: 10 digits starting with 6, 7, 8, or 9
    - Landline: 10 digits with area code
    
    For international applications, use a library like phonenumbers (Google's
    libphonenumber) which handles all country formats and validation.
    
    Examples:
        >>> validate_phone("9876543210")
        '9876543210'
        >>> validate_phone("+91 98765 43210")
        '9876543210'
        >>> validate_phone("12345")
        ValueError: Invalid phone number
    """
    if not phone:
        raise ValueError('Phone number is required')
    
    # Remove all non-digit characters
    # Academic Note: This handles various formats:
    # - "+91 98765 43210"
    # - "(987) 654-3210"
    # - "9876543210"
    phone_digits = re.sub(r'\D', '', phone)
    
    # Remove country code if present (+91 for India)
    if phone_digits.startswith('91') and len(phone_digits) == 12:
        phone_digits = phone_digits[2:]
    
    # Validate length (10 digits for Indian numbers)
    if len(phone_digits) != 10:
        raise ValueError('Phone number must be 10 digits')
    
    # Validate first digit (6-9 for Indian mobile numbers)
    if phone_digits[0] not in '6789':
        raise ValueError('Phone number must start with 6, 7, 8, or 9')
    
    return phone_digits


def validate_positive_number(value: Union[int, float, str], field_name: str = "Value") -> float:
    """
    Validate that a value is a positive number.
    
    Args:
        value: Value to validate
        field_name: Name of field for error messages
    
    Returns:
        float: Validated positive number
    
    Raises:
        ValueError: If value is not a positive number
    
    Academic Note:
    This is a generic validator for numeric fields like prices, quantities,
    visitor counts, etc. We return float for maximum flexibility (handles
    both integers and decimals).
    
    Examples:
        >>> validate_positive_number(100, "Price")
        100.0
        >>> validate_positive_number("50.5", "Quantity")
        50.5
        >>> validate_positive_number(-10, "Amount")
        ValueError: Amount must be positive
    """
    try:
        num = float(value)
        if num <= 0:
            raise ValueError(f'{field_name} must be positive')
        return num
    except (ValueError, TypeError):
        raise ValueError(f'{field_name} must be a valid positive number')


# Academic Note on Input Validation Best Practices:
#
# 1. Validate Early:
#    - Validate as soon as input is received
#    - Fail fast with clear error messages
#
# 2. Whitelist vs Blacklist:
#    - Whitelist: Allow only known good input (preferred)
#    - Blacklist: Block known bad input (incomplete)
#    - Our email validator uses whitelist (only allows valid characters)
#
# 3. Layered Validation:
#    - Client-side: User experience (immediate feedback)
#    - Server-side: Security (never trust client)
#    - Database: Data integrity (constraints, foreign keys)
#
# 4. Error Messages:
#    - Be specific but not too revealing
#    - Help users fix errors
#    - Don't leak system information
#
# 5. Type Safety:
#    - Use type hints for documentation
#    - Validate types before processing
#    - Convert types explicitly (don't rely on implicit conversion)
#
# 6. Length Limits:
#    - Always enforce maximum lengths
#    - Prevents buffer overflow and DoS attacks
#    - Matches database column constraints
#
# 7. Character Encoding:
#    - Always use UTF-8
#    - Handle unicode properly
#    - Normalize input (NFC vs NFD)
#
# 8. Testing:
#    - Test with valid input
#    - Test with invalid input
#    - Test with edge cases (empty, null, very long)
#    - Test with malicious input (XSS, SQL injection)
