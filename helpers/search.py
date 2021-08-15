import telegram
import telebot
import logging
import requests
from telegraph import Telegraph

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

def searchmes(m):
    chat = m.text[7:]
    if chat == "" :
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n*To Search for Content :-*
        Send /search `<search_query>`
        """, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        query = m.text[8:]
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
                                            <b> - Release Date : </b><code>''' + str(releaseDate) + '''</code><br>
                                            <b> - Type : </b><code>''' + str(type_) + '''</code><br><br>
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
