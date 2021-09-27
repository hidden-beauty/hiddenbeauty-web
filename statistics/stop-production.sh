#!/bin/bash

echo "---- stop influxdb"
docker stop influxdb
docker rm influxdb

echo "---- stop telegraf"
docker stop telegraf
docker rm telegraf

echo "---- stop grafana"
docker stop grafana
docker rm grafana
