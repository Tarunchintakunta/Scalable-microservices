"""Main FastAPI application for Service A - Identity & Commerce"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, addresses, cart, checkout, orders, webhooks

app = FastAPI(
    title="Service A - Identity & Commerce",
    description="Authentication, users, cart, checkout, orders, and payments",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(addresses.router)
app.include_router(cart.router)
app.include_router(checkout.router)
app.include_router(orders.router)
app.include_router(webhooks.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "Identity & Commerce",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
