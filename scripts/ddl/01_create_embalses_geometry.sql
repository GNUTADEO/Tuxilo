CREATE TABLE embalses_polygons (
    reservoir_id VARCHAR(38),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nombre VARCHAR(50),
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
ALTER TABLE embalses_polygons ADD PRIMARY KEY ("reservoir_id");
