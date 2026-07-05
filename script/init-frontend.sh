#!/usr/bin/env bash

set -e

cd "${0%/*}"
cd ..

docker-compose -f docker-compose.dev.yml run --rm frontend yarn install
bash ./script/copy-node-modules.sh
