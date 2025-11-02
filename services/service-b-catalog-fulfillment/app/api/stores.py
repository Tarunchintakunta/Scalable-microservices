"""Store location routes"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import math

from app.core.deps import get_db
from app.models import Store
from app.schemas.store import StoreResponse

router = APIRouter(prefix="/stores", tags=["stores"])


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula (in km)"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


@router.get("/nearby", response_model=List[StoreResponse])
def get_nearby_stores(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius_km: float = Query(50, description="Search radius in kilometers"),
    db: Session = Depends(get_db)
):
    """Get stores within radius of given coordinates"""
    stores = db.query(Store).filter(Store.is_active == True).all()
    
    nearby_stores = []
    for store in stores:
        distance = calculate_distance(lat, lng, store.latitude, store.longitude)
        if distance <= radius_km:
            store_response = StoreResponse.model_validate(store)
            store_response.distance_km = round(distance, 2)
            nearby_stores.append(store_response)
    
    # Sort by distance
    nearby_stores.sort(key=lambda x: x.distance_km)
    
    return nearby_stores


@router.get("", response_model=List[StoreResponse])
def list_stores(db: Session = Depends(get_db)):
    """Get all active stores"""
    stores = db.query(Store).filter(Store.is_active == True).all()
    return stores


@router.get("/{store_id}", response_model=StoreResponse)
def get_store(store_id: int, db: Session = Depends(get_db)):
    """Get store by ID"""
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store
