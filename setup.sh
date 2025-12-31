#!/bin/bash

# Expert Knowledge Repository - Setup Script

echo "======================================"
echo "Expert Knowledge Repository Setup"
echo "======================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python $PYTHON_VERSION detected"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠ Please edit .env file and set your SECRET_KEY"
fi

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p uploads/documents uploads/media
mkdir -p search_index

# Initialize database
echo ""
echo "Initializing database..."
python3 << END
from app import create_app
from models import db

app = create_app()
with app.app_context():
    db.create_all()
    print("✓ Database initialized")
END

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "To start the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the application: python app.py"
echo ""
echo "The application will be available at http://localhost:5000"
