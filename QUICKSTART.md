# Quick Start Guide - E-Commerce MVP

Get the e-commerce platform running in 5 minutes!

## Prerequisites Check

```bash
# Check Node.js (need 18+)
node --version

# Check Python (need 3.11+)
python3 --version

# Check PostgreSQL
psql --version
```

If any are missing, install them first.

## One-Command Setup

```bash
./setup.sh
```

This script will:
1. ✅ Create PostgreSQL databases
2. ✅ Setup all Python virtual environments
3. ✅ Install all dependencies
4. ✅ Run database migrations
5. ✅ Seed demo data
6. ✅ Configure environment files

## Start Services

### Option 1: Using tmux (Recommended)

```bash
./start-all.sh
```

This starts all 4 services in separate tmux windows.

**tmux Commands**:
- `Ctrl+B` then `n` - Next window
- `Ctrl+B` then `p` - Previous window
- `Ctrl+B` then `d` - Detach (services keep running)
- `tmux attach -t ecommerce` - Reattach
- `Ctrl+C` in each window - Stop services

### Option 2: Manual (4 Terminals)

**Terminal 1 - Service A**:
```bash
cd services/service-a-identity-commerce
source .venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

**Terminal 2 - Service B**:
```bash
cd services/service-b-catalog-fulfillment
source .venv/bin/activate
uvicorn app.main:app --reload --port 8002
```

**Terminal 3 - Service C**:
```bash
cd services/service-c-notifications-serverless
source .venv/bin/activate
uvicorn app.main:app --reload --port 8010
```

**Terminal 4 - Frontend**:
```bash
cd frontend
npm run dev
```

## Access the Application

🌐 **Frontend**: http://localhost:5173

📚 **API Documentation**:
- Service A: http://localhost:8001/docs
- Service B: http://localhost:8002/docs
- Service C: http://localhost:8010/docs

## Demo Accounts

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | Admin@123 | Admin |
| alice@example.com | Alice@123 | Customer |
| bob@example.com | Bob@123 | Customer |

## Test the Flow

1. **Login** as alice@example.com
2. **Browse** products on homepage
3. **Add to cart** - Click any product
4. **Checkout** - Use test card: `4242 4242 4242 4242`
5. **View order** - Check order history

## Stripe Test Mode

The app uses Stripe test mode. Use these test cards:

- **Success**: 4242 4242 4242 4242
- **Decline**: 4000 0000 0000 0002
- **Requires Auth**: 4000 0025 0000 3155

Any future expiry date and any 3-digit CVC.

## Troubleshooting

### Port Already in Use

```bash
# Find and kill process on port 8001
lsof -i :8001
kill -9 <PID>
```

### Database Connection Error

```bash
# Check PostgreSQL is running
brew services list | grep postgresql
# or
sudo systemctl status postgresql

# Start if needed
brew services start postgresql
# or
sudo systemctl start postgresql
```

### Module Not Found (Python)

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Module Not Found (Node)

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

- Read [README.md](./README.md) for full documentation
- Check [ARCHITECTURE.md](./docs/ARCHITECTURE.md) for system design
- Explore API docs at `/docs` endpoints
- Customize `.env` files for your needs

## Common Tasks

### Reset Database

```bash
# Drop and recreate
dropdb ecom_identity_commerce
dropdb ecom_catalog_fulfillment
createdb ecom_identity_commerce
createdb ecom_catalog_fulfillment

# Run migrations and seed
cd services/service-a-identity-commerce
source .venv/bin/activate
alembic upgrade head
python scripts/seed.py

cd ../service-b-catalog-fulfillment
source .venv/bin/activate
alembic upgrade head
python scripts/seed.py
```

### Add New Product (via API)

```bash
# Get admin token first
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"Admin@123"}'

# Use token to create product
curl -X POST http://localhost:8002/admin/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "New Product",
    "slug": "new-product",
    "description": "Description",
    "base_price": 29.99,
    "category_id": 1
  }'
```

### View Logs

All services output to console. Check the terminal where each service is running.

## Support

If you encounter issues:

1. Check the terminal output for error messages
2. Verify all prerequisites are installed
3. Ensure PostgreSQL is running
4. Check that all ports (8001, 8002, 8010, 5173) are available
5. Review the [README.md](./README.md) for detailed setup

Happy coding! 🚀
