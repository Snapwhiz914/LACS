import time
import syslog
from .subsystems.config import get_config_object
from .subsystems.firewall import UFWManager
from .subsystems.mail import MailManager
from .subsystems.nodes import NodesManager
from .subsystems.utils import get_req_from_email

def main():
    syslog.syslog(syslog.LOG_INFO, "Initializing...")
    conf = get_config_object()
    ufw_man = UFWManager()
    mail_man = MailManager(conf["server"], conf["port"], conf["email"], conf["password"])
    nodes_man = None
    try:
        nodes_man = NodesManager(conf["nodes"])
    except KeyError:
        #Will uncomment when the nodes feature is ready.
        #syslog.syslog(syslog.LOG_INFO, "No nodes present in the config. If you think this is a mistake, check your config.")
        pass

    syslog.syslog(syslog.LOG_INFO, "Done. Periodic loop started.")
    while True:
        try:
            for message in mail_man.get_new_messages_periodic():
                mail_from = message['from']
                mail_subject = message['subject']
                syslog.syslog(syslog.LOG_INFO, "Recieved message from: " + mail_from + ", Subject: " + mail_subject)
                result = get_req_from_email(message)
                if result != False:
                    syslog.syslog(syslog.LOG_INFO, "New message successfully requested access for IP: " + result.compressed)
                    ufw_man.add_ip_to_ufw(result.compressed)
                    nodes_man.update_nodes(result.compressed, conf["time_in_hours"])
        except Exception as e:
            print(f"Peridic Error: {e}")
        time.sleep(15)