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

-- Add MAGNA-SIRGAS 2018 / Origen-Nacional (EPSG:9377) for coordinate transformation
INSERT INTO spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext) VALUES (
    9377,
    'EPSG',
    9377,
    '+proj=tmerc +lat_0=4.596200416666666 +lon_0=-74.08091666666667 +k=1 +x_0=5000000 +y_0=2000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs',
    'PROJCS["MAGNA-SIRGAS 2018 / Origen-Nacional",GEOGCS["MAGNA-SIRGAS 2018",DATUM["MAGNA-SIRGAS_2018",SPHEROID["GRS 1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",4.596200416666666],PARAMETER["central_meridian",-74.08091666666667],PARAMETER["scale_factor",1],PARAMETER["false_easting",5000000],PARAMETER["false_northing",2000000],UNIT["metre",1]]'
) ON CONFLICT (srid) DO NOTHING;
