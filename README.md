# Expert Knowledge Repository

A modular knowledge repository platform designed for educators, researchers, and industry experts to store, manage, and share knowledge with robust media support, document management, search indexing, access control, and cloud deployment capabilities.

## Features

- **📚 Knowledge Management**: Create, read, update, and delete knowledge items with rich metadata (title, description, content, category, tags)
- **📄 Document Support**: Upload and manage various document formats (PDF, DOC, DOCX, TXT)
- **🎬 Media Management**: Handle images, videos, and audio files with organized storage
- **🔍 Full-Text Search**: Powered by Whoosh for fast and accurate search across all knowledge items
- **🔐 Access Control**: Role-based access (admin, educator, researcher, expert, user) with granular permissions
- **👥 User Authentication**: Secure registration, login, and session management
- **☁️ Cloud-Ready**: Docker containerization for easy deployment to any cloud platform
- **🔄 RESTful API**: Comprehensive API for all operations
- **📊 Modular Architecture**: Clean separation of concerns for easy maintenance and extension

## Technology Stack

- **Backend**: Flask (Python 3.11+)
- **Database**: SQLAlchemy with SQLite (easily configurable for PostgreSQL/MySQL)
- **Search**: Whoosh full-text search engine
- **Authentication**: Flask-Login with bcrypt password hashing
- **API**: RESTful JSON API
- **Containerization**: Docker and Docker Compose

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/fa1829/expert-knowledge-repository.git
cd expert-knowledge-repository
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env and set your configuration
```

5. **Initialize the database**:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Docker Deployment

### Using Docker Compose

1. **Build and run**:
```bash
docker-compose up -d
```

2. **Access the application**:
```
http://localhost:5000
```

3. **Stop the application**:
```bash
docker-compose down
```

### Using Docker only

1. **Build the image**:
```bash
docker build -t expert-knowledge-repo .
```

2. **Run the container**:
```bash
docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads expert-knowledge-repo
```

## API Documentation

### Authentication Endpoints

#### Register a new user
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "role": "user"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

#### Logout
```http
POST /auth/logout
```

#### Get current user info
```http
GET /auth/me
```

### Knowledge Item Endpoints

#### List all knowledge items
```http
GET /api/knowledge?page=1&per_page=20&category=education
```

#### Get a specific knowledge item
```http
GET /api/knowledge/{item_id}
```

#### Create a knowledge item
```http
POST /api/knowledge
Content-Type: application/json

{
  "title": "Introduction to Machine Learning",
  "description": "A comprehensive guide to ML basics",
  "content": "Machine learning is...",
  "category": "education",
  "tags": "ml,ai,learning",
  "visibility": "public"
}
```

#### Update a knowledge item
```http
PUT /api/knowledge/{item_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description"
}
```

#### Delete a knowledge item
```http
DELETE /api/knowledge/{item_id}
```

### File Upload Endpoints

#### Upload a document
```http
POST /api/knowledge/{item_id}/document
Content-Type: multipart/form-data

file: [document file]
```

#### Upload media (image, video, audio)
```http
POST /api/knowledge/{item_id}/media
Content-Type: multipart/form-data

file: [media file]
```

### Search Endpoint

#### Search knowledge items
```http
GET /api/search?q=machine+learning&limit=20
```

### Access Control Endpoints

#### Grant access to a knowledge item
```http
POST /api/access/{item_id}
Content-Type: application/json

{
  "user_id": 2,
  "permission": "read"
}
```

#### Revoke access
```http
DELETE /api/access/{item_id}/{user_id}
```

## User Roles and Permissions

- **admin**: Full access to all resources and administrative functions
- **educator**: Can create and manage educational content
- **researcher**: Can create and manage research materials
- **expert**: Can create and share expert knowledge
- **user**: Basic access to public content

## Access Control Levels

- **public**: Accessible to all authenticated users
- **private**: Only accessible to the author
- **restricted**: Accessible based on explicit access control rules

## Configuration

Key environment variables (see `.env.example`):

- `SECRET_KEY`: Flask secret key for session management
- `DATABASE_URL`: Database connection string
- `UPLOAD_FOLDER`: Directory for uploaded files
- `MAX_CONTENT_LENGTH`: Maximum upload file size (bytes)
- `ALLOWED_EXTENSIONS`: Comma-separated list of allowed file extensions
- `SEARCH_INDEX_PATH`: Directory for search index files

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=. --cov-report=html
```

## Project Structure

```
expert-knowledge-repository/
├── app.py                 # Main application file
├── models.py              # Database models
├── auth.py                # Authentication routes
├── api.py                 # API routes
├── search.py              # Search indexing module
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── conftest.py            # Test configuration
├── test_auth.py           # Authentication tests
├── test_api.py            # API tests
└── README.md              # This file
```

## Security Features

- Password hashing with bcrypt
- Session-based authentication
- Role-based access control (RBAC)
- Granular permission system
- File type validation
- File size limits
- Secure filename handling

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Future Enhancements

- [ ] PostgreSQL/MySQL support
- [ ] S3/Cloud storage integration
- [ ] Real-time collaboration
- [ ] Version control for knowledge items
- [ ] Advanced analytics and reporting
- [ ] REST API rate limiting
- [ ] GraphQL API
- [ ] Mobile application
- [ ] Advanced search filters
- [ ] Content recommendation system