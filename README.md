# LACS

Aka. "L's Access Control System"

This is a relatively simple python program for a quick and easy access control system for an internet-facing server.

## How it works

1. This program attaches to an email account and continously checks for a specific type of email.
    - The email will have a specific subject, and its content is the IP Address to allow
2. When this email is recieved:
    - Allow the IP Address from the email using UFW
    - The IP Address will automatically be deleted from UFW in a configurable amount of time
    - When the node program is released, it will be able to send allow changes to other servers

## Quick start

This code assumes you already have:
 - An email address accessable by a password
 - UFW installed and set up

```bash
git clone https://github.com/Snapwhiz914/LACS
cd LACS-master
chmod +x install.sh
./install.sh
```

### Configuring your config

The configuration file will be at /etc/lacs.yaml after running the install instructions above.

Here is a general guide for what your configuration should look like:

```yaml
email: account@example.com
password: AccountPassword123
server: imap.server.com
subject: "SubjectRequirement"
time_in_hours: 24
```

Notes:
 - Your subject requirement should be secure. I recommend generating a key.
 - The Nodes feature is not ready yet as of April 21, so do not use that in the config yet.
 - If you are using Gmail, make sure to enable access from third party/unsecure apps (Described in the tutorial below)

## Tutorials

 - It doesn't matter what email service you use, as long as there is a way for this program to access it. [Here is a tutorial for Gmail](https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development). I recommend using a dedicated email address.
 - [Tutorial](https://www.digitalocean.com/community/tutorials/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server) on setting up UFW.

## Contributing

Be sure to read the CONTRIBUTING.md file before you submit a pull request

## Future

 - Soon (as of April 21), I will release a node package, which can run on another server that is update by changes to the hub server.
