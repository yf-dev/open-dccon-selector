#!/usr/bin/env bash

set -e

cd "${0%/*}"
cd ..

echo "Remove old files..."
if [ -f "./frontend/node_modules" ]
then
	rm -rf ./frontend/node_modules
fi
if [ -f "./frontend/node_modules.tar" ]
then
	rm -rf ./frontend/node_modules.tar
fi
echo "Create tar archive..."
docker-compose -f docker-compose.frontend.yml run --rm frontend yarn tnm
echo "Extract tar archive..."
tar xf ./frontend/node_modules.tar -C ./frontend
echo "Remove tar archive..."
rm ./frontend/node_modules.tar
