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

class accountsetup:
    def accountsmes(m):
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        
        try:

            tempacc = bot.send_message(m.chat.id, text="`Getting Your Accounts ...`", parse_mode=telegram.ParseMode.MARKDOWN)
            r = requests.get(url)
            res = r.json()
            if res["code"] == 200 and res["success"] == True:
                AccL = res["content"]["account_list"]
                AccS = ""
                AccN = 0
                for account in AccL:
                    if "bot_id" in account.keys():
                        AccN+=1
                        AccS=AccS + str(AccN) + ". *" + str(account["username"]) + " :* `" + str(account["auth"]) + "`\n    To Delete : /rmaccid `" + str(account["bot_id"]) + "`\n\n"
                    else:
                        AccN+=1
                        AccS=AccS + str(AccN) + ". *" + str(account["username"]) + " :* `" + str(account["auth"]) + "`\n\n"
                bot.delete_message(m.chat.id, message_id=tempacc.message_id)
                bot.send_message(m.chat.id, text="*Registered Accounts :-*\n\n" + str(AccS) , parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.delete_message(m.chat.id, message_id=tempacc.message_id)
                bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.delete_message(m.chat.id, message_id=tempacc.message_id)
            bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

    def accountsclipmes(m):
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        try:

            tempacc = bot.send_message(m.chat.id, text="`Getting Your Accounts ...`", parse_mode=telegram.ParseMode.MARKDOWN)
            r = requests.get(url)
            res = r.json()
            if res["code"] == 200 and res["success"] == True:
                AccL = res["content"]["account_list"]
                TAcc = 0
                AccS = ""
                AccN = 0
                for account in AccL:
                    if "bot_id" in account.keys():
                        AccN+=1
                        AccS=AccS + str(AccN) + ". " + str(account["username"]) + " : " + str(account["auth"]) + "\n    To Delete : /rmaccid " + str(account["bot_id"]) + "\n\n"
                    else:
                        AccN+=1
                        AccS=AccS + str(AccN) + ". " + str(account["username"]) + " : " + str(account["auth"]) + "\n\n"
                    TAcc+=1

                headers = {
                    'Content-Type': 'text/html; charset=UTF-8',
                }

                data = str(AccS)

                clip_random = "".join(choice(allchar) for x in range(randint(20, 20)))

                clip_api_url = 'https://api.cl1p.net/{}'.format(clip_random)
                clip_url = 'https://cl1p.net/{}'.format(clip_random)

                response = requests.post(clip_api_url, headers=headers, data=data)

                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.row(
                    telebot.types.InlineKeyboardButton("Your Accounts !!", url=clip_url)
                )

                bot.delete_message(m.chat.id, message_id=tempacc.message_id)
                bot.send_message(m.chat.id, text=f"*Accounts Found !!*\n\n`Total Accounts : `{TAcc}", reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN)
                print(clip_api_url, "  &  ", clip_url)
            else:
                bot.delete_message(m.chat.id, message_id=tempacc.message_id)
                bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.delete_message(m.chat.id, message_id=tempacc.message_id)
            bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

    def addaccountmes(m):
        chat = m.text[11:]
        if chat == "":
            bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
            \n*To Add an Account :-*
            Send /addaccount `<user> <pass> <pic>`
            """, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot_id = "".join(choice(allchar) for x in range(randint(8, 8)))
            username = m.text.split()[1]
            password = m.text.split()[2]
            if len(m.text.split()) == 4:
                pic = m.text.split()[3]
            else:
                pic = ""
            auth = "".join(choice(allchar) for x in range(randint(50, 50)))
            url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
            try:
                r1 = requests.get(url)
                res1 = r1.json()
                conf = res1["content"]
                confacc = res1["content"]["account_list"]
                accdic = {
                    "auth":auth,
                    "password":password,
                    "pic":pic,
                    "username":username,
                    "bot_id":bot_id
                }
                confacc.append(accdic)

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
                    AccS="*Username :* `" + username + "`\n*Password :* `" + password + "`\n*Auth :* `" + auth + "`\n*Pic :* `" + pic + "`\n"
                    bot.send_message(m.chat.id, text="*Account Added Successfully :- *\n\n" + AccS , parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                else:
                    bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
            except:
                bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

    def rmaccountmes(m):
        chat = m.text[10:]
        if chat == "":
            bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
            \n*To Remove an Account :-*
            Send /rmaccount `<user> <pass>`
            """, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            username = m.text.split()[1]
            password = m.text.split()[2]
            url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
            try:
                r1 = requests.get(url)
                res1 = r1.json()
                conf = res1["content"]
                confacc = res1["content"]["account_list"]
                for acc in confacc:
                    if acc["username"] == username and acc["password"] == password:
                        confacc.remove(acc)
                    else:
                        continue
                
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
                    AccS="*Username :* `" + username + "`\n*Password :* `" + password + "`"
                    bot.send_message(m.chat.id, text="*Account Removed Successfully :- *\n\n" + AccS , parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                else:
                    bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
            except:
                bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

    def rmaccidmes(m):
        chat = m.text[8:]
        if chat == "":
            bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
            \n*To Remove an Account :-*
            Send /rmaccid `<id>`
            \nGet Account's ID with /accounts
            """, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            id = m.text.split()[1]
            url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
            try:
                r1 = requests.get(url)
                res1 = r1.json()
                conf = res1["content"]
                confacc = res1["content"]["account_list"]
        
                for acc in confacc:
                    if acc["bot_id"] == id:
                        confacc.remove(acc)
                        username = acc["username"]
                        password = acc["password"]
                    else:
                        continue
                
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
                    AccS="*Username :* `" + username + "`\n*Password :* `" + password + "`"
                    bot.send_message(m.chat.id, text="*Account with ID - *`" + id + "`* Removed Successfully :- *\n\n" + AccS , parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
                else:
                    bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
            except:
                bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)
