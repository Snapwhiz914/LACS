from datetime import datetime
import subprocess
import syslog

class UFWManager:
    def __init__(self):
        pass
    
    def add_ip_to_ufw(self, ip_addr, hours_until_removal):
        try:
            check_res = subprocess.run(f"ufw status", shell=True, check=True, capture_output=True)
            for rule in check_res.stdout.decode("ascii").split("\n"):
                if ip_addr in rule and "ALLOW" in rule:
                    syslog.syslog(syslog.LOG_WARN, f"ufw allow {ip_addr} does not need to run, it is already present in the firewall.")
                    return
            result = subprocess.run(f"ufw allow from {ip_addr}", shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            syslog.syslog(syslog.LOG_ALERT, f"UFW allow command failed with: {e.output}")
            return
        
        syslog.syslog(syslog.LOG_INFO, "ADDED firewall rule to allow from " + ip_addr)

        try:
            subprocess.run(f'echo "ufw delete allow from {ip_addr}" | at now +{hours_until_removal} hours', shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            syslog.syslog(syslog.LOG_ALERT, f"Scheduling the UFW rule removal using 'at' failed: {e.output}")
