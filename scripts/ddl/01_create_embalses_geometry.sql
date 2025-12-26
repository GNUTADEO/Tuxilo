CREATE TABLE geodata.embalses_polygons (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50),
    proyecto VARCHAR(30),
    symbol VARCHAR(254),
    fecha DATE,
    ruleid float8,
    fecha_1 DATE,
    pk_cue NUMERIC,
    shape_leng NUMERIC,
    shape_area NUMERIC,
    geom GEOMETRY(MULTIPOLYGON, 9377)
);