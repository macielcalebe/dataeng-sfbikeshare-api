"""
API routes for Weather endpoints.
"""
from typing import List
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Weather as WeatherModel
from app.schemas.weather import Weather, WeatherCreate, WeatherUpdate

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/", response_model=List[Weather], summary="Get all weather records")
def get_weather_records(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    zip_code: str = Query(None, description="Filter by ZIP code"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all weather records with pagination and optional filtering.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (max 1000)
    - **zip_code**: Filter by specific ZIP code (optional)
    """
    query = db.query(WeatherModel)
    
    if zip_code is not None:
        query = query.filter(WeatherModel.zip_code == zip_code)
    
    weather_records = query.offset(skip).limit(limit).all()
    return weather_records


@router.get("/{weather_date}/{zip_code}", response_model=Weather, summary="Get weather by date and ZIP code")
def get_weather(weather_date: date, zip_code: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific weather record by date and ZIP code.
    
    - **weather_date**: The date of the weather record (format: YYYY-MM-DD)
    - **zip_code**: The ZIP code
    """
    weather = db.query(WeatherModel).filter(
        WeatherModel.date == weather_date,
        WeatherModel.zip_code == zip_code
    ).first()
    
    if weather is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Weather record for date {weather_date} and ZIP code {zip_code} not found"
        )
    return weather


@router.post("/", response_model=Weather, status_code=status.HTTP_201_CREATED, summary="Create a new weather record")
def create_weather(weather: WeatherCreate, db: Session = Depends(get_db)):
    """
    Create a new weather record.
    
    - **date**: Date of the weather record
    - **zip_code**: ZIP code
    - All other fields are optional weather measurements
    """
    # Check if weather record already exists
    db_weather = db.query(WeatherModel).filter(
        WeatherModel.date == weather.date,
        WeatherModel.zip_code == weather.zip_code
    ).first()
    
    if db_weather:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Weather record for date {weather.date} and ZIP code {weather.zip_code} already exists"
        )
    
    db_weather = WeatherModel(**weather.model_dump())
    db.add(db_weather)
    try:
        db.commit()
        db.refresh(db_weather)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating weather record: {str(e)}"
        )
    return db_weather


@router.put("/{weather_date}/{zip_code}", response_model=Weather, summary="Update a weather record")
def update_weather(
    weather_date: date,
    zip_code: str,
    weather: WeatherUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing weather record.
    
    - **weather_date**: The date of the weather record (format: YYYY-MM-DD)
    - **zip_code**: The ZIP code
    - Updates only the fields provided in the request body
    """
    db_weather = db.query(WeatherModel).filter(
        WeatherModel.date == weather_date,
        WeatherModel.zip_code == zip_code
    ).first()
    
    if db_weather is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Weather record for date {weather_date} and ZIP code {zip_code} not found"
        )
    
    # Update only provided fields
    update_data = weather.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_weather, field, value)
    
    try:
        db.commit()
        db.refresh(db_weather)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating weather record: {str(e)}"
        )
    return db_weather


@router.delete("/{weather_date}/{zip_code}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a weather record")
def delete_weather(weather_date: date, zip_code: str, db: Session = Depends(get_db)):
    """
    Delete a weather record by date and ZIP code.
    
    - **weather_date**: The date of the weather record (format: YYYY-MM-DD)
    - **zip_code**: The ZIP code
    """
    db_weather = db.query(WeatherModel).filter(
        WeatherModel.date == weather_date,
        WeatherModel.zip_code == zip_code
    ).first()
    
    if db_weather is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Weather record for date {weather_date} and ZIP code {zip_code} not found"
        )
    
    try:
        db.delete(db_weather)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting weather record: {str(e)}"
        )
    return None
