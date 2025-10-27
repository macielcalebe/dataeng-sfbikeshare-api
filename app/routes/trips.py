"""
API routes for Trip endpoints.
"""
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Trip as TripModel
from app.schemas.trip import Trip, TripCreate, TripUpdate

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.get("/", response_model=List[Trip], summary="Get all trips")
def get_trips(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all bike trips with pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (max 1000)
    """
    trips = db.query(TripModel).offset(skip).limit(limit).all()
    return trips


@router.get("/{trip_id}", response_model=Trip, summary="Get trip by ID")
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific trip by its ID.
    
    - **trip_id**: The unique identifier of the trip
    """
    trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with id {trip_id} not found"
        )
    return trip


@router.post("/", response_model=Trip, status_code=status.HTTP_201_CREATED, summary="Create a new trip")
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    """
    Create a new bike trip.
    
    - **id**: Unique trip identifier
    - **duration**: Trip duration in seconds
    - **start_date**: Trip start timestamp
    - **start_station_id**: Starting station ID (optional)
    - **end_date**: Trip end timestamp
    - **end_station_id**: Ending station ID (optional)
    - **bike_id**: Bike identifier (optional)
    - **subscription_type**: Type of subscription (optional)
    - **zip_code**: User's ZIP code (optional)
    """
    # Check if trip already exists
    db_trip = db.query(TripModel).filter(TripModel.id == trip.id).first()
    if db_trip:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Trip with id {trip.id} already exists"
        )
    
    db_trip = TripModel(**trip.model_dump())
    db.add(db_trip)
    try:
        db.commit()
        db.refresh(db_trip)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating trip: {str(e)}"
        )
    return db_trip


@router.put("/{trip_id}", response_model=Trip, summary="Update a trip")
def update_trip(trip_id: int, trip: TripUpdate, db: Session = Depends(get_db)):
    """
    Update an existing trip.
    
    - **trip_id**: The unique identifier of the trip to update
    - Updates only the fields provided in the request body
    """
    db_trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with id {trip_id} not found"
        )
    
    # Update only provided fields
    update_data = trip.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_trip, field, value)
    
    try:
        db.commit()
        db.refresh(db_trip)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating trip: {str(e)}"
        )
    return db_trip


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a trip")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    """
    Delete a trip by its ID.
    
    - **trip_id**: The unique identifier of the trip to delete
    """
    db_trip = db.query(TripModel).filter(TripModel.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with id {trip_id} not found"
        )
    
    try:
        db.delete(db_trip)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting trip: {str(e)}"
        )
    return None
