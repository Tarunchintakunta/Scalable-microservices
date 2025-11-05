# Database Setup Guide

Complete guide for setting up and verifying PostgreSQL database connection with AWS RDS.

## Quick Start

1. **Install Dependencies**:
   ```powershell
   cd services\service-a-identity-commerce
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Security Group** (see Security Group Setup below)

3. **Create Databases** (if not exists):
   ```powershell
   python create_databases.py
   ```

4. **Test Connection**:
   ```powershell
   python test_db_connection.py
   ```

5. **Run Migrations**:
   ```powershell
   alembic upgrade head
   ```

6. **Test CRUD Operations**:
   ```powershell
   python test_crud.py
   ```

## Security Group Setup

### Step-by-Step:

1. **AWS Console** → RDS → Your Database → **Connectivity & security**
2. **Click Security Group** link
3. **Inbound rules** → **Edit inbound rules** → **Add rule**:
   - **Type:** `PostgreSQL`
   - **Port:** `5432`
   - **Source:** Your IP address (or `0.0.0.0/0` for testing only)
4. **Save rules**

### ⚠️ Security Warning

**DO NOT use "All Traffic, All Protocols, All Ports"** - Only open port 5432 for PostgreSQL.

### Verify Public Access

Ensure **Publicly accessible** is set to **Yes** in RDS instance settings.

## Configuration Files

Both services use `.env` files with these parameters:

```env
DB_HOST=scalable-microservices.c9i60askkyuh.eu-north-1.rds.amazonaws.com
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=ecom_identity_commerce  # or ecom_catalog_fulfillment
```

The config automatically constructs `DATABASE_URL` from these parameters.

## Testing

### Connection Test

```powershell
cd services\service-a-identity-commerce
python test_db_connection.py
```

### CRUD Test

After running migrations:

```powershell
python test_crud.py
```

## Expected Output

### Successful Connection Test:
```
[OK] Connection successful!
PostgreSQL version: PostgreSQL 17.6
Current database: ecom_identity_commerce
[OK] Database 'ecom_identity_commerce' is accessible
```

### Successful CRUD Test:
```
[OK] CREATE - User created successfully
[OK] READ   - User retrieved successfully
[OK] UPDATE - User updated successfully
[OK] DELETE - User deleted successfully
[OK] LIST   - Users listed successfully
```

## Troubleshooting

- **Connection refused:** Check security group allows your IP on port 5432
- **Database doesn't exist:** Run `python create_databases.py`
- **Tables not found:** Run `alembic upgrade head`
- **Connection timeout:** Verify RDS is publicly accessible
- **Module not found:** Install dependencies with `pip install -r requirements.txt`

## Files Reference

- `test_db_connection.py` - Test database connection
- `test_crud.py` - Test CRUD operations  
- `create_databases.py` - Create databases if needed
- `.env` - Database configuration (not in git)

