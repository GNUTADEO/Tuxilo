CREATE TABLE IF NOT EXISTS data.predicted_data (
    id BIGSERIAL PRIMARY KEY,

    embalse VARCHAR(50) NOT NULL,
    periodo VARCHAR(10) NOT NULL,

    precipitacion_project DECIMAL(25, 16) NOT NULL,
    ar DECIMAL(25, 16) NOT NULL,
    br DECIMAL(25, 4) NOT NULL,

    ar_km2 DECIMAL(25, 3) NOT NULL,
    ai_km2 DECIMAL(25, 3) NOT NULL,

    q_proyectado DECIMAL(25, 16) NOT NULL
);