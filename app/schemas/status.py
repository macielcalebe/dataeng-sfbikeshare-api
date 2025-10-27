"""
Pydantic schemas for Status data validation and serialization.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class StatusBase(BaseModel):
    """Base schema for Status data"""
    station_id: int = Field(..., description="Station identifier", examples=[70])
    bikes_available: int = Field(..., description="Number of bikes available", examples=[10])
    docks_available: int = Field(..., description="Number of docks available", examples=[13])
    time: datetime = Field(..., description="Timestamp of status record", examples=["2013-08-29T12:06:01"])
    category1: Optional[int] = Field(None, description="Category 1 classification", examples=[1])
    category2: Optional[int] = Field(None, description="Category 2 classification", examples=[5432])


class StatusCreate(StatusBase):
    """Schema for creating a new status record"""
    pass


class StatusUpdate(BaseModel):
    """Schema for updating an existing status record"""
    bikes_available: Optional[int] = None
    docks_available: Optional[int] = None
    category1: Optional[int] = None
    category2: Optional[int] = None


class Status(StatusBase):
    """Schema for status response"""
    model_config = ConfigDict(from_attributes=True)
