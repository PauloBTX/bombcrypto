from pathlib import Path
import mss
import numpy as np
import telegram


tokenTelegramBot = ''
meuChatIdTelegram = ''
bot=telegram.Bot(token=tokenTelegramBot)

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def printScreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:,:,:3]

def sendMsgTelegram(msg):
    #r = requests.get("https://api.telegram.org/bot" + tokenTelegramBot + "/sendMessage?chat_id=" + meuChatIdTelegram + "&parse_mode=telegram.ParseMode.HTML&text=" + msg)
    bot.send_message(chat_id=meuChatIdTelegram, 
                 text=msg,
                 parse_mode=telegram.ParseMode.HTML,
                 timeout=60)   
