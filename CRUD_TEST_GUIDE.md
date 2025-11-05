# CRUD Test Guide

This guide shows you how to test CRUD (Create, Read, Update, Delete) operations on your database to verify everything is working correctly.

## Prerequisites

1. **Database tables must exist** - Run migrations first:
   ```powershell
   # Service A
   cd services\service-a-identity-commerce
   .venv\Scripts\activate
   alembic upgrade head
   
   # Service B
   cd services\service-b-catalog-fulfillment
   .venv\Scripts\activate
   alembic upgrade head
   ```

2. **Dependencies installed** - Make sure requirements are installed

## Running CRUD Tests

### Service A - User Model Test

Tests CRUD operations on the `users` table:

```powershell
cd services\service-a-identity-commerce
.venv\Scripts\activate
python test_crud.py
```

**What it tests:**
- ✅ **CREATE** - Creates a new user with email, password, and role
- ✅ **READ** - Reads the user by ID and email
- ✅ **UPDATE** - Updates user's name and role
- ✅ **DELETE** - Deletes the test user
- ✅ **LIST** - Lists all users in the database

### Service B - Category Model Test

Tests CRUD operations on the `categories` table:

```powershell
cd services\service-b-catalog-fulfillment
.venv\Scripts\activate
python test_crud.py
```

**What it tests:**
- ✅ **CREATE** - Creates a new category
- ✅ **READ** - Reads the category by ID and slug
- ✅ **UPDATE** - Updates category name and description
- ✅ **DELETE** - Deletes the test category
- ✅ **LIST** - Lists all categories in the database

## Expected Output

When successful, you should see:

```
============================================================
CRUD TEST - User Model
============================================================

Database: ecom_identity_commerce
Host: scalable-microservices.c9i60askkyuh.eu-north-1.rds.amazonaws.com

============================================================
0. PREREQUISITE - Checking if tables exist...
============================================================
   ✓ 'users' table exists
   Found 8 table(s) in database

============================================================
1. CREATE - Creating a new user...
============================================================
   ✓ User created successfully!
   ID: 1
   Email: test@example.com
   Name: Test User
   Role: customer
   Created at: 2024-01-01 12:00:00

============================================================
2. READ - Reading user from database...
============================================================
   ✓ User found!
   ID: 1
   Email: test@example.com
   Name: Test User
   Role: customer
   ✓ User also found by email lookup!
   Total users in database: 1

============================================================
3. UPDATE - Updating user...
============================================================
   ✓ User updated successfully!
   Old name: Test User
   New name: Updated Test User
   New role: admin
   Updated at: 2024-01-01 12:01:00

...

============================================================
✓ ALL CRUD OPERATIONS PASSED!
============================================================

Summary:
  ✓ CREATE - User created successfully
  ✓ READ   - User retrieved successfully
  ✓ UPDATE - User updated successfully
  ✓ DELETE - User deleted successfully
  ✓ LIST   - Users listed successfully
```

## Troubleshooting

### "Table does not exist" Error
**Solution:** Run migrations first:
```powershell
alembic upgrade head
```

### "Connection failed" Error
**Solution:** 
1. Check your `.env` file has correct credentials
2. Verify RDS security group allows your IP
3. Test connection: `python test_db_connection.py`

### "Module not found" Error
**Solution:** Install dependencies:
```powershell
pip install -r requirements.txt
```

### "IntegrityError: duplicate key" Error
**Solution:** The test user/category already exists. Delete it manually or modify the test to use unique values.

## What This Verifies

Running these CRUD tests confirms:
1. ✅ Database connection is working
2. ✅ Tables are created correctly
3. ✅ SQLAlchemy models are working
4. ✅ Database transactions work (commit/rollback)
5. ✅ Foreign keys and constraints are set up
6. ✅ All CRUD operations function correctly

## Next Steps

After successful CRUD tests:
1. ✅ Your database is properly configured
2. ✅ Tables are created and accessible
3. ✅ You can start using the API endpoints
4. ✅ You can seed data using the seed scripts

## Customizing Tests

You can modify the test scripts to:
- Test different models
- Test with different data
- Test relationships between models
- Test complex queries
- Test transactions

The test scripts are located at:
- `services/service-a-identity-commerce/test_crud.py`
- `services/service-b-catalog-fulfillment/test_crud.py`

