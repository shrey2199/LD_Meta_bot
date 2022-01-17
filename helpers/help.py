from helpers.groupcmd import BOT_USERNAME
import telegram
import telebot
import logging
import time

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
BOT_USERNAME = Config.BOT_USERNAME

try:
    ADMIN_LIST = ADMIN_IDS 
    restricted_mode = True
except:
    ADMIN_LIST = []  # ==> Do Not Touch This !!
    restricted_mode = False

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

def grphelp(m):
    ghelpstr = f"""*Available Commands in Group :*
        \n/rebuild - *To Rebuild the Metadata of your Libdrive.*
        \n/search - *To Search Libdrive and Get Direct Download Links.*
        \n/find - *To Search Libdrive and Get View Online Links.*
        \n/m3u8 - *To Get M3U8 Playlists from Bot itself.*
        """
    bot.send_message(m.chat.id, ghelpstr, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

def helpmes(m):
    global Helpstring
    Helpstring = """*This Bot will help you to Manage your Libdrive Server.*
        \n/grouphelp - *To View Available Commands when Bot is Added in Group.*
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
        \n/find - *To Search Libdrive and Get View Online Links.*
        \n/m3u8 - *To Get M3U8 Playlists from Bot itself.*
        \n/webhooks - *To View the Webhooks Usage of this Bot.*
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

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)

def get_callback(query):
    bot.answer_callback_query(query.id)
    help_update_message(query.message)

def help_update_message(m, data):
    if data == 'instructions' or data == 'help' or data == 'closehelp':
        if data == 'instructions' or data == 'help':
            if data == 'instructions':
                pg = Inststring
            if data == 'help':
                pg = Helpstring
            bot.edit_message_text(pg,
                m.chat.id, message_id=HelpMessage.message_id,
                reply_markup=help_update_keyboard(pg, data),
                parse_mode=telegram.ParseMode.MARKDOWN)
        elif data == 'closehelp':
            bot.delete_message(m.chat.id, message_id=HelpMessage.message_id)
        else:
            pass 
    else:
        pass

def help_update_keyboard(pg, data):
    if data == 'instructions':
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