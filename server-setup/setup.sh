#!/bin/bash

# Most bits gratuituously stolen from the MetaBrainz server setup scripts.

HOSTNAME=`hostname`
echo "Settting up $HOSTNAME..."

apt-get update
apt-get upgrade -y
apt-get install -y build-essential git fail2ban ufw vim python3-dev python3-pip

./hostname.sh $HOSTNAME
./sysctl.sh
./docker.sh
./firewall.sh
./ssh.sh

adduser --disabled-password --gecos "Robert Kaye" robert
adduser robert sudo
adduser robert docker

adduser --disabled-password --gecos "WAB website" wab
adduser wab sudo
adduser wab docker
mkdir /home/wab/logs
chown 101:101 /home/wab/logs
mkdir /home/wab/goaccess
mkdir /home/wab/goaccess-html

install -m 440 sudoers /etc/sudoers.d/90-wab
echo "Domains=wearebeautiful.info" >> /etc/systemd/resolved.conf

# install authorized_keys for users
mkdir /home/robert/.ssh
chmod a+rx /home/robert/.ssh
cp robert.pub /home/robert/.ssh/authorized_keys
chown robert:robert /home/robert/.ssh/authorized_keys
chmod 0600 /home/robert/.ssh/authorized_keys

echo "Setup complete!"
