import telegram
import telebot
import logging
import requests
import os

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

def getm3u8(m):
    chat = m.text[8:]
    if chat == "" :
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n*To Search for Content :-*
        Send /search `<search_query>`
        """, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        query = m.text.split()[1]
        try:
            
            search_results = bot.send_message(m.chat.id, "`Searching Your LibDrive ...`\n\n`Query` : *{}*".format(query), parse_mode=telegram.ParseMode.MARKDOWN)

            url_conf = "https://{}/api/v1/config?secret={}".format(LD_DOMAIN, SECRET)

            r1 = requests.get(url_conf)
            res1 = r1.json()
            search_acc_auth = res1["content"]["account_list"][0]["auth"]

            url_meta = "https://{}/api/v1/metadata?a={}&q={}".format(LD_DOMAIN, search_acc_auth, query)

            r2 = requests.get(url_meta)
            res2 = r2.json()

            num_of_results = 0
            shows_list = []

            if res2["code"] == 200 and res2["success"] == True:
                for cat in res2["content"]:
                    if len(cat["children"]) != 0:
                        for media in cat["children"]:
                            num_of_results += 1
                            type_ = cat["categoryInfo"]["type"]

                            if str(type_) == "TV Shows":
                                show_id = media["id"]
                                title = media["name"]
                                if "releaseDate" in media.keys():
                                    releaseDate = media["releaseDate"]
                                else:
                                    releaseDate = "Not Found !!"
                                url_show = "https://{}/api/v1/metadata?a={}&id={}".format(LD_DOMAIN, search_acc_auth, show_id)
                                r3 = requests.get(url_show)
                                res3 = r3.json()

                                num_of_seasons = len(res3["content"]["children"])

                                root_path = os.getcwd().replace("\\", "/")

                                m3u8_path = root_path + "/m3u8"

                                show_path = m3u8_path + "/" + show_id

                                show_dict = {"showname":title, "showpath":show_path, "rD":releaseDate, "nos":num_of_seasons}
                                shows_list.append(show_dict)

                                if "m3u8" in os.listdir(path=root_path):
                                    pass
                                else:
                                    os.mkdir(path=m3u8_path)
                                
                                if show_id in os.listdir(path=m3u8_path):
                                    pass
                                else:
                                    os.mkdir(path=show_path)

                                    season_eplist = ["#EXTM3U", "\n#EXTENC: UTF-8", "#PLAYLIST: {}"]

                                    for season in res3["content"]["children"]:
                                        season_name = season["name"]
                                        season_id = season["id"]

                                        season_eplist = ["#EXTM3U", "\n#EXTENC: UTF-8", "\n#PLAYLIST: {}".format(season_name)]

                                        url_season = "https://{}/api/v1/metadata?a={}&id={}".format(LD_DOMAIN, search_acc_auth, season_id)
                                        r4 = requests.get(url_season)
                                        res4 = r4.json()

                                        for episode in res4["content"]["children"]:
                                            episode_name = episode["name"]
                                            episode_id = episode["id"]
                                            dir_down_url = "https://{}/api/v1/redirectdownload/{}?a={}&id={}".format(LD_DOMAIN, episode_name.replace(" ","%20"), search_acc_auth, episode_id)  

                                            ep_str = f"\n#EXTINF:0, {episode_name}\n{dir_down_url}"

                                            season_eplist.append(ep_str)

                                        file_path = show_path + "/" + season_name + " - " + title

                                        with open(file=file_path + ".m3u8", mode='w+') as file:
                                            file.writelines(season_eplist)
                            else:
                                continue
                    else:
                        continue
                if num_of_results > 0:
                    bot.delete_message(m.chat.id, message_id=search_results.message_id)
                    for x in shows_list:
                        files_path = x["showpath"]
                        stitle = x["showname"]
                        numseason = x["nos"]
                        rD = x["rD"]
                        bot.send_message(m.chat.id, text=f"*Show Name* : `{stitle}`\n*Total Seasons* : `{numseason}`\n*Release Date* : `{rD}`\n\n`Here Are You M3U8 Files for this Show !!`", parse_mode=telegram.ParseMode.MARKDOWN)
                        for y in os.listdir(files_path):
                            file_data = files_path + "/" + y
                            with open(file=file_data, mode="rb") as file_mes:
                                bot.send_document(m.chat.id, file_mes)
                else:
                    bot.delete_message(m.chat.id, message_id=search_results.message_id)
                    bot.send_message(m.chat.id, text="*No Matching Shows Found !!*", parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.edit_message_text("`Something Went Wrong. Check Credentials !!`", m.chat.id, message_id=search_results.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.edit_message_text("`LibDrive Server Not Accessible !!`", m.chat.id, message_id=search_results.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
