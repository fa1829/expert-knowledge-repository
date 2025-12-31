# API Usage Examples

This document provides examples of how to use the Expert Knowledge Repository API.

## Authentication

### 1. Register a New User

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "researcher_jane",
    "email": "jane@university.edu",
    "password": "secure_password123",
    "role": "researcher"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "researcher_jane",
    "password": "secure_password123"
  }'
```

### 3. Get Current User Info

```bash
curl -X GET http://localhost:5000/auth/me \
  -b cookies.txt
```

## Knowledge Items

### 1. Create a Knowledge Item

```bash
curl -X POST http://localhost:5000/api/knowledge \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Introduction to Machine Learning",
    "description": "A comprehensive guide covering fundamental ML concepts",
    "content": "Machine learning is a subset of artificial intelligence...",
    "category": "education",
    "tags": "ml,ai,education,tutorial",
    "visibility": "public"
  }'
```

### 2. List All Knowledge Items

```bash
curl -X GET "http://localhost:5000/api/knowledge?page=1&per_page=20" \
  -b cookies.txt
```

### 3. List by Category

```bash
curl -X GET "http://localhost:5000/api/knowledge?category=education" \
  -b cookies.txt
```

### 4. Get a Specific Knowledge Item

```bash
curl -X GET http://localhost:5000/api/knowledge/1 \
  -b cookies.txt
```

### 5. Update a Knowledge Item

```bash
curl -X PUT http://localhost:5000/api/knowledge/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Introduction to Deep Learning",
    "description": "Updated comprehensive guide",
    "content": "Deep learning is a specialized subset of machine learning..."
  }'
```

### 6. Delete a Knowledge Item

```bash
curl -X DELETE http://localhost:5000/api/knowledge/1 \
  -b cookies.txt
```

## File Uploads

### 1. Upload a Document

```bash
curl -X POST http://localhost:5000/api/knowledge/1/document \
  -b cookies.txt \
  -F "file=@/path/to/document.pdf"
```

### 2. Upload Media (Image)

```bash
curl -X POST http://localhost:5000/api/knowledge/1/media \
  -b cookies.txt \
  -F "file=@/path/to/image.jpg"
```

### 3. Upload Media (Video)

```bash
curl -X POST http://localhost:5000/api/knowledge/1/media \
  -b cookies.txt \
  -F "file=@/path/to/video.mp4"
```

## Search

### 1. Search Knowledge Items

```bash
curl -X GET "http://localhost:5000/api/search?q=machine+learning&limit=10" \
  -b cookies.txt
```

### 2. Advanced Search with Multiple Terms

```bash
curl -X GET "http://localhost:5000/api/search?q=neural+networks+AND+deep+learning" \
  -b cookies.txt
```

## Access Control

### 1. Grant Access to a User

```bash
curl -X POST http://localhost:5000/api/access/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "user_id": 2,
    "permission": "read"
  }'
```

### 2. Grant Write Access

```bash
curl -X POST http://localhost:5000/api/access/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "user_id": 3,
    "permission": "write"
  }'
```

### 3. Revoke Access

```bash
curl -X DELETE http://localhost:5000/api/access/1/2 \
  -b cookies.txt
```

## Admin Functions

### 1. List All Users (Admin Only)

```bash
curl -X GET http://localhost:5000/api/users \
  -b cookies.txt
```

## Health Check

```bash
curl -X GET http://localhost:5000/health
```

## Python Example

```python
import requests

# Base URL
BASE_URL = "http://localhost:5000"

# Create a session
session = requests.Session()

# Login
login_data = {
    "username": "researcher_jane",
    "password": "secure_password123"
}
response = session.post(f"{BASE_URL}/auth/login", json=login_data)
print("Login:", response.json())

# Create a knowledge item
knowledge_data = {
    "title": "Neural Networks Basics",
    "description": "Understanding neural network fundamentals",
    "content": "Neural networks are computing systems...",
    "category": "education",
    "tags": "neural-networks,deep-learning,ai",
    "visibility": "public"
}
response = session.post(f"{BASE_URL}/api/knowledge", json=knowledge_data)
item_id = response.json()["id"]
print("Created item:", item_id)

# Upload a document
files = {"file": open("research_paper.pdf", "rb")}
response = session.post(f"{BASE_URL}/api/knowledge/{item_id}/document", files=files)
print("Document uploaded:", response.json())

# Search
response = session.get(f"{BASE_URL}/api/search", params={"q": "neural networks"})
print("Search results:", response.json())

# Logout
response = session.post(f"{BASE_URL}/auth/logout")
print("Logout:", response.json())
```

## JavaScript Example

```javascript
// Using fetch API
const BASE_URL = 'http://localhost:5000';

// Login
async function login(username, password) {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({ username, password }),
  });
  return response.json();
}

// Create knowledge item
async function createKnowledgeItem(data) {
  const response = await fetch(`${BASE_URL}/api/knowledge`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(data),
  });
  return response.json();
}

// Upload file
async function uploadDocument(itemId, file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${BASE_URL}/api/knowledge/${itemId}/document`, {
    method: 'POST',
    credentials: 'include',
    body: formData,
  });
  return response.json();
}

// Search
async function search(query) {
  const response = await fetch(`${BASE_URL}/api/search?q=${encodeURIComponent(query)}`, {
    credentials: 'include',
  });
  return response.json();
}

// Example usage
(async () => {
  await login('researcher_jane', 'secure_password123');
  
  const item = await createKnowledgeItem({
    title: 'AI Ethics',
    description: 'Ethical considerations in AI development',
    content: 'As AI systems become more prevalent...',
    category: 'research',
    tags: 'ethics,ai,research',
    visibility: 'public',
  });
  
  const results = await search('AI ethics');
  console.log(results);
})();
```
