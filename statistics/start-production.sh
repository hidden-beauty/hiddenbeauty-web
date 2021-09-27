#!/bin/bash

HOSTNAME=`hostname`

echo "---- create network"
docker network create wab-network

echo "---- create grafana volume"
docker volume create --driver local --name grafana-volume

echo "---- create influx volume"
docker volume create --driver local --name influx-volume

echo "---- start influxdb"
docker run -d \
    --name influxdb \
    --restart unless-stopped \
    --network=host \
    -v influx-volume:/var/lib/influxdb \
    influxdb:1.8.2

sudo ufw allow from 95.216.117.155 to any port 8086
sudo ufw allow from 135.181.86.222 to any port 8086

echo "---- start telegraf"
docker run -d \
    --name telegraf \
    --network=host \
    -e HOST_PROC=/host/proc \
    -v /proc:/host/proc:ro \
    -v `pwd`/telegraf.conf:/etc/telegraf/telegraf.conf:ro \
    -v /home/wab/logs:/logs:ro \
    --restart unless-stopped \
    telegraf:1.15.2

echo "---- start grafana"
docker run -d \
    --name grafana \
    --network=host \
    --restart unless-stopped \
    -v grafana-volume:/var/lib/grafana \
    grafana/grafana:7.1.5

sudo ufw deny tcp/3000
