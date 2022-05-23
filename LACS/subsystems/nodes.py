import requests
import syslog

class NodesManager:
    def __init__(self, nodes_arr):
        self.nodes = nodes_arr
        pass

    def update_nodes(self, ip, hours):
        for node_dict in self.nodes:
            try:
                r = requests.post(f"http://" + node_dict["address"] + ":" + str(node_dict["port"]) + "/processrequest", json={"key": node_dict["key"], "ip": ip, "time": hours})
                res = r.json()
                if res["success"] == True:
                    print(f"Updated node {node_dict['address']} successfully.")
                else: 
                    syslog.syslog(syslog.LOG_INFO, "Updating node {node_dict['address']} failed.")
            except Exception as e:
                syslog.syslog(syslog.LOG_INFO, "Updating node {node_dict['address']} errored with e: {e}.")