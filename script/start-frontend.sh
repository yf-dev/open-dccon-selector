#!/usr/bin/env bash

set -e

cd "${0%/*}"
cd ..

docker-compose -f docker-compose.frontend.yml stop
docker-compose -f docker-compose.frontend.yml up
