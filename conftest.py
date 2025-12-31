"""
Test configuration and fixtures
"""
import os
import pytest
from app import create_app
from models import db, User, KnowledgeItem


@pytest.fixture
def app():
    """Create and configure a test application instance"""
    config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key',
        'UPLOAD_FOLDER': '/tmp/test_uploads',
        'SEARCH_INDEX_PATH': '/tmp/test_search_index',
        'WTF_CSRF_ENABLED': False
    }
    
    app = create_app(config)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    
    # Cleanup test directories
    import shutil
    for path in ['/tmp/test_uploads', '/tmp/test_search_index']:
        if os.path.exists(path):
            shutil.rmtree(path)


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def admin_user(app):
    """Create an admin user for testing"""
    with app.app_context():
        user = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    return {'id': user_id, 'username': 'admin', 'password': 'admin123'}


@pytest.fixture
def regular_user(app):
    """Create a regular user for testing"""
    with app.app_context():
        user = User(
            username='user',
            email='user@example.com',
            role='user'
        )
        user.set_password('user123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    return {'id': user_id, 'username': 'user', 'password': 'user123'}


@pytest.fixture
def knowledge_item(app, admin_user):
    """Create a knowledge item for testing"""
    with app.app_context():
        item = KnowledgeItem(
            title='Test Knowledge Item',
            description='Test description',
            content='Test content',
            category='test',
            tags='test,sample',
            visibility='public',
            author_id=admin_user['id']
        )
        db.session.add(item)
        db.session.commit()
        item_id = item.id
    
    return {'id': item_id, 'title': 'Test Knowledge Item'}
