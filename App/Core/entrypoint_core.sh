#!/usr/bin/env bash
set -e

# PORT
: "${PORT_CORE:?Environment variable PORT_CORE is required}"

# DB
: "${POSTGRES_USER:?Environment variable POSTGRES_USER is required}"
: "${POSTGRES_DB:?Environment variable POSTGRES_DB is required}"

# If validation passes, run the CMD
exec "$@"