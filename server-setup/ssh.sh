#!/bin/bash

cp sshd_config /etc/ssh/sshd_config
chown root:root /etc/ssh/sshd_config
chmod u+rw /etc/ssh/sshd_config
chmod o+r /etc/ssh/sshd_config
