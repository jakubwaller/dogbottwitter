import os
import time
import traceback
from random import random

from mastodon import Mastodon

import requests
import tweepy
from telegram import Bot
import asyncio

from tools import read_config, run_request

config = read_config()
dog_api_key = config["dog_api_key"]
telegram_chat_id = config["telegram_chat_id"]
telegram_bot_id = config["telegram_bot_id"]

if random() < 0.5:
    image_type = "?mime_types=gif"
else:
    image_type = "?mime_types=jpg,png"

url = run_request(
    "GET",
    f"https://api.thedogapi.com/v1/images/search{image_type}",
    num_of_tries=5,
    request_headers={"Content-Type": "application/json", "x-api-key": dog_api_key},
)[0]["url"]

try:
    bot = Bot(telegram_bot_id)

    if url.endswith(".gif"):
        asyncio.run(bot.send_animation(telegram_chat_id, url))
    else:
        asyncio.run(bot.send_photo(telegram_chat_id, url))
except Exception as exc:
    print(exc)
    traceback.print_exc()

image_name = url.split("/")[-1]

img_data = requests.get(url).content
with open(image_name, 'wb') as handler:
    handler.write(img_data)

try:
    auth = tweepy.OAuth1UserHandler(
        config['twitter_key'],
        config['twitter_secret'],
        config['twitter_token_key'],
        config['twitter_token_secret']
    )

    api = tweepy.API(auth)

    api.update_status_with_media("One #dog per day keeps the doctor away. #dogsoftwitter", image_name)
except Exception as exc:
    print(exc)
    traceback.print_exc()

try:
    mastodon = Mastodon(access_token=config["mastodon_token"], api_base_url="hostux.social")
    mastodon_media = mastodon.media_post(image_name)
    if url.endswith(".gif"):
        time.sleep(30)
        print(mastodon.media(mastodon_media["id"]))
    mastodon.status_post('One #dog per day keeps the doctor away. #dogsofmastodon', media_ids=mastodon_media["id"])
except Exception as exc:
    print(exc)
    traceback.print_exc()

os.remove(image_name)
