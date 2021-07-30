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

class settingsedit:
    def settings_mod(m):
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        
        try:
            r = requests.get(url)
            res = r.json()
            if res["code"] == 200 and res["success"] == True:
                config = res["content"]
                SetS = ""
                for i in config.keys():
                    if i == "category_list" or i == "account_list" or i == "service_accounts" or i == "token_expiry" or i == "ui_config":
                        continue
                    SetAddS = "• `" + i + "` : `" + str(config[i]) + "`\n\n"
                    SetS = SetS + SetAddS
                bot.send_message(m.chat.id, text="*Libdrive Server Settings :-*\n\n" + str(SetS) , parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        
    def set_mod(m):
        chat = m.text[4:]
        i = ""
        if len(m.text.split()) == 1:
            i = ""
        elif len(m.text.split()) == 2 or len(m.text.split()) == 3:
            i += m.text.split()[1]
        if chat == "":
            bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
            \n*To Change a Setting :-*
            Send /set `<key> <value>`
            \nGet `keys` by sending /settings
            \n⚠ Do Not Use This Command For Accounts, Categories and UI Config
            \nSeperate Commands are available for that !!""", parse_mode=telegram.ParseMode.MARKDOWN)
        elif i == "category_list" or i == "account_list" or i == "service_accounts" or i == "token_expiry" or i == "ui_config":
            bot.send_message(m.chat.id, text = """The /set Command does not work for this key.
            \n⚠️ Do Not Use The /set Command For :-
            Accounts, Categories and UI Config
            \nSome other keys are also not supported...
            """, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            key = m.text.split()[1]
            value_script = m.text.split()[2]
            if value_script.isnumeric() == True:
                value = int(value_script)
            else:
                value = value_script
            url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET    
            try:
                r1 = requests.get(url)
                res1 = r1.json()
                conf = res1["content"]
                prev = conf[key]
                conf[key] = value

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

                    bot.send_message(m.chat.id, text="*Libdrive Setting *`" + key + "` Successfully Changed !!\n\nFrom `" + str(prev) + "` *→* `" + str(value) + "`" , parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                else:
                    bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
            except:
                bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)
    
    def ui_mod(m):
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        
        try:
            r = requests.get(url)
            res = r.json()
            if res["code"] == 200 and res["success"] == True:
                config = res["content"]["ui_config"]
                SetS = ""
                for i in config.keys():
                    SetAddS = "• `" + i + "` : `" + str(config[i]) + "`\n\n"
                    SetS = SetS + SetAddS
                bot.send_message(m.chat.id, text="*Libdrive UI Settings :-*\n\n" + str(SetS) , parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

    def setui_mod(m):
        chat = m.text[6:]
        if chat == "":
            bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
            \n*To Change a Setting :-*
            Send /setui `<key> <value>`
            \nGet `keys` by sending /ui
            """, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            key = m.text.split()[1]
            value_script = m.text.split()[2]
            if value_script.isnumeric() == True:
                value = int(value_script)
            else:
                value = value_script
            url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
            try:
                r1 = requests.get(url)
                res1 = r1.json()
                conf = res1["content"]
                confui = res1["content"]["ui_config"]
                prev = confui[key]
                confui[key] = value

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

                    bot.send_message(m.chat.id, text="*Libdrive UI Setting *`" + key + "` Successfully Changed !!\n\nFrom `" + str(prev) + "` *→* `" + str(value) + "`" , parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                else:
                    bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
            except:
                bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)
