#!/usr/bin/env bash

set -e

cd "${0%/*}"
cd ..

docker-compose -f docker-compose.backend.yml stop backend
docker-compose -f docker-compose.backend.yml up -d
docker-compose -f docker-compose.backend.yml logs -f -t --tail=100
