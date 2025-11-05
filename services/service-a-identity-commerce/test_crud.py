"""CRUD Test Example - User Model"""
import sys
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.core.config import settings

def test_create():
    """Test CREATE operation"""
    print("\n" + "=" * 60)
    print("1. CREATE - Creating a new user...")
    print("=" * 60)
    
    db: Session = SessionLocal()
    try:
        # Create a test user
        test_user = User(
            email="test@example.com",
            hashed_password=get_password_hash("testpassword123"),
            full_name="Test User",
            role=UserRole.CUSTOMER
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"   ✓ User created successfully!")
        print(f"   ID: {test_user.id}")
        print(f"   Email: {test_user.email}")
        print(f"   Name: {test_user.full_name}")
        print(f"   Role: {test_user.role.value}")
        print(f"   Created at: {test_user.created_at}")
        
        return test_user.id
    except Exception as e:
        db.rollback()
        print(f"   ✗ Failed to create user: {str(e)}")
        raise
    finally:
        db.close()

def test_read(user_id: int):
    """Test READ operation"""
    print("\n" + "=" * 60)
    print("2. READ - Reading user from database...")
    print("=" * 60)
    
    db: Session = SessionLocal()
    try:
        # Read by ID
        user = db.query(User).filter(User.id == user_id).first()
        
        if user:
            print(f"   ✓ User found!")
            print(f"   ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   Name: {user.full_name}")
            print(f"   Role: {user.role.value}")
            
            # Also test reading by email
            user_by_email = db.query(User).filter(User.email == "test@example.com").first()
            if user_by_email:
                print(f"\n   ✓ User also found by email lookup!")
            
            # Count all users
            total_users = db.query(User).count()
            print(f"\n   Total users in database: {total_users}")
        else:
            print(f"   ✗ User with ID {user_id} not found!")
            return False
        
        return True
    except Exception as e:
        print(f"   ✗ Failed to read user: {str(e)}")
        raise
    finally:
        db.close()

def test_update(user_id: int):
    """Test UPDATE operation"""
    print("\n" + "=" * 60)
    print("3. UPDATE - Updating user...")
    print("=" * 60)
    
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            print(f"   ✗ User with ID {user_id} not found!")
            return False
        
        # Update user information
        old_name = user.full_name
        user.full_name = "Updated Test User"
        user.role = UserRole.ADMIN
        
        db.commit()
        db.refresh(user)
        
        print(f"   ✓ User updated successfully!")
        print(f"   Old name: {old_name}")
        print(f"   New name: {user.full_name}")
        print(f"   New role: {user.role.value}")
        print(f"   Updated at: {user.updated_at}")
        
        return True
    except Exception as e:
        db.rollback()
        print(f"   ✗ Failed to update user: {str(e)}")
        raise
    finally:
        db.close()

def test_delete(user_id: int):
    """Test DELETE operation"""
    print("\n" + "=" * 60)
    print("4. DELETE - Deleting user...")
    print("=" * 60)
    
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            print(f"   ✗ User with ID {user_id} not found!")
            return False
        
        user_email = user.email
        db.delete(user)
        db.commit()
        
        # Verify deletion
        deleted_user = db.query(User).filter(User.id == user_id).first()
        if deleted_user is None:
            print(f"   ✓ User '{user_email}' deleted successfully!")
            print(f"   ✓ Verified: User no longer exists in database")
        else:
            print(f"   ✗ Deletion failed - user still exists!")
            return False
        
        return True
    except Exception as e:
        db.rollback()
        print(f"   ✗ Failed to delete user: {str(e)}")
        raise
    finally:
        db.close()

def test_list_all():
    """Test listing all records"""
    print("\n" + "=" * 60)
    print("5. LIST - Listing all users...")
    print("=" * 60)
    
    db: Session = SessionLocal()
    try:
        users = db.query(User).all()
        
        print(f"   ✓ Found {len(users)} user(s) in database:")
        for user in users[:5]:  # Show first 5
            print(f"     - ID: {user.id}, Email: {user.email}, Name: {user.full_name}")
        
        if len(users) > 5:
            print(f"     ... and {len(users) - 5} more")
        
        return True
    except Exception as e:
        print(f"   ✗ Failed to list users: {str(e)}")
        raise
    finally:
        db.close()

def check_tables_exist():
    """Check if required tables exist"""
    print("\n" + "=" * 60)
    print("0. PREREQUISITE - Checking if tables exist...")
    print("=" * 60)
    
    db: Session = SessionLocal()
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.get_bind())
        tables = inspector.get_table_names()
        
        if 'users' in tables:
            print(f"   ✓ 'users' table exists")
            print(f"   Found {len(tables)} table(s) in database")
            return True
        else:
            print(f"   ✗ 'users' table does not exist!")
            print(f"   Available tables: {', '.join(tables) if tables else 'None'}")
            print(f"\n   Please run migrations first:")
            print(f"   alembic upgrade head")
            return False
    except Exception as e:
        print(f"   ✗ Error checking tables: {str(e)}")
        return False
    finally:
        db.close()

def main():
    """Run all CRUD tests"""
    print("\n" + "=" * 60)
    print("CRUD TEST - User Model")
    print("=" * 60)
    print(f"\nDatabase: {settings.DB_NAME}")
    print(f"Host: {settings.DB_HOST}")
    
    try:
        # Check if tables exist first
        if not check_tables_exist():
            print("\n✗ Tables not found. Please run migrations first!")
            print("   Command: alembic upgrade head")
            sys.exit(1)
        
        # Test CREATE
        user_id = test_create()
        
        # Test READ
        if not test_read(user_id):
            print("\n✗ Read test failed, skipping remaining tests")
            return
        
        # Test UPDATE
        if not test_update(user_id):
            print("\n✗ Update test failed, skipping delete test")
            return
        
        # Test READ again to verify update
        print("\n" + "-" * 60)
        print("Verifying update by reading again...")
        test_read(user_id)
        
        # Test LIST
        test_list_all()
        
        # Test DELETE
        if not test_delete(user_id):
            print("\n✗ Delete test failed")
            return
        
        # Final verification
        print("\n" + "=" * 60)
        print("✓ ALL CRUD OPERATIONS PASSED!")
        print("=" * 60)
        print("\nSummary:")
        print("  ✓ CREATE - User created successfully")
        print("  ✓ READ   - User retrieved successfully")
        print("  ✓ UPDATE - User updated successfully")
        print("  ✓ DELETE - User deleted successfully")
        print("  ✓ LIST   - Users listed successfully")
        print("\n" + "=" * 60 + "\n")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("✗ CRUD TEST FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

