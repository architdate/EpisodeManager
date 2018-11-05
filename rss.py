import requests
import datetime
import urllib
import json
import sys
import os

with open('config.json', 'r') as f:
    config = json.load(f)

r = requests.get("http://api.jsonbin.io/b/{}/latest".format(config['jsonbin_key']))
data = json.loads(r.text)

def login(username, password):
    payload = {'username': username, 'password': password}
    r = requests.post('http://{}/api/v2/auth/login'.format(config['webui_ipport']), data = payload)
    return r.cookies.get_dict()

def get_feeds(cookie):
    r = requests.get('http://{}/api/v2/rss/items'.format(config['webui_ipport']), cookies = cookie)
    items = json.loads(r.text)
    urls = []
    for i in list(items.values()):
        urls.append(i['url'])
    return urls

def add_feeds(data, cookie):
    all_urls = []
    for d in data:
        all_urls.append(d[1])
    all_urls = list(set(all_urls))
    for q in get_feeds(cookie):
        if q in all_urls:
            all_urls.remove(q)
    for u in all_urls:
        r = requests.post("http://{}/api/v2/rss/addFeed".format(config['webui_ipport']), data = {'url': u, 'path': ""}, cookies = cookie)
    return all_urls

def add_rules(data, urls, cookie, onlynew = True):
    new_data = []
    for d in data:
        if d[1] in urls:
            new_data.append(d)
    for n in new_data:
        rule = json.dumps(form_rule(n[2], n[1], onlynew))
        name = "{} : (Feed: {})".format(n[0], n[1])
        data = 'ruleName={}&ruleDef={}'.format(urllib.parse.quote(name), urllib.parse.quote(rule))
        r = requests.post('http://{}/api/v2/rss/setRule'.format(config['webui_ipport']), data = data, cookies = cookie, headers = {'Content-Type': 'application/x-www-form-urlencoded'})

def form_rule(mustContain, affectedFeeds, onlynew = True):
    with open('sample_rule.json', 'r') as f:
        rule = json.load(f)
    rule['mustContain'] = mustContain
    rule['affectedFeeds'] = [affectedFeeds]
    rule['savePath'] = config['dest_folder']
    if onlynew:
        rule['ignoreDays'] = 1
        yesterday = datetime.datetime.now() - datetime.timedelta(1)
        rule['lastMatch'] = yesterday.strftime("%d %b %Y %H:%M:%S")
    return rule

def part_a():
    cookie = login(config['webui_user'], config['webui_pass'])
    return add_feeds(data, cookie)

def part_b(urls, onlynew = True):
    cookie = login(config['webui_user'], config['webui_pass'])
    add_rules(data, urls, cookie, onlynew)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        if sys.argv[1] == "true":
            if sys.argv[2] == "true":
                part_b(part_a())
            else:
                part_b(part_a(), False)
        else:
            part_a()
    else:
        part_a()