'''
Created on 31 mar. 2022

@author: francesco.vaccaro
'''
import subprocess
import time

def lb_set():
    subprocess.call(["lxc", "start", "lb"])
    eth1_in = False
    while not eth1_in:
        time.sleep(3)
        subprocess.call(["lxc", "file", "push", "50-cloud-init.yaml", "lb/etc/netplan/50-cloud-init.yaml"])
        time.sleep(2)
        respuesta = subprocess.run(["lxc", "exec", "lb", "--", "cat", "/etc/netplan/50-cloud-init.yaml"], stdout=subprocess.PIPE)
        eth1_in = "eth1" in respuesta.stdout.decode("utf-8")
    subprocess.call(["lxc", "stop", "lb", "--force"])
    subprocess.call(["lxc", "start", "lb"])
    return None

