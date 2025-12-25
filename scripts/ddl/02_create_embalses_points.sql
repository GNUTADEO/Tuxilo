CREATE TABLE IF NOT EXISTS embalses_points (
    reservoir_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nombre VARCHAR(255),
    latitud NUMERIC,
    longitud NUMERIC,
    geom GEOMETRY(POINT, 4326)
);
