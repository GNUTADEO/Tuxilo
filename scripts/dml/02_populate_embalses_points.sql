-- ============================================
-- Database initialization script
-- Creates embalses table and imports data
-- ============================================

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Insert SRID 9377 (MAGNA-SIRGAS / Colombia Bogota zone) into spatial_ref_sys if it doesn't exist
INSERT INTO spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext)
SELECT 9377, 'EPSG', 9377,
'+proj=tmerc +lat_0=4.596200416666666 +lon_0=-74.07750791666666 +k=1 +x_0=1000000 +y_0=1000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs',
'PROJCS["MAGNA-SIRGAS / Colombia Bogota zone",GEOGCS["MAGNA-SIRGAS",DATUM["Marco_Geocentrico_Nacional_de_Referencia",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6686"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4686"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",4.596200416666666],PARAMETER["central_meridian",-74.07750791666666],PARAMETER["scale_factor",1],PARAMETER["false_easting",1000000],PARAMETER["false_northing",1000000],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AUTHORITY["EPSG","9377"]]'
WHERE NOT EXISTS (SELECT 1 FROM spatial_ref_sys WHERE srid = 9377);

-- Wait for embalses_geom table to be created by the other init script
-- This script runs after 02-init-embalses-geom.sql

-- Populate embalses table from embalses_geom centroids
INSERT INTO embalses (nombre, latitud, longitud, geom)
SELECT 
    "NOMBRE_GEO" as nombre,
    ST_Y(ST_Transform(ST_Centroid(geom), 4326)) as latitud,
    ST_X(ST_Transform(ST_Centroid(geom), 4326)) as longitud,
    ST_Transform(ST_Centroid(geom), 4326) as geom
FROM embalses_geom
WHERE geom IS NOT NULL;

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
