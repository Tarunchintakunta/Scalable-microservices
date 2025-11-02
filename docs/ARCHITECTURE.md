# E-Commerce MVP - Architecture Documentation

## System Overview

This e-commerce platform follows a microservices architecture with three backend services and a React frontend. Services communicate via REST APIs and are designed to be independently deployable.

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│                    http://localhost:5173                         │
│                                                                   │
│  Pages: Home, Catalog, Product, Cart, Checkout, Orders,         │
│         Login, Signup, Profile, Addresses, Store Locator        │
└────────────┬──────────────────────────────────┬─────────────────┘
             │                                   │
             │ HTTP/REST                         │ HTTP/REST
             │                                   │
    ┌────────▼────────┐                 ┌───────▼────────┐
    │   Service A     │                 │   Service B    │
    │  Identity &     │◄────────────────┤   Catalog &    │
    │   Commerce      │   Inter-service │  Fulfillment   │
    │  Port: 8001     │   Communication │  Port: 8002    │
    └────────┬────────┘                 └───────┬────────┘
             │                                   │
             │                                   │
    ┌────────▼────────┐                         │
    │  PostgreSQL DB  │                ┌────────▼────────┐
    │   identity_     │                │  PostgreSQL DB  │
    │   commerce      │                │   catalog_      │
    └─────────────────┘                │  fulfillment    │
                                       └─────────────────┘
             │
             │ Event notifications
             │
    ┌────────▼────────┐
    │   Service C     │
    │  Notifications  │
    │  Port: 8010     │
    │  (Serverless)   │
    └─────────────────┘
```

## Service Responsibilities

### Service A - Identity & Commerce
**Port**: 8001  
**Database**: `ecom_identity_commerce`

**Responsibilities**:
- User authentication and authorization (JWT)
- User profile management
- Address management (shipping/billing)
- Shopping cart operations
- Checkout process
- Payment processing (Stripe integration)
- Order management
- Webhook handling (Stripe)

**Key Models**:
- User
- Address
- Cart, CartItem
- Order, OrderItem
- Payment

**External Dependencies**:
- Stripe API (payments)
- Service B (inventory checks)
- Service C (notifications)

### Service B - Catalog & Fulfillment
**Port**: 8002  
**Database**: `ecom_catalog_fulfillment`

**Responsibilities**:
- Product catalog management
- Category management
- Product variants (SKUs)
- Inventory management (two-phase commit)
- Product search
- Product reviews
- Store location management
- Fulfillment tracking

**Key Models**:
- Category
- Product, ProductImage, Variant
- Inventory
- Review
- Store
- Fulfillment

**External Dependencies**:
- Service C (low stock notifications)

### Service C - Notifications
**Port**: 8010  
**No Database** (stateless)

**Responsibilities**:
- Email notifications (stubbed)
- SMS notifications (stubbed)
- Event handling (ORDER_PLACED, ORDER_PAID, ORDER_SHIPPED, LOW_STOCK)
- Lambda-ready architecture

**Design Pattern**:
- Serverless-style with `handle_event()` function
- Can be deployed to AWS Lambda
- Currently runs as FastAPI app locally

## Data Flow Examples

### 1. User Registration & Login

```
User → Frontend → Service A
                   ├─ Hash password (bcrypt)
                   ├─ Store in DB
                   ├─ Generate JWT token
                   └─ Return token + user data
```

### 2. Product Browse & Search

```
User → Frontend → Service B
                   ├─ Query products from DB
                   ├─ Apply filters (category, search)
                   ├─ Join with images, variants
                   └─ Return product list
```

### 3. Add to Cart

```
User → Frontend → Service A
                   ├─ Authenticate user (JWT)
                   ├─ Get/Create cart
                   ├─ Add cart item
                   └─ Return updated cart
```

### 4. Checkout Process

```
User → Frontend → Service A
                   │
                   ├─ Create payment intent
                   │   ├─ Validate cart
                   │   ├─ Calculate totals
                   │   ├─ Create order (status: created)
                   │   ├─ Call Stripe API
                   │   └─ Return client_secret
                   │
                   ├─ Confirm payment (after Stripe.js)
                   │   ├─ Verify with Stripe
                   │   ├─ Update order (status: paid)
                   │   ├─ Clear cart
                   │   └─ Notify Service C
                   │
                   └─ Service C sends email
