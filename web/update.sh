#!/bin/bash

echo "---- build"
git pull origin master
./build.sh

echo "---- stop containers"
./stop-containers.sh

echo "---- start containers"
./start-containers.sh

echo "---- clear cache"
docker exec -it wab-comp admin/clear_cache.sh
