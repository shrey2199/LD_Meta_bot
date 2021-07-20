<p align="center">
  <a href="https://heroku.com/deploy?template=https://github.com/shrey2199/LD_Meta_bot">
    <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200" />
  </a>
</p>

# Libdrive Manager Bot (LMR-Bot)

## Run Locally

Installing Requirements.. `pip install -r requirements.txt`

Then Edit config.py

And then run the bot by `python3 bot.py`

## Deploy with Docker

Edit bot.py CONFIGS

Build Docker Image.. `docker build . -t lmr-bot`

Run Docker Container.. `docker run --name lmr-bot lmr-bot`

## Bot Commands

`/start` - Welcome Message !!

`/help` - Get Instructions on How to Use to bot !!

`/rebuild` - Rebuild Libdrive Metadata !!

## BotFather SetCommands

    rebuild - To Rebuild the Metadata of your Libdrive.
    accounts - To View Registered Accounts of your Libdrive.
    addaccount - To Add an Account to Libdrive.
    rmaccount - To Remove an Account from Libdrive.
    categories - To View the Categories of your Libdrive.
    config - To View The Configs of your Libdrive.
    settings - To View the Settings of your Libdrive.
    set - To change The Settings of your Libdrive.
    ui - To View the UI Configuration of your Libdrive.
    setui - To change The UI Settings of your Libdrive
    speedtest - To Perform a Speedtest on the Server. (Completely Irrelevant 😂)
