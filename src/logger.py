from src.utils import get_project_root,sendMsgTelegram
import logging
import os

root = get_project_root()
logFileName = str(root) + "/logs/acoes.log"
if not os.path.exists(logFileName):
    with open(logFileName, 'w'): pass
logging.basicConfig(filename = logFileName,  
                    level = logging.DEBUG, 
                    format = "%(asctime)s :: %(message)s", 
                     # w -> sobrescreve o arquivo a cada log
                    # a -> não sobrescreve o arquivo
                    filemode = "a")
logger = logging.getLogger('root')

def writeLog(msg, tipo = 'info'):
    #sendMsgTelegram(msg)
    if tipo == 'debug':
        logger.info(msg)
        
    elif tipo == 'error':
        logger.error(msg)
        print("ERROR: " + msg)
    else:
        logger.info(msg)
        print(msg)
    
    