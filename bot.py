# -*- coding: utf-8 -*-
 
import telegram
import telebot
import logging
import requests
import json
from functools import wraps

# CONFIG

from config import Config

BOT_TOKEN = Config.BOT_TOKEN
LD_DOMAIN = Config.LD_DOMAIN
SECRET = Config.SECRET
ADMIN_IDS = Config.ADMIN_IDS

# BOT CODE

try:
    ADMIN_LIST = ADMIN_IDS 
    restricted_mode = True
except:
    ADMIN_LIST = []  # ==> Do Not Touch This !!
    restricted_mode = False

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

def restricted(func):
    @wraps(func)
    def wrapped(update, *args, **kwargs):
        user_id = update.from_user.id
        if (restricted_mode) and (str(user_id) not in ADMIN_LIST):
            print("Unauthorized access denied for {} - {}.".format(user_id, update.from_user.username))
            bot.send_message(update.chat.id, "*Error :\t\t*You are not Authorized to access the bot.\n\nPls Contact [Bot Admin](https://t.me/s_rawal) !!", parse_mode='Markdown', disable_web_page_preview=True)
            return
        return func(update, *args, **kwargs)
    return wrapped

@bot.message_handler(commands=['start'])
@restricted
def start(m):
    bot.send_message(m.chat.id, text="Hi ! Welcome to Libdrive Metadata Rebuild Bot !\n\nSend /help for More Info !", parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['help'])
@restricted
def help(m):
    bot.send_message(chat_id=m.chat.id, text="""This Bot will help you to rebuild the metadata of your Libdrive Server.
    	\n<b>To Rebuild the Metadata of your Libdrive :-</b>
    	Send /rebuild to the bot.""", parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['rebuild'])
@restricted
def short(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/rebuild?secret=' + SECRET
    
    try:
        r = requests.get(url)
        res = r.json()
        if res["code"] == 200 and res["success"] == True:
            bot.send_message(m.chat.id, text="<code>Metadata Rebuilt Successfully !!</code>", parse_mode=telegram.ParseMode.HTML)
        else:
            bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
    except:
        bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

bot.polling(none_stop=True, timeout=3600)
