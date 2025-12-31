"""
Tests for authentication functionality
"""
import json


def test_register_user(client):
    """Test user registration"""
    response = client.post('/auth/register', 
        json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['username'] == 'newuser'
    assert 'message' in data


def test_register_duplicate_username(client, regular_user):
    """Test registration with duplicate username"""
    response = client.post('/auth/register',
        json={
            'username': 'user',
            'email': 'another@example.com',
            'password': 'password123'
        }
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'already exists' in data['error'].lower()


def test_login_success(client, regular_user):
    """Test successful login"""
    response = client.post('/auth/login',
        json={
            'username': 'user',
            'password': 'user123'
        }
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['username'] == 'user'
    assert data['role'] == 'user'


def test_login_invalid_credentials(client, regular_user):
    """Test login with invalid credentials"""
    response = client.post('/auth/login',
        json={
            'username': 'user',
            'password': 'wrongpassword'
        }
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'invalid' in data['error'].lower()


def test_logout(client, regular_user):
    """Test logout"""
    # Login first
    client.post('/auth/login',
        json={
            'username': 'user',
            'password': 'user123'
        }
    )
    
    # Then logout
    response = client.post('/auth/logout')
    assert response.status_code == 200


def test_get_current_user(client, regular_user):
    """Test getting current user info"""
    # Login first
    client.post('/auth/login',
        json={
            'username': 'user',
            'password': 'user123'
        }
    )
    
    # Get current user
    response = client.get('/auth/me')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['username'] == 'user'
    assert data['email'] == 'user@example.com'
