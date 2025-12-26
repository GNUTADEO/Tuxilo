CREATE TABLE IF NOT EXISTS geodata.embalses_points (
    reservoir_id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    geom GEOMETRY(POINT, 4326)
);
