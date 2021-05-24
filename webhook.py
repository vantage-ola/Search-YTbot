from flask import Flask, request
from youtubesearchpython import VideosSearch

import telepot
import urllib3

from pathlib import Path
from dotenv import load_dotenv
import os


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = os.getenv('SECRET')
bot = telepot.Bot(os.getenv('TOKEN'))
domain = ''
bot.setWebhook("https://{}.pythonanywhere.com/{}".format(domain,secret), max_connections=1)

def YSearch(keyword):
    search = VideosSearch(keyword, limit = 1)
    video= search.result()
    a=video['result']
    each= 0
    info=[a[each]['title'],a[each]['viewCount']['short'],a[each]['publishedTime'],a[each]['duration'],a[each]['link']]
    return('Video Title: {} \nVideo Views: {}\nPublishedTime: {}\nDuration: {}\nLink: {}'.format(info[0],info[1],info[2],info[3],info[4]))

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if "text" in update["message"]:
            text = update["message"]["text"]
            if text == "/start":
                bot.sendMessage(chat_id, "Search Keyword:")
            else:
                bot.sendMessage(chat_id, "You searched for '{}' \n\n\nResults: \n\n{}'".format(text, YSearch(text)))
        else:
            bot.sendMessage(chat_id, "From the web: sorry, I didn't understand that kind of message")
    return "OK"
