"""
Pydantic schemas for Weather data validation and serialization.
"""
from datetime import date as date_type
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class WeatherBase(BaseModel):
    """Base schema for Weather data"""
    date: date_type = Field(..., description="Date of the weather record", examples=["2024-01-15"])
    zip_code: str = Field(..., max_length=14, description="ZIP code", examples=["94107"])
    max_temperature_f: Optional[Decimal] = Field(None, description="Maximum temperature in Fahrenheit", examples=[75.5])
    mean_temperature_f: Optional[Decimal] = Field(None, description="Mean temperature in Fahrenheit", examples=[65.2])
    min_temperature_f: Optional[Decimal] = Field(None, description="Minimum temperature in Fahrenheit", examples=[55.1])
    max_dew_point_f: Optional[Decimal] = Field(None, description="Maximum dew point in Fahrenheit")
    mean_dew_point_f: Optional[Decimal] = Field(None, description="Mean dew point in Fahrenheit")
    min_dew_point_f: Optional[Decimal] = Field(None, description="Minimum dew point in Fahrenheit")
    max_humidity: Optional[Decimal] = Field(None, description="Maximum humidity percentage")
    mean_humidity: Optional[Decimal] = Field(None, description="Mean humidity percentage")
    min_humidity: Optional[Decimal] = Field(None, description="Minimum humidity percentage")
    max_sea_level_pressure_inches: Optional[Decimal] = Field(None, description="Maximum sea level pressure in inches")
    mean_sea_level_pressure_inches: Optional[Decimal] = Field(None, description="Mean sea level pressure in inches")
    min_sea_level_pressure_inches: Optional[Decimal] = Field(None, description="Minimum sea level pressure in inches")
    max_visibility_miles: Optional[Decimal] = Field(None, description="Maximum visibility in miles")
    mean_visibility_miles: Optional[Decimal] = Field(None, description="Mean visibility in miles")
    min_visibility_miles: Optional[Decimal] = Field(None, description="Minimum visibility in miles")
    max_wind_speed_mph: Optional[Decimal] = Field(None, description="Maximum wind speed in mph")
    mean_wind_speed_mph: Optional[Decimal] = Field(None, description="Mean wind speed in mph")
    max_gust_speed_mph: Optional[Decimal] = Field(None, description="Maximum gust speed in mph")
    precipitation_inches: Optional[Decimal] = Field(None, description="Precipitation in inches")
    cloud_cover: Optional[Decimal] = Field(None, description="Cloud cover percentage")
    events: Optional[str] = Field(None, max_length=100, description="Weather events", examples=["Rain"])
    wind_dir_degrees: Optional[Decimal] = Field(None, description="Wind direction in degrees")


class WeatherCreate(WeatherBase):
    """Schema for creating a new weather record"""
    pass


class WeatherUpdate(BaseModel):
    """Schema for updating an existing weather record"""
    max_temperature_f: Optional[Decimal] = None
    mean_temperature_f: Optional[Decimal] = None
    min_temperature_f: Optional[Decimal] = None
    max_dew_point_f: Optional[Decimal] = None
    mean_dew_point_f: Optional[Decimal] = None
    min_dew_point_f: Optional[Decimal] = None
    max_humidity: Optional[Decimal] = None
    mean_humidity: Optional[Decimal] = None
    min_humidity: Optional[Decimal] = None
    max_sea_level_pressure_inches: Optional[Decimal] = None
    mean_sea_level_pressure_inches: Optional[Decimal] = None
    min_sea_level_pressure_inches: Optional[Decimal] = None
    max_visibility_miles: Optional[Decimal] = None
    mean_visibility_miles: Optional[Decimal] = None
    min_visibility_miles: Optional[Decimal] = None
    max_wind_speed_mph: Optional[Decimal] = None
    mean_wind_speed_mph: Optional[Decimal] = None
    max_gust_speed_mph: Optional[Decimal] = None
    precipitation_inches: Optional[Decimal] = None
    cloud_cover: Optional[Decimal] = None
    events: Optional[str] = Field(None, max_length=100)
    wind_dir_degrees: Optional[Decimal] = None


class Weather(WeatherBase):
    """Schema for weather response"""
    model_config = ConfigDict(from_attributes=True)
