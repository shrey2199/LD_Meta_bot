# -*- coding: utf-8 -*-

import telegram
import telebot
import logging
import time
import sys
from telegraph import Telegraph
from functools import wraps
from random import *

# UPTIME

botStartTime = time.time()

# CONFIG

from config import Config

BOT_TOKEN = Config.BOT_TOKEN
ADMIN_IDS = Config.ADMIN_IDS

# ADMIN / OWNER

try:
    ADMIN_LIST = ADMIN_IDS
    if len(ADMIN_LIST) != 0:
        restricted_mode = True
    else:
        restricted_mode = False
except:
    ADMIN_LIST = []  # ==> Do Not Touch This !!
    restricted_mode = False

# BOT CODE

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

CHAT_IDS = ADMIN_IDS.split()

class SIG():
    def sigterm_handler(signum, frame):
        print("Stopping Bot...")
        for i in CHAT_IDS:
            if len(i) != 0 and i.isnumeric() == True:
                bot.send_message(int(i), "*SIGTERM* Received\n\nExiting With Status Code : *0*\n\n`The BOT will Shut Down Now !`", parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                pass
        sys.exit(1)

    def sigint_handler(signum, frame):
        print("Stopping Bot...")
        for i in CHAT_IDS:
            if len(i) != 0 and i.isnumeric() == True:
                bot.send_message(int(i), "*SIGINT* Received\n\nExiting With Status Code : *0*\n\n`The BOT will Shut Down Now !`", parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                pass
        sys.exit(143)