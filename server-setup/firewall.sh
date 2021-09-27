#!/bin/bash

# only log ufw stuff to one file (/var/log/ufw.log by default)
sed -i 's/^#& stop/\& stop/' /etc/rsyslog.d/20-ufw.conf && systemctl restart rsyslog

# magic to get UFW and docker to play together: https://github.com/chaifeng/ufw-docker
wget -O /usr/local/bin/ufw-docker https://github.com/chaifeng/ufw-docker/raw/master/ufw-docker
chmod +x /usr/local/bin/ufw-docker

ufw enable
ufw allow ssh

ufw-docker install
systemctl restart ufw
