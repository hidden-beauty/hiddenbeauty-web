#!/bin/bash

docker build -f Dockerfile.dev -t hb-web .

mkdir -p .kits

docker run -it \
    --rm --name hb-web \
    -p 80:5000 \
    -v `pwd`:/code/hiddenbeauty \
    -v `pwd`/.kits:/kits \
    -v `pwd`/../../hiddenbeauty-models:/hiddenbeauty-models \
    hb-web
