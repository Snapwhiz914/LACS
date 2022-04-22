#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "This must be run as root. No exceptions (limitation of UFW)."
  exit
fi
echo "This will overwrite /etc/lacs.yaml. Do not run if there is something important in that file."

#Install packages
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install dist/LACS-1.0-py3-none-any.whl

#Create a config file
CONFIG_TEMPLATE=$'email: account@example.com
password: AccountPassword123
server: imap.server.com
subject: "SubjectRequirement" #MAKE SURE THIS IS SECURE!
time_in_hours: 24
nodes:
  - address: nodeAddress
  - port: 1234
  - key: 1234567890asdfghjk'
touch /etc/lacs.yaml
echo "$CONFIG_TEMPLATE" > /etc/lacs.yaml

#Create a systemd service file so it will start on boot
SYSTEMD_FILE=$'[Unit]
Description=LACS
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=root
ExecStart=start-LACS

[Install]
WantedBy=multi-user.target'
touch /lib/systemd/system/lacs.service
echo "$SYSTEMD_FILE" > /lib/systemd/system/lacs.service
systemctl daemon-reload
systemctl enable lacs.service --now

echo "Done. Have fun with a secure system. Make sure to edit your configuration file at /etc/lacs.yaml"
