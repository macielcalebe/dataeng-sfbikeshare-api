COPY public.station (id, name, lat, long, dock_count, city, installation_date)
FROM '/app/data/station.csv'
DELIMITER ','
CSV HEADER;

DROP TABLE IF EXISTS public.weather_staging;
CREATE TABLE public.weather_staging (
    date TEXT,
    max_temperature_f TEXT,
    mean_temperature_f TEXT,
    min_temperature_f TEXT,
    max_dew_point_f TEXT,
    mean_dew_point_f TEXT,
    min_dew_point_f TEXT,
    max_humidity TEXT,
    mean_humidity TEXT,
    min_humidity TEXT,
    max_sea_level_pressure_inches TEXT,
    mean_sea_level_pressure_inches TEXT,
    min_sea_level_pressure_inches TEXT,
    max_visibility_miles TEXT,
    mean_visibility_miles TEXT,
    min_visibility_miles TEXT,
    max_wind_speed_mph TEXT,
    mean_wind_speed_mph TEXT,
    max_gust_speed_mph TEXT,
    precipitation_inches TEXT,
    cloud_cover TEXT,
    events TEXT,
    wind_dir_degrees TEXT,
    zip_code TEXT
);


COPY public.weather_staging
FROM '/app/data/weather.csv'
DELIMITER ','
CSV HEADER;

INSERT INTO public.weather (
    date,
    max_temperature_f,
    mean_temperature_f,
    min_temperature_f,
    max_dew_point_f,
    mean_dew_point_f,
    min_dew_point_f,
    max_humidity,
    mean_humidity,
    min_humidity,
    max_sea_level_pressure_inches,
    mean_sea_level_pressure_inches,
    min_sea_level_pressure_inches,
    max_visibility_miles,
    mean_visibility_miles,
    min_visibility_miles,
    max_wind_speed_mph,
    mean_wind_speed_mph,
    max_gust_speed_mph,
    precipitation_inches,
    cloud_cover,
    events,
    wind_dir_degrees,
    zip_code
)
SELECT
    TO_DATE(date, 'MM/DD/YYYY'),
    NULLIF(max_temperature_f, '')::NUMERIC,
    NULLIF(mean_temperature_f, '')::NUMERIC,
    NULLIF(min_temperature_f, '')::NUMERIC,
    NULLIF(max_dew_point_f, '')::NUMERIC,
    NULLIF(mean_dew_point_f, '')::NUMERIC,
    NULLIF(min_dew_point_f, '')::NUMERIC,
    NULLIF(max_humidity, '')::NUMERIC,
    NULLIF(mean_humidity, '')::NUMERIC,
    NULLIF(min_humidity, '')::NUMERIC,
    NULLIF(max_sea_level_pressure_inches, '')::NUMERIC,
    NULLIF(mean_sea_level_pressure_inches, '')::NUMERIC,
    NULLIF(min_sea_level_pressure_inches, '')::NUMERIC,
    NULLIF(max_visibility_miles, '')::NUMERIC,
    NULLIF(mean_visibility_miles, '')::NUMERIC,
    NULLIF(min_visibility_miles, '')::NUMERIC,
    NULLIF(max_wind_speed_mph, '')::NUMERIC,
    NULLIF(mean_wind_speed_mph, '')::NUMERIC,
    NULLIF(max_gust_speed_mph, '')::NUMERIC,
    NULLIF(NULLIF(precipitation_inches, 'T'), '')::NUMERIC,
    NULLIF(cloud_cover, '')::NUMERIC,
    events,
    NULLIF(wind_dir_degrees, '')::NUMERIC,
    zip_code
FROM public.weather_staging;

DROP TABLE IF EXISTS public.weather_staging;

DROP TABLE IF EXISTS public.trip_staging;
CREATE TABLE public.trip_staging (
    id INTEGER,
    duration INTEGER NOT NULL,
    start_date TIMESTAMP NOT NULL,
    start_station_name VARCHAR(255),
    start_station_id INTEGER,
    end_date TIMESTAMP NOT NULL,
    end_station_name VARCHAR(255),
    end_station_id INTEGER,
    bike_id INTEGER,
    subscription_type VARCHAR(50),
    zip_code VARCHAR(14)
);

COPY public.trip_staging (
    id,
    duration,
    start_date,
    start_station_name,
    start_station_id,
    end_date,
    end_station_name,
    end_station_id,
    bike_id,
    subscription_type,
    zip_code
)
FROM '/app/data/trip.csv'
DELIMITER ','
CSV HEADER;

INSERT INTO public.trip (
    id,
    duration,
    start_date,
    start_station_id,
    end_date,
    end_station_id,
    bike_id,
    subscription_type,
    zip_code
)
SELECT 
    id,
    duration,
    start_date,
    start_station_id,
    end_date,
    end_station_id,
    bike_id,
    subscription_type,
    zip_code
FROM public.trip_staging;

DROP TABLE IF EXISTS public.trip_staging;
