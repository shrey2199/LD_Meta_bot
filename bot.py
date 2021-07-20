# -*- coding: utf-8 -*-

import telegram
import telebot
import logging
import requests
import json
import time
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
    uptime = get_readable_time((time.time() - botStartTime))
    bot.send_message(m.chat.id, text="Hi ! Welcome to Libdrive Manager Bot !\n\n<b>I'm Alive Since : </b><code>" + uptime + "</code>\n\nSend /help for More Info !", parse_mode=telegram.ParseMode.HTML)


@bot.message_handler(commands=['help'])
@restricted
def help(m):
    bot.send_message(chat_id=m.chat.id, text="""This Bot will help you to Manage your Libdrive Server.
    	\n/rebuild - <b>To Rebuild the Metadata of your Libdrive.</b>
        \n/accounts - <b>To View Registered Accounts of your Libdrive.</b>
        \n/addaccount - <b>To Add an Account to Libdrive.</b>
        \n/rmaccount - <b>To Remove an Account from Libdrive.</b>
        \n/categories - <b>To View the Categories of your Libdrive.</b>
        \n/config - <b>To View The Configs of your Libdrive.</b>
        \n/settings - <b>To View the Settings of your Libdrive.</b>
        \n/set - <b>To change The Settings of your Libdrive.</b>
        \n⚠️ <code>Do Not Use The "</code> /set <code>" Command For Accounts, Categories and UI Config.</code>
        \n/ui - <b>To View the UI Configuration of your Libdrive.</b>
        \n/setui - <b>To change The UI Settings of your Libdrive.</b>
        \n/speedtest - <b>To Perform a Speedtest on the Server. (Completely Irrelevant 😂)</b>
        """, parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['speedtest'])
@restricted
def speedtest(m):
    test = Speedtest()
    test.get_best_server()
    dl = bot.send_message(m.chat.id, "<code>Checking Download Speeds ...</code>", parse_mode=telegram.ParseMode.HTML)
    test.download()
    ul = bot.edit_message_text("<code>Checking Upload Speeds ...</code>", chat_id=m.chat.id, message_id=dl.message_id, parse_mode=telegram.ParseMode.HTML)
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result["share"])
    string_speed = f'''
    <b>Server :</b>
    <b>Name:</b> <code>{result['server']['name']}</code>
    <b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
    <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
    <b>ISP:</b> <code>{result['client']['isp']}</code>

<b>SpeedTest Results :</b>
    <b>Upload:</b> <code>{speed_convert(result['upload'] / 8)}</code>
    <b>Download:</b>  <code>{speed_convert(result['download'] / 8)}</code>
    <b>Ping:</b> <code>{result['ping']} ms</code>
    <b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
    '''
    st = bot.edit_message_text(str(string_speed), chat_id=m.chat.id, message_id=ul.message_id, parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['rebuild'])
@restricted
def rebuild(m):
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
                AccN+=1
                AccS=AccS + str(AccN) + ". <b>" + str(account["username"]) + " :</b> <code>" + str(account["auth"]) + "</code>\n"
            bot.send_message(m.chat.id, text="<b>Registered Accounts :-</b>\n\n" + str(AccS) , parse_mode=telegram.ParseMode.HTML)
        else:
            bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
    except:
        bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['addaccount'])
@restricted
def addaccount(m):
    chat = m.text[11:]
    if chat == "":
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n<b>To Add an Account :-</b>
        Send /addaccount <code>&lt;user&gt; &lt;pass&gt; &lt;pic&gt;</code>
        """, parse_mode=telegram.ParseMode.HTML)
    else:
        username = m.text.split()[1]
        password = m.text.split()[2]
        if len(m.text.split()) == 4:
            pic = m.text.split()[3]
        else:
            pic = ""
        allchar = "abcdefghijklmnopqrstuvwxyz0123456789"
        min_char = 50
        max_char = 50
        auth = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
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
                "username":username
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
                AccS="<b>Username :</b> <code>" + username + "</code>\n<b>Password :</b> <code>" + password + "</code>\n<b>Auth :</b> <code>" + auth + "</code>\n<b>Pic :</b> <code>" + pic + "</code>\n"
                bot.send_message(m.chat.id, text="<b>Account Added Successfully :- </b>\n\n" + AccS , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
        except:
            bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['rmaccount'])
@restricted
def rmaccount(m):
    chat = m.text[10:]
    if chat == "":
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n<b>To Remove an Account :-</b>
        Send /addaccount <code>&lt;user&gt; &lt;pass&gt;</code>
        """, parse_mode=telegram.ParseMode.HTML)
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
                AccS="<b>Username :</b> <code>" + username + "</code>\n<b>Password :</b> <code>" + password + "</code>"
                bot.send_message(m.chat.id, text="<b>Account Removed Successfully :- </b>\n\n" + AccS , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
        except:
            bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['categories'])
