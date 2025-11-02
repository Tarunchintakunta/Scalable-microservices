# Microservices Web Application

A scalable microservices-based web application with React frontend and Node.js backend services, designed for AWS deployment.

## 🏗️ Architecture

- **Frontend**: React + Vite + TypeScript
- **Backend Services**:
  - `user-service`: Authentication and user management
  - `product-service`: Product catalog management
- **Infrastructure**: Docker, Docker Compose (local), AWS ECS/Fargate (production)

## 📁 Project Structure

```
/project-root
├── backend/
│   ├── user-service/       # Authentication microservice
│   └── product-service/    # Product management microservice
├── frontend/               # React application
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md
│   └── AWS_SETUP.md
├── docker-compose.yml      # Local development environment
└── README.md
```

## 🚀 Quick Start (Local Development)

### Prerequisites
- Node.js 18+
- Docker & Docker Compose
- npm or yarn

### 1. Start All Services
```bash
docker-compose up --build
```

### 2. Access Applications
- **Frontend**: http://localhost:3000
- **User Service**: http://localhost:4001
- **Product Service**: http://localhost:4002
- **PostgreSQL**: localhost:5432

### 3. Stop Services
```bash
docker-compose down
```

## 🔧 Development

### Backend Services

#### User Service (Port 4001)
```bash
cd backend/user-service
npm install
npm run dev
```

**Endpoints**:
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /me` - Get current user (requires auth)

#### Product Service (Port 4002)
```bash
cd backend/product-service
npm install
npm run dev
```

**Endpoints**:
- `GET /products` - List all products
- `POST /products` - Create product
- `GET /products/:id` - Get product by ID

### Frontend (Port 3000)
```bash
cd frontend
npm install
npm run dev
```

## 🌐 AWS Deployment

See [AWS_SETUP.md](./docs/AWS_SETUP.md) for detailed AWS deployment instructions.

### AWS Services Used
- Amazon ECS (Fargate)
- Application Load Balancer (ALB)
- Amazon API Gateway
- AWS CloudWatch
- AWS X-Ray
- AWS Auto Scaling
- AWS Cloud Map

## 📚 Documentation

- [Architecture Overview](./docs/ARCHITECTURE.md)
- [AWS Setup Guide](./docs/AWS_SETUP.md)

## 🔐 Environment Variables

Each service requires environment variables. See `.env.example` in each service directory.

## 🧪 Testing

```bash
# Test user service
curl -X POST http://localhost:4001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

# Test product service
curl http://localhost:4002/products
```

## 📝 License

MIT
