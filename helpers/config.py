import telegram
import telebot
import logging
import time
import requests

# UPTIME

botStartTime = time.time()

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

def configmes(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
    r = requests.get(url)
    res = r.json()
    config = res["content"]
    if "ui_config" in config.keys():
        try:
            if res["code"] == 200 and res["success"] == True:
                global ConSgoogle
                ConSgoogle = "*Google Credentials :-*\n\n✯ * Access Token :* `" + str(config["access_token"]) + "`\n\n" + "✯ * Client ID :* `" + str(config["client_id"]) + "`\n\n" + "✯ * Client Secret :* `" + str(config["client_secret"]) + "`\n\n" + "✯ * Refresh Token :* `" + str(config["refresh_token"]) + "`\n\n" + "✯ * Token Expiry :* `" + str(config["token_expiry"]) + "`\n\n"
                global ConSothers
                ConSothers = "*Server Configs :-*\n\n✯ * Build Interval :* `" + str(config["build_interval"]) + "`\n\n" + "✯ * Build Type :* `" + str(config["build_type"]) + "`\n\n" + "✯ * Cloudflare :* `" + str(config["cloudflare"]) + "`\n\n" + "✯ * Signup :* `" + str(config["signup"]) + "`\n\n" + "✯ * Subtitles :* `" + str(config["subtitles"]) + "`\n\n" + "✯ * TMDB API :* `" + str(config["tmdb_api_key"]) + "`\n\n" + "✯ * Transcoded :* `" + str(config["transcoded"]) + "`\n\n"
                global ConSsite
                ConSsite = "*Website Configs :-*\n\n✯ * Title :* `" + str(config["ui_config"]["title"]) + "`\n\n" + "✯ * Icon :* `" + str(config["ui_config"]["icon"]) + "`\n\n" + "✯ * Page Range :* `" + str(config["ui_config"]["range"]) + "`\n\n"
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.row(
                    telebot.types.InlineKeyboardButton('❌', callback_data='close'),
                    telebot.types.InlineKeyboardButton('Server Configs', callback_data='1')
                )
                ConShome = '<b>Hello <a href="telegram.me/' + m.from_user.username + '">' + m.from_user.first_name + '</a>,\n\nIf You Want to Change a Config :\n\n1. Get the Config <code>key</code> by using : /settings\n\n2. Change the Config using : /set <code>key</code> <code>value</code></b>'
                global configs
                configs = bot.send_message(m.chat.id, ConShome, reply_markup=keyboard, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        try:
            if res["code"] == 200 and res["success"] == True:
                global ConSgooglewui
                ConSgooglewui = "*Google Credentials :-*\n\n✯ * Access Token :* `" + str(config["access_token"]) + "`\n\n" + "✯ * Client ID :* `" + str(config["client_id"]) + "`\n\n" + "✯ * Client Secret :* `" + str(config["client_secret"]) + "`\n\n" + "✯ * Refresh Token :* `" + str(config["refresh_token"]) + "`\n\n" + "✯ * Token Expiry :* `" + str(config["token_expiry"]) + "`\n\n"
                global ConSotherswui
                ConSotherswui = "*Server Configs :-*\n\n✯ * Build Interval :* `" + str(config["build_interval"]) + "`\n\n" + "✯ * Build Type :* `" + str(config["build_type"]) + "`\n\n" + "✯ * Cloudflare :* `" + str(config["cloudflare"]) + "`\n\n" + "✯ * Signup :* `" + str(config["signup"]) + "`\n\n" + "✯ * Subtitles :* `" + str(config["subtitles"]) + "`\n\n" + "✯ * TMDB API :* `" + str(config["tmdb_api_key"]) + "`\n\n" + "✯ * Transcoded :* `" + str(config["transcoded"]) + "`\n\n"
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.row(
                    telebot.types.InlineKeyboardButton('❌', callback_data='closewui'),
                    telebot.types.InlineKeyboardButton('Server Configs', callback_data='1wui')
                )
                ConShome = '<b>Hello <a href="telegram.me/' + m.from_user.username + '">' + m.from_user.first_name + '</a>,\n\nIf You Want to Change a Config :\n\n1. Get the Config <code>key</code> by using : /settings\n\n2. Change the Config using : /set <code>key</code> <code>value</code></b>'
                global configswui
                configswui = bot.send_message(m.chat.id, ConShome, reply_markup=keyboard, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)

def get_callback(query):
    bot.answer_callback_query(query.id)
    config_update_message(query.message)

def config_update_message(m, data):
    if data == '1' or data == '2' or data == '3' or data == 'close':
        if data == '1' or data == '2' or data == '3':  
            if data == '1':
                pg = ConSgoogle
            elif data == '2':
                pg = ConSothers
            elif data == '3':
                pg = ConSsite
            bot.edit_message_text(pg,
                m.chat.id, message_id=configs.message_id,
                reply_markup=config_update_keyboard(pg, data),
                parse_mode=telegram.ParseMode.MARKDOWN)
        elif data == 'close':
            bot.delete_message(m.chat.id, message_id=configs.message_id)
        else:
            pass
    elif data == '1wui' or data == '2wui' or data == 'closewui':
        if data == '1wui' or data == '2wui':  
            if data == '1wui':
                pg = ConSgooglewui
            elif data == '2wui':
                pg = ConSotherswui
            bot.edit_message_text(pg,
                m.chat.id, message_id=configswui.message_id,
                reply_markup=config_update_keyboard(pg),
                parse_mode=telegram.ParseMode.MARKDOWN)
        elif data == 'closewui':
            bot.delete_message(m.chat.id, message_id=configswui.message_id)
        else:
            pass
    else:
        pass

def config_update_keyboard(pg, data):
    if data == '1':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('⬅️', callback_data='3'),
            telebot.types.InlineKeyboardButton('❌', callback_data='close'),
            telebot.types.InlineKeyboardButton('➡️', callback_data='2')
        )
        return keyboard
    elif data == '2':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('⬅️', callback_data='1'),
            telebot.types.InlineKeyboardButton('❌', callback_data='close'),
            telebot.types.InlineKeyboardButton('➡️', callback_data='3')
        )
        return keyboard
    elif data == '3':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('⬅️', callback_data='2'),
            telebot.types.InlineKeyboardButton('❌', callback_data='close'),
            telebot.types.InlineKeyboardButton('➡️', callback_data='1')
        )
        return keyboard
    elif data == '1wui':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('❌', callback_data='closewui'),
            telebot.types.InlineKeyboardButton('➡️', callback_data='2wui')
        )
        return keyboard
    elif data == '2wui':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('⬅️', callback_data='1wui'),
            telebot.types.InlineKeyboardButton('❌', callback_data='closewui')
        )
        return keyboard
    else:
        pass

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)