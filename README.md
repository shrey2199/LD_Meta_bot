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

`/start` Welcome Message !!

`/help` Get Instructions on How to Use to bot !!

`/rebuild` Rebuild Libdrive Metadata !!
