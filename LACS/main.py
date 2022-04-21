import syslog
import time
from .subsystems.config import get_config_object
from .subsystems.firewall import UFWManager
from .subsystems.mail import MailManager
from .subsystems.nodes import NodesManager
from .subsystems.utils import get_req_from_email

def main():
    print("Initializing...")
    conf = get_config_object()
    ufw_man = UFWManager()
    mail_man = MailManager(conf["server"], conf["email"], conf["password"])
    nodes_man = None
    try:
        nodes_man = NodesManager(conf["nodes"])
    except KeyError:
        print("No nodes present in the config. If you think this is a mistake, check your config.")

    print("Done. Periodic loop started.")
    while True:
        try:
            for message in mail_man.get_new_messages_periodic():
                mail_from = message['from']
                mail_subject = message['subject']
                print("Recieved message from: " + mail_from + ", Subject: " + mail_subject)
                result = get_req_from_email(message)
                if result != False:
                    print("New message successfully requested access for IP: " + result.compressed)
                    ufw_man.add_ip_to_ufw(result.compressed)
                    nodes_man.update_nodes(result.compressed, conf["time_in_hours"])
            time.sleep(15)
        except Exception as e:
            print(f"Peridic Error: {e}")