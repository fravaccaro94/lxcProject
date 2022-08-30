'''
Created on 6 may. 2022

@author: francesco.vaccaro
'''
import time
import subprocess

def mongo_inst():
    
    subprocess.call(["lxc", "start", "db"])
    time.sleep(5)
    subprocess.call(["lxc", "restart", "db"])
    time.sleep(5)

    subprocess.call(["lxc", "exec", "db", "--", "apt", "update"])
        
    subprocess.call(["lxc", "stop", "db"])
    subprocess.call(["lxc", "start", "db"])


    subprocess.call(["lxc", "exec", "db", "--", "apt", "update"])
    subprocess.call(["lxc", "exec", "db", "--", "apt", "update"])

    subprocess.call(["lxc", "exec", "db", "--", "apt", "install", "-y", "mongodb"])
    subprocess.call(["lxc", "restart", "db"])

