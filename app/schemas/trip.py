"""
Pydantic schemas for Trip data validation and serialization.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TripBase(BaseModel):
    """Base schema for Trip data"""
    duration: int = Field(..., description="Trip duration in seconds", examples=[765])
    start_date: datetime = Field(..., description="Trip start timestamp", examples=["2013-08-29T14:13:00"])
    start_station_id: Optional[int] = Field(None, description="ID of the starting station", examples=[70])
    end_date: datetime = Field(..., description="Trip end timestamp", examples=["2013-08-29T14:26:00"])
    end_station_id: Optional[int] = Field(None, description="ID of the ending station", examples=[63])
    bike_id: Optional[int] = Field(None, description="Bike identifier", examples=[288])
    subscription_type: Optional[str] = Field(None, max_length=50, description="Type of subscription", examples=["Subscriber"])
    zip_code: Optional[str] = Field(None, max_length=14, description="User's ZIP code", examples=["94107"])


class TripCreate(TripBase):
    """Schema for creating a new trip"""
    id: int = Field(..., description="Unique trip identifier", examples=[913460])


class TripUpdate(BaseModel):
    """Schema for updating an existing trip"""
    duration: Optional[int] = None
    start_date: Optional[datetime] = None
    start_station_id: Optional[int] = None
    end_date: Optional[datetime] = None
    end_station_id: Optional[int] = None
    bike_id: Optional[int] = None
    subscription_type: Optional[str] = Field(None, max_length=50)
    zip_code: Optional[str] = Field(None, max_length=14)


class Trip(TripBase):
    """Schema for trip response"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
