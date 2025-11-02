"""Catalog routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.core.deps import get_db
from app.models import Category, Product, ProductImage, Variant, Inventory
from app.schemas.catalog import (
    CategoryResponse, CategoryCreate,
    ProductResponse, ProductCreate, ProductUpdate, ProductListResponse
)

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """Get all categories"""
    categories = db.query(Category).all()
    return categories


@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get category by ID"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.get("/products", response_model=List[ProductListResponse])
def list_products(
    category_id: Optional[int] = None,
    featured: Optional[bool] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List products with optional filters"""
    query = db.query(Product).filter(Product.is_active == True)
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if featured is not None:
        query = query.filter(Product.featured == featured)
    
    products = query.offset(skip).limit(limit).all()
    
    # Add primary image
    result = []
    for product in products:
        primary_image = db.query(ProductImage).filter(
            ProductImage.product_id == product.id,
            ProductImage.is_primary == True
        ).first()
        
        result.append(ProductListResponse(
            id=product.id,
            name=product.name,
            slug=product.slug,
            base_price=product.base_price,
            featured=product.featured,
            category_id=product.category_id,
            primary_image=primary_image.url if primary_image else None
        ))
    
    return result


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product details"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.get("/search", response_model=List[ProductListResponse])
def search_products(
    q: str = Query(..., min_length=2),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Search products by name or description"""
    search_term = f"%{q}%"
    products = db.query(Product).filter(
        Product.is_active == True,
        or_(
            Product.name.ilike(search_term),
            Product.description.ilike(search_term)
        )
    ).offset(skip).limit(limit).all()
    
    result = []
    for product in products:
        primary_image = db.query(ProductImage).filter(
            ProductImage.product_id == product.id,
            ProductImage.is_primary == True
        ).first()
        
        result.append(ProductListResponse(
            id=product.id,
            name=product.name,
            slug=product.slug,
            base_price=product.base_price,
            featured=product.featured,
            category_id=product.category_id,
            primary_image=primary_image.url if primary_image else None
        ))
    
    return result


# Admin endpoints
@router.post("/admin/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category (admin)"""
    new_category = Category(**category_data.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.post("/admin/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product (admin)"""
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put("/admin/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product (admin)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    for key, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/admin/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product (admin)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return None
