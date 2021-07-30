import telegram
import telebot
import logging
import os

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

def hrestart_mod(m):
    try:
        restart = bot.send_message(m.chat.id, text="`Restarting Dynos ...n\n\nPls Wait for 2-3 minutes for LibDrive to be Back...`", parse_mode=telegram.ParseMode.MARKDOWN)

        cmd = 'heroku dyno:restart web.1 -a ' + HEROKU_APP_NAME
        stream = os.popen(cmd)
        output = stream.readlines()

    except:
        bot.edit_message_text("`Heroku Not Accessible !!`", m.chat.id, message_id=restart.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

def hdyno_mod(m):
    try:
        dyno = bot.send_message(m.chat.id, text="`Getting Dyno Stats ...`", parse_mode=telegram.ParseMode.MARKDOWN)

        cmd = 'heroku ps -a ' + HEROKU_APP_NAME
        stream = os.popen(cmd)
        output = stream.readlines()

        res = "*Heroku Dyno STATS :-*\n\n" + output[0] + "\n" + output[1] + "\n" + output[6]
        print(res)
        
        bot.edit_message_text(res, m.chat.id, message_id=dyno.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        bot.edit_message_text("`Heroku Not Accessible !!`", m.chat.id, message_id=dyno.message_id, parse_mode=telegram.ParseMode.MARKDOWN)