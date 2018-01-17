#!/usr/bin/env bash

set -e

cd "${0%/*}"
cd ..

docker-compose -f docker-compose.frontend.yml run --rm frontend yarn lint-fix

