import json
import logging
import time
from random import *

import requests
import telebot
import telegram
from telegraph import Telegraph

from config import Config

# CONFIG


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

class catsetup:
    def categories_mod(m):
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        try:

            tempcat = bot.send_message(m.chat.id, text="`Getting Your Categories ...`", parse_mode=telegram.ParseMode.MARKDOWN)

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
                bot.delete_message(m.chat.id, message_id=tempcat.message_id)
                categories = bot.send_message(m.chat.id, text="*Categories :-*" , parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=keyboard, disable_web_page_preview=True)
            else:
                bot.delete_message(m.chat.id, message_id=tempcat.message_id)
                bot.send_message(m.chat.id, text="`Unknown Error Occured !!\nPlease Verify Your Credentials !!`", parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.delete_message(m.chat.id, message_id=tempcat.message_id)
            bot.send_message(m.chat.id, text="`LibDrive Server Not Accessible !!`", parse_mode=telegram.ParseMode.MARKDOWN)

    def setanilist_mod(m):
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
                    'accept': 'application/json, text/plain, */*',
                    'content-type': 'application/json;charset=UTF-8',
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

    def addcategory_mod(m):
        chat = m.text[12:]
        if chat == "":
            bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
            \n*To Add a Category :-*
            Send /addcategory `<name> <folder_id>`
            
            Use *_* to denote spaces in name.
            Eg. Typing `MY_FOLDER` as `<name>` will create a category named `MY FOLDER`.
            """, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            global bot_id
            bot_id = "".join(choice(allchar) for x in range(randint(8, 8)))
            namecoded = m.text.split()[1]
            global name
            name = namecoded.replace("_", " ")
            global folder_id
            folder_id = m.text.split()[2]
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Movies', callback_data='movies'),
                telebot.types.InlineKeyboardButton('TV Shows', callback_data='tv_shows'),
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('Anilist - Movies', callback_data='amovies'),
                telebot.types.InlineKeyboardButton('Anilist - TV Shows', callback_data='atv_shows')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('❌ CANCEL ❌', callback_data='canceladd')
            )
            catadddet = "*Category Details :-*\n\n*Name : *`" + name + "`\n*Folder ID : *`" + folder_id + "`\n\nNow Choose Category Type :-"
            global catadd
            catadd = bot.send_message(m.chat.id, catadddet, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN)
            
            global cataddS
            cataddS = "Adding Category `" + name + "` to Libdrive ...\n\n`This might take around 5-10 Seconds...`"

        

    def rmcategory_mod(m):
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
                    'accept': 'application/json, text/plain, */*',
                    'content-type': 'application/json;charset=UTF-8',
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

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)

def get_callback(query):
    bot.answer_callback_query(query.id)
    cat_update_message(query.message)
    action_keyboard(query.message)

def cat_update_message(m, data):
    if data in ['movies', 'tv_shows', 'amovies', 'atv_shows']:
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
        else:
            messg = cataddS
            catadd2 = bot.edit_message_text(messg,
                m.chat.id, message_id=catadd.message_id,
                parse_mode=telegram.ParseMode.MARKDOWN)
            type_media = "atv_shows"
    elif data == 'canceladd':
        bot.delete_message(
            m.chat.id, message_id=catadd.message_id
        )
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
                    reply_markup=cat_update_keyboard(pg, data),
                    parse_mode=telegram.ParseMode.MARKDOWN
                )

def cat_update_keyboard(pg, data):
    if data == "closecat":
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

def action_addcategory(m, type_media):
    try:    
        url = 'https://' + LD_DOMAIN + '/api/v1/config?secret=' + SECRET
        r1 = requests.get(url)
        res1 = r1.json()
        conf = res1["content"]
        confcat = res1["content"]["category_list"]

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
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
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

def action_keyboard(m, data):
    if data == "back":
        action_listcategory(m)
    elif str(data).startswith("delete"):
        global category
        for category in CatC:
            if data == category["delete"]:
                global bot_id
                bot_id = category["bot_id"]
                global delname
                delname = category["name"]
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
            bot.edit_message_text(f"`Deleting Category` *{delname}*", m.chat.id, message_id=categories.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton("Back To Categories", callback_data='back')
            )
            keyboard.row(
                telebot.types.InlineKeyboardButton('❌ CLOSE ❌', callback_data='closecat')
            )

            headers = {
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json;charset=UTF-8',
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
                bot.edit_message_text(CatB + CatS, m.chat.id, message_id=categories.message_id, reply_markup=cat_update_keyboard(CatB, action), parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
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

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)
