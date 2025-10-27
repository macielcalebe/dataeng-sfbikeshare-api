"""
Pydantic schemas for Station data validation and serialization.
"""

from datetime import date as date_type
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class StationBase(BaseModel):
    """Base schema for Station data"""

    name: str = Field(
        ...,
        max_length=255,
        description="Station name",
        examples=["San Francisco Caltrain (Townsend at 4th)"],
    )
    lat: Decimal = Field(..., description="Latitude coordinate", examples=[37.776617])
    long: Decimal = Field(
        ..., description="Longitude coordinate", examples=[-122.395180]
    )
    dock_count: Optional[int] = Field(
        None, description="Number of docks at the station", examples=[23]
    )
    city: Optional[str] = Field(
        None, max_length=100, description="City name", examples=["San Francisco"]
    )
    installation_date: Optional[date_type] = Field(
        None, description="Date of station installation", examples=["2013-08-05"]
    )


class StationCreate(StationBase):
    """Schema for creating a new station"""

    id: int = Field(..., description="Unique station identifier", examples=[70])


class StationUpdate(BaseModel):
    """Schema for updating an existing station"""

    name: Optional[str] = Field(None, max_length=255)
    lat: Optional[Decimal] = None
    long: Optional[Decimal] = None
    dock_count: Optional[int] = None
    city: Optional[str] = Field(None, max_length=100)
    installation_date: Optional[date_type] = None


class Station(StationBase):
    """Schema for station response"""

    id: int

    model_config = ConfigDict(from_attributes=True)
