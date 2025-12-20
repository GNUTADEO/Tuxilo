#!/usr/bin/env bash

set -euo pipefail

DATA_DIR="data/GRDC/"

cd "$DATA_DIR" || {
    echo "Error: cannot cd into $DATA_DIR" >&2
    exit 1
}

for clean in *_Q_Day_Clean.Cmd.txt; do
    orig="${clean/_Clean/}"
    [[ -f "$orig" ]] || continue

    echo "Processing $clean ← $orig"

    metadata=$(grep -E '^# (River|Station|Latitude|Longitude)' "$orig")

    tmp=$(mktemp)
    {
        echo "$metadata"
        echo
        cat "$clean"
    } > "$tmp"

    mv "$tmp" "$clean"
done

