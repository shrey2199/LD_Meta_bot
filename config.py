import os

# CLASSES
class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    LD_DOMAIN = os.environ.get("LD_DOMAIN", "")
    SECRET = os.environ.get("SECRET", "")
    ADMIN_IDS = os.environ.get("ADMIN_IDS", "")
    PIC = os.environ.get("PIC", "")
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", "")
    GROUP_IDS = os.environ.get("GROUP_IDS", "")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
    GROUP_CMDS = os.environ.get("GROUP_CMDS", "")