@restricted
def categories(m):
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
                CatID=str(category["name"])
                CatURL=f"https://{LD_DOMAIN}/browse/{CatID}"
                CatS=CatS + str(CatN) + ". <b>" + str(category["name"]) + " :</b>\n    Type : <code>" + str(category["type"]) + "</code>\n    Folder ID : <code>" + str(category["id"]) + "</code>\n    URL : <a href='" + str(CatURL) + "'>" + str(category["name"]) + "</a>\n"
            bot.send_message(m.chat.id, text="<b>Categories :-</b>\n\n" + str(CatS) , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        else:
            bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
    except:
        bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['config'])
@restricted
def config(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
    
    try:
        r = requests.get(url)
        res = r.json()
        if res["code"] == 200 and res["success"] == True:
            config = res["content"]
            ConSgoogle = "✯ <b> Access Token :</b> <code>" + str(config["access_token"]) + "</code>\n\n" + "✯ <b> Client ID :</b> <code>" + str(config["client_id"]) + "</code>\n\n" + "✯ <b> Client Secret :</b> <code>" + str(config["client_secret"]) + "</code>\n\n" + "✯ <b> Refresh Token :</b> <code>" + str(config["refresh_token"]) + "</code>\n\n" + "✯ <b> Token Expiry :</b> <code>" + str(config["token_expiry"]) + "</code>\n\n"
            bot.send_message(m.chat.id, text="<b>Google Credentials :-</b>\n\n" + str(ConSgoogle) , parse_mode=telegram.ParseMode.HTML)
            ConSothers = "✯ <b> Build Interval :</b> <code>" + str(config["build_interval"]) + "</code>\n\n" + "✯ <b> Build Type :</b> <code>" + str(config["build_type"]) + "</code>\n\n" + "✯ <b> Cloudflare :</b> <code>" + str(config["cloudflare"]) + "</code>\n\n" + "✯ <b> Kill Switch :</b> <code>" + str(config["kill_switch"]) + "</code>\n\n" + "✯ <b> Signup :</b> <code>" + str(config["signup"]) + "</code>\n\n" + "✯ <b> Subtitles :</b> <code>" + str(config["subtitles"]) + "</code>\n\n" + "✯ <b> TMDB API :</b> <code>" + str(config["tmdb_api_key"]) + "</code>\n\n" + "✯ <b> Transcoded :</b> <code>" + str(config["transcoded"]) + "</code>\n\n"
            bot.send_message(m.chat.id, text="<b>Website Configs :-</b>\n\n" + str(ConSothers) , parse_mode=telegram.ParseMode.HTML)
            ConSsite = "✯ <b> Title :</b> <code>" + str(config["ui_config"]["title"]) + "</code>\n\n" + "✯ <b> Icon :</b> <code>" + str(config["ui_config"]["icon"]) + "</code>\n\n" + "✯ <b> Page Range :</b> <code>" + str(config["ui_config"]["range"]) + "</code>\n\n"
            bot.send_message(m.chat.id, text="<b>Website Configs :-</b>\n\n" + str(ConSsite) , parse_mode=telegram.ParseMode.HTML)
            
        else:
            bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
    except:
        bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

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
                SetAddS = "• <code>" + i + "</code> : <code>" + str(config[i]) + "</code>\n\n"
                SetS = SetS + SetAddS
            bot.send_message(m.chat.id, text="<b>Libdrive Server Settings :-</b>\n\n" + str(SetS) , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        else:
            bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
    except:
        bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

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
        \n<b>To Change a Setting :-</b>
        Send /set <code>&lt;key&gt; &lt;value&gt;</code>
        \nGet <code>keys</code> by sending /settings
        \n⚠ Do Not Use This Command For Accounts, Categories and UI Config
        \nSeperate Commands are available for that !!""", parse_mode=telegram.ParseMode.HTML)
    elif i == "category_list" or i == "account_list" or i == "service_accounts" or i == "token_expiry" or i == "ui_config":
        bot.send_message(m.chat.id, text = """The /set Command does not work for this key.
        \n⚠️ Do Not Use The /set Command For :-
        Accounts, Categories and UI Config
        \nSome other keys are also not supported...
        """, parse_mode=telegram.ParseMode.HTML)
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

                bot.send_message(m.chat.id, text="<b>Libdrive Setting </b><code>" + key + "</code> Successfully Changed !!\n\nFrom <code>" + str(prev) + "</code> <b>→</b> <code>" + str(value) + "</code>" , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
        except:
            bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

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
                SetAddS = "• <code>" + i + "</code> : <code>" + str(config[i]) + "</code>\n\n"
                SetS = SetS + SetAddS
            bot.send_message(m.chat.id, text="<b>Libdrive UI Settings :-</b>\n\n" + str(SetS) , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        else:
            bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
    except:
        bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['setui'])
@restricted
def setui(m):
    chat = m.text[6:]
    if chat == "":
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n<b>To Change a Setting :-</b>
        Send /setui <code>&lt;key&gt; &lt;value&gt;</code>
        \nGet <code>keys</code> by sending /ui
        """, parse_mode=telegram.ParseMode.HTML)
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

                bot.send_message(m.chat.id, text="<b>Libdrive UI Setting </b><code>" + key + "</code> Successfully Changed !!\n\nFrom <code>" + str(prev) + "</code> <b>→</b> <code>" + str(value) + "</code>" , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
        except:
            bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

bot.polling(none_stop=True, timeout=999999)
