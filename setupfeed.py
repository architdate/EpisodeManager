import json
import requests
import sys
import os
import rss as rssfeed

def form_data(show, rss, uid, fid, s1, s2, path, tvdb):
    return [show, rss, uid, [fid, [s1, s2]], path, int(tvdb)]

def argsetup(arglist):
    dlr = True
    with open('config.json', 'r') as f:
        config = json.load(f)
    r = requests.get("http://api.jsonbin.io/b/{}/latest".format(config['jsonbin_key']))
    data = json.loads(r.text)
    show, rss, uid, fid, s1, s2, path, tvdb, onlynew = arglist
    if onlynew.lower() == "y":
        onlynew = "true"
    else:
        onlynew = "false"

    data.append(form_data(show, rss, uid, fid, s1, s2, path, tvdb))

    r = requests.put("http://api.jsonbin.io/b/{}".format(config['jsonbin_key']), json = data, headers = {'Content-Type':'application/json'})

    if dlr:
        os.system("python rss.py true {} {}".format(onlynew, config['webui_ipport']))
    else:
        os.system("python rss.py false {} {}".format(onlynew))


if __name__ == "__main__":
    dlr = True

    with open('config.json', 'r') as f:
        config = json.load(f)

    r = requests.get("http://api.jsonbin.io/b/{}/latest".format(config['jsonbin_key']))
    data = json.loads(r.text)
    
    if len(sys.argv) == 1:
        # Inputs
        show = input("Enter Show Name: ")
        rss = input("Enter a valid RSS feed for the show: ")
        uid = input("Enter a unique file identifier for the RSS Shows (Only files with this string will be downloaded from the feed): ")
        fid = input("Enter a string to identify the media file from the torrent (Can be 'The.Big.Bang.Theory' or '.mkv' for example): ")
        s1 = input("Enter First Split for episode rename: ")
        s2 = input("Enter Second Split for episode rename: ")
        path = input("Enter path for the new episode to be saved: ")
        tvdb = input("Enter TVDB ID for being notified about the new episode: ")
        onlynew = input("Download new episodes only? (Y/N): ")
    else:
        # Assume All arguments passed
        show, rss, uid, fid, s1, s2, path, tvdb, onlynew = sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]

    if onlynew.lower() == "y":
        onlynew = "true"
    else:
        onlynew = "false"

    data.append(form_data(show, rss, uid, fid, s1, s2, path, tvdb))

    r = requests.put("http://api.jsonbin.io/b/{}".format(config['jsonbin_key']), json = data, headers = {'Content-Type':'application/json'})

    if dlr:
        os.system("python rss.py true {}".format(onlynew))
    else:
        os.system("python rss.py false {}".format(onlynew))
