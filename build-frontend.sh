#!/usr/bin/env bash

rm -r ./frontend/dist/*
docker-compose -f docker-compose.build-frontend.yml run --rm build

