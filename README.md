# LACS

<p align=center><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pyyaml"> <img alt="GitHub" src="https://img.shields.io/github/license/Snapwhiz914/LACS"> </p>

Aka. "L's Access Control System"

This is a relatively simple python program for a quick and easy access control system for an internet-facing server.

## How it works

1. This program "attaches" to an email account and checks every 15 seconds for a specific type of email.
    - The email will have a specific subject, and its content is the IP Address to allow
2. When this email is recieved:
    - Allow the IP Address from the email using UFW
    - The IP Address will automatically be deleted from UFW in a configurable amount of time
    - When the node program is released, it will be able to send allow changes to other servers (see future section at bottom)

## Quick start

### 1. Pre-Setup Tutorials

 - It doesn't matter what email service you use, as long as there is a way for this program to access it. [Here is a tutorial for Gmail](https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development). I recommend using a dedicated email address.
 - [Tutorial](https://www.digitalocean.com/community/tutorials/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server) on setting up UFW.

### 2. Copy-Paste terminal commands

This code assumes you already have:
 - An email address accessable by a password
 - UFW installed and set up
 - The "at" command installed (comes by default on most linux distros)
(Refer to the tutorials section if you don't have both of these)

```bash
git clone https://github.com/Snapwhiz914/LACS
cd LACS
chmod +x install.sh
./install.sh
```

### 3. Configuring your config

The configuration file will be at /etc/lacs.yaml after running the install instructions above.

Here is a general guide for what your configuration should look like (this is the default config with no comments):

```yaml
email: account@example.com
password: AccountPassword123
server: imap.server.com
port: 143
subject: "SubjectRequirement"
time_in_hours: 24
```

### 4. Starting/stoppping LACS

Start LACS:
```bash
systemctl start lacs.service
```
LACS is automatically configured to run on boot through a systemd service.
You must run ```systemctl restart lacs.service``` after editing your config.

### 5. Problems? Read the notes

### 6. Updating

Simply run ```git pull``` in whatever directory you cloned lacs in before and run the ```install.sh``` file again.

## Notes/Requirments:
 - Any linux OS that supports UFW and python should be able to run this program.
 - Your subject requirement should be secure. I recommend generating a key.
 - Non-SSL mail services are not supported at this time (support may come in the future, but for now stick to the secure option)
 - The Nodes feature is not ready yet as of April 21, so do not use that in the config yet.
 - If you are using Gmail, make sure to enable access from third party/unsecure apps (Described in the tutorials above)
 - I recommend creating a script or shortcut that automatically emails your public IP address to your LACS mail address. [Here](https://www.icloud.com/shortcuts/91d8e88b4e5741a3ba9ac3010ea57041) is one for MacOS/iOS.
 - Due to the nature of checking emails, do not expect to have access immediately. It usually takes 30 seconds or under for it to update UFW
 - Mail with attachments are automatically ignored, no matter what the text contents of the message are.
 - On a related subject to the above note, the message body containing the ip address cannot have any formatting (just normal ascii)
 - **Do not** run multiple instances of this service on the same account at the same time, they will interfere with each other. If you want to use one account to control access on multiple machines, delegate one machine as the host and install [LACS-node](https://github.com/Snapwhiz914/LACS-node) on the other machines.

## Contributing

Be sure to read the CONTRIBUTING.md file before you submit a pull request

## Future
 - Docker container compatibility
