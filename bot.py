# -*- coding: utf-8 -*-

import telegram
import telebot
import logging
import requests
import os
import json
import time
import heroku3
from telegraph import Telegraph
from functools import wraps
from random import *
from speedtest import Speedtest
from helpers.speedtest import speed_convert
from helpers.uptime import get_readable_time

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

CHAT_IDS = ADMIN_IDS.split()

for i in CHAT_IDS:
    if len(i) != 0 and i.isnumeric() == True:
        bot.send_message(int(i), "`Hey ! The Bot Is Up and Running !`", parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        pass

allchar = "abcdefghijklmnopqrstuvwxyz0123456789"

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

@bot.message_handler(commands=['start','hi'])
@restricted
def start(m):
    uptime = get_readable_time((time.time() - botStartTime))
    start_string = "Hi ! Welcome to Libdrive Manager Bot by [Shreyansh Rawal](telegram.me/s_rawal) !\n\n*I'm Alive Since : *`" + uptime + "`\n\n ✯ *For More Info*, Send /help to the Bot !!\n\n ✯ *Also Read the Important Instructions* by clicking the Instructions Button in /help !!"
    if len(PIC.replace(" ", "")) != 0:
        bot.send_photo(m.chat.id, PIC, caption = start_string, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.send_message(m.chat.id, start_string, parse_mode=telegram.ParseMode.MARKDOWN)


@bot.message_handler(commands=['help'])
@restricted
def help(m):
    global Helpstring
    Helpstring = """*This Bot will help you to Manage your Libdrive Server.*
    	\n/rebuild - *To Rebuild the Metadata of your Libdrive.*
        \n/restart - *To Restart LibDrive Server.*
        \n/fixconfig - *To Fix the Config of Your LibDrive by Adding Missing Keys.*
        \n/assignid - *To Assign `bot_id` to All Accounts and Categories.*
        \n/unassignid - *To Remove `bot_id` from All Accounts and Categories.*
        \n/accountsclip - *To View Your Accounts in An Online Paste. (One Time Visit Pastes at cl1p.net)*
        \n/accounts - *To View Registered Accounts of your Libdrive.*
        \n/addaccount - *To Add an Account to Libdrive.*
        \n/rmaccount - *To Remove an Account from Libdrive.*
        \n/rmaccid - *To Remove an Account from Libdrive using id.*
        \n/categories - *To View the Categories of your Libdrive.*
        \n/addcategory - *To Add a Category to Libdrive.*
        \n/rmcategory - *To Remove a Category from Libdrive.*
        \n/setanilist - *To Set/Change Anilist Config of a Category.*
        \n/config - *To View The Configs of your Libdrive.*
        \n/settings - *To View the Settings of your Libdrive.*
        \n/set - *To change The Settings of your Libdrive.*
        \n/ui - *To View the UI Configuration of your Libdrive.*
        \n/setui - *To change The UI Settings of your Libdrive.*
        \n/hrestart - *To Restart Heroku Dynos. (Only Heroku Deploys)*
        \n/hdyno - *To View Heroku Dyno Stats. (Only Heroku Deploys)*
        \n/search - *To Search Libdrive and Get Direct Download Links.*
        \n/speedtest - *To Perform a Speedtest on the Server. (Completely Irrelevant 😂)*
        """
    global Inststring
    Inststring = """*Instructions for Using The Bot : *
    \n1. `Do Not Use The "` /set `" Command For Accounts, Categories and UI Config.`
    \n2. `Before Using The Bot, Please Use The Command "` /fixconfig `" to Fix the Config of Your LibDrive by Adding Missing Keys.` 
    \n3. `Before Using the Features of this Bot, Please Use The Command "` /assignid `" to assign Bot Identifiable IDs to your LibDrive Accounts and Categories.`
    \n4. `Assigning these IDs is `*Important for Full Fuctionality*` of the Bot.`
    \n5. `Using This command adds an element `*bot_id*` to your Accounts and Categories in LibDrive Config.`
    \n6. `This will not affect any kind of functioning in your LibDrive.`
    \n7. `These IDs can be removed from your LibDrive Config by using "` /unassignid `" Command.`
        """
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('❌', callback_data='closehelp'),
        telebot.types.InlineKeyboardButton('Instructions', callback_data='instructions')
    )
    global HelpMessage
    HelpMessage = bot.send_message(m.chat.id, Helpstring, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

@bot.message_handler(commands=['speedtest'])
@restricted
def speedtest(m):
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
    

@bot.message_handler(commands=['rebuild'])
@restricted
def rebuild(m):
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

@bot.message_handler(commands=['restart'])
@restricted
def restart(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/restart?secret=' + SECRET
    
    try:
        r = requests.get(url)
        res = str(r)
        if res == str("<Response [503]>"):
            bot.send_message(m.chat.id, text="`LibDrive Restarted Successfully !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

@bot.message_handler(commands=['fixconfig'])
@restricted
def fixconfig(m):
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
        prefer_mp4 = {"prefer_mp4":False}

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
        if "prefer_mp4" not in conf.keys():
            conf.update(prefer_mp4)
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

@bot.message_handler(commands=['assignid'])
@restricted
def assignid(m):
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

@bot.message_handler(commands=['unassignid'])
@restricted
def unassignid(m):
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

@bot.message_handler(commands=['accounts'])
@restricted
def accounts(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
    
    try:
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
            bot.send_message(m.chat.id, text="*Registered Accounts :-*\n\n" + str(AccS) , parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

@bot.message_handler(commands=['accountsclip'])
def accountsclip(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
    try:
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

            bot.send_message(m.chat.id, text=f"*Accounts Found !!*\n\n`Total Accounts : `{TAcc}", reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN)
            print(clip_api_url, "  &  ", clip_url)
        else:
            bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

@bot.message_handler(commands=['addaccount'])
@restricted
def addaccount(m):
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

@bot.message_handler(commands=['rmaccount'])
@restricted
def rmaccount(m):
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

@bot.message_handler(commands=['rmaccid'])
@restricted
def rmaccid(m):
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

@bot.message_handler(commands=['categories'])
@restricted
def categories(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
    try:
        r1 = requests.get(url)
        r2 = requests.get(url)
        res1 = r1.json()
        res2 = r2.json()
        if res1["code"] == 200 and res1["success"] == True and res2["code"] == 200 and res2["success"] == True:
            global conf
            conf = res1["content"]
            global CatL
            CatL = res1["content"]["category_list"]
            global CatC
            CatC = res2["content"]["category_list"]
            keyboard = telebot.types.InlineKeyboardMarkup()
            CatNum = 0
            CatSer = "cat"
            for category in CatC:
                CatName = category["name"]
                CatNum+=1
                CatSerial = CatSer + str(CatNum)
                category.update({"cats":CatSerial, "delete":"delete"+CatSerial})
                keyboard.row(
                    telebot.types.InlineKeyboardButton(CatName, callback_data=CatSerial)
                )
            keyboard.row(
                telebot.types.InlineKeyboardButton('❌ CLOSE ❌', callback_data='closecat')
            )
            global categories
            categories = bot.send_message(m.chat.id, text="*Categories :-*" , parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard, disable_web_page_preview=True)
        else:
            bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

@bot.message_handler(commands=['setanilist'])
@restricted
def setanilist(m):
    chat = m.text[11:]
    if chat == "":
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n*To Change Anilist :-*
        Send /setanilist `<id> <true/false>`
        \nGet Category's ID with /categories\n
        """, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        id = m.text.split()[1]
        value = m.text.split()[2]
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        try:
            r1 = requests.get(url)
            res1 = r1.json()
            conf = res1["content"]
            confcat = res1["content"]["category_list"]
            

            for cat in confcat:
                if cat["bot_id"] == id:
                    name = cat["name"]
                    if "anilist" in cat:
                        prev = cat["anilist"]
                        cat["anilist"] = value
                        changeanilist = "Anilist Value changed for Category `" + str(name) + "`\n\nFrom `" + str(prev) + "` *→* `" + str(value) + "`"
                    else:
                        cat.update({"anilist":value})
                        changeanilist = "Anilist Value set for Category `" + str(name) + "` to `" + str(value) + "`"
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
                bot.send_message(m.chat.id, changeanilist , parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

@bot.message_handler(commands=['addcategory'])
@restricted
def addcategory(m):
    chat = m.text[12:]
    if chat == "":
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n*To Add a Category :-*
        Send /addcategory `<name> <folder_id>`
        
        Use *_* to denote spaces in name.
        Eg. Typing `MY_FOLDER` as `<name>` will create a category named `MY FOLDER`.
        """, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot_id = "".join(choice(allchar) for x in range(randint(8, 8)))
        namecoded = m.text.split()[1]
        name = namecoded.replace("_", " ")
        folder_id = m.text.split()[2]
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        try:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Movies', callback_data='movies'),
                telebot.types.InlineKeyboardButton('TV Shows', callback_data='tv_shows'),
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Anilist - Movies', callback_data='amovies'),
                telebot.types.InlineKeyboardButton('Anilist - TV Shows', callback_data='atv_shows')
            )
            catadddet = "*Category Details :-*\n\n*Name : *" + name + "\n*Folder ID : *" + folder_id + "\n\nNow Choose Category Type (*Within 15 seconds*) :-"
            global catadd
            catadd = bot.send_message(m.chat.id, catadddet, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN)
            
            global cataddS
            cataddS = "Adding Category `" + name + "` to Libdrive ...\n\n`This might take around 15-30 Seconds...`"

            r1 = requests.get(url)
            res1 = r1.json()
            conf = res1["content"]
            confcat = res1["content"]["category_list"]

            for timex in range(1, 15):
                bot.send_chat_action(m.chat.id, 'typing')
                time.sleep(1)

            if type_media=='movies' or type_media=='tv_shows':
                anilist = False
                if type_media=='movies':
                    type_cat = 'Movies'
                if type_media=='tv_shows':
                    type_cat = 'TV Shows'
                else:
                    pass
            if type_media=='amovies' or type_media=='atv_shows':
                anilist = True
                if type_media=='amovies':
                    type_cat = 'Movies'
                if type_media=='atv_shows':
                    type_cat = 'TV Shows'
                else:
                    pass
            else:
                pass

            category_dict = {"id": folder_id, "name": name, "bot_id":bot_id, "type": str(type_cat)}
            CatS="*Name :* `" + name + "`\n*Folder ID :* `" + folder_id + "`\n*Type :* `" + type_cat + "`\n"

            if anilist==True:
                category_dict.update({"anilist":True})
                CatS = CatS + "*Anilist :* `" + "True" + "`\n"
            else:
                pass
            
            confcat.append(category_dict)

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
                bot.edit_message_text("*Category Added Successfully :- *\n\n" + CatS, m.chat.id, message_id=catadd2.message_id, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.edit_message_text("`LibDrive Server Not Accessible !!`", m.chat.id, message_id=catadd.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

@bot.message_handler(commands=['rmcategory'])
@restricted
def rmcategory(m):
    chat = m.text[11:]
    if chat == "":
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n*To Remove a Category :-*
        Send /rmcategory `<id>`
        \nGet Category's ID with /categories\n
        """, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        id = m.text.split()[1]
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        try:
            r1 = requests.get(url)
            res1 = r1.json()
            conf = res1["content"]
            confcat = res1["content"]["category_list"]
            

            for cat in confcat:
                if cat["bot_id"] == id:
                    confcat.remove(cat)
                    name = cat["name"]
                    type = cat["type"]
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
                CatS="*Name :* `" + name + "`\n*Type :* `" + type + "`"
                bot.send_message(m.chat.id, text="*Category with ID - *`" + id + "`* Removed Successfully :- *\n\n" + CatS , parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

@bot.message_handler(commands=['config'])
@restricted
def config(m):
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
                ConShome = '*Hello [' + m.from_user.first_name + '](' + m.from_user.username + '),\n\nIf You Want to Change a Config :\n\n1. Get the Config `key` by using : /settings\n\n2. Change to Config using : /set `key` `value`*'
                global configs
                configs = bot.send_message(m.chat.id, ConShome, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
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
                ConShome = '*Hello [' + m.from_user.first_name + '](' + m.from_user.username + '),\n\nIf You Want to Change a Config :\n\n1. Get the Config `key` by using : /settings\n\n2. Change the Config using : /set `key` `value`*'
                global configswui
                configswui = bot.send_message(m.chat.id, ConShome, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

@bot.message_handler(commands=['settings'])
@restricted
def settings(m):
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

@bot.message_handler(commands=['set'])
@restricted
def set(m):
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

@bot.message_handler(commands=['ui'])
@restricted
def ui(m):
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

@bot.message_handler(commands=['setui'])
@restricted
def setui(m):
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

@bot.message_handler(commands=['hrestart'])
def hrestart(m):
    try:
        restart = bot.send_message(m.chat.id, text="`Restarting Dynos ...n\n\nPls Wait for 2-3 minutes for LibDrive to be Back...`", parse_mode=telegram.ParseMode.MARKDOWN)

        cmd = 'heroku dyno:restart web.1 -a ' + HEROKU_APP_NAME
        stream = os.popen(cmd)
        output = stream.readlines()

    except:
        bot.edit_message_text("`Heroku Not Accessible !!`", m.chat.id, message_id=restart.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

@bot.message_handler(commands=['hdyno'])
def hdyno(m):
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

@bot.message_handler(commands=['search'])
def search(m):
    chat = m.text[7:]
    if chat == "" :
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n*To Search for Content :-*
        Send /search `<search_query>`
        """, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        query = m.text.split()[1]
        try:
            telegraph = Telegraph()

            telegraph_acc = telegraph.create_account(
                short_name="Shrey Lib",
                author_name="Shrey LibDrive Bot",
                author_url="https://github.com/shrey2199/LD_Meta_bot"
            )

            search_results = bot.send_message(m.chat.id, "`Searching Your LibDrive ...`\n\n`Query` : *{}*".format(query), parse_mode=telegram.ParseMode.MARKDOWN)

            url_conf = "https://{}/api/v1/config?secret={}".format(LD_DOMAIN, SECRET)

            r1 = requests.get(url_conf)
            res1 = r1.json()
            search_acc_auth = res1["content"]["account_list"][0]["auth"]

            url_meta = "https://{}/api/v1/metadata?a={}&q={}".format(LD_DOMAIN, search_acc_auth, query)

            r2 = requests.get(url_meta)
            res2 = r2.json()

            html_string = ""
            num_of_results = 0

            if res2["code"] == 200 and res2["success"] == True:
                for cat in res2["content"]:
                    if len(cat["children"]) != 0:
                        for media in cat["children"]:
                            num_of_results += 1
                            title = media["title"]
                            type_ = cat["categoryInfo"]["type"]
                            if "releaseDate" in media.keys():
                                releaseDate = media["releaseDate"]
                            else:
                                releaseDate = ""
                            if "backdropPath" in media.keys():
                                backdrop = media["backdropPath"]
                            else:
                                backdrop = ""
                            if "overview" in media.keys():
                                overview = media["overview"]
                            else:
                                overview = ""

                            if str(type_) == "TV Shows":
                                show_id = media["id"]
                                url_show = "https://{}/api/v1/metadata?a={}&id={}".format(LD_DOMAIN, search_acc_auth, show_id)
                                r3 = requests.get(url_show)
                                res3 = r3.json()

                                f_season_html = ""

                                for season in res3["content"]["children"]:
                                    season_name = season["name"]
                                    season_id = season["id"]

                                    url_season = "https://{}/api/v1/metadata?a={}&id={}".format(LD_DOMAIN, search_acc_auth, season_id)
                                    r4 = requests.get(url_season)
                                    res4 = r4.json()

                                    episode_num = 0
                                    episode_html = ""

                                    for episode in res4["content"]["children"]:
                                        episode_name = episode["name"]
                                        episode_id = episode["id"]
                                        episode_num+=1
                                        dir_down_url = "https://{}/api/v1/redirectdownload/{}?a={}&id={}".format(LD_DOMAIN, episode_name.replace(" ","%20"), search_acc_auth, episode_id)

                                        episode_str = '''<p>
                                                        <b> - - - - - - - - - - - - Episode : </b><code>''' + str(episode_num) + '''</code><br>
                                                        <b> - - - - - - - - - - - - Direct Download Link : </b><a href={}>Download From Here</a> !!<br>
                                                        </p>'''.format(dir_down_url)

                                        episode_html = episode_html + '{}'.format(episode_str)
                                    
                                    season_html = '''
                                                    <b> - - - - - Season : </b><code>''' + season_name + '''</code><br><br>
                                                    {}
                                                    '''.format(episode_html)
                                    
                                    telegraph_season = telegraph.create_page(
                                        title=season_name,
                                        html_content=season_html,
                                        author_name='Shrey Libdrive Bot',
                                        author_url='https://github.com/shrey2199/LD_Meta_bot'
                                    )
                                    season_url = telegraph_season['path']

                                    season_html_url = '''
                                                    <b> - - - - - Season : </b><a href="https://telegra.ph/''' + season_url + '''">''' + season_name + '''</a><br><br>
                                                    '''

                                    f_season_html = f_season_html + season_html_url

                            else:
                                name = media["name"]
                                dir_down = "https://{}/api/v1/redirectdownload/{}?a={}&id={}".format(LD_DOMAIN, name.replace(" ","%20"), search_acc_auth, media["id"])
                                f_season_html = "<b> - - - - - - - Direct Download Link : </b><a href={}>Download From Here</a> !!<br>".format(dir_down)

                            TG_html = '''<p>
                                            <img src=''' + str(backdrop) + '''>
                                            <b>Name : </b><code>''' + str(title) + '''</code><br>
                                            <b> - Overview : </b><code>''' + str(overview) + '''</code><br>
                                            <b> - Release Date: </b><code>''' + str(releaseDate) + '''</code><br>
                                            <b> - Type: </b><code>''' + str(type_) + '''</code><br><br>
                                            {}<br>➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖<br>
                                        </p>'''.format(f_season_html)

                            html_string = html_string + TG_html
                    else:
                        continue
            else:
                pass

            if num_of_results != 0:
                telegraph_res = telegraph.create_page(
                    title="LibDrive Search Results",
                    html_content=html_string,
                    author_name='Shrey Libdrive Bot',
                    author_url='https://github.com/shrey2199/LD_Meta_bot'
                )

                telegraph_url = 'https://telegra.ph/{}'.format(telegraph_res['path'])
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.row(
                    telebot.types.InlineKeyboardButton("🔍Search Results", url=telegraph_url)
                )
                bot.edit_message_text("`Query` : *{}*\n\n`Found `*{}*` Matching Search Results !!`".format(query, str(num_of_results)), m.chat.id, message_id=search_results.message_id, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.edit_message_text("*No Matching Search Results !!*", m.chat.id, message_id=search_results.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.edit_message_text("`LibDrive Server Not Accessible !!`", m.chat.id, message_id=search_results.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)

def get_callback(query):
   bot.answer_callback_query(query.id)
   update_message(query.message)
   action_keyboard(query.message)
   
def action_keyboard(m):
    if data == "back":
        action_listcategory(m)
    elif str(data).startswith("delete"):
        global category
        for category in CatC:
            if data == category["delete"]:
                global bot_id
                bot_id = category["bot_id"]
                for delcat in CatL:
                    if delcat["bot_id"]==bot_id:
                        CatL.remove(delcat)
                    else:
                        pass
            else:
                continue
        action_category("delete", m)

def action_category(action, m):
    if action == "delete":
        try:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton("Back To Categories", callback_data='back')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('❌ CLOSE ❌', callback_data='closecat')
            )

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
                CatS="*Name :* `" + category["name"] + "`\n*Type :* `" + category["type"] + "`"
                CatB = "*Category with ID - *`" + bot_id + "`* Removed :- *\n\n"
                bot.edit_message_text(CatB + CatS, m.chat.id, message_id=categories.message_id, reply_markup=update_keyboard(CatB), parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            else:
                bot.edit_message_text("`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", m.chat.id, message_id=categories.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
        except:
                bot.edit_message_text("`LibDrive Server Not Accessible !!`", m.chat.id, message_id=categories.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

def action_listcategory(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
    
    try:
        r1 = requests.get(url)
        r2 = requests.get(url)
        res1 = r1.json()
        res2 = r2.json()
        if res1["code"] == 200 and res1["success"] == True and res2["code"] == 200 and res2["success"] == True:
            global conf
            conf = res1["content"]
            global CatL
            CatL = res1["content"]["category_list"]
            global CatC
            CatC = res2["content"]["category_list"]
            keyboard = telebot.types.InlineKeyboardMarkup()
            CatNum = 0
            CatSer = "cat"
            for category in CatC:
                CatName = category["name"]
                CatNum+=1
                CatSerial = CatSer + str(CatNum)
                category.update({"cats":CatSerial, "delete":"delete"+CatSerial})
                keyboard.row(
                    telebot.types.InlineKeyboardButton(CatName, callback_data=CatSerial)
                )
            keyboard.row(
                telebot.types.InlineKeyboardButton('❌ CLOSE ❌', callback_data='closecat')
            )
            global categories
            categories = bot.edit_message_text("*Categories :-*" , m.chat.id, message_id=categories.message_id, parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard, disable_web_page_preview=True)
        else:
            bot.edit_message_text("`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", m.chat.id, message_id=categories.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        bot.send_message("`LibDrive Server Not Accessible !!`", m.chat.id, message_id=categories.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

def update_message(m):
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
                reply_markup=update_keyboard(pg),
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
                reply_markup=update_keyboard(pg),
                parse_mode=telegram.ParseMode.MARKDOWN)
        elif data == 'closewui':
            bot.delete_message(m.chat.id, message_id=configswui.message_id)
        else:
            pass
    elif data == 'movies' or data == 'tv_shows' or data == 'amovies' or data == 'atv_shows':
        global type_media
        global catadd2
        if data == 'movies':
            messg = cataddS          
            catadd2 = bot.edit_message_text(messg,
                m.chat.id, message_id=catadd.message_id,
                parse_mode=telegram.ParseMode.MARKDOWN)
            type_media = "movies"
        elif data == 'tv_shows':
            messg = cataddS               
            catadd2 = bot.edit_message_text(messg,
                m.chat.id, message_id=catadd.message_id,
                parse_mode=telegram.ParseMode.MARKDOWN)
            type_media = "tv_shows"
        elif data == 'amovies':
            messg = cataddS          
            catadd2 = bot.edit_message_text(messg,
                m.chat.id, message_id=catadd.message_id,
                parse_mode=telegram.ParseMode.MARKDOWN)
            type_media = "amovies"
        elif data == 'atv_shows':
            messg = cataddS          
            catadd2 = bot.edit_message_text(messg,
                m.chat.id, message_id=catadd.message_id,
                parse_mode=telegram.ParseMode.MARKDOWN)
            type_media = "atv_shows"
    elif data == 'instructions' or data == 'help' or data == 'closehelp':
        if data == 'instructions' or data == 'help':
            if data == 'instructions':
                pg = Inststring
            if data == 'help':
                pg = Helpstring
            bot.edit_message_text(pg,
                m.chat.id, message_id=HelpMessage.message_id,
                reply_markup=update_keyboard(pg),
                parse_mode=telegram.ParseMode.MARKDOWN)
        elif data == 'closehelp':
            bot.delete_message(m.chat.id, message_id=HelpMessage.message_id)
        else:
            pass  
    elif data == "closecat":
        bot.delete_message(
            m.chat.id, message_id=categories.message_id
        )
    elif str(data).startswith("cat"):
        pg = "*Category Configs :-*\n\n"
        for category in CatC:
            if data == category["cats"]:
                if "anilist" in category.keys():
                    pg = pg + "Name : `" + category["name"] + "`\nFolder ID : `" + category["id"] + "`\nType : `" + category["type"] + "`\nAnilist : `" + str(category["anilist"]) + "`\n"
                else:
                    pg = pg + "Name : `" + category["name"] + "`\nFolder ID : `" + category["id"] + "`\nType : `" + category["type"] + "`\n"
                bot.edit_message_text(pg,
                    m.chat.id, message_id=categories.message_id,
                    reply_markup=update_keyboard(pg),
                    parse_mode=telegram.ParseMode.MARKDOWN
                )
            else:
                pass
    else:
        pass
    
def update_keyboard(pg):
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
    elif data == 'instructions':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('❌', callback_data='closehelp'),
            telebot.types.InlineKeyboardButton('Help', callback_data='help')
        )
        return keyboard
    elif data == 'help':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('❌', callback_data='closehelp'),
            telebot.types.InlineKeyboardButton('Instructions', callback_data='instructions')
        )
        return keyboard
    elif data == "closecat":
        pass
    elif str(data).startswith("delete"):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton("Back To Categories", callback_data="back")
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('❌ CLOSE ❌', callback_data='closecat')
        )
        return keyboard
    elif str(data).startswith("cat"):    
        for category in CatC:
            if data == category["cats"]:
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.row(
                    telebot.types.InlineKeyboardButton("Name : "+category["name"], callback_data="name")
                )
                keyboard.row(
                    telebot.types.InlineKeyboardButton("Folder ID : "+category["id"], callback_data="folder_id")
                )
                keyboard.row(
                    telebot.types.InlineKeyboardButton("Delete Category", callback_data=category["delete"])
                )
                keyboard.row(
                    telebot.types.InlineKeyboardButton("Back To Categories", callback_data="back")
                )
                keyboard.row(
                    telebot.types.InlineKeyboardButton('❌ CLOSE ❌', callback_data='closecat')
                )
                return keyboard
            else:
                pass
    else:
        pass
    
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)

bot.polling(none_stop=True, timeout=999999)
