"""Review routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.deps import get_db
from app.models import Review, Product
from app.schemas.review import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/product/{product_id}", response_model=List[ReviewResponse])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a product"""
    reviews = db.query(Review).filter(Review.product_id == product_id).order_by(Review.created_at.desc()).all()
    return reviews


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review_data: ReviewCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new review"""
    # Verify product exists
    product = db.query(Product).filter(Product.id == review_data.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    # Check if user already reviewed this product
    existing_review = db.query(Review).filter(
        Review.product_id == review_data.product_id,
        Review.user_id == user_id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product"
        )
    
    # Create review
    new_review = Review(
        **review_data.model_dump(),
        user_id=user_id,
        verified_purchase=0  # Should verify with Service A
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review
