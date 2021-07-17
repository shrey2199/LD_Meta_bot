# Libdrive Metadata Rebuild Bot (LMR-Bot)

## Run Locally

Installing Requirements.. `pip install -r requirements.txt`

Then Edit config.py

And then run the bot by `python3 bot.py`

## Deploy with Docker

Edit bot.py CONFIGS

Build Docker Image.. `docker build . -t lmr-bot`

Run Docker Container.. `docker run --name lmr-bot lmr-bot`

## Bot Commands

`/start` Welcome Message !!

`/help` Get Instructions on How to Use to bot !!

`/refresh` Rebuild Libdrive Metadata !!