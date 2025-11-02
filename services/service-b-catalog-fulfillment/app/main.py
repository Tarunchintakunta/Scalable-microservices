"""Main FastAPI application for Service B - Catalog & Fulfillment"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import catalog, inventory, stores, reviews

app = FastAPI(
    title="Service B - Catalog & Fulfillment",
    description="Products, categories, inventory, search, reviews, and store locations",
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
app.include_router(catalog.router)
app.include_router(inventory.router)
app.include_router(stores.router)
app.include_router(reviews.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "Catalog & Fulfillment",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
