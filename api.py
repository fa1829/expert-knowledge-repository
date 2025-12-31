"""
API routes for the Expert Knowledge Repository
"""
import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, KnowledgeItem, Document, MediaFile, User, AccessControl
from utils import (
    allowed_file, generate_unique_filename, get_file_type,
    get_upload_path, check_access, require_access, admin_required
)
from search import SearchIndex

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/knowledge', methods=['GET'])
@login_required
def list_knowledge_items():
    """List all accessible knowledge items"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    
    query = KnowledgeItem.query
    
    # Filter by visibility and access
    if current_user.role != 'admin':
        query = query.filter(
            db.or_(
                KnowledgeItem.visibility == 'public',
                KnowledgeItem.author_id == current_user.id
            )
        )
    
    if category:
        query = query.filter_by(category=category)
    
    pagination = query.order_by(KnowledgeItem.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    items = [
        {
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'category': item.category,
            'tags': item.tags,
            'visibility': item.visibility,
            'author': item.author.username,
            'created_at': item.created_at.isoformat(),
            'updated_at': item.updated_at.isoformat()
        }
        for item in pagination.items
    ]
    
    return jsonify({
        'items': items,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@api.route('/knowledge/<int:item_id>', methods=['GET'])
@login_required
@require_access('read')
def get_knowledge_item(item_id):
    """Get a specific knowledge item"""
    item = KnowledgeItem.query.get_or_404(item_id)
    
    return jsonify({
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'content': item.content,
        'category': item.category,
        'tags': item.tags,
        'visibility': item.visibility,
        'author': item.author.username,
        'created_at': item.created_at.isoformat(),
        'updated_at': item.updated_at.isoformat(),
        'documents': [
            {
                'id': doc.id,
                'filename': doc.original_filename,
                'file_type': doc.file_type,
                'file_size': doc.file_size
            }
            for doc in item.documents
        ],
        'media': [
            {
                'id': media.id,
                'filename': media.original_filename,
                'media_type': media.media_type,
                'file_size': media.file_size
            }
            for media in item.media_files
        ]
    })


@api.route('/knowledge', methods=['POST'])
@login_required
def create_knowledge_item():
    """Create a new knowledge item"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    item = KnowledgeItem(
        title=data['title'],
        description=data.get('description', ''),
        content=data.get('content', ''),
        category=data.get('category', ''),
        tags=data.get('tags', ''),
        visibility=data.get('visibility', 'public'),
        author_id=current_user.id
    )
    
    db.session.add(item)
    db.session.commit()
    
    # Add to search index
    search_index = SearchIndex(current_app.config['SEARCH_INDEX_PATH'])
    search_index.add_document(item)
    
    return jsonify({
        'id': item.id,
        'message': 'Knowledge item created successfully'
    }), 201


@api.route('/knowledge/<int:item_id>', methods=['PUT'])
@login_required
@require_access('write')
def update_knowledge_item(item_id):
    """Update a knowledge item"""
    item = KnowledgeItem.query.get_or_404(item_id)
    data = request.get_json()
    
    if 'title' in data:
        item.title = data['title']
    if 'description' in data:
        item.description = data['description']
    if 'content' in data:
        item.content = data['content']
    if 'category' in data:
        item.category = data['category']
    if 'tags' in data:
        item.tags = data['tags']
    if 'visibility' in data:
        item.visibility = data['visibility']
    
    db.session.commit()
    
    # Update search index
    search_index = SearchIndex(current_app.config['SEARCH_INDEX_PATH'])
    search_index.add_document(item)
    
    return jsonify({'message': 'Knowledge item updated successfully'})


@api.route('/knowledge/<int:item_id>', methods=['DELETE'])
@login_required
@require_access('admin')
def delete_knowledge_item(item_id):
    """Delete a knowledge item"""
    item = KnowledgeItem.query.get_or_404(item_id)
    
    # Delete associated files with error handling
    for doc in item.documents:
        try:
            if os.path.exists(doc.file_path):
                os.remove(doc.file_path)
        except OSError as e:
            current_app.logger.warning(f"Failed to delete document file {doc.file_path}: {e}")
    
    for media in item.media_files:
        try:
            if os.path.exists(media.file_path):
                os.remove(media.file_path)
            if media.thumbnail_path and os.path.exists(media.thumbnail_path):
                os.remove(media.thumbnail_path)
        except OSError as e:
            current_app.logger.warning(f"Failed to delete media file {media.file_path}: {e}")
    
    # Remove from search index
    search_index = SearchIndex(current_app.config['SEARCH_INDEX_PATH'])
    search_index.remove_document(item_id)
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Knowledge item deleted successfully'})


