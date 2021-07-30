import telegram
import telebot
import logging
import time
from speedtest import Speedtest

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

def speedtestmes(m):
    test = Speedtest()
    test.get_best_server()
    dl = bot.send_message(m.chat.id, "`Checking Download Speeds ...`", parse_mode=telegram.ParseMode.MARKDOWN)
    test.download()
    ul = bot.edit_message_text("`Checking Upload Speeds ...`", chat_id=m.chat.id, message_id=dl.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result["share"])
    string_speed = f'''
    *Server :*
    *Name:* `{result['server']['name']}`
    *Country:* `{result['server']['country']}, {result['server']['cc']}`
    *Sponsor:* `{result['server']['sponsor']}`
    *ISP:* `{result['client']['isp']}`

*SpeedTest Results :*
    *Upload:* `{speed_convert(result['upload'] / 8)}`
    *Download:*  `{speed_convert(result['download'] / 8)}`
    *Ping:* `{result['ping']} ms`
    *ISP Rating:* `{result['client']['isprating']}`
    '''
    
    bot.send_photo(m.chat.id, path, caption = string_speed, parse_mode=telegram.ParseMode.MARKDOWN)
    bot.delete_message(chat_id=m.chat.id, message_id=ul.message_id)

def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "MB/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"