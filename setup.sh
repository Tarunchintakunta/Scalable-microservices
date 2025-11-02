#!/bin/bash

# E-Commerce MVP Setup Script
# This script sets up the entire development environment

set -e  # Exit on error

echo "================================================"
echo "E-Commerce MVP - Setup Script"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi
echo -e "${GREEN}✓ Node.js $(node --version)${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.11+ from https://python.org/"
    exit 1
fi
echo -e "${GREEN}✓ Python $(python3 --version)${NC}"

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL is not installed${NC}"
    echo "Please install PostgreSQL from https://www.postgresql.org/"
    exit 1
fi
echo -e "${GREEN}✓ PostgreSQL installed${NC}"

echo ""
echo "================================================"
echo "Step 1: Creating Databases"
echo "================================================"

# Create databases
echo "Creating PostgreSQL databases..."
createdb ecom_identity_commerce 2>/dev/null || echo "Database ecom_identity_commerce already exists"
createdb ecom_catalog_fulfillment 2>/dev/null || echo "Database ecom_catalog_fulfillment already exists"
echo -e "${GREEN}✓ Databases created${NC}"

echo ""
echo "================================================"
echo "Step 2: Setting up Service A (Identity & Commerce)"
echo "================================================"

cd services/service-a-identity-commerce

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null

# Copy env file
if [ ! -f .env ]; then
    cp .env.sample .env
    echo -e "${YELLOW}⚠ Created .env file. Please update with your Stripe keys!${NC}"
fi

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Seed database
echo "Seeding database with demo data..."
python scripts/seed.py

deactivate
cd ../..

echo -e "${GREEN}✓ Service A setup complete${NC}"

echo ""
echo "================================================"
echo "Step 3: Setting up Service B (Catalog & Fulfillment)"
echo "================================================"

cd services/service-b-catalog-fulfillment

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null

# Copy env file
if [ ! -f .env ]; then
    cp .env.sample .env
fi

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Seed database
echo "Seeding database with demo data..."
python scripts/seed.py

deactivate
cd ../..

echo -e "${GREEN}✓ Service B setup complete${NC}"

echo ""
echo "================================================"
echo "Step 4: Setting up Service C (Notifications)"
echo "================================================"

cd services/service-c-notifications-serverless

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null

# Copy env file
if [ ! -f .env ]; then
    cp .env.sample .env
fi

deactivate
cd ../..

echo -e "${GREEN}✓ Service C setup complete${NC}"

echo ""
echo "================================================"
echo "Step 5: Setting up Frontend"
echo "================================================"

cd frontend

# Install dependencies
echo "Installing npm dependencies (this may take a while)..."
npm install > /dev/null 2>&1

# Copy env file
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠ Created .env file. Please update with your Stripe publishable key!${NC}"
fi

cd ..

echo -e "${GREEN}✓ Frontend setup complete${NC}"

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "Demo Users:"
echo "  Admin:     admin@example.com / Admin@123"
echo "  Customer:  alice@example.com / Alice@123"
echo "  Customer:  bob@example.com / Bob@123"
echo ""
echo "To start the services:"
echo ""
echo "Terminal 1 - Service A:"
echo "  cd services/service-a-identity-commerce"
echo "  source .venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8001"
echo ""
echo "Terminal 2 - Service B:"
echo "  cd services/service-b-catalog-fulfillment"
echo "  source .venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8002"
echo ""
echo "Terminal 3 - Service C:"
echo "  cd services/service-c-notifications-serverless"
echo "  source .venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8010"
echo ""
echo "Terminal 4 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then visit: http://localhost:5173"
echo ""
echo "API Documentation:"
echo "  Service A: http://localhost:8001/docs"
echo "  Service B: http://localhost:8002/docs"
echo "  Service C: http://localhost:8010/docs"
echo ""
echo "================================================"
