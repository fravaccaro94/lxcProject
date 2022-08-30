'''
Created on 29 mar. 2022

@author: francesco.vaccaro
'''
import subprocess
import pickle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def destruir():
    with open('num_cont.txt', 'rb') as fich:
        var = pickle.load(fich)    
    logger.info("This operation will delete all the containers and the network's devices,\nincluding the image")
    
    for i in range(1, var+1):
        y = 's' + str(i)
        subprocess.call(["lxc", "delete", y, "--force"])
    subprocess.call(["lxc", "delete", "lb", "--force"])
    subprocess.call(["lxc", "delete", "cl", "--force"])
    subprocess.call(["lxc", "delete", "db", "--force"])
    subprocess.Popen(["lxc", "list"])
    subprocess.Popen(["lxc", "network", "delete", "lxdbr1"])
    subprocess.Popen(["lxc", "image", "delete", "servidor"])
    subprocess.Popen(["lxc", "image", "delete", "ubuntu1804"])
    subprocess.Popen(["lxc", "image", "delete", "imagenlb"])
    subprocess.Popen(["lxc", "image", "delete", "imagendb"])

    return None

