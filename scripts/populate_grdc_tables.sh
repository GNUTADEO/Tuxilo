#!/bin/bash
# Script to populate GRDC tables from Clean CSV files
# Processes all *_Q_Day_Clean.Cmd.txt files in data/GRDC directory

set -e

# Configuration
DATA_DIR="data/GRDC"
OUTPUT_SQL="App/Deploy-2/init-grdc-data.sql"
TEMP_STATIONS="/tmp/grdc_stations.csv"
TEMP_FLOW="/tmp/grdc_flow.csv"

# Check if data directory exists
if [ ! -d "$DATA_DIR" ]; then
    echo "Error: Data directory not found at $DATA_DIR"
    exit 1
fi

echo "Processing GRDC Clean files..."

# Initialize CSV files with headers
echo "station_id,river_name,station_name,latitude,longitude" > "$TEMP_STATIONS"
echo "station_id,observation_date,flow_value,month_number,flow_value_imputed" > "$TEMP_FLOW"

# Process each Clean file
for clean_file in "$DATA_DIR"/*_Q_Day_Clean.Cmd.txt; do
    if [ ! -f "$clean_file" ]; then
        continue
    fi
    
    filename=$(basename "$clean_file")
    station_id="${filename%_Q_Day_Clean.Cmd.txt}"
    
    echo "Processing: $filename (Station ID: $station_id)"
    
    # Extract metadata from header comments and remove carriage returns
    river=$(grep "^# River:" "$clean_file" | sed 's/^# River:[[:space:]]*//' | tr -d '\r' | xargs)
    station=$(grep "^# Station:" "$clean_file" | sed 's/^# Station:[[:space:]]*//' | tr -d '\r' | xargs)
    latitude=$(grep "^# Latitude" "$clean_file" | sed 's/^# Latitude[^:]*:[[:space:]]*//' | tr -d '\r' | xargs)
    longitude=$(grep "^# Longitude" "$clean_file" | sed 's/^# Longitude[^:]*:[[:space:]]*//' | tr -d '\r' | xargs)
    
    # Escape any commas or quotes in text fields
    river=$(echo "$river" | sed 's/,/\\,/g' | sed 's/"/\\"/g')
    station=$(echo "$station" | sed 's/,/\\,/g' | sed 's/"/\\"/g')
    
    # Add station to CSV
    echo "$station_id,\"$river\",\"$station\",$latitude,$longitude" >> "$TEMP_STATIONS"
    
    # Extract flow data (skip header lines starting with #)
    grep -v "^#" "$clean_file" | grep -v "^YYYY-MM-DD" | while IFS=';' read -r date value month value_imputed; do
        if [ -n "$date" ]; then
            echo "$station_id,$date,$value,$month,$value_imputed" >> "$TEMP_FLOW"
        fi
    done
done

echo "Generating SQL import script..."

# Create SQL script
cat > "$OUTPUT_SQL" << 'EOF'
-- ============================================
-- GRDC Database initialization script
-- Imports station metadata and daily flow data
-- ============================================

-- Create tables if they don't exist
-- River:                 RIO SINU
-- Station:               COTOCA ABAJO  - AUT [13077060]
-- Latitude (DD):       9.224444444
-- Longitude (DD):      -75.83444444

CREATE TABLE IF NOT EXISTS stations (
    station_id VARCHAR(50) PRIMARY KEY,
    river_name VARCHAR(255) NOT NULL,
    station_name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_stations_river ON stations(river_name);
CREATE INDEX IF NOT EXISTS idx_stations_name ON stations(station_name);

-- YYYY-MM-DD;Value;month;Value_imputed
-- 1970-03-01;146.3;3;146.3

CREATE TABLE IF NOT EXISTS grdc_daily_flow (
    id BIGSERIAL PRIMARY KEY,
    station_id VARCHAR(50) NOT NULL,
    observation_date DATE NOT NULL,
    flow_value DECIMAL(12, 3),
    month_number SMALLINT NOT NULL,
    flow_value_imputed DECIMAL(12, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(station_id) ON DELETE CASCADE,
    UNIQUE (station_id, observation_date)
);

CREATE INDEX IF NOT EXISTS idx_grdc_station_date ON grdc_daily_flow(station_id, observation_date);
CREATE INDEX IF NOT EXISTS idx_grdc_date ON grdc_daily_flow(observation_date);
CREATE INDEX IF NOT EXISTS idx_grdc_month ON grdc_daily_flow(month_number);

-- Load stations data
\COPY stations (station_id, river_name, station_name, latitude, longitude) FROM '/tmp/grdc_stations.csv' WITH CSV HEADER;

-- Load daily flow data
\COPY grdc_daily_flow (station_id, observation_date, flow_value, month_number, flow_value_imputed) FROM '/tmp/grdc_flow.csv' WITH CSV HEADER;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'Stations table populated with % rows', (SELECT COUNT(*) FROM stations);
    RAISE NOTICE 'GRDC daily flow table populated with % rows', (SELECT COUNT(*) FROM grdc_daily_flow);
END $$;
EOF

echo ""
echo "Done!"
echo "Generated files:"
echo "  - Stations CSV: $TEMP_STATIONS"
echo "  - Flow data CSV: $TEMP_FLOW"
echo "  - SQL script: $OUTPUT_SQL"
echo ""
echo "To import into PostgreSQL, run:"
echo "  psql -U username -d database_name -f $OUTPUT_SQL"
