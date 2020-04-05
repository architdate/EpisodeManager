import requests
import urllib
import json
import random
import sys
import os

randomart = True
try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

with open('config.json', 'r') as f:
    config = json.load(f)

r = requests.get("https://jsonblob.com/api/jsonBlob/{}".format(config['jsonbin_key']))
data = json.loads(r.text)

TOKEN = config['telegram_api']
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode('utf8')
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    get_url(url)

def send_image(url, chat_id):
    url = URL + "sendPhoto?photo={}&chat_id={}".format(url, chat_id)
    get_url(url)

def tvdb_art(series):
    artwork = []
    apikey = config['tvdb_api']
    tvdbtoken = json.loads(requests.post("https://api.thetvdb.com/login", data = json.dumps({"apikey":apikey}), headers = {"Content-Type": "application/json", "Accept":"application/json"}).text)['token']
    headers = {"Authorization":"Bearer {}".format(tvdbtoken), "Accept-Language":"en"}
    r = requests.get("https://api.thetvdb.com/series/{}/images/query?subKey=graphical&keyType=fanart".format(series), headers=headers)
    base_url = 'http://thetvdb.com/banners/'
    if r.status_code != 404:
        imgdata = json.loads(r.text)['data']
        for i in imgdata:
            artwork.append(base_url + i['fileName'])
    else:
        artwork.append('https://wallpaperplay.com/walls/full/d/7/2/56560.jpg')
    return artwork

def extract_data(filename):
    series_name = filename.rsplit(" - ", 1)[0]
    series_id = -1
    for d in data:
        if d[0] == series_name:
            series_id = d[5]
    episode_num = filename.rsplit(" - ", 1)[1].rsplit(".", 1)[0]
    if series_id < 0:
        artwork = ['https://wallpaperplay.com/walls/full/d/7/2/56560.jpg']
    else:
        artwork = tvdb_art(series_id)
    return {'name': series_name, 'id': series_id, 'num': episode_num, 'artwork': artwork}
       
def notify(filename):
    metadata = extract_data(filename)
    metadata_str = "*New Episode Downloaded*\n\n*Series:* {}\n*Episode Number:* {}\n*TVDB ID:* {}".format(metadata['name'], metadata['num'], metadata['id'])
    if randomart:
        artwork = random.choice(metadata['artwork'])
    else:
        artwork = metadata['artwork'][0]
    send_image(artwork, config['chat_id'])
    send_message(metadata_str, config['chat_id'])

def notify_discord(filename):
    metadata = extract_data(filename)
    if randomart:
        artwork = random.choice(metadata['artwork'])
    else:
        artwork = metadata['artwork'][0]
    emjson = {"title": "New Episode Downloaded", "fields": [{"name": "Show", "value":metadata['name'], "inline":"true"},{"name":"Episode Number", "value":metadata['num'], "inline":"true"}], "url": "https://plex.tv", "footer": {"icon_url":"https://flixed.io/wp-content/uploads/2017/10/plex-logo.png", "text": metadata['name']}, "author": {"name": metadata['name'] + " (TVDB ID: {})".format(metadata['id'])}, "image": {"url": artwork}, 'color':15445836}
    resp = {"embeds": [emjson]}
    r = requests.post(config['discord_webhook'], data=json.dumps(resp), headers = {"Content-Type": "application/json"})

def sonarr_notify(tvdb_id, series_title, ep):
    if randomart:
        artwork = random.choice(tvdb_art(tvdb_id))
    else:
        artwork = tvdb_art(tvdb_art)[0]
    emjson = {"title": "New Episode Downloaded", "fields": [{"name": "Show", "value":series_title, "inline":"true"},{"name":"Episode Number", "value":ep, "inline":"true"}], "url": "https://plex.tv", "footer": {"icon_url":"https://flixed.io/wp-content/uploads/2017/10/plex-logo.png", "text": series_title}, "author": {"name": series_title + " (TVDB ID: {})".format(tvdb_id)}, "image": {"url": artwork}, 'color':15445836}
    resp = {"embeds": [emjson]}
    r = requests.post(config['discord_webhook'], data=json.dumps(resp), headers = {"Content-Type": "application/json"})
    metadata_str = "*New Episode Downloaded*\n\n*Series:* {}\n*Episode Number:* {}\n*TVDB ID:* {}".format(series_title, ep, tvdb_id)
    send_image(artwork, config['chat_id'])
    send_message(metadata_str, config['chat_id'])


if __name__ == "__main__":
    notify_discord("Tower of God - 01.mkv")