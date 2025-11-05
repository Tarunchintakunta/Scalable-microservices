"""Script to create databases on RDS if they don't exist"""
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings

def create_database(db_name: str):
    """Create a database if it doesn't exist"""
    # Connect to default postgres database to create new databases
    default_url = settings.DATABASE_URL.replace(f"/{settings.DB_NAME}", "/postgres")
    
    print(f"\nCreating database: {db_name}")
    print(f"Connecting to: {default_url.split('@')[1] if '@' in default_url else 'RDS'}...")
    
    try:
        engine = create_engine(default_url, pool_pre_ping=True, isolation_level="AUTOCOMMIT")
        
        with engine.connect() as connection:
            # Check if database exists
            result = connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": db_name}
            )
            exists = result.fetchone()
            
            if exists:
                print(f"   [OK] Database '{db_name}' already exists")
                return True
            
            # Create database
            connection.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f"   [OK] Database '{db_name}' created successfully!")
            
            # Verify creation
            result = connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": db_name}
            )
            if result.fetchone():
                print(f"   [OK] Verified: Database '{db_name}' exists")
                return True
            else:
                print(f"   [ERROR] Database creation verification failed")
                return False
                
    except Exception as e:
        print(f"   [ERROR] Error creating database: {str(e)}")
        return False
    finally:
        engine.dispose()

def main():
    """Create required databases"""
    print("=" * 60)
    print("Database Creation Script")
    print("=" * 60)
    print(f"\nRDS Endpoint: {settings.DB_HOST}")
    print(f"Default database: postgres")
    
    databases = [
        "ecom_identity_commerce",
        "ecom_catalog_fulfillment"
    ]
    
    success = True
    for db_name in databases:
        if not create_database(db_name):
            success = False
    
    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] All databases created/verified!")
        print("\nNext steps:")
        print("1. Run migrations: alembic upgrade head")
        print("2. Test connection: python test_db_connection.py")
        print("3. Run CRUD tests: python test_crud.py")
    else:
        print("[FAILED] Some databases could not be created")
        print("Please check the errors above and ensure:")
        print("- You have CREATE DATABASE permissions")
        print("- RDS instance is accessible")
        sys.exit(1)
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

