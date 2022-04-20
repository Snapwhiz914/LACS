from datetime import datetime
import subprocess
import syslog
from crontab import CronTab

class UFWManager:
    def __init__(self):
        self.cron = CronTab(user='root')
    
    def add_ip_to_ufw(self, ip_addr):
        try:
            result = subprocess.run(f"ufw allow from {ip_addr}", shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            syslog.syslog(syslog.LOG_CRIT, f"UFW allow command failed with: {e.output}")
        
        syslog.syslog(syslog.LOG_WARNING, "ADDED firewall rule to allow from " + ip_addr)

        dt = datetime.now() + datetime.timedelta(hours=24)
        job = self.cron.new(command='f"ufw delete allow from {ip_addr}"')
        job.setall(f"{dt.minute} {dt.hour} {dt.day} {dt.month} ? {dt.year}")
        self.cron.write()