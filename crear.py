'''
Created on 6 may. 2022

@author: francesco.vaccaro
'''
import logging
import subprocess
import sys
import pickle
import time
from sqlalchemy.sql.expression import except_
from mongo_inst import mongo_inst
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    
    
def crear():
    
        try:
            arg = int(sys.argv[2])
        except IndexError:
            arg ='2'
            logger.info("No se ha teclado el numero de server que se desea crear,\nse van a crear un numero de server de default")
        except ValueError:
            logger.info("hay que insertar un numero!")
            sys.exit()
        arg = int(arg)
    
        if arg not in range(1, 6):
            sys.exit("El numero permitido es entre 1 y 5")
        logger.info("el numero de server que se va a crear es: %s ",arg)
        
        
        nombre = 's'
    
        with open('num_cont.txt', 'wb') as fich:
            pickle.dump(arg, fich)  #para guardar el numero de contenedores creados en un fichero
        arg = arg + 1
        
        
        subprocess.call(["lxc", "image", "import", "servidor.tar.gz", "--alias", "servidor"])
        subprocess.call(["lxc", "image", "import", "imagenlb.tar.gz", "--alias", "imagenlb"])
        subprocess.call(["lxc", "image", "import", "imagendb.tar.gz", "--alias", "imagendb"])

        subprocess.call(["lxc", "network", "create", "lxdbr0"])
        subprocess.call(["lxc", "network", "set", "lxdbr0", "ipv4.nat", "true"])
        subprocess.call(["lxc", "network", "set", "lxdbr0", "ipv4.address", "10.0.0.1/24"])#la direccion de el bridge tiene que ser diferente con la de el balanceador
        subprocess.call(["lxc", "network", "set", "lxdbr0", "ipv6.address", "none"])
        subprocess.call(["lxc", "network", "set", "lxdbr0", "ipv6.nat", "false"])
        
        
        subprocess.call(["lxc", "network", "create", "lxdbr1"])
        subprocess.call(["lxc", "network", "set", "lxdbr1", "ipv4.nat", "true"])
        subprocess.call(["lxc", "network", "set", "lxdbr1", "ipv4.address", "10.0.1.1/24"])#la direccin de el bridge tiene que ser diferente con la de el balanceador
        subprocess.call(["lxc", "network", "set", "lxdbr1", "ipv6.address", "none"])
        subprocess.call(["lxc", "network", "set", "lxdbr1", "ipv6.nat", "false"])
        
        #################################creando db y instalando mongodb##############################
        
        
        logger.info("creando y arrancando db")

        subprocess.call(["lxc", "init", "imagendb", "db"])
        subprocess.call(["lxc", "network", "attach", "lxdbr0", "db", "eth0"])
        subprocess.call(["lxc", "config", "device", "set", "db", "eth0", "ipv4.address", "10.0.0.20"])
        
        
        time.sleep(5)
        #logger.info("instalando mongodb")
        subprocess.call(["lxc", "start", "db"])

        mongo_inst()
        subprocess.call(["lxc", "exec", "db", "--", "mongod", "--version"])
        
        
        
        ################copiando fichero mongodb.conf en el contenedor db#####################################
       
       
        
        #ip_config = False
        #while not ip_config:
        #    time.sleep(3)
        #    subprocess.call(["lxc", "file", "push", "mongodb.conf", "db/etc/mongodb.conf"])
        #    time.sleep(2)
        #    respuesta = subprocess.run(["lxc", "exec", "db", "--", "cat", "/etc/mongodb.conf"], stdout=subprocess.PIPE)
        #    ip_config = "10.0.0.20" in respuesta.stdout.decode("utf-8")
        #subprocess.call(["lxc", "stop", "db", "--force"])
        
        
        #subprocess.call(["lxc", "start", "db"])
        
        
        
        #subprocess.call(["lxc", "restart", "db"])
        
        
        
        #######################creando y instalando NODEJS en S1##########################
        #logger.info("creando s1")
        #subprocess.call(["lxc", "init", "servidor", "s1"])
        #subprocess.call(["lxc", "network", "attach", "lxdbr0", "s1", "eth0"])
        #subprocess.call(["lxc", "config", "device", "set", "s1", "eth0", "ipv4.address", "10.0.0.11"])

        #logger.info("instalando nodeJS en s1")
        #subprocess.call(["lxc", "start", "s1"])
        #time.sleep(5)

        #logger.info("copiando el file install en s1")
        #subprocess.call(["lxc", "file", "push", "install.sh", "s1/root/install.sh"])    #instalando la web app
        #subprocess.call(["lxc", "exec", "s1", "--", "chmod", "+x", "install.sh"])
        #subprocess.call(["lxc", "file", "push", "-r", "app", "s1/root"])
        #time.sleep(5)
        #logger.info("restart de s1 y arrancando install.sh")
        #subprocess.call(["lxc", "restart", "s1"])
        #time.sleep(3)
        #subprocess.call(["lxc", "exec", "s1", "--", "./install.sh"])
        #subprocess.call(["lxc", "restart", "s1"])
        
       
        
        ######################################copiar imagen s1###########################
        
        
        #logger.info("Copiar la imagen de S1")
        #subprocess.call(["lxc", "stop", "s1"])
        #subprocess.call(["lxc", "publish", "s1", "--alias", "servidor"]) 
        
        
        #######################creando los otros servidores##################
        
        
        logger.info("creando los servidores a partir de la imagen de servidor")

        for i in range(1, arg):
            nombre_cont = nombre + str(i)
            subprocess.call(["lxc", "init", "servidor", nombre_cont])
            subprocess.call(["lxc", "network", "attach", "lxdbr0", nombre_cont, "eth0"])
            subprocess.call(["lxc", "config", "device", "set", nombre_cont, "eth0", "ipv4.address", "10.0.0.1"+str(i)])

        
################creando el client###############################        
        
        subprocess.call(["lxc", "init", "servidor", "cl"])


        time.sleep(5)
        subprocess.call(["lxc", "network", "attach", "lxdbr1", "cl", "eth0"]) 
        subprocess.call(["lxc", "config", "device", "set", "cl", "eth0", "ipv4.address", "10.0.1.2"])
        
        
        
##############creacion y configuracion del balanceador de carga####################

        logger.info("creando el balanceador de carga")

        from create_lb import create_lb
        create_lb()
        
        subprocess.call(["lxc", "stop", "lb"])
        subprocess.call(["lxc", "stop", "db"])

        #subprocess.call(["lxc", "publish", "lb", "--alias", "lb"])
        #subprocess.call(["lxc", "publish", "db", "--alias", "db"]) 
 

        time.sleep(3)
        subprocess.Popen(["lxc", "list"])

        
        