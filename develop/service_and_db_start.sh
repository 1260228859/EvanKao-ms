#!/usr/bin/env bash

source "$(dirname ${BASH_SOURCE[0]})/utils.sh"

ensure ">>> starting services" docker-compose up -d
ensure ">>> create tables" docker-compose run --rm user_server python -m migrations
docker-compose run --rm role_server python -m migrations
docker-compose run --rm region_server python -m migrations

# create testing data
curl -X POST "http://localhost:8020/roles" -H  "accept: application/json" -H  "content-type: application/json" -d "{  \"name\": \"admin\"}"
curl -X POST "http://localhost:8030/users" -H  "accept: application/json" -H  "content-type: application/json" -d "{\"name\": \"Kevinqqnj\",\"age\":11,\"role_id\":1}"
