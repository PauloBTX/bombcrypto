from src.utils import get_project_root,sendMsgTelegram
from colorama import init, Fore, Back, Style
import logging
import os

#init do colorama
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL
init(autoreset=True)
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
        print(Back.RED + 'ERROR:' + Back.WHITE + Fore.MAGENTA + msg)
    else:
        logger.info(msg)
        print(Back.BLUE + 'INFO:' + Back.WHITE + Fore.BLACK + msg)
    
    