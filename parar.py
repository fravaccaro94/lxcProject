'''
Created on 7 may. 2022

@author: francesco.vaccaro
'''
import subprocess
import pickle

def parar():
    with open('num_cont.txt', 'rb') as fich:
        count = pickle.load(fich)
    count = int(count)
    count = count + 1

    for i in range(1, count):
        contenedor1 = "s" + str(i)
        subprocess.call(["lxc", "stop", contenedor1, "--force"])


    subprocess.call(["lxc", "stop", "lb", "--force"])
    subprocess.call(["lxc", "stop", "cl", "--force"])
    subprocess.call(["lxc", "stop", "db", "--force"])

    
    subprocess.call(["lxc", "list"])
    return None