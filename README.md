# E-Commerce MVP - Microservices Architecture

A production-quality, local-first e-commerce platform built with React + Vite frontend and Python FastAPI microservices. Features include user authentication, product catalog, shopping cart, Stripe payments, order management, and store locator with interactive maps.

## 🏗️ Architecture

### Tech Stack
- **Frontend**: React 18 + Vite + TypeScript + Tailwind CSS
- **Backend**: Python 3.11 + FastAPI + SQLAlchemy 2.x
- **Database**: PostgreSQL (2 separate databases)
- **Payments**: Stripe (test mode)
- **Maps**: Leaflet + OpenStreetMap
- **State Management**: Zustand
- **API Client**: Axios + React Query

### Microservices

#### Service A - Identity & Commerce (Port 8001)
- User authentication (JWT)
- Address management
- Shopping cart
- Checkout & payments (Stripe)
- Order management
- Webhooks

#### Service B - Catalog & Fulfillment (Port 8002)
- Product catalog
- Categories & variants
- Inventory management (two-phase commit)
- Search functionality
- Reviews
- Store locations (with lat/lng)
- Fulfillment tracking

#### Service C - Notifications (Port 8010)
- Serverless-style notification service
- Email/SMS stubs (console logging)
- Event handlers (ORDER_PLACED, ORDER_PAID, ORDER_SHIPPED, LOW_STOCK)
- Lambda-ready architecture

## 📁 Project Structure

```
ecommerce-mvp/
├── README.md
├── Makefile                    # Build automation
├── .env.sample
├── .gitignore
│
├── frontend/                   # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── store/            # Zustand stores
│   │   ├── types/            # TypeScript types
│   │   ├── config/           # Configuration
│   │   └── lib/              # Utilities
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── .env.example
│
├── services/
│   ├── service-a-identity-commerce/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── api/          # FastAPI routers
│   │   │   ├── models/       # SQLAlchemy models
│   │   │   ├── schemas/      # Pydantic schemas
│   │   │   ├── core/         # Config, security, deps
│   │   │   ├── services/     # Business logic
│   │   │   └── db/           # Database session
│   │   ├── alembic/          # Database migrations
│   │   ├── scripts/          # Seed scripts
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   ├── alembic.ini
│   │   └── .env.sample
│   │
│   ├── service-b-catalog-fulfillment/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── api/
│   │   │   ├── models/
│   │   │   ├── schemas/
│   │   │   ├── core/
│   │   │   └── db/
│   │   ├── alembic/
│   │   ├── scripts/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   ├── alembic.ini
│   │   └── .env.sample
│   │
│   └── service-c-notifications-serverless/
│       ├── app/
│       │   ├── main.py           # FastAPI wrapper
│       │   ├── lambda_like.py    # Lambda handler
│       │   └── providers/        # Email/SMS stubs
│       ├── requirements.txt
│       └── .env.sample
│
└── docs/                       # Documentation & screenshots
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** running locally
- **Git**

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ecommerce-mvp
```

### 2. Create Databases

```bash
createdb ecom_identity_commerce
createdb ecom_catalog_fulfillment
```

Or use the Makefile:
```bash
make initdb
```

### 3. Setup Service A (Identity & Commerce)

```bash
cd services/service-a-identity-commerce

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.sample .env
# Edit .env with your settings (Stripe keys, etc.)

# Run migrations
alembic upgrade head

# Seed demo data
python scripts/seed.py

# Start service
uvicorn app.main:app --reload --port 8001
```

### 4. Setup Service B (Catalog & Fulfillment)

```bash
cd services/service-b-catalog-fulfillment

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.sample .env

# Run migrations
alembic upgrade head

# Seed demo data
python scripts/seed.py

# Start service
uvicorn app.main:app --reload --port 8002
```

### 5. Setup Service C (Notifications)

```bash
cd services/service-c-notifications-serverless

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.sample .env

# Start service
uvicorn app.main:app --reload --port 8010
```

### 6. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with API URLs and Stripe publishable key

# Start development server
npm run dev
```

### 7. Access the Application

- **Frontend**: http://localhost:5173
- **Service A API Docs**: http://localhost:8001/docs
- **Service B API Docs**: http://localhost:8002/docs
- **Service C API Docs**: http://localhost:8010/docs

## 🎯 Demo Flow

### Demo Users (Created by Seed Scripts)

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | Admin@123 | Admin |
| alice@example.com | Alice@123 | Customer |
| bob@example.com | Bob@123 | Customer |

### Test the Application

1. **Browse Products**
   - Visit http://localhost:5173
   - View featured products on homepage
   - Browse categories
   - Search for products

2. **User Registration & Login**
   - Sign up with a new account or login with demo credentials
   - View/edit profile
   - Add shipping/billing addresses

3. **Shopping**
   - Add products to cart
   - Update quantities
   - View cart total

4. **Checkout**
   - Select shipping and billing addresses
   - Enter payment details (use Stripe test card: `4242 4242 4242 4242`)
   - Complete purchase

5. **Order Management**
   - View order history
   - Track order status
   - See order timeline

6. **Admin Features** (login as admin@example.com)
   - Manage products
   - Update order status
   - View all orders

7. **Store Locator**
   - Find nearby stores on interactive map
   - View store details

### Stripe Test Cards

- **Success**: 4242 4242 4242 4242
- **Decline**: 4000 0000 0000 0002
- Use any future expiry date and any 3-digit CVC

## 🛠️ Development

### Using Makefile

```bash
# Initialize databases
make initdb

