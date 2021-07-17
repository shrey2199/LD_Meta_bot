import os

class Config(object):
	BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
	LD_DOMAIN = os.environ.get("LD_DOMAIN", "") # Without https:// or http://
	SECRET = os.environ.get("SECRET "")
	ADMIN_IDS = os.environ.get("ADMIN_IDS", "") # ==> Enter Admin Chat IDs here !!
