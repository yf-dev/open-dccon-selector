#!/usr/bin/env bash

if [ "$(id -u)" != "0" ]; then
	echo "Sorry, you are not root."
	exit 1
fi

rm -r ./frontend/dist/*
docker-compose -f docker-compose.build-frontend.yml run --rm build
cd ./frontend/dist
zip -r ods-$(date +'%Y%m%d-%H%M%S').zip ./*

