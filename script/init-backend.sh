#!/usr/bin/env bash

set -e

cd "${0%/*}"
cd ..

docker-compose -f docker-compose.dev.yml run --rm backend flask --app manage db upgrade
