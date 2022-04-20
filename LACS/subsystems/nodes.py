import syslog
import requests

class NodesManager:
    def __init__(self, nodes_arr):
        self.nodes = nodes_arr
        pass

    def update_nodes(self, ip, hours):
        for node_dict in self.nodes:
            try:
                r = requests.post(f"http://" + node_dict["address"] + ":" + str(node_dict["port"]) + "/processrequest", json={"key": node_dict["key"], "ip": ip, "time": hours})
                syslog.syslog(syslog.LOG_DEBUG, str(r.status_code))
                syslog.syslog(syslog.LOG_DEBUG, r.content.decode("utf-8"))
                res = r.json()
                if res["success"] == True:
                    syslog.syslog(syslog.LOG_INFO, f"Updated node {node_dict['address']} successfully.")
                else: 
                    syslog.syslog(syslog.LOG_WARNING, f"Updating node {node_dict['address']} failed.")
            except Exception as e:
                syslog.syslog(syslog.LOG_ERR, f"Updating node {node_dict['address']} errored with e: {e}.")