import os
import json

with open('config.json', 'r') as f:
    config = json.load(f)

with open('data.json', 'r') as f:
    data = json.load(f)

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
                    e = tf.split(v[1][0])[1].split(v[1][1])[0]
                    tf = v[0] + " - " + e + ext
                    os.rename(f, tf)
    os.chdir(init_path)

def main():
    uid = unique_identifiers(data)
    rename("F:\\RSSDownloads", uid)