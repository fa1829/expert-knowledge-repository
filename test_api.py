"""
Tests for API functionality
"""
import json


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'Expert Knowledge Repository' in data['name']


def test_create_knowledge_item(client, admin_user):
    """Test creating a knowledge item"""
    # Login first
    client.post('/auth/login',
        json={
            'username': 'admin',
            'password': 'admin123'
        }
    )
    
    response = client.post('/api/knowledge',
        json={
            'title': 'New Knowledge Item',
            'description': 'Description',
            'content': 'Content',
            'category': 'education',
            'tags': 'learning,test',
            'visibility': 'public'
        }
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['message'] == 'Knowledge item created successfully'


def test_list_knowledge_items(client, admin_user, knowledge_item):
    """Test listing knowledge items"""
    # Login first
    client.post('/auth/login',
        json={
            'username': 'admin',
            'password': 'admin123'
        }
    )
    
    response = client.get('/api/knowledge')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert len(data['items']) > 0


def test_get_knowledge_item(client, admin_user, knowledge_item):
    """Test getting a specific knowledge item"""
    # Login first
    client.post('/auth/login',
        json={
            'username': 'admin',
            'password': 'admin123'
        }
    )
    
    response = client.get(f'/api/knowledge/{knowledge_item["id"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Test Knowledge Item'
    assert data['category'] == 'test'


def test_update_knowledge_item(client, admin_user, knowledge_item):
    """Test updating a knowledge item"""
    # Login first
    client.post('/auth/login',
        json={
            'username': 'admin',
            'password': 'admin123'
        }
    )
    
    response = client.put(f'/api/knowledge/{knowledge_item["id"]}',
        json={
            'title': 'Updated Title',
            'description': 'Updated description'
        }
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'updated successfully' in data['message'].lower()


def test_delete_knowledge_item(client, admin_user, knowledge_item):
    """Test deleting a knowledge item"""
    # Login first
    client.post('/auth/login',
        json={
            'username': 'admin',
            'password': 'admin123'
        }
    )
    
    response = client.delete(f'/api/knowledge/{knowledge_item["id"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'deleted successfully' in data['message'].lower()


def test_search_knowledge(client, admin_user, knowledge_item):
    """Test searching knowledge items"""
    # Login first
    client.post('/auth/login',
        json={
            'username': 'admin',
            'password': 'admin123'
        }
    )
    
    response = client.get('/api/search?q=test')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'results' in data


def test_unauthorized_access(client):
    """Test that unauthorized users cannot access protected endpoints"""
    response = client.get('/api/knowledge')
    # Flask-Login redirects to login page (302), not 401
    assert response.status_code == 302


def test_access_control(client, regular_user, knowledge_item):
    """Test access control for private items"""
    # Login as regular user
    client.post('/auth/login',
        json={
            'username': 'user',
            'password': 'user123'
        }
    )
    
    # Should be able to access public item
    response = client.get(f'/api/knowledge/{knowledge_item["id"]}')
    assert response.status_code == 200
