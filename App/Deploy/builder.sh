#!/usr/bin/env bash
cd ../Persistence && docker compose build "$@"
cd ../Core && docker compose build "$@"
cd ../Front && docker compose --profile prod build "$@"
