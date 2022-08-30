import subprocess
import sys
import time
import pickle



with open('num_cont.txt', 'rb') as fich:
    var = pickle.load(fich)
print("value from the file: ",var)
var = int(var)
for i in range(1, var):
    nombre_cont = "s" + str(i)     
    ip_in = False
    while not ip_in:
        time.sleep(3)
        subprocess.call(["lxc", "file", "push", "rest_server.js", nombre_cont+"/root/app/rest_server.js"])
        time.sleep(2)
        respuesta = subprocess.run(["lxc", "exec", nombre_cont, "--", "cat", "app/rest_server.js"], stdout=subprocess.PIPE)
        ip_in = str(var) in respuesta.stdout.decode("utf-8")
        subprocess.call(["lxc", "stop", nombre_cont, "--force"])
        subprocess.call(["lxc", "start", nombre_cont])