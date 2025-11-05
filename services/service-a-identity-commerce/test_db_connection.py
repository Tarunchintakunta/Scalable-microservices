"""Test script to verify database configuration and connection"""
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings

def test_configuration():
    """Test that configuration is loaded correctly"""
    print("=" * 60)
    print("Testing Database Configuration - Service A")
    print("=" * 60)
    
    print(f"\n1. Configuration loaded:")
    print(f"   DB_HOST: {settings.DB_HOST}")
    print(f"   DB_PORT: {settings.DB_PORT}")
    print(f"   DB_USER: {settings.DB_USER}")
    print(f"   DB_NAME: {settings.DB_NAME}")
    print(f"   DB_PASSWORD: {'*' * len(settings.DB_PASSWORD) if settings.DB_PASSWORD else 'None'}")
    
    print(f"\n2. Constructed DATABASE_URL:")
    print(f"   {settings.DATABASE_URL.replace(settings.DB_PASSWORD, '***' if settings.DB_PASSWORD else '')}")
    
    return True

def test_connection():
    """Test database connection"""
    print("\n3. Testing database connection...")
    try:
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"   [OK] Connection successful!")
            print(f"   PostgreSQL version: {version.split(',')[0]}")
            
            # Check if database exists and is accessible
            result = connection.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            print(f"   Current database: {db_name}")
            
            return True
    except Exception as e:
        print(f"   [ERROR] Connection failed: {str(e)}")
        return False

def test_database_exists():
    """Check if the database exists"""
    print("\n4. Checking database...")
    try:
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT current_database();"))
            db_name = result.fetchone()[0]
            print(f"   [OK] Database '{db_name}' is accessible")
            return True
    except Exception as e:
        print(f"   [ERROR] Database check failed: {str(e)}")
        return False

def check_tables():
    """Check existing tables"""
    print("\n5. Checking existing tables...")
    try:
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result]
            if tables:
                print(f"   Found {len(tables)} table(s):")
                for table in tables:
                    print(f"     - {table}")
            else:
                print("   No tables found yet. Run migrations to create tables.")
            return True
    except Exception as e:
        print(f"   [ERROR] Failed to check tables: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n")
    success = True
    
    try:
        success &= test_configuration()
        success &= test_connection()
        success &= test_database_exists()
        success &= check_tables()
        
        print("\n" + "=" * 60)
        if success:
            print("[SUCCESS] All checks passed! Configuration is correct.")
            print("\nNext steps:")
            print("1. Run migrations: alembic upgrade head")
            print("2. Seed data (optional): python scripts/seed.py")
        else:
            print("[FAILED] Some checks failed. Please review the errors above.")
            sys.exit(1)
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\n[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