@api.route('/knowledge/<int:item_id>/document', methods=['POST'])
@login_required
@require_access('write')
def upload_document(item_id):
    """Upload a document to a knowledge item"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    item = KnowledgeItem.query.get_or_404(item_id)
    
    # Generate unique filename and save
    original_filename = secure_filename(file.filename)
    unique_filename = generate_unique_filename(original_filename)
    file_type = get_file_type(original_filename)
    upload_path = get_upload_path('documents')
    file_path = os.path.join(upload_path, unique_filename)
    
    file.save(file_path)
    file_size = os.path.getsize(file_path)
    
    # Create document record
    document = Document(
        filename=unique_filename,
        original_filename=original_filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        mime_type=file.content_type,
        uploader_id=current_user.id,
        knowledge_item_id=item_id
    )
    
    db.session.add(document)
    db.session.commit()
    
    return jsonify({
        'id': document.id,
        'message': 'Document uploaded successfully'
    }), 201


@api.route('/knowledge/<int:item_id>/media', methods=['POST'])
@login_required
@require_access('write')
def upload_media(item_id):
    """Upload media (image, video, audio) to a knowledge item"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    item = KnowledgeItem.query.get_or_404(item_id)
    
    # Generate unique filename and save
    original_filename = secure_filename(file.filename)
    unique_filename = generate_unique_filename(original_filename)
    file_type = get_file_type(original_filename)
    
    if file_type not in ['image', 'video', 'audio']:
        return jsonify({'error': 'Not a media file'}), 400
    
    upload_path = get_upload_path('media')
    file_path = os.path.join(upload_path, unique_filename)
    
    file.save(file_path)
    file_size = os.path.getsize(file_path)
    
    # Create media record
    media = MediaFile(
        filename=unique_filename,
        original_filename=original_filename,
        file_path=file_path,
        media_type=file_type,
        file_size=file_size,
        mime_type=file.content_type,
        uploader_id=current_user.id,
        knowledge_item_id=item_id
    )
    
    db.session.add(media)
    db.session.commit()
    
    return jsonify({
        'id': media.id,
        'message': 'Media uploaded successfully'
    }), 201


@api.route('/search', methods=['GET'])
@login_required
def search_knowledge():
    """Search knowledge items"""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 20, type=int)
    
    if not query:
        return jsonify({'results': []})
    
    search_index = SearchIndex(current_app.config['SEARCH_INDEX_PATH'])
    results = search_index.search(query, limit=limit)
    
    # Filter results based on access control
    accessible_results = []
    for result in results:
        item = KnowledgeItem.query.get(result['id'])
        if item and check_access(current_user, item, 'read'):
            accessible_results.append(result)
    
    return jsonify({'results': accessible_results})


@api.route('/users', methods=['GET'])
@login_required
@admin_required
def list_users():
    """List all users (admin only)"""
    users = User.query.all()
    return jsonify({
        'users': [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat()
            }
            for user in users
        ]
    })


@api.route('/access/<int:item_id>', methods=['POST'])
@login_required
@require_access('admin')
def grant_access(item_id):
    """Grant access to a knowledge item"""
    data = request.get_json()
    
    if not data or not data.get('user_id'):
        return jsonify({'error': 'User ID is required'}), 400
    
    user = User.query.get_or_404(data['user_id'])
    permission = data.get('permission', 'read')
    
    # Check if access already exists
    access = AccessControl.query.filter_by(
        knowledge_item_id=item_id,
        user_id=user.id
    ).first()
    
    if access:
        access.permission = permission
    else:
        access = AccessControl(
            knowledge_item_id=item_id,
            user_id=user.id,
            permission=permission
        )
        db.session.add(access)
    
    db.session.commit()
    
    return jsonify({'message': 'Access granted successfully'})


@api.route('/access/<int:item_id>/<int:user_id>', methods=['DELETE'])
@login_required
@require_access('admin')
def revoke_access(item_id, user_id):
    """Revoke access to a knowledge item"""
    access = AccessControl.query.filter_by(
        knowledge_item_id=item_id,
        user_id=user_id
    ).first_or_404()
    
    db.session.delete(access)
    db.session.commit()
    
    return jsonify({'message': 'Access revoked successfully'})
