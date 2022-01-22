#!/usr/bin/env bash

set -e

cd "${0%/*}"
cd ..

if [ "$(ls -A ./frontend/dist)" ]
then
	rm -rf ./frontend/dist/*
fi

docker-compose -f docker-compose.frontend.yml run --rm frontend yarn build

cd ./frontend/dist
zip -r ../dist-$(date '+%Y-%m-%d_%H-%M-%S').zip .
