import telegram
import telebot
import logging
import requests
from telegraph import Telegraph
import json
from random import *

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

allchar = "abcdefghijklmnopqrstuvwxyz0123456789"

class configsetups:
    def fixconfigmes(m):
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        try:

            fix = bot.send_message(m.chat.id, text="`Fixing Your LibDrive Config ...`", parse_mode=telegram.ParseMode.MARKDOWN)

            r1 = requests.get(url)
            res1 = r1.json()
            conf = res1["content"]

            # configs

            kill_switch = {
                "kill_switch":False
                }
            ui_config = {
                "ui_config":{
                    "title":"libDrive", 
                    "icon":"https://avatars.githubusercontent.com/u/75073550?v=4", 
                    "range":"16"
                    }
                }

            if "ui_config" in conf.keys():
                uiconf = conf["ui_config"]
                if "title" in uiconf.keys() and "icon" in uiconf.keys() and "range" in uiconf.keys():
                    pass
                if "title" not in uiconf.keys():
                    uiconf.update({"title":"libDrive"})
                if "range" not in uiconf.keys():
                    uiconf.update({"range":16})
                if "icon" not in uiconf.keys():
                    uiconf.update({"icon":"https://avatars.githubusercontent.com/u/75073550?v=4"})
                else:
                    pass
            if "ui_config" not in conf.keys():
                conf.update(ui_config)
            if "kill_switch" not in conf.keys():
                conf.update(kill_switch)
            else:
                pass

            headers = {
                'authority': LD_DOMAIN,
                'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
                'accept': 'application/json, text/plain, */*',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://' + LD_DOMAIN,
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://' + LD_DOMAIN + '/settings',
                'accept-language': 'en-US,en;q=0.9',
            }

            params = (
                ('secret', SECRET),
            )

            data = json.dumps(conf)
                
            r = requests.post('https://' + LD_DOMAIN + '/api/v1/config', headers=headers, params=params, data=data)
            res = r.json()
            if res["code"] == 200 and res["success"] == True:
                bot.edit_message_text("*Successfully Fixed Your LibDrive Config.*", m.chat.id, message_id=fix.message_id, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            else:
                bot.edit_message_text("`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", m.chat.id, message_id=fix.message_id, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        except:
            bot.edit_message_text("`LibDrive Server Not Accessible !!`", m.chat.id, message_id=fix.message_id, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

    def assignidmes(m):
        min_char = 8
        max_char = 8
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        try:

            assign = bot.send_message(m.chat.id, text="`Assigning IDs ...`", parse_mode=telegram.ParseMode.MARKDOWN)

            r1 = requests.get(url)
            res1 = r1.json()
            conf = res1["content"]
            confacc = res1["content"]["account_list"]
            for acc in confacc:
                bot_id = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
                if "bot_id" in acc.keys():
                    pass
                else:
                    acc.update({"bot_id": bot_id})
            
            confcat = res1["content"]["category_list"]
            for cat in confcat:
                bot_id = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
                if "bot_id" in cat.keys():
                    pass
                else:
                    cat.update({"bot_id": bot_id})

            headers = {
                'authority': LD_DOMAIN,
                'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
                'accept': 'application/json, text/plain, */*',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://' + LD_DOMAIN,
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://' + LD_DOMAIN + '/settings',
                'accept-language': 'en-US,en;q=0.9',
            }

            params = (
                ('secret', SECRET),
            )

            data = json.dumps(conf)
                
            r = requests.post('https://' + LD_DOMAIN + '/api/v1/config', headers=headers, params=params, data=data)
            res = r.json()
            if res["code"] == 200 and res["success"] == True:
                bot.edit_message_text("*Successfully Assigned IDs to all Accounts and Categories*", m.chat.id, message_id=assign.message_id, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            else:
                bot.edit_message_text("`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", m.chat.id, message_id=assign.message_id, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        except:
            bot.edit_message_text("`LibDrive Server Not Accessible !!`", m.chat.id, message_id=assign.message_id, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    def unassignidmes(m):
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        try:

            unassign = bot.send_message(m.chat.id, text="`Deleting Assigned IDs ...`", parse_mode=telegram.ParseMode.MARKDOWN)

            r1 = requests.get(url)
            res1 = r1.json()
            conf = res1["content"]
            confacc = res1["content"]["account_list"]
            for acc in confacc:
                if "bot_id" in acc.keys():
                    del acc["bot_id"]
                else:
                    pass
            
            confcat = res1["content"]["category_list"]
            for cat in confcat:
                if "bot_id" in cat.keys():
                    del cat["bot_id"]
                else:
                    pass

            headers = {
                'authority': LD_DOMAIN,
                'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
                'accept': 'application/json, text/plain, */*',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://' + LD_DOMAIN,
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://' + LD_DOMAIN + '/settings',
                'accept-language': 'en-US,en;q=0.9',
            }

            params = (
                ('secret', SECRET),
            )

            data = json.dumps(conf)
                
            r = requests.post('https://' + LD_DOMAIN + '/api/v1/config', headers=headers, params=params, data=data)
            res = r.json()
            if res["code"] == 200 and res["success"] == True:
                bot.edit_message_text("*Successfully Deleted IDs of all Accounts and Categories*", m.chat.id, message_id=unassign.message_id, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            else:
                bot.edit_message_text("`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", m.chat.id, message_id=unassign.message_id, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
        except:
            bot.edit_message_text("`LibDrive Server Not Accessible !!`", m.chat.id, message_id=unassign.message_id, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
