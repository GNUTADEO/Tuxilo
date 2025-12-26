\COPY data.predicted_data (embalse,periodo,precipitacion_project,ar,br,ar_km2,ai_km2,q_proyectado) FROM '/tmp/predicted_data.csv' WITH CSV HEADER;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'Predicted data table populated with % rows', (SELECT COUNT(*) FROM data.predicted_data);
END $$;
