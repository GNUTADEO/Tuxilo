#!/usr/bin/env bash
# Script to convert embalses.shp to PostGIS SQL format
# This reproduces the init-embalses-geom.sql file

set -e

# Configuration
SHAPEFILE="data/geodata/embalses.shp"
OUTPUT_SQL="scripts/init-embalses-geom-shp2pgsql-2.sql"
TABLE_NAME="embalses_polygons"
SCHEMA="geodata"

# Check if shapefile exists
if [ ! -f "$SHAPEFILE" ]; then
    echo "Error: Shapefile not found at $SHAPEFILE"
    exit 1
fi

echo "Converting $SHAPEFILE to SQL..."

# Use shp2pgsql to convert shapefile to SQL
# Options:
#   -I - Create a spatial index (GIST)
#   -W UTF-8 - Specify UTF-8 encoding
#   -g geom - Name the geometry column 'geom'
#   -k - Keep case of PostgreSQL identifiers (preserve uppercase/lowercase)
# Note: No -s option means no coordinate transformation (keeps original SRID 0)

shp2pgsql -I -W UTF-8 -g geom -k \
    "$SHAPEFILE" "$SCHEMA"."$TABLE_NAME" > "$OUTPUT_SQL"

echo "SQL file generated at: $OUTPUT_SQL"
echo "Done!"
