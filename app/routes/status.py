"""
API routes for Status endpoints.
"""
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Status as StatusModel
from app.schemas.status import Status, StatusCreate, StatusUpdate

router = APIRouter(prefix="/status", tags=["Status"])


@router.get("/", response_model=List[Status], summary="Get all status records")
def get_status_records(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    station_id: int = Query(None, description="Filter by station ID"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all status records with pagination and optional filtering.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (max 1000)
    - **station_id**: Filter by specific station ID (optional)
    """
    query = db.query(StatusModel)
    
    if station_id is not None:
        query = query.filter(StatusModel.station_id == station_id)
    
    status_records = query.offset(skip).limit(limit).all()
    return status_records


@router.get("/{station_id}/{timestamp}", response_model=Status, summary="Get status by station and time")
def get_status(station_id: int, timestamp: datetime, db: Session = Depends(get_db)):
    """
    Retrieve a specific status record by station ID and timestamp.
    
    - **station_id**: The station identifier
    - **timestamp**: The timestamp of the status record
    """
    status_record = db.query(StatusModel).filter(
        StatusModel.station_id == station_id,
        StatusModel.time == timestamp
    ).first()
    
    if status_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Status record for station {station_id} at {timestamp} not found"
        )
    return status_record


@router.post("/", response_model=Status, status_code=status.HTTP_201_CREATED, summary="Create a new status record")
def create_status(status_data: StatusCreate, db: Session = Depends(get_db)):
    """
    Create a new station status record.
    
    - **station_id**: Station identifier
    - **bikes_available**: Number of bikes available
    - **docks_available**: Number of docks available
    - **time**: Timestamp of the status record
    - **category1**: Category 1 classification (optional)
    - **category2**: Category 2 classification (optional)
    """
    # Check if status record already exists
    db_status = db.query(StatusModel).filter(
        StatusModel.station_id == status_data.station_id,
        StatusModel.time == status_data.time
    ).first()
    
    if db_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status record for station {status_data.station_id} at {status_data.time} already exists"
        )
    
    db_status = StatusModel(**status_data.model_dump())
    db.add(db_status)
    try:
        db.commit()
        db.refresh(db_status)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating status record: {str(e)}"
        )
    return db_status


@router.put("/{station_id}/{timestamp}", response_model=Status, summary="Update a status record")
def update_status(
    station_id: int,
    timestamp: datetime,
    status_data: StatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing status record.
    
    - **station_id**: The station identifier
    - **timestamp**: The timestamp of the status record
    - Updates only the fields provided in the request body
    """
    db_status = db.query(StatusModel).filter(
        StatusModel.station_id == station_id,
        StatusModel.time == timestamp
    ).first()
    
    if db_status is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Status record for station {station_id} at {timestamp} not found"
        )
    
    # Update only provided fields
    update_data = status_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_status, field, value)
    
    try:
        db.commit()
        db.refresh(db_status)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating status record: {str(e)}"
        )
    return db_status


@router.delete("/{station_id}/{timestamp}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a status record")
def delete_status(station_id: int, timestamp: datetime, db: Session = Depends(get_db)):
    """
    Delete a status record by station ID and timestamp.
    
    - **station_id**: The station identifier
    - **timestamp**: The timestamp of the status record
    """
    db_status = db.query(StatusModel).filter(
        StatusModel.station_id == station_id,
        StatusModel.time == timestamp
    ).first()
    
    if db_status is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Status record for station {station_id} at {timestamp} not found"
        )
    
    try:
        db.delete(db_status)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting status record: {str(e)}"
        )
    return None
