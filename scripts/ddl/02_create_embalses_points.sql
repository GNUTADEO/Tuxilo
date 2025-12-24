-- ============================================
-- Database initialization script
-- Creates embalses table and imports data
-- ============================================
-- Create the embalses table with geometry support
CREATE TABLE IF NOT EXISTS embalses (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    latitud NUMERIC,
    longitud NUMERIC,
    geom GEOMETRY(POINT, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);