#!/usr/bin/env bash

set -e

cd "${0%/*}"
cd ..

docker-compose -f docker-compose.backend.yml run --rm backend python3 manage.py db upgrade
