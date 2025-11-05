"""CRUD Test Example - Category Model"""
import sys
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.category import Category
from app.core.config import settings

def test_create():
    """Test CREATE operation"""
    print("\n" + "=" * 60)
    print("1. CREATE - Creating a new category...")
    print("=" * 60)
    
    db: Session = SessionLocal()
    try:
        # Create a test category
        test_category = Category(
            name="Test Category",
            slug="test-category",
            description="This is a test category for CRUD operations"
        )
        db.add(test_category)
        db.commit()
        db.refresh(test_category)
        
        print(f"   ✓ Category created successfully!")
        print(f"   ID: {test_category.id}")
        print(f"   Name: {test_category.name}")
        print(f"   Slug: {test_category.slug}")
        print(f"   Description: {test_category.description}")
        print(f"   Created at: {test_category.created_at}")
        
        return test_category.id
    except Exception as e:
        db.rollback()
        print(f"   ✗ Failed to create category: {str(e)}")
        raise
    finally:
        db.close()

def test_read(category_id: int):
    """Test READ operation"""
    print("\n" + "=" * 60)
    print("2. READ - Reading category from database...")
    print("=" * 60)
    
    db: Session = SessionLocal()
    try:
        # Read by ID
        category = db.query(Category).filter(Category.id == category_id).first()
        
        if category:
            print(f"   ✓ Category found!")
            print(f"   ID: {category.id}")
            print(f"   Name: {category.name}")
            print(f"   Slug: {category.slug}")
            print(f"   Description: {category.description}")
            
            # Also test reading by slug
            category_by_slug = db.query(Category).filter(Category.slug == "test-category").first()
            if category_by_slug:
                print(f"\n   ✓ Category also found by slug lookup!")
            
            # Count all categories
            total_categories = db.query(Category).count()
            print(f"\n   Total categories in database: {total_categories}")
        else:
            print(f"   ✗ Category with ID {category_id} not found!")
            return False
        
        return True
    except Exception as e:
        print(f"   ✗ Failed to read category: {str(e)}")
        raise
    finally:
        db.close()

def test_update(category_id: int):
    """Test UPDATE operation"""
    print("\n" + "=" * 60)
    print("3. UPDATE - Updating category...")
    print("=" * 60)
    
    db: Session = SessionLocal()
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        
        if not category:
            print(f"   ✗ Category with ID {category_id} not found!")
            return False
        
        # Update category information
        old_name = category.name
        category.name = "Updated Test Category"
        category.description = "This category has been updated"
        
        db.commit()
        db.refresh(category)
        
        print(f"   ✓ Category updated successfully!")
        print(f"   Old name: {old_name}")
        print(f"   New name: {category.name}")
        print(f"   New description: {category.description}")
        print(f"   Updated at: {category.updated_at}")
        
        return True
    except Exception as e:
        db.rollback()
        print(f"   ✗ Failed to update category: {str(e)}")
        raise
    finally:
        db.close()

def test_delete(category_id: int):
    """Test DELETE operation"""
    print("\n" + "=" * 60)
    print("4. DELETE - Deleting category...")
    print("=" * 60)
    
    db: Session = SessionLocal()
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        
        if not category:
            print(f"   ✗ Category with ID {category_id} not found!")
            return False
        
        category_name = category.name
        db.delete(category)
        db.commit()
        
        # Verify deletion
        deleted_category = db.query(Category).filter(Category.id == category_id).first()
        if deleted_category is None:
            print(f"   ✓ Category '{category_name}' deleted successfully!")
            print(f"   ✓ Verified: Category no longer exists in database")
        else:
            print(f"   ✗ Deletion failed - category still exists!")
            return False
        
        return True
    except Exception as e:
        db.rollback()
        print(f"   ✗ Failed to delete category: {str(e)}")
        raise
    finally:
        db.close()

def test_list_all():
    """Test listing all records"""
    print("\n" + "=" * 60)
    print("5. LIST - Listing all categories...")
    print("=" * 60)
    
    db: Session = SessionLocal()
    try:
        categories = db.query(Category).all()
        
        print(f"   ✓ Found {len(categories)} category(ies) in database:")
        for category in categories[:5]:  # Show first 5
            print(f"     - ID: {category.id}, Name: {category.name}, Slug: {category.slug}")
        
        if len(categories) > 5:
            print(f"     ... and {len(categories) - 5} more")
        
        return True
    except Exception as e:
        print(f"   ✗ Failed to list categories: {str(e)}")
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
        
        if 'categories' in tables:
            print(f"   ✓ 'categories' table exists")
            print(f"   Found {len(tables)} table(s) in database")
            return True
        else:
            print(f"   ✗ 'categories' table does not exist!")
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
    print("CRUD TEST - Category Model")
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
        category_id = test_create()
        
        # Test READ
        if not test_read(category_id):
            print("\n✗ Read test failed, skipping remaining tests")
            return
        
        # Test UPDATE
        if not test_update(category_id):
            print("\n✗ Update test failed, skipping delete test")
            return
        
        # Test READ again to verify update
        print("\n" + "-" * 60)
        print("Verifying update by reading again...")
        test_read(category_id)
        
        # Test LIST
        test_list_all()
        
        # Test DELETE
        if not test_delete(category_id):
            print("\n✗ Delete test failed")
            return
        
        # Final verification
        print("\n" + "=" * 60)
        print("✓ ALL CRUD OPERATIONS PASSED!")
        print("=" * 60)
        print("\nSummary:")
        print("  ✓ CREATE - Category created successfully")
        print("  ✓ READ   - Category retrieved successfully")
        print("  ✓ UPDATE - Category updated successfully")
        print("  ✓ DELETE - Category deleted successfully")
        print("  ✓ LIST   - Categories listed successfully")
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

