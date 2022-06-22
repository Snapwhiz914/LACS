from datetime import datetime
import subprocess
import syslog

class UFWManager:
    def __init__(self):
        self.cron = CronTab(user='root')
    
    def add_ip_to_ufw(self, ip_addr):
        try:
            result = subprocess.run(f"ufw allow from {ip_addr}", shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            syslog.syslog(syslog.LOG_ALERT, f"UFW allow command failed with: {e.output}")
        
        syslog.syslog(syslog.LOG_INFO, "ADDED firewall rule to allow from " + ip_addr)

        try:
            subprocess.run(f'echo "ufw delete allow from {ip_addr}" | at now +{hours_until_removal} hours', shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            syslog.syslog(syslog.LOG_ALERT, f"Scheduling the UFW rule removal using 'at' failed: {e.output}")