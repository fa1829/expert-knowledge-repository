"""
Database models for the Expert Knowledge Repository
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, educator, researcher, expert, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    knowledge_items = db.relationship('KnowledgeItem', backref='author', lazy=True)
    documents = db.relationship('Document', backref='uploader', lazy=True)
    media_files = db.relationship('MediaFile', backref='uploader', lazy=True)
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify user password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class KnowledgeItem(db.Model):
    """Main knowledge item model"""
    __tablename__ = 'knowledge_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    category = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    visibility = db.Column(db.String(20), default='public')  # public, private, restricted
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documents = db.relationship('Document', backref='knowledge_item', lazy=True, cascade='all, delete-orphan')
    media_files = db.relationship('MediaFile', backref='knowledge_item', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<KnowledgeItem {self.title}>'


class Document(db.Model):
    """Document model for file attachments"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    knowledge_item_id = db.Column(db.Integer, db.ForeignKey('knowledge_items.id'))
    
    def __repr__(self):
        return f'<Document {self.original_filename}>'


class MediaFile(db.Model):
    """Media file model for images, videos, and audio"""
    __tablename__ = 'media_files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    media_type = db.Column(db.String(50))  # image, video, audio
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    thumbnail_path = db.Column(db.String(500))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    knowledge_item_id = db.Column(db.Integer, db.ForeignKey('knowledge_items.id'))
    
    def __repr__(self):
        return f'<MediaFile {self.original_filename}>'


class AccessControl(db.Model):
    """Access control model for knowledge items"""
    __tablename__ = 'access_control'
    
    id = db.Column(db.Integer, primary_key=True)
    knowledge_item_id = db.Column(db.Integer, db.ForeignKey('knowledge_items.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    permission = db.Column(db.String(20), default='read')  # read, write, admin
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AccessControl Item:{self.knowledge_item_id} User:{self.user_id}>'