# Run migrations for all services
make migrate

# Seed all databases
make seed

# Run tests
make test

# Clean up (drop databases and virtual environments)
make clean
```

### Manual Database Operations

```bash
# Service A migrations
cd services/service-a-identity-commerce
source .venv/bin/activate
alembic revision --autogenerate -m "Description"
alembic upgrade head

# Service B migrations
cd services/service-b-catalog-fulfillment
source .venv/bin/activate
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Running Tests

```bash
# Service A tests
cd services/service-a-identity-commerce
source .venv/bin/activate
pytest

# Service B tests
cd services/service-b-catalog-fulfillment
source .venv/bin/activate
pytest

# Frontend tests
cd frontend
npm test
```

## 📡 API Endpoints

### Service A - Identity & Commerce

#### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

#### Addresses
- `GET /addresses` - List user addresses
- `POST /addresses` - Create address
- `PUT /addresses/{id}` - Update address
- `DELETE /addresses/{id}` - Delete address

#### Cart
- `GET /cart` - Get user cart
- `POST /cart/items` - Add item to cart
- `PUT /cart/items/{id}` - Update cart item
- `DELETE /cart/items/{id}` - Remove from cart

#### Checkout
- `POST /checkout/create-payment-intent` - Create Stripe payment intent
- `POST /checkout/confirm` - Confirm payment

#### Orders
- `GET /orders` - List user orders
- `GET /orders/{id}` - Get order details
- `POST /admin/orders/{id}/status` - Update order status (admin)

#### Webhooks
- `POST /payments/webhook` - Stripe webhook handler

### Service B - Catalog & Fulfillment

#### Catalog
- `GET /catalog/categories` - List categories
- `GET /catalog/products` - List products
- `GET /catalog/products/{id}` - Get product details
- `GET /catalog/search?q=query` - Search products

#### Admin (Catalog)
- `POST /admin/categories` - Create category
- `POST /admin/products` - Create product
- `PUT /admin/products/{id}` - Update product
- `DELETE /admin/products/{id}` - Delete product

#### Inventory
- `GET /inventory/{sku}` - Get inventory for SKU
- `POST /inventory/reserve` - Reserve inventory
- `POST /inventory/commit` - Commit reservation
- `POST /inventory/release` - Release reservation

#### Stores
- `GET /stores` - List all stores
- `GET /stores/nearby?lat=&lng=&radius_km=` - Find nearby stores
- `GET /stores/{id}` - Get store details

#### Reviews
- `GET /reviews/product/{id}` - Get product reviews
- `POST /reviews` - Create review

### Service C - Notifications

- `POST /notify` - Send notification event
- `GET /health` - Health check

## 🔐 Security

- **JWT Authentication**: HS256 algorithm with configurable expiry
- **Password Hashing**: bcrypt via passlib
- **CORS**: Configured for localhost:5173
- **Input Validation**: Pydantic schemas
- **SQL Injection Protection**: SQLAlchemy ORM
- **Rate Limiting**: Simple in-memory limiter on auth endpoints

## 🗄️ Database Schema

### Service A Tables
- `users` - User accounts
- `addresses` - User addresses
- `carts` - Shopping carts
- `cart_items` - Cart line items
- `orders` - Orders
- `order_items` - Order line items
- `payments` - Payment records

### Service B Tables
- `categories` - Product categories
- `products` - Products
- `product_images` - Product images
- `variants` - Product variants (SKUs)
- `inventory` - Stock levels
- `reviews` - Product reviews
- `stores` - Physical store locations
- `fulfillments` - Order fulfillment tracking

## 🧪 Testing

### Backend Tests (Pytest)

```bash
# Service A
cd services/service-a-identity-commerce
pytest tests/ -v

# Service B
cd services/service-b-catalog-fulfillment
pytest tests/ -v
```

### Frontend Tests (Vitest)

```bash
cd frontend
npm test
```

## 🚢 Deployment

### Environment Variables

Ensure all `.env` files are properly configured:

**Service A (.env)**:
```env
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/ecom_identity_commerce
JWT_SECRET=your-secret-key
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

**Service B (.env)**:
```env
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/ecom_catalog_fulfillment
```

**Frontend (.env)**:
```env
VITE_SERVICE_A_URL=https://api-a.yourdomain.com
VITE_SERVICE_B_URL=https://api-b.yourdomain.com
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### Production Checklist

- [ ] Update JWT_SECRET to a strong random value
- [ ] Configure production Stripe keys
- [ ] Set up SSL/TLS certificates
- [ ] Configure production database connections
- [ ] Enable database backups
- [ ] Set up monitoring and logging
- [ ] Configure CORS for production domain
- [ ] Review and harden security settings
- [ ] Set up CI/CD pipeline
- [ ] Configure auto-scaling

## 📚 Additional Documentation

- **API Documentation**: Available at `/docs` and `/redoc` endpoints
- **Database Migrations**: See `alembic/` directories
- **Seed Data**: See `scripts/seed.py` files

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready

# Verify databases exist
psql -l | grep ecom
```

### Port Already in Use
```bash
# Find process using port
lsof -i :8001

# Kill process
kill -9 <PID>
```

### Migration Issues
```bash
# Reset migrations (⚠️ destroys data)
alembic downgrade base
alembic upgrade head
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 👥 Authors

Built as a production-quality e-commerce MVP demonstrating microservices architecture with Python FastAPI and React.

---

**Note**: This is a development setup. For production deployment, consider containerization (Docker), orchestration (Kubernetes), API gateways, service mesh, and cloud-native services.
