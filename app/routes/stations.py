"""
API routes for Station endpoints.
"""

from typing import List
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Station as StationModel
from app.schemas.station import Station, StationCreate, StationUpdate

router = APIRouter(prefix="/stations", tags=["Stations"])


@router.get("/", response_model=List[Station], summary="Get all stations")
def get_stations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to return"
    ),
    db: Session = Depends(get_db),
):
    """
    Retrieve all bike stations with pagination.

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (max 1000)
    """
    stations = db.query(StationModel).offset(skip).limit(limit).all()
    return stations


@router.get("/{station_id}", response_model=Station, summary="Get station by ID")
def get_station(station_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific station by its ID.

    - **station_id**: The unique identifier of the station
    """
    station = db.query(StationModel).filter(StationModel.id == station_id).first()
    if station is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with id {station_id} not found",
        )
    return station


@router.post(
    "/",
    response_model=Station,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new station",
)
def create_station(station: StationCreate, db: Session = Depends(get_db)):
    """
    Create a new bike station.

    - **id**: Unique station identifier
    - **name**: Station name
    - **lat**: Latitude coordinate
    - **long**: Longitude coordinate
    - **dock_count**: Number of docks (optional)
    - **city**: City name (optional)
    - **installation_date**: Installation date (optional)
    """
    db_station = db.query(StationModel).filter(StationModel.id == station.id).first()
    if db_station:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Station with id {station.id} already exists",
        )

    db_station = StationModel(**station.model_dump())
    db.add(db_station)
    try:
        db.commit()
        db.refresh(db_station)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating station: {str(e)}",
        )
    return db_station


@router.put("/{station_id}", response_model=Station, summary="Update a station")
def update_station(
    station_id: int, station: StationUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing station.

    - **station_id**: The unique identifier of the station to update
    - Updates only the fields provided in the request body
    """
    db_station = db.query(StationModel).filter(StationModel.id == station_id).first()
    if db_station is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with id {station_id} not found",
        )

    update_data = station.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_station, field, value)

    try:
        db.commit()
        db.refresh(db_station)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating station: {str(e)}",
        )
    return db_station


@router.delete(
    "/{station_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a station"
)
def delete_station(station_id: int, db: Session = Depends(get_db)):
    """
    Delete a station by its ID.

    - **station_id**: The unique identifier of the station to delete
    """
    db_station = db.query(StationModel).filter(StationModel.id == station_id).first()
    if db_station is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station with id {station_id} not found",
        )

    try:
        db.delete(db_station)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting station: {str(e)}",
        )
    return None
