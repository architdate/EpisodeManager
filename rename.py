import os
import json
import requests

with open('config.json', 'r') as f:
    config = json.load(f)

r = requests.get("https://api.myjson.com/bins/{}".format(config['jsonbin_key']))
data = json.loads(r.text)

def unique_identifiers(data):
    i = {}
    for d in data:
        i[d[3][0]] = (d[0], d[3][1])
    return i

def rename(path, uid):
    init_path = os.getcwd()
    os.chdir(path)
    files = []
    for root, dirs, fi in os.walk(os.getcwd()):
        for n in fi:
            if n[-3:] in ['mkv', 'mp4', 'flv', 'avi']:
                files.append(os.path.join(root, n))
    for f in files:
        if ".!qB" not in f:
            tf = f
            for k, v in uid.items():
                if k.lower() in tf.lower():
                    ext = "." + tf.rsplit(".", 1)[1]
                    e = tf.lower().split(v[1][0].lower())[1].split(v[1][1])[0]
                    tf = v[0] + " - " + e + ext
                    os.rename(f, tf)
    os.chdir(init_path)

def main():
    uid = unique_identifiers(data)
    rename("F:\\RSSDownloads", uid)