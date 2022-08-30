'''
Created on 7 may. 2022

@author: francesco.vaccaro
'''
import subprocess
import time
#from lb_set import lb_set
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

####################creando y configurando lb
def create_lb():
    logger.info("creando y configurando lb")
    subprocess.call(["lxc", "init", "imagenlb", "lb"])
    subprocess.call(["lxc", "network", "attach", "lxdbr0", "lb", "eth0"])
    subprocess.call(["lxc", "config", "device", "set", "lb", "eth0", "ipv4.address", "10.0.0.10"])
    


    subprocess.call(["lxc", "network", "attach", "lxdbr1", "lb", "eth1"])
    subprocess.call(["lxc", "config", "device", "set", "lb", "eth1", "ipv4.address", "10.0.1.10"])  
    
    
    #logger.info("copiando el fichero 50-cloud-init.yaml en lb")

    #lb_set()
    
    
    time.sleep(2)
    subprocess.call(["lxc", "exec", "lb", "--", "apt", "update"])
    subprocess.call(["lxc", "restart", "lb"])
    time.sleep(5)
    
    
    
    #logger.info("\n\n\n\n\ninstalando haproxy\n\n\n\n\n")
    subprocess.call(["lxc", "exec", "lb", "--", "apt", "update"])
    subprocess.call(["lxc", "exec", "lb", "--", "apt", "update"])
    subprocess.call(["lxc", "exec", "lb", "--", "apt", "install", "haproxy"])
    subprocess.call(["lxc", "start", "lb"])
    
    subprocess.call(["lxc", "exec", "lb", "haproxy", "-v"])
    
    logger.info("\n\n\n\ncopiando haproxy.cfg en lb\n\n\n\n\n")

    ha_config = False
    while not ha_config:
        time.sleep(3)
        subprocess.call(["lxc", "file", "push", "haproxy.cfg", "lb/etc/haproxy/haproxy.cfg"])
        time.sleep(2)
        respuesta = subprocess.run(["lxc", "exec", "lb", "--", "cat", "/etc/haproxy/haproxy.cfg"], stdout=subprocess.PIPE)
        ha_config = "10.0.0.11" in respuesta.stdout.decode("utf-8")
        
    
    subprocess.call(["lxc", "exec", "lb", "--", "haproxy", "-f", "/etc/haproxy/haproxy.cfg", "-c"])
    subprocess.call(["lxc", "exec", "lb", "--", "service", "haproxy", "start"])
    
        
        
    subprocess.call(["lxc", "restart", "lb"])
    
