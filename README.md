<p align="center">
  <a href="https://heroku.com/deploy?template=https://github.com/shrey2199/LD_Meta_bot">
    <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200" />
  </a>
</p>

# Libdrive Manager Bot (LMR-Bot)

## Deploy on Heroku

Use The Deploy to Heroku Button given at the TOP !!

Enter the Relevant Configurations and Deploy !!

## Run Locally

Installing Requirements.. 

    pip install -r requirements.txt

Then Edit config.py with variables listed below !

And then run the bot by 

    python3 bot.py

## Deploy with Docker

### Two Methods

#### Method 1

Edit config.py with variables listed below !

Build Docker Image.. 

    docker build . -t libdrivebot

Run Docker Container.. 

    docker run --name libdrivebot libdrivebot

#### Method 2

Build Docker Image ..

    docker build . -t libdrivebot

Run The Docker Container and Define the Variables in One Command

    docker run --name libdrivebot -e BOT_TOKEN="<your_bot_token>" -e LD_DOMAIN="<your_libdrive_domain>" -e SECRET="<your_libdrive_secret>" -e ADMIN_IDS="<chat_ids>" -e PIC="<picture_url>" -d libdrivebot

## Bot Commands

`/start` - Welcome Message !!

`/help` - Get Instructions on How to Use to bot !!

`/rebuild` - Rebuild Libdrive Metadata !!

## Variables

- `BOT_TOKEN`
  - Values :- Valid BOT TOKEN Obtained from Botfather.
  - Default Value :- `"XXXXXXXXX:ABCDEFGHIJKLMNOPQRST"`
  - Use :- To connect to Telegram as BOT.

- `LD_DOMAIN`
  - Values :- Domain of LibDrive Server.
  - Default Value :- `<appname>.herokuapp.com`
  - Use :- To connect to Libdrive.

- `SECRET`
  - Values :- Secret of LibDrive Server Settings - The Secret Key set in LibDrive Config.
  - Default Value :- `""`
  - Use :- To connect to Libdrive.

- `ADMIN_IDS`
  - Values :- It is a list of IDs of all the allowed groups and useres who can use this bot in private. 
    - To supply multiple IDs in config.py seperate by comma ','. 
    - To supply multiple IDs from Environemnt variable (Heroku & Docker) seperate by spaces.
  - Default Value :- `[]` 
  - Use :- Users and groups with ids here can use the bot.

## BotFather SetCommands

    start - To Start The Bot.
    help - To Get Help about Using the Bot.
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
