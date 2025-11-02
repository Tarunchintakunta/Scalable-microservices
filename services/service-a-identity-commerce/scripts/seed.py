"""Seed script for Service A - Identity & Commerce"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal, engine, Base
from app.models import User, Address
from app.core.security import get_password_hash


def seed_database():
    """Seed the database with initial data"""
    print("Seeding Service A database...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).count() > 0:
            print("Database already seeded. Skipping...")
            return
        
        # Create admin user
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("Admin@123"),
            full_name="Admin User",
            role="admin"
        )
        db.add(admin)
        
        # Create customer users
        alice = User(
            email="alice@example.com",
            hashed_password=get_password_hash("Alice@123"),
            full_name="Alice Johnson",
            role="customer"
        )
        db.add(alice)
        
        bob = User(
            email="bob@example.com",
            hashed_password=get_password_hash("Bob@123"),
            full_name="Bob Smith",
            role="customer"
        )
        db.add(bob)
        
        db.commit()
        db.refresh(alice)
        db.refresh(bob)
        
        # Create addresses for Alice
        alice_address1 = Address(
            user_id=alice.id,
            address_type="both",
            street="123 Main St",
            city="San Francisco",
            state="CA",
            postal_code="94102",
            country="USA",
            is_default=True
        )
        db.add(alice_address1)
        
        alice_address2 = Address(
            user_id=alice.id,
            address_type="shipping",
            street="456 Oak Ave",
            city="Los Angeles",
            state="CA",
            postal_code="90001",
            country="USA",
            is_default=False
        )
        db.add(alice_address2)
        
        # Create address for Bob
        bob_address = Address(
            user_id=bob.id,
            address_type="both",
            street="789 Pine Rd",
            city="New York",
            state="NY",
            postal_code="10001",
            country="USA",
            is_default=True
        )
        db.add(bob_address)
        
        db.commit()
        
        print("✓ Created 3 users (1 admin, 2 customers)")
        print("✓ Created 3 addresses")
        print("\nDemo Users:")
        print("  Admin: admin@example.com / Admin@123")
        print("  Customer 1: alice@example.com / Alice@123")
        print("  Customer 2: bob@example.com / Bob@123")
        print("\nService A seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
