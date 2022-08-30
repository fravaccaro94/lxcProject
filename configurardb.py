'''
Created on 10 may. 2022

@author: francesco.vaccaro
'''
import subprocess
import sys
import time
def configurardb():
    subprocess.call(["lxc", "network", "create", "lxdbr0"])
    subprocess.call(["lxc", "network", "set", "lxdbr0", "ipv4.nat", "true"])
    subprocess.call(["lxc", "network", "set", "lxdbr0", "ipv4.address", "10.0.0.1/24"])#la direccion de el bridge tiene que ser diferente con la de el balanceador
    subprocess.call(["lxc", "network", "set", "lxdbr0", "ipv6.address", "none"])
    subprocess.call(["lxc", "network", "set", "lxdbr0", "ipv6.nat", "false"])
    subprocess.call(["lxc", "image", "import", "imagendb.tar.gz", "--alias", "imagendb"])
    subprocess.call(["lxc", "init", "imagendb", "db"])
    
    subprocess.call(["lxc", "network", "attach", "lxdbr0", "db", "eth0"])

    subprocess.call(["lxc", "config", "device", "set", "db", "eth0", "ipv4.address", "10.0.0.20"])
    subprocess.call(["lxc", "start", "db"]) 
    
    
    time.sleep(3) 
    
    
    arg = str(sys.argv[1])
    subprocess.call(["lxc", "config", "set", "core.https_address", arg+":8443"])
    subprocess.call(["lxc", "config", "set", "core.trust_password", "mypass"])
    
#lxc network create remote1:lxdbr0
configurardb()    
   
    

