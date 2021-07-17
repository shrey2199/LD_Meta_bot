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
    	Send /rebuild to the bot.
        \n<b>To View Registered Accounts of your Libdrive :-</b>
        Send /accounts to the bot.
        \n<b>To View the Categories of your Libdrive :-</b>
        Send /categories to the bot.
        \n<b>To View all other configs of your Libdrive :-</b>
        Send /config to the bot.
        """, parse_mode=telegram.ParseMode.HTML)

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

@bot.message_handler(commands=['accounts'])
@restricted
def short(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
    
    try:
        r = requests.get(url)
        res = r.json()
        if res["code"] == 200 and res["success"] == True:
            AccL = res["content"]["account_list"]
            AccS = ""
            AccN = 0
            for account in AccL:
                AccN+=1
                AccS=AccS + str(AccN) + ". <b>" + str(account["username"]) + " :</b> <code>" + str(account["auth"]) + "</code>\n"
            bot.send_message(m.chat.id, text="<b>Registered Accounts :-</b>\n\n" + str(AccS) , parse_mode=telegram.ParseMode.HTML)
        else:
            bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
    except:
        bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['categories'])
@restricted
def short(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
    
    try:
        r = requests.get(url)
        res = r.json()
        if res["code"] == 200 and res["success"] == True:
            CatL = res["content"]["category_list"]
            CatS = ""
            CatN = 0
            for category in CatL:
                CatN+=1
                CatS=CatS + str(CatN) + ". <b>" + str(category["name"]) + " :</b>\n    Type : <code>" + str(category["type"]) + "</code>\n    Folder ID : <code>" + str(category["id"]) + "</code>\n"
            bot.send_message(m.chat.id, text="<b>Categories :-</b>\n\n" + str(CatS) , parse_mode=telegram.ParseMode.HTML)
        else:
            bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
    except:
        bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['config'])
@restricted
def short(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
    
    try:
        r = requests.get(url)
        res = r.json()
        if res["code"] == 200 and res["success"] == True:
            config = res["content"]
            ConSgoogle = "✯ <b> Access Token :</b> <code>" + str(config["access_token"]) + "</code>\n\n" + "✯ <b> Client ID :</b> <code>" + str(config["client_id"]) + "</code>\n\n" + "✯ <b> Client Secret :</b> <code>" + str(config["client_secret"]) + "</code>\n\n" + "✯ <b> Refresh Token :</b> <code>" + str(config["refresh_token"]) + "</code>\n\n" + "✯ <b> Token Expiry :</b> <code>" + str(config["token_expiry"]) + "</code>\n\n"
            bot.send_message(m.chat.id, text="<b>Google Credentials :-</b>\n\n" + str(ConSgoogle) , parse_mode=telegram.ParseMode.HTML)
            ConSsite = "✯ <b> Title :</b> <code>" + str(config["ui_config"]["title"]) + "</code>\n\n" + "✯ <b> Icon :</b> <code>" + str(config["ui_config"]["icon"]) + "</code>\n\n" + "✯ <b> Page Range :</b> <code>" + str(config["ui_config"]["range"]) + "</code>\n\n"
            bot.send_message(m.chat.id, text="<b>Website Configs :-</b>\n\n" + str(ConSsite) , parse_mode=telegram.ParseMode.HTML)
            ConSbuild = "✯ <b> Build Interval :</b> <code>" + str(config["build_interval"]) + "</code>\n\n" + "✯ <b> Build Type :</b> <code>" + str(config["build_type"]) + "</code>\n\n"
            bot.send_message(m.chat.id, text="<b>Build Settings :-</b>\n\n" + str(ConSbuild) , parse_mode=telegram.ParseMode.HTML)
        else:
            bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
    except:
        bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

bot.polling(none_stop=True, timeout=3600)
