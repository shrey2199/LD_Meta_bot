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
PIC = Config.PIC

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
    start_string = "Hi ! Welcome to Libdrive Manager Bot by <a href='telegram.me/s_rawal'>Shreyansh Rawal</a> !\n\n<b>I'm Alive Since : </b><code>" + uptime + "</code>\n\n ✯ <b>For More Info</b>, Send /help to the Bot !!\n\n ✯ <b>Also Read the Important Instructions</b> by clicking the Instructions Button in /help !!"
    if len(PIC.replace(" ", "")) != 0:
        bot.send_photo(m.chat.id, PIC, caption = start_string, parse_mode=telegram.ParseMode.HTML)
    else:
        bot.send_message(m.chat.id, start_string, parse_mode=telegram.ParseMode.HTML)


@bot.message_handler(commands=['help'])
@restricted
def help(m):
    global Helpstring
    Helpstring = """<b>This Bot will help you to Manage your Libdrive Server.</b>
    	\n/rebuild - <b>To Rebuild the Metadata of your Libdrive.</b>
        \n/assignid - <b>To Assign <code>bot_id</code> to All Accounts and Categories.</b>
        \n/unassignid - <b>To Remove <code>bot_id</code> from All Accounts and Categories.</b>
        \n/accounts - <b>To View Registered Accounts of your Libdrive.</b>
        \n/addaccount - <b>To Add an Account to Libdrive.</b>
        \n/rmaccount - <b>To Remove an Account from Libdrive.</b>
        \n/rmaccid - <b>To Remove an Account from Libdrive using id.</b>
        \n/categories - <b>To View the Categories of your Libdrive.</b>
        \n/addcategory - <b>To Add a Category to Libdrive.</b>
        \n/rmcategory - <b>To Remove a Category from Libdrive.</b>
        \n/config - <b>To View The Configs of your Libdrive.</b>
        \n/settings - <b>To View the Settings of your Libdrive.</b>
        \n/set - <b>To change The Settings of your Libdrive.</b>
        \n/ui - <b>To View the UI Configuration of your Libdrive.</b>
        \n/setui - <b>To change The UI Settings of your Libdrive.</b>
        \n/speedtest - <b>To Perform a Speedtest on the Server. (Completely Irrelevant 😂)</b>
        """
    global Inststring
    Inststring = """<b>Instructions for Using The Bot : </b>
    \n1. <code>Do Not Use The "</code> /set <code>" Command For Accounts, Categories and UI Config.</code>
    \n2. <code>Before Using the Features of this Bot, Please Use The Command "</code> /assignid <code>" to assign Bot Identifiable IDs to your LibDrive Accounts and Categories.</code>
    \n3. <code>Assigning these IDs is </code><b>Important for Full Fuctionality</b><code> of the Bot.</code>
    \n4. <code>Using This command adds an element </code><b>bot_id</b><code> to your Accounts and Categories in LibDrive Config.</code>
    \n5. <code>This will not affect any kind of functioning in your LibDrive.</code>
    \n6. <code>These IDs can be removed from your LibDrive Config by using "</code> /unassignid <code>" Command.</code>
        """
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('❌', callback_data='closehelp'),
        telebot.types.InlineKeyboardButton('Instructions', callback_data='instructions')
    )
    global HelpMessage
    HelpMessage = bot.send_message(m.chat.id, Helpstring, reply_markup=keyboard, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

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
    
    bot.send_photo(m.chat.id, path, caption = string_speed, parse_mode=telegram.ParseMode.HTML)
    bot.delete_message(chat_id=m.chat.id, message_id=ul.message_id)
    

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

@bot.message_handler(commands=['assignid'])
@restricted
def assignid(m):
    min_char = 8
    max_char = 8
    url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
    try:

        assign = bot.send_message(m.chat.id, text="<code>Assigning IDs ...</code>", parse_mode=telegram.ParseMode.HTML)

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
            bot.edit_message_text("<b>Successfully Assigned IDs to all Accounts and Categories</b>", m.chat.id, message_id=assign.message_id, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        else:
            bot.edit_message_text("<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", m.chat.id, message_id=assign.message_id, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
    except:
        bot.edit_message_text("<code>LibDrive Server Not Accessible !!</code>", m.chat.id, message_id=assign.message_id, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

@bot.message_handler(commands=['unassignid'])
@restricted
def unassignid(m):
    url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
    try:

        unassign = bot.send_message(m.chat.id, text="<code>Deleting Assigned IDs ...</code>", parse_mode=telegram.ParseMode.HTML)

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
            bot.edit_message_text("<b>Successfully Deleted IDs of all Accounts and Categories</b>", m.chat.id, message_id=unassign.message_id, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        else:
            bot.edit_message_text("<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", m.chat.id, message_id=unassign.message_id, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
    except:
        bot.edit_message_text("<code>LibDrive Server Not Accessible !!</code>", m.chat.id, message_id=unassign.message_id, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)

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
                    AccS=AccS + str(AccN) + ". <b>" + str(account["username"]) + " :</b> <code>" + str(account["auth"]) + "</code>\n    To Delete : /rmaccid <code>" + str(account["bot_id"]) + "</code>\n\n"
                else:
                    AccN+=1
                    AccS=AccS + str(AccN) + ". <b>" + str(account["username"]) + " :</b> <code>" + str(account["auth"]) + "</code>\n\n"
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
        Send /rmaccount <code>&lt;user&gt; &lt;pass&gt;</code>
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

@bot.message_handler(commands=['rmaccid'])
@restricted
def rmaccid(m):
    chat = m.text[8:]
    if chat == "":
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n<b>To Remove an Account :-</b>
        Send /rmaccid <code>&lt;id&gt;</code>
        \nGet Account's ID with /accounts
        """, parse_mode=telegram.ParseMode.HTML)
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
                AccS="<b>Username :</b> <code>" + username + "</code>\n<b>Password :</b> <code>" + password + "</code>"
                bot.send_message(m.chat.id, text="<b>Account with ID - </b><code>" + id + "</code><b> Removed Successfully :- </b>\n\n" + AccS , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
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
                CatName=str(category["name"])
                CatURL=f"https://{LD_DOMAIN}/browse/{CatName}"
                CatS=CatS + str(CatN) + ". <b>" + str(category["name"]) + " :</b>\n    Type : <code>" + str(category["type"]) + "</code>\n    Folder ID : <code>" + str(category["id"]) + "</code>\n    To Delete : /rmcategory <code>" + str(category["bot_id"]) + "</code>\n    URL : <a href='" + str(CatURL) + "'>" + str(category["name"]) + "</a>\n"
            bot.send_message(m.chat.id, text="<b>Categories :-</b>\n\n" + str(CatS) , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        else:
            bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
    except:
        bot.send_message(m.chat.id, text="<code>LibDrive Server Not Accessible !!</code>", parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['addcategory'])
@restricted
def addcategory(m):
    chat = m.text[12:]
    if chat == "":
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n<b>To Add a Category :-</b>
        Send /addcategory <code>&lt;name&gt; &lt;folder_id&gt;</code>
        
        Use <b>_</b> to denote spaces in name.
        Eg. Typing <code>MY_FOLDER</code> as <code>&lt;name&gt;</code> will create a category named <code>MY FOLDER</code>.
        """, parse_mode=telegram.ParseMode.HTML)
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
                telebot.types.InlineKeyboardButton('TV Shows', callback_data='tv_shows')
            )
            catadddet = "<b>Category Details :-</b>\n\n<b>Name : </b>" + name + "\n<b>Folder ID : </b>" + folder_id + "\n\nNow Choose Category Type (<b>Within 15 seconds</b>) :-"
            global catadd
            catadd = bot.send_message(m.chat.id, catadddet, reply_markup=keyboard, parse_mode=telegram.ParseMode.HTML)
            @bot.callback_query_handler(func=lambda call: True)
            def iq_callback(query):
                global catdata
                catdata = query.data
                get_callback(query)
            
            def get_callback(query):
                bot.answer_callback_query(query.id)
                update_message(query.message)

            global cataddS
            cataddS = "Adding Category <code>" + name + "</code> to Libdrive ...\n\n<code>This might take around 15-30 Seconds...</code>"

            r1 = requests.get(url)
            res1 = r1.json()
            conf = res1["content"]
            confcat = res1["content"]["category_list"]

            for timex in range(1, 15):
                bot.send_chat_action(m.chat.id, 'typing')
                time.sleep(15)

            category_dict = {"id": folder_id, "name": name, "bot_id":bot_id, "type": str(type_media)}
            
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
                CatS="<b>Name :</b> <code>" + name + "</code>\n<b>Folder ID :</b> <code>" + folder_id + "</code>\n<b>Type :</b> <code>" + type_media + "</code>\n"
                bot.edit_message_text("<b>Category Added Successfully :- </b>\n\n" + CatS, m.chat.id, message_id=catadd2.message_id, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
            else:
                bot.send_message(m.chat.id, text="<code>Unknown Error Occured !!\nPlease Verify Your Credentials !!</code>", parse_mode=telegram.ParseMode.HTML)
        except:
            bot.edit_message_text("<code>LibDrive Server Not Accessible !!</code>", m.chat.id, message_id=catadd.message_id, parse_mode=telegram.ParseMode.HTML)

@bot.message_handler(commands=['rmcategory'])
@restricted
def rmcategory(m):
    chat = m.text[7:]
    if chat == "":
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n<b>To Remove a Category :-</b>
        Send /rmcategory <code>&lt;id&gt;</code>
        \nGet Category's ID with /categories\nPlease Send /assignid to the bot 
        """, parse_mode=telegram.ParseMode.HTML)
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
                CatS="<b>Name :</b> <code>" + name + "</code>\n<b>Type :</b> <code>" + type + "</code>"
                bot.send_message(m.chat.id, text="<b>Category with ID - </b><code>" + id + "</code><b> Removed Successfully :- </b>\n\n" + CatS , parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
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
            global ConSgoogle
            ConSgoogle = "<b>Google Credentials :-</b>\n\n✯ <b> Access Token :</b> <code>" + str(config["access_token"]) + "</code>\n\n" + "✯ <b> Client ID :</b> <code>" + str(config["client_id"]) + "</code>\n\n" + "✯ <b> Client Secret :</b> <code>" + str(config["client_secret"]) + "</code>\n\n" + "✯ <b> Refresh Token :</b> <code>" + str(config["refresh_token"]) + "</code>\n\n" + "✯ <b> Token Expiry :</b> <code>" + str(config["token_expiry"]) + "</code>\n\n"
            global ConSothers
            ConSothers = "<b>Server Configs :-</b>\n\n✯ <b> Build Interval :</b> <code>" + str(config["build_interval"]) + "</code>\n\n" + "✯ <b> Build Type :</b> <code>" + str(config["build_type"]) + "</code>\n\n" + "✯ <b> Cloudflare :</b> <code>" + str(config["cloudflare"]) + "</code>\n\n" + "✯ <b> Kill Switch :</b> <code>" + str(config["kill_switch"]) + "</code>\n\n" + "✯ <b> Signup :</b> <code>" + str(config["signup"]) + "</code>\n\n" + "✯ <b> Subtitles :</b> <code>" + str(config["subtitles"]) + "</code>\n\n" + "✯ <b> TMDB API :</b> <code>" + str(config["tmdb_api_key"]) + "</code>\n\n" + "✯ <b> Transcoded :</b> <code>" + str(config["transcoded"]) + "</code>\n\n"
            global ConSsite
            ConSsite = "<b>Website Configs :-</b>\n\n✯ <b> Title :</b> <code>" + str(config["ui_config"]["title"]) + "</code>\n\n" + "✯ <b> Icon :</b> <code>" + str(config["ui_config"]["icon"]) + "</code>\n\n" + "✯ <b> Page Range :</b> <code>" + str(config["ui_config"]["range"]) + "</code>\n\n"
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('❌', callback_data='close'),
                telebot.types.InlineKeyboardButton('Server Configs', callback_data='1')
            )
            ConShome = '<b>Hello <a href="telegram.me/' + m.from_user.username + '">' + m.from_user.first_name + '</a>,\n\nIf You Want to Change a Config :\n\n1. Get the Config <code>key</code> by using : /settings\n\n2. Change to Config using : /set <code>key</code> <code>value</code></b>'
            global configs
            configs = bot.send_message(m.chat.id, ConShome, reply_markup=keyboard, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
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

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)

def get_callback(query):
   bot.answer_callback_query(query.id)
   update_message(query.message)

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
                parse_mode=telegram.ParseMode.HTML)
        else:
            bot.delete_message(m.chat.id, message_id=configs.message_id)
        
    elif data == 'movies' or data == 'tv_shows':
        global type_media
        global catadd2
        if data == 'movies':
            messg = cataddS          
            catadd2 = bot.edit_message_text(messg,
                m.chat.id, message_id=catadd.message_id,
                parse_mode=telegram.ParseMode.HTML)
            type_media = "Movies"
        elif data == 'tv_shows':
            messg = cataddS               
            catadd2 = bot.edit_message_text(messg,
                m.chat.id, message_id=catadd.message_id,
                parse_mode=telegram.ParseMode.HTML)
            type_media = "TV Shows"
    elif data == 'instructions' or data == 'help' or data == 'closehelp':
        if data == 'instructions' or data == 'help':
            if data == 'instructions':
                pg = Inststring
            if data == 'help':
                pg = Helpstring
            bot.edit_message_text(pg,
                m.chat.id, message_id=HelpMessage.message_id,
                reply_markup=update_keyboard(pg),
                parse_mode='HTML')
        else:
            bot.delete_message(m.chat.id, message_id=HelpMessage.message_id)        
    else:
        pass
    
def update_keyboard(pg):
    if data == '1':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('⮜⮜⮜', callback_data='3'),
            telebot.types.InlineKeyboardButton('❌', callback_data='close'),
            telebot.types.InlineKeyboardButton('⮞⮞⮞', callback_data='2')
        )
        return keyboard
    elif data == '2':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('⮜⮜⮜', callback_data='1'),
            telebot.types.InlineKeyboardButton('❌', callback_data='close'),
            telebot.types.InlineKeyboardButton('⮞⮞⮞', callback_data='3')
        )
        return keyboard
    elif data == '3':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('⮜⮜⮜', callback_data='2'),
            telebot.types.InlineKeyboardButton('❌', callback_data='close'),
            telebot.types.InlineKeyboardButton('⮞⮞⮞', callback_data='1')
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
    else:
        pass
    
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)

bot.polling(none_stop=True, timeout=999999)
