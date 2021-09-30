#!/bin/bash


echo "---- hiddenbeauty-logs"
cd ../logging
./build.sh
cd -

echo "---- hiddenbeauty-web"
docker build -t hiddenbeauty:prod .

echo "---- DONE"
