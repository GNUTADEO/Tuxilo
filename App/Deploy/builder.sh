#!/usr/bin/env bash
cd ../Core && docker compose build "$@"
cd ../Front && docker compose --profile prod build "$@"
