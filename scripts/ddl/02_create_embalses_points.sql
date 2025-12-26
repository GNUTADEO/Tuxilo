CREATE TABLE IF NOT EXISTS geodata.embalses_points (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    geom GEOMETRY(POINT, 4326)
);
