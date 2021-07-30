import telegram
import telebot
import logging
import requests

# CONFIG

from config import Config

BOT_TOKEN = Config.BOT_TOKEN
LD_DOMAIN = Config.LD_DOMAIN
SECRET = Config.SECRET
ADMIN_IDS = Config.ADMIN_IDS
PIC = Config.PIC
HEROKU_API_KEY = Config.HEROKU_API_KEY
HEROKU_APP_NAME = Config.HEROKU_APP_NAME

try:
    ADMIN_LIST = ADMIN_IDS 
    restricted_mode = True
except:
    ADMIN_LIST = []  # ==> Do Not Touch This !!
    restricted_mode = False

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

def rebuildmes(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/rebuild?secret=' + SECRET
    
    try:
        r = requests.get(url)
        res = r.json()
        if res["code"] == 200 and res["success"] == True:
            bot.send_message(m.chat.id, text="`Metadata Rebuilt Successfully !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)