"""
SQLAlchemy models for database tables.
"""

from datetime import date, datetime
from typing import Optional
from decimal import Decimal

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Date,
    DateTime,
    ForeignKey,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Weather(Base):
    """
    Weather data model.

    Stores weather information for different zip codes and dates.
    """

    __tablename__ = "weather"

    date = Column(Date, primary_key=True, nullable=False)
    zip_code = Column(String(14), primary_key=True, nullable=False)
    max_temperature_f = Column(Numeric(8, 3))
    mean_temperature_f = Column(Numeric(8, 3))
    min_temperature_f = Column(Numeric(8, 3))
    max_dew_point_f = Column(Numeric(8, 3))
    mean_dew_point_f = Column(Numeric(8, 3))
    min_dew_point_f = Column(Numeric(8, 3))
    max_humidity = Column(Numeric(8, 3))
    mean_humidity = Column(Numeric(8, 3))
    min_humidity = Column(Numeric(8, 3))
    max_sea_level_pressure_inches = Column(Numeric(8, 3))
    mean_sea_level_pressure_inches = Column(Numeric(8, 3))
    min_sea_level_pressure_inches = Column(Numeric(8, 3))
    max_visibility_miles = Column(Numeric(8, 3))
    mean_visibility_miles = Column(Numeric(8, 3))
    min_visibility_miles = Column(Numeric(8, 3))
    max_wind_speed_mph = Column(Numeric(8, 3))
    mean_wind_speed_mph = Column(Numeric(8, 3))
    max_gust_speed_mph = Column(Numeric(8, 3))
    precipitation_inches = Column(Numeric(8, 3))
    cloud_cover = Column(Numeric(8, 3))
    events = Column(String(100))
    wind_dir_degrees = Column(Numeric(8, 3))


class Station(Base):
    """
    Bike station model.

    Represents a physical bike-sharing station location.
    """

    __tablename__ = "station"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    lat = Column(Numeric(11, 8), nullable=False)
    long = Column(Numeric(11, 8), nullable=False)
    dock_count = Column(Integer)
    city = Column(String(100))
    installation_date = Column(Date)

    trips_started = relationship(
        "Trip", foreign_keys="Trip.start_station_id", back_populates="start_station"
    )
    trips_ended = relationship(
        "Trip", foreign_keys="Trip.end_station_id", back_populates="end_station"
    )


class Trip(Base):
    """
    Trip model.

    Represents a bike trip from one station to another.
    """

    __tablename__ = "trip"

    id = Column(Integer, primary_key=True)
    duration = Column(Integer, nullable=False)
    start_date = Column(TIMESTAMP, nullable=False)
    start_station_id = Column(Integer, ForeignKey("station.id"))
    end_date = Column(TIMESTAMP, nullable=False)
    end_station_id = Column(Integer, ForeignKey("station.id"))
    bike_id = Column(Integer)
    subscription_type = Column(String(50))
    zip_code = Column(String(14))

    start_station = relationship(
        "Station", foreign_keys=[start_station_id], back_populates="trips_started"
    )
    end_station = relationship(
        "Station", foreign_keys=[end_station_id], back_populates="trips_ended"
    )


class Status(Base):
    """
    Station status model.

    Tracks the availability of bikes and docks at each station over time.
    """

    __tablename__ = "status"

    station_id = Column(Integer, nullable=False, primary_key=True)
    bikes_available = Column(Integer, nullable=False)
    docks_available = Column(Integer, nullable=False)
    time = Column(TIMESTAMP, nullable=False, primary_key=True)
    category1 = Column(Integer)
    category2 = Column(Integer)
