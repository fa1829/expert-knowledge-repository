"""
Utility functions for file handling, validation, and access control
"""
import os
import uuid
from functools import wraps
from flask import current_app, abort
from flask_login import current_user
from werkzeug.utils import secure_filename
from models import AccessControl, KnowledgeItem


def allowed_file(filename):
    """Check if file extension is allowed"""
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', '').split(',')
    if '.' not in filename:
        return False
    parts = filename.rsplit('.', 1)
    if len(parts) != 2 or not parts[1]:
        return False
    ext = parts[1].lower()
    return ext in allowed_extensions


def generate_unique_filename(original_filename):
    """Generate a unique filename while preserving extension"""
    if '.' not in original_filename:
        return f"{uuid.uuid4().hex}"
    parts = original_filename.rsplit('.', 1)
    if len(parts) != 2 or not parts[1]:
        return f"{uuid.uuid4().hex}"
    ext = parts[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return unique_name


def get_file_type(filename):
    """Determine file type based on extension"""
    if '.' not in filename:
        return 'other'
    parts = filename.rsplit('.', 1)
    if len(parts) != 2 or not parts[1]:
        return 'other'
    ext = parts[1].lower()
    
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp']
    video_extensions = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm']
    audio_extensions = ['mp3', 'wav', 'ogg', 'aac', 'flac']
    document_extensions = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt']
    
    if ext in image_extensions:
        return 'image'
    elif ext in video_extensions:
        return 'video'
    elif ext in audio_extensions:
        return 'audio'
    elif ext in document_extensions:
        return 'document'
    else:
        return 'other'


def get_upload_path(file_type):
    """Get upload directory path based on file type"""
    base_path = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    type_path = os.path.join(base_path, file_type)
    
    if not os.path.exists(type_path):
        os.makedirs(type_path)
    
    return type_path


def check_access(user, knowledge_item, required_permission='read'):
    """Check if user has access to a knowledge item"""
    # Admin has access to everything
    if user.role == 'admin':
        return True
    
    # Author has full access
    if knowledge_item.author_id == user.id:
        return True
    
    # Public items are readable by all authenticated users
    if knowledge_item.visibility == 'public' and required_permission == 'read':
        return True
    
    # Check explicit access control
    access = AccessControl.query.filter_by(
        knowledge_item_id=knowledge_item.id,
        user_id=user.id
    ).first()
    
    if access:
        if required_permission == 'read':
            return access.permission in ['read', 'write', 'admin']
        elif required_permission == 'write':
            return access.permission in ['write', 'admin']
        elif required_permission == 'admin':
            return access.permission == 'admin'
    
    return False


def require_access(required_permission='read'):
    """Decorator to check access to a knowledge item"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            item_id = kwargs.get('item_id')
            if not item_id:
                abort(400, description="Knowledge item ID required")
            
            knowledge_item = KnowledgeItem.query.get_or_404(item_id)
            
            if not current_user.is_authenticated:
                abort(401, description="Authentication required")
            
            if not check_access(current_user, knowledge_item, required_permission):
                abort(403, description="Access denied")
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403, description="Admin access required")
        return f(*args, **kwargs)
    return decorated_function
