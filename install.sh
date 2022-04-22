#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "This must be run as root. No exceptions (limitation of UFW)."
  exit
fi
echo "This will overwrite /etc/lacs.yaml. Do not run if there is something important in that file."

#Install packages
if python3 -m pip install . ; then
    echo "Package install succeeded."
else
    echo "Package install failed! Check and resolve using errors above."
    exit
fi

#Create a config file
CONFIG_TEMPLATE=$'email: account@example.com
password: AccountPassword123
server: imap.server.com
port: 143 #Default imap port, do not change unless necessary
subject: "SubjectRequirement" #MAKE SURE THIS IS SECURE!
time_in_hours: 24'
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
if systemctl enable lacs.service ; then
    echo "Service installed successfullly. LACS will run on boot."
else
    echo "Service install failed! Check for errors above"
    exit
fi
echo "Done. Have fun with a secure system. Make sure to edit your configuration file at /etc/lacs.yaml, then run systemctl start lacs.service."