```

### 5. Inventory Management (Two-Phase Commit)

```
Checkout → Service A → Service B
                        │
                        ├─ Reserve inventory
                        │   ├─ Check availability
                        │   ├─ Increment reserved count
                        │   └─ Return success/failure
                        │
                        ├─ Commit (on payment success)
                        │   └─ Finalize reservation
                        │
                        └─ Release (on cancel)
                            └─ Decrement reserved count
```

## Security Architecture

### Authentication Flow

```
1. User Login
   ├─ POST /auth/login {email, password}
   ├─ Verify password hash
   ├─ Generate JWT token
   │   ├─ Payload: {sub: user_id, exp: timestamp}
   │   ├─ Algorithm: HS256
   │   └─ Secret: JWT_SECRET
   └─ Return {access_token, user}

2. Authenticated Requests
   ├─ Header: Authorization: Bearer <token>
   ├─ Decode & verify token
   ├─ Extract user_id
   ├─ Load user from DB
   └─ Attach to request context
```

### Authorization

- **Role-Based Access Control (RBAC)**
  - Roles: `admin`, `customer`
  - Admin endpoints protected by `get_current_admin` dependency
  - Customer endpoints protected by `get_current_user` dependency

### Security Measures

- Password hashing with bcrypt
- JWT tokens with expiration
- CORS configured for specific origins
- Input validation with Pydantic
- SQL injection protection (SQLAlchemy ORM)
- Rate limiting on auth endpoints (in-memory)

## Database Schema

### Service A - Identity & Commerce

```sql
users
├─ id (PK)
├─ email (unique)
├─ hashed_password
├─ full_name
├─ role (admin/customer)
└─ timestamps

addresses
├─ id (PK)
├─ user_id (FK)
├─ address_type
├─ street, city, state, postal_code, country
└─ is_default

carts
├─ id (PK)
├─ user_id (FK, nullable)
├─ session_id (for guests)
└─ timestamps

cart_items
├─ id (PK)
├─ cart_id (FK)
├─ product_id, variant_id, sku
├─ quantity
└─ price (snapshot)

orders
├─ id (PK)
├─ user_id (FK)
├─ order_number (unique)
├─ status (created/paid/packed/shipped/delivered/cancelled)
├─ subtotal, tax, shipping_cost, total
├─ shipping_address, billing_address (JSON)
└─ timestamps (created, paid, shipped, delivered)

order_items
├─ id (PK)
├─ order_id (FK)
├─ product_id, variant_id, sku
├─ product_name
├─ quantity
└─ price

payments
├─ id (PK)
├─ order_id (FK)
├─ stripe_payment_intent_id
├─ amount, currency
├─ status (pending/completed/failed/refunded)
└─ timestamps
```

### Service B - Catalog & Fulfillment

```sql
categories
├─ id (PK)
├─ name, slug (unique)
├─ description
├─ image_url
└─ created_at

products
├─ id (PK)
├─ category_id (FK)
├─ name, slug (unique)
├─ description
├─ base_price
├─ is_active, featured
└─ timestamps

product_images
├─ id (PK)
├─ product_id (FK)
├─ url, alt_text
├─ is_primary
└─ display_order

variants
├─ id (PK)
├─ product_id (FK)
├─ sku (unique)
├─ name
├─ price, weight
└─ attributes (JSON)

inventory
├─ id (PK)
├─ variant_id (FK, unique)
├─ quantity
├─ reserved
├─ available (computed)
├─ low_stock_threshold
└─ updated_at

reviews
├─ id (PK)
├─ product_id (FK)
├─ user_id (reference to Service A)
├─ rating (1-5)
├─ title, comment
├─ verified_purchase
└─ created_at

stores
├─ id (PK)
├─ name, address, city, state, postal_code, country
├─ latitude, longitude
├─ phone, email
└─ is_active

fulfillments
├─ id (PK)
├─ order_id (reference to Service A)
├─ order_number
├─ status (pending/processing/packed/shipped/delivered)
├─ tracking_number, carrier
└─ timestamps
```

## API Design Patterns

### RESTful Conventions

- `GET` - Retrieve resource(s)
- `POST` - Create resource
- `PUT` - Update resource (full)
- `PATCH` - Update resource (partial)
- `DELETE` - Delete resource

### Response Format

**Success**:
```json
{
  "id": 1,
  "name": "Product Name",
  "price": 29.99
}
```

**Error**:
```json
{
  "detail": "Error message"
}
```

### Status Codes

- `200` - OK
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Inter-Service Communication

### Service A → Service B

**Inventory Operations**:
```python
# Reserve inventory during checkout
POST http://localhost:8002/inventory/reserve
{
  "items": [{"sku": "PRODUCT-SKU", "quantity": 2}],
  "order_id": 123
}

