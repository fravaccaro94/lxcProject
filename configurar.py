'''
Created on 6 may. 2022

@author: francesco.vaccaro
'''
import logging
import subprocess
import sys
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    
    
def configurar():
    subprocess.call(["lxc", "delete", "db", "--force"])        

        
        
    name_remote= sys.argv[3]    
    arg = sys.argv[2]
    print("ip addres inserted: ",arg)
    print("name remote device inserted: ",name_remote)


    subprocess.call(["lxc", "remote", "add", name_remote, arg+":8443", "--password", "mypass", "--accept-certificate"])        
    
    time.sleep(5)
    
    subprocess.call(["lxc", "config", "device", "add", name_remote+":db", "miproxy", "proxy", "listen=tcp:"+arg+":27017","connect=tcp:10.0.0.20:27017"])
    print("tcp:"+arg+":27017")
    
    for i in range(1, 4):
        subprocess.call(["lxc", "exec", "s"+str(i), "--", "nano", "app/rest_server.js"])        

    time.sleep(3)
    for i in range(1, 4):
        subprocess.call(["lxc", "stop", "s"+str(i), "--force"])
        subprocess.call(["lxc", "start", "s"+str(i)])

    subprocess.call(["lxc", "restart", "lb"])
    subprocess.call(["lxc", "restart", "db"])

    time.sleep(5)

    
    subprocess.call(["lxc", "exec", "lb","--", "service", "haproxy", "start"])
    from arrancar import arrancar
    arrancar()

