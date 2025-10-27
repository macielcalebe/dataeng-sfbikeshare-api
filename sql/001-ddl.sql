DROP TABLE IF EXISTS public.weather_staging;
DROP TABLE IF EXISTS public.weather;
DROP TABLE IF EXISTS public.status;
DROP TABLE IF EXISTS public.trip;
DROP TABLE IF EXISTS public.station;

CREATE TABLE public.weather (
    date DATE NOT NULL,
    max_temperature_f NUMERIC(8,3),
    mean_temperature_f NUMERIC(8,3),
    min_temperature_f NUMERIC(8,3),
    max_dew_point_f NUMERIC(8,3),
    mean_dew_point_f NUMERIC(8,3),
    min_dew_point_f NUMERIC(8,3),
    max_humidity NUMERIC(8,3),
    mean_humidity NUMERIC(8,3),
    min_humidity NUMERIC(8,3),
    max_sea_level_pressure_inches NUMERIC(8,3),
    mean_sea_level_pressure_inches NUMERIC(8,3),
    min_sea_level_pressure_inches NUMERIC(8,3),
    max_visibility_miles NUMERIC(8,3),
    mean_visibility_miles NUMERIC(8,3),
    min_visibility_miles NUMERIC(8,3),
    max_wind_speed_mph NUMERIC(8,3),
    mean_wind_speed_mph NUMERIC(8,3),
    max_gust_speed_mph NUMERIC(8,3),
    precipitation_inches NUMERIC(8,3),
    cloud_cover NUMERIC(8,3),
    events VARCHAR(100),
    wind_dir_degrees NUMERIC(8,3),
    zip_code VARCHAR(14) NOT NULL,
    PRIMARY KEY (date, zip_code)
);

CREATE TABLE public.station (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    lat NUMERIC(11,8) NOT NULL,
    long NUMERIC(11,8) NOT NULL,
    dock_count INTEGER,
    city VARCHAR(100),
    installation_date DATE
);

CREATE TABLE public.trip (
    id INTEGER PRIMARY KEY,
    duration INTEGER NOT NULL,
    start_date TIMESTAMP NOT NULL,
    start_station_id INTEGER,
    end_date TIMESTAMP NOT NULL,
    end_station_id INTEGER,
    bike_id INTEGER,
    subscription_type VARCHAR(50),
    zip_code VARCHAR(14),
    FOREIGN KEY (start_station_id) REFERENCES station(id),
    FOREIGN KEY (end_station_id) REFERENCES station(id)
);
