#!/bin/bash

set -eu

install -m 644 sysctl.conf /etc/sysctl.conf && systemctl restart systemd-sysctl
