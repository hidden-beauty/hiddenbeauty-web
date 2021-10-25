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
./ssh.sh

adduser --disabled-password --gecos "Robert Kaye" robert
adduser robert sudo
adduser robert docker

adduser --disabled-password --gecos "HB website" hb
adduser hb sudo
adduser hb docker
mkdir /home/hb/logs
chown 101:101 /home/hb/logs

install -m 440 sudoers /etc/sudoers.d/90-hb
echo "Domains=hiddenbeauty.ch" >> /etc/systemd/resolved.conf

# install authorized_keys for users
mkdir /home/robert/.ssh
chmod a+rx /home/robert/.ssh
cp robert.pub /home/robert/.ssh/authorized_keys
chown robert:robert /home/robert/.ssh/authorized_keys
chmod 0600 /home/robert/.ssh/authorized_keys

echo "Setup complete!"
