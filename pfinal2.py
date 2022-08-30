'''
Created on 6 may. 2022

@author: francesco.vaccaro
'''
#libraries
import logging
import sys
from sqlalchemy.sql.expression import except_


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    logger.info("el comando teclado es: %s ", sys.argv[1])
except IndexError:
    sys.exit("no se ha insertado algun comando o es equivocado") 
    
    
    
if sys.argv[1] == 'crear':
    from crear import crear
    crear()
    logger.info("se esta creando el sistema")
    
    
elif sys.argv[1] == 'arrancar':
    logger.info("se esta arrancando el sistema")
    from arrancar import arrancar
    arrancar()    

elif sys.argv[1] == 'destruir':
    logger.info("se esta destruyendo el sistema")
    from destruir import destruir
    destruir() 
    
elif sys.argv[1] == 'parar':
    logger.info("se esta parando el sistema")
    from parar import parar
    parar()

elif sys.argv[1] == 'configurar':
    logger.info("se esta configurando el sistema en remoto (DB)")
    from configurar import configurar
    configurar()   
    
else:
    logger.error("Comando no reconocido")
