# LACS

Aka. "L's Access Control System"

This is a relatively simple python program for a quick and easy access control system for an internet-facing server.

# How it works

1. This program attaches to an email account and continously checks for a specific type of email.
    - The email will have a specific subject, and its content is the IP Address to allow
2. When this email is recieved:
    - Allow the IP Address from the email using UFW
    - The IP Address will automatically be deleted from UFW in a configurable amount of time

# Quick start

This code assumes you already have:
 - An email address accessable by a password
 - UFW installed and set up

```bash
git clone https://github.com/Snapwhiz914/LACS
cd LACS-master
chmod +x install.sh
./install.sh
```

# Tutorials

 - It doesn't matter what email service you use, as long as there is a way for this program to access it. [Here is a tutorial for GMail](https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development). I recommend using a dedicated email address.
 - [Tutorial](https://www.digitalocean.com/community/tutorials/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server) on setting up UFW.
