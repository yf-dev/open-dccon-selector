#!/usr/bin/env bash

docker-compose -f docker-compose.dev.yml stop && docker-compose -f docker-compose.dev.yml up -d && docker-compose -f docker-compose.dev.yml logs -f -t --tail=100