# Commit on payment success
POST http://localhost:8002/inventory/commit
{"order_id": 123}

# Release on cancellation
POST http://localhost:8002/inventory/release
{"order_id": 123}
```

### Service A/B → Service C

**Notifications**:
```python
POST http://localhost:8010/notify
{
  "type": "ORDER_PLACED",
  "data": {
    "order_id": 123,
    "order_number": "ORD-20240101-1234",
    "user_email": "customer@example.com"
  }
}
```

## Scalability Considerations

### Horizontal Scaling

Each service can be scaled independently:
- **Service A**: Scale based on checkout/auth load
- **Service B**: Scale based on catalog browsing
- **Service C**: Serverless auto-scaling

### Database Scaling

- **Read Replicas**: For heavy read operations (product catalog)
- **Connection Pooling**: SQLAlchemy pool configuration
- **Indexing**: On frequently queried fields (email, sku, slug)

### Caching Strategy

Future improvements:
- Redis for session storage
- Product catalog caching
- Cart caching
- API response caching

### Load Balancing

For production:
- Application Load Balancer (ALB)
- Health check endpoints: `/health`
- Sticky sessions for cart (if needed)

## Monitoring & Observability

### Logging

- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging
- Error tracking

### Metrics

Key metrics to track:
- Request rate (requests/second)
- Response time (p50, p95, p99)
- Error rate
- Database query performance
- Payment success rate

### Health Checks

All services expose:
- `GET /health` - Basic health check
- `GET /` - Service info

## Deployment Architecture

### Local Development

```
Developer Machine
├─ Service A (uvicorn, port 8001)
├─ Service B (uvicorn, port 8002)
├─ Service C (uvicorn, port 8010)
├─ Frontend (vite dev server, port 5173)
└─ PostgreSQL (local, port 5432)
```

### Production (Recommended)

```
Cloud Infrastructure
├─ Frontend
│   ├─ Static hosting (S3 + CloudFront / Vercel / Netlify)
│   └─ CDN for assets
│
├─ API Gateway / Load Balancer
│   └─ Routes to services
│
├─ Service A (Container / VM)
│   ├─ Auto-scaling group
│   └─ Database: RDS PostgreSQL
│
├─ Service B (Container / VM)
│   ├─ Auto-scaling group
│   └─ Database: RDS PostgreSQL
│
└─ Service C (AWS Lambda / Cloud Function)
    └─ Triggered by events or HTTP
```

## Future Enhancements

1. **API Gateway**: Centralized routing, rate limiting, authentication
2. **Service Mesh**: Istio/Linkerd for service-to-service communication
3. **Message Queue**: RabbitMQ/SQS for async operations
4. **Event Sourcing**: Track all state changes
5. **CQRS**: Separate read/write models
6. **GraphQL**: Alternative to REST for frontend
7. **WebSockets**: Real-time order updates
8. **Elasticsearch**: Advanced product search
9. **Redis**: Caching and session storage
10. **Kubernetes**: Container orchestration

## Technology Choices

### Why FastAPI?

- High performance (async support)
- Automatic API documentation (OpenAPI/Swagger)
- Type safety with Pydantic
- Easy to learn and use
- Great for microservices

### Why PostgreSQL?

- ACID compliance
- Rich feature set (JSON, full-text search)
- Proven reliability
- Good performance
- Open source

### Why React + Vite?

- Fast development experience
- Modern build tooling
- Large ecosystem
- Component-based architecture
- TypeScript support

### Why Zustand?

- Lightweight state management
- Simple API
- No boilerplate
- TypeScript support
- Good for small to medium apps

## Conclusion

This architecture provides a solid foundation for an e-commerce platform with:
- Clear separation of concerns
- Independent scalability
- Maintainable codebase
- Production-ready patterns
- Room for growth

The microservices approach allows teams to work independently on different services while maintaining a cohesive user experience.
