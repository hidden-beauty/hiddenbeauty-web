#!/bin/bash

# Setup docker config
mkdir -p /etc/docker/
cat <<EOF >daemon.json
{
    "dns": ["8.8.8.8", "8.8.4.4"],
    "log-driver": "json-file",
    "log-opts": {
      "max-size": "10m",
      "max-file": "3"
    }
}
EOF
sudo mv -f daemon.json /etc/docker/daemon.json

apt-get install -y \
     apt-transport-https \
     ca-certificates \

apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

apt-get update

apt-get install -y docker-ce docker-ce-cli containerd.io
