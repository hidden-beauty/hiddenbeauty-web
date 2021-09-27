#!/bin/bash

echo "---- wearebeautiful-logs"
docker build -f Dockerfile.logging -t wearebeautiful-logs .

echo "---- DONE"
