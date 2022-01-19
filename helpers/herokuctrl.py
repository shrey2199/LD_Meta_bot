import logging
import math

import heroku3
import requests
import telebot
import telegram

# CONFIG
from config import Config

BOT_TOKEN = Config.BOT_TOKEN
LD_DOMAIN = Config.LD_DOMAIN
SECRET = Config.SECRET
ADMIN_IDS = Config.ADMIN_IDS
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

# HEROKU 
if len(HEROKU_APP_NAME) != 0 and len(HEROKU_API_KEY) != 0:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)

# Request Headers
headers = {
    "accept": "application/vnd.heroku+json; version=3.account-quotas",
    "authorization": "Bearer {}".format(HEROKU_API_KEY),
    "content-type": "application/json"
}

def hrestart_mod(m):
    resmes = bot.send_message(m.chat.id, text="`Restarting Dynos ...\n\nPls Wait for 2-3 minutes for LibDrive to be Back...`", parse_mode=telegram.ParseMode.MARKDOWN)
    try:
        # Requests
        url = f"https://api.heroku.com/apps/{HEROKU_APP_NAME}/dynos"
        r = requests.delete(url, headers=headers)
    except:
        bot.edit_message_text("`Heroku Not Accessible !!`", m.chat.id, message_id=resmes.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

def hdyno_mod(m):
    try:
        dyno = bot.send_message(m.chat.id, text="`Getting Dyno Stats ...`", parse_mode=telegram.ParseMode.MARKDOWN)
        # Requests
        acc_id = Heroku.account().id

        url2 = "https://api.heroku.com/accounts/{}/actions/get-quota".format(acc_id)
        r2 = requests.get(url2, headers=headers)
        res2 = r2.json()

        # Account Quota
        quota = res2["account_quota"]
        quota_used = res2["quota_used"]
        quota_remain = quota - quota_used
        quota_percent = math.floor(quota_remain / quota * 100)
        minutes_remain = quota_remain / 60
        hours = math.floor(minutes_remain / 60)
        minutes = math.floor(minutes_remain % 60)
        day = math.floor(hours / 24)

        # App Quota
        Apps = res2["apps"]
        for apps in Apps:
            if apps.get("app_uuid") == app.id:
                AppQuotaUsed = apps.get("quota_used") / 60
                AppPercent = math.floor(apps.get("quota_used") * 100 / quota)
                break
        else:
            AppQuotaUsed = 0
            AppPercent = 0

        AppHours = math.floor(AppQuotaUsed / 60)
        AppMinutes = math.floor(AppQuotaUsed % 60)

        res_string = f"*Dyno Usage for* `{app.name}`:\n" + f"• `{AppHours}` *Hours and* `{AppMinutes}` *Minutes - {AppPercent}%*\n\n" + "*Dyno Remaining this month:*\n" + f"• `{hours}` *Hours and* `{minutes}` *Minutes - {quota_percent}%*\n\n" + "*Estimated Dyno Expired:*\n" + f"• `{day}` *Days*"

        bot.edit_message_text(res_string, m.chat.id, message_id=dyno.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        bot.edit_message_text("`Heroku Not Accessible !!`", m.chat.id, message_id=dyno.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
