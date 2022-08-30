'''
Created on 7 may. 2022

@author: francesco.vaccaro
'''
import pickle
import subprocess
import time
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def arrancar():
    with open('num_cont.txt', 'rb') as fich:
        var = pickle.load(fich)
    print("value from the file: ",var)
    var = int(var)
    var = var + 1
    
    subprocess.call(["lxc", "start", "cl"])
    subprocess.call(["lxc", "start", "lb"])
    subprocess.call(["lxc", "start", "db"]) 
    


    
    nombre = 's'

    for i in range(1, var):
            nombre_cont = nombre + str(i)
            subprocess.call(["lxc", "start", nombre_cont])
            time.sleep(5)
            subprocess.call(["lxc", "exec", nombre_cont, "--", "forever", "start", "app/rest_server.js"])
        

    time.sleep(2)
    logger.info("arrancando haproxy")
    subprocess.call(["lxc", "exec", "lb","--", "service", "haproxy", "start"])
    
    
    
    time.sleep(3)
    subprocess.Popen(["lxc", "list"])        