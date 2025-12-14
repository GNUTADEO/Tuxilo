-- ============================================
-- Database initialization script
-- Creates embalses table and imports data
-- ============================================

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Create the embalses table with geometry support
CREATE TABLE IF NOT EXISTS embalses (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    operador VARCHAR(255),
    region_hidrologica VARCHAR(255),
    latitud NUMERIC,
    longitud NUMERIC,
    geom GEOMETRY(POINT, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Import data from CSV
COPY embalses(nombre, operador, region_hidrologica, latitud, longitud) 
FROM '/docker-entrypoint-initdb.d/EmbalsesColombia.csv' 
WITH CSV HEADER DELIMITER ',';

-- Generate geometry from lat/long coordinates
UPDATE embalses 
SET geom = ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)
WHERE latitud IS NOT NULL AND longitud IS NOT NULL;

-- Create spatial index for fast queries
CREATE INDEX IF NOT EXISTS idx_embalses_geom ON embalses USING GIST(geom);

-- Grant permissions
GRANT ALL PRIVILEGES ON TABLE embalses TO postgres;
GRANT USAGE, SELECT ON SEQUENCE embalses_id_seq TO postgres;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'Embalses table created and populated with % rows', (SELECT COUNT(*) FROM embalses);
END $$;
