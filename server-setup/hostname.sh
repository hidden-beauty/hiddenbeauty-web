#!/bin/bash

set -eu

DOMAIN="wearebeautiful.info"

if [[ $# == 0 || $1 == --help ]]; then
    echo "$0 NAME"
    echo "Set hostname to NAME.$DOMAIN on hetzner machines"
    exit 0
fi

cp /etc/hosts /etc/hosts.bak
NAME="$1"
IPV4=$(ifconfig eth0|grep 'inet addr:'|cut -d ':' -f2|awk '{print $1}')
IPV6=$(ifconfig eth0|grep 'inet6 addr:.*Global'|cut -d ':' -f2-|awk '{print $1}'|sed 's#/64$##')
if grep -q -F "$IPV4" /etc/hosts; then
    IPV4ESC=$(echo -n "$IPV4"|sed 's/\./\\./g')
    sed -i "s/^$IPV4ESC\s\+.*$/$IPV4 $NAME.$DOMAIN $NAME/" /etc/hosts
fi
if grep -q -F "$IPV6" /etc/hosts; then
    sed -i "s/^$IPV6\s\+.*$/$IPV6 $NAME.$DOMAIN/" /etc/hosts
fi

echo "$NAME" > /etc/hostname
hostname $NAME
hostnamectl set-hostname $NAME
hostnamectl status
