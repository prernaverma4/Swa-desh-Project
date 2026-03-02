"""
File Upload Utilities for Digital Catalyst Platform

This module provides secure file upload handling utilities for image uploads
in the Digital Catalyst platform. It implements security best practices including:
- File extension validation
- Secure filename sanitization
- File size limits
- Path traversal prevention

Academic Context:
-----------------
File upload security is critical in web applications. Common vulnerabilities include:
1. Arbitrary File Upload: Attackers upload executable files (e.g., .php, .exe)
2. Path Traversal: Malicious filenames like "../../etc/passwd" access restricted areas
3. Denial of Service: Large files consume server resources
4. Content Type Spoofing: Files with misleading extensions

This module addresses these vulnerabilities through:
- Whitelist-based extension validation (only allow known safe types)
- werkzeug.secure_filename() to sanitize filenames and prevent path traversal
- File size validation before saving
- Unique filename generation to prevent overwrites

References:
- OWASP File Upload Cheat Sheet
- CWE-434: Unrestricted Upload of File with Dangerous Type
- werkzeug.utils.secure_filename documentation
"""

import os
from werkzeug.utils import secure_filename
from datetime import datetime

# Allowed file extensions for image uploads
# Only permit common image formats to prevent executable uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Maximum file size: 5MB (5 * 1024 * 1024 bytes)
# Prevents denial of service attacks via large file uploads
MAX_FILE_SIZE = 5 * 1024 * 1024


def allowed_file(filename):
    """
    Check if a filename has an allowed extension.
    
    Security Note:
    Uses whitelist approach - only explicitly allowed extensions are permitted.
    This is more secure than blacklist approach (blocking specific extensions).
    
    Args:
        filename (str): The filename to validate
        
    Returns:
        bool: True if extension is allowed, False otherwise
        
    Example:
        >>> allowed_file('photo.jpg')
        True
        >>> allowed_file('script.php')
        False
        >>> allowed_file('image.PNG')  # Case insensitive
        True
    """
    # Check if filename contains a dot and extension is in allowed set
    # rsplit('.', 1) splits from right, handling filenames with multiple dots
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file_size(file):
    """
    Validate that uploaded file does not exceed maximum size limit.
    
    Security Note:
    File size validation prevents denial of service attacks where attackers
    upload extremely large files to consume server disk space and bandwidth.
    
    Args:
        file: FileStorage object from Flask request.files
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
        
    Example:
        >>> is_valid, error = validate_file_size(uploaded_file)
        >>> if not is_valid:
        ...     flash(error, 'danger')
    """
    # Seek to end of file to get size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    # Reset file pointer to beginning for subsequent reads
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        size_mb = file_size / (1024 * 1024)
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        return False, f"File size ({size_mb:.2f}MB) exceeds maximum allowed size ({max_mb}MB)"
    
    return True, None


def generate_unique_filename(original_filename):
    """
    Generate a unique filename to prevent overwrites and collisions.
    
    Implementation:
    Combines timestamp with original filename to ensure uniqueness.
    Format: {timestamp}_{secure_filename}
    
    Args:
        original_filename (str): Original uploaded filename
        
    Returns:
        str: Unique, secure filename
        
    Example:
        >>> generate_unique_filename('my photo.jpg')
        '20240214_153045_my_photo.jpg'
    """
    # Sanitize filename first to remove dangerous characters
    safe_filename = secure_filename(original_filename)
    
    # Generate timestamp prefix
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Combine timestamp with filename
    return f"{timestamp}_{safe_filename}"


def save_uploaded_image(file, upload_folder):
    """
    Securely save an uploaded image file to the specified folder.
    
    This function implements multiple security checks:
    1. Validates file extension is allowed
    2. Validates file size is within limits
    3. Sanitizes filename to prevent path traversal
    4. Generates unique filename to prevent overwrites
    5. Creates upload directory if it doesn't exist
    
    Args:
        file: FileStorage object from Flask request.files
        upload_folder (str): Relative path to upload directory (e.g., 'static/uploads/heritage')
        
    Returns:
        tuple: (success: bool, result: str)
            - If success: (True, relative_file_path)
            - If failure: (False, error_message)
            
    Example:
        >>> from flask import request
        >>> file = request.files['image']
        >>> success, result = save_uploaded_image(file, 'static/uploads/products')
        >>> if success:
        ...     product.image_url = result
        ...     db.session.commit()
        ... else:
        ...     flash(result, 'danger')
    
    Academic Note:
    This function demonstrates defense-in-depth security strategy:
    multiple layers of validation ensure comprehensive protection.
    """
    # Validation 1: Check if file exists
    if not file or file.filename == '':
        return False, "No file selected"
    
    # Validation 2: Check file extension
    if not allowed_file(file.filename):
        return False, f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Validation 3: Check file size
    is_valid_size, size_error = validate_file_size(file)
    if not is_valid_size:
        return False, size_error
    
    # Generate secure, unique filename
    unique_filename = generate_unique_filename(file.filename)
    
    # Ensure upload directory exists
    # exist_ok=True prevents error if directory already exists
    os.makedirs(upload_folder, exist_ok=True)
    
    # Construct full file path
    file_path = os.path.join(upload_folder, unique_filename)
    
    try:
        # Save file to disk
        file.save(file_path)
        
        # Return relative path for database storage
        # This allows flexibility in deployment (different static file servers)
        return True, file_path
        
    except Exception as e:
        # Catch any file system errors (permissions, disk full, etc.)
        return False, f"Error saving file: {str(e)}"


def delete_uploaded_image(file_path):
    """
    Safely delete an uploaded image file.
    
    Used when updating or deleting records with associated images.
    Prevents orphaned files from accumulating on disk.
    
    Args:
        file_path (str): Relative path to the file to delete
        
    Returns:
        bool: True if deleted successfully, False otherwise
        
    Example:
        >>> # When updating heritage site image
        >>> if heritage_site.image_url:
        ...     delete_uploaded_image(heritage_site.image_url)
        >>> success, new_path = save_uploaded_image(new_file, 'static/uploads/heritage')
        >>> heritage_site.image_url = new_path
    """
    try:
        # Check if file exists before attempting deletion
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        # Log error but don't raise exception
        # Missing files shouldn't break the application
        print(f"Error deleting file {file_path}: {str(e)}")
        return False
