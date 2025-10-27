
SET maintenance_work_mem = '2GB';

BEGIN;

DROP TABLE IF EXISTS public.status CASCADE;

CREATE TABLE public.status (
    station_id INTEGER NOT NULL,
    bikes_available INTEGER NOT NULL,
    docks_available INTEGER NOT NULL,
    time TIMESTAMP NOT NULL
);

COPY public.status (station_id, bikes_available, docks_available, time)
FROM '/app/data/status.csv'
WITH (FORMAT CSV, DELIMITER ',', HEADER true, FREEZE true);

COMMIT;

SET maintenance_work_mem = '64MB';