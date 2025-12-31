"""
Admin utility script for Expert Knowledge Repository
"""
import sys
import os
from app import create_app
from models import db, User, KnowledgeItem
from search import SearchIndex


def create_admin_user(username, email, password):
    """Create an admin user"""
    app = create_app()
    with app.app_context():
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"Error: User '{username}' already exists")
            return False
        
        # Create admin user
        user = User(
            username=username,
            email=email,
            role='admin'
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        print(f"✓ Admin user '{username}' created successfully")
        return True


def list_users():
    """List all users"""
    app = create_app()
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("No users found")
            return
        
        print("\nUsers:")
        print("-" * 80)
        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Role':<15} {'Active':<10}")
        print("-" * 80)
        
        for user in users:
            print(f"{user.id:<5} {user.username:<20} {user.email:<30} {user.role:<15} {'Yes' if user.is_active else 'No':<10}")


def reindex_all():
    """Rebuild the search index"""
    app = create_app()
    with app.app_context():
        items = KnowledgeItem.query.all()
        search_index = SearchIndex(app.config['SEARCH_INDEX_PATH'])
        search_index.reindex_all(items)
        
        print(f"✓ Reindexed {len(items)} knowledge items")


def show_stats():
    """Show repository statistics"""
    app = create_app()
    with app.app_context():
        user_count = User.query.count()
        item_count = KnowledgeItem.query.count()
        
        print("\nRepository Statistics:")
        print("-" * 40)
        print(f"Users: {user_count}")
        print(f"Knowledge Items: {item_count}")
        
        # Count by category
        categories = db.session.query(
            KnowledgeItem.category,
            db.func.count(KnowledgeItem.id)
        ).group_by(KnowledgeItem.category).all()
        
        if categories:
            print("\nBy Category:")
            for category, count in categories:
                print(f"  {category or 'Uncategorized'}: {count}")


def main():
    """Main CLI function"""
    if len(sys.argv) < 2:
        print("Expert Knowledge Repository - Admin Utility")
        print("\nUsage:")
        print("  python admin.py create-admin <username> <email> <password>")
        print("  python admin.py list-users")
        print("  python admin.py reindex")
        print("  python admin.py stats")
        return
    
    command = sys.argv[1]
    
    if command == "create-admin":
        if len(sys.argv) != 5:
            print("Usage: python admin.py create-admin <username> <email> <password>")
            return
        create_admin_user(sys.argv[2], sys.argv[3], sys.argv[4])
    
    elif command == "list-users":
        list_users()
    
    elif command == "reindex":
        reindex_all()
    
    elif command == "stats":
        show_stats()
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: create-admin, list-users, reindex, stats")


if __name__ == "__main__":
    main()
