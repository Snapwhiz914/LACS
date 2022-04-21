#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "This must be run as root. No exceptions (limitation of UFW)."
  exit
fi
echo "This will overwrite /etc/lacs.yaml. Do not run if there is something important in that file."

#Install packages
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install dist/LACS-1.0-py3-none-any.whl

#Create a config file
CONFIG_TEMPLATE=$'email: account@example.com\n
password: AccountPassword123\n
server: imap.server.com\n
subject: "SubjectRequirement" #MAKE SURE THIS IS SECURE!\n
time_in_hours: 24\n
nodes:\n
  - address: nodeAddress\n
  - port: 1234\n
  - key: 1234567890asdfghjk'
touch /etc/lacs.yaml
echo "$CONFIG_TEMPLATE" > /etc/lacs.yaml

#Create a systemd service file so it will start on boot
SYSTEMD_FILE=$'[Unit]\n
Description=LACS\n
After=network.target\n
StartLimitIntervalSec=0\n
\n
[Service]\n
Type=simple\n
User=root\n
ExecStart=start-LACS\n
\n
[Install]\n
WantedBy=multi-user.target'
touch /lib/systemd/system/lacs.service
echo "$CONFIG_TEMPLATE" > /lib/systemd/system/lacs.service
systemctl daemon-reload
systemctl enable lacs.service --now

echo "Done. Have fun with a secure system. Make sure to edit your configuration file at /etc/lacs.yaml"
