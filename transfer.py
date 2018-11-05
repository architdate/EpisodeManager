import os
import json
import shutil
import notify
import subprocess
import threading
import time
import requests

with open('config.json', 'r') as f:
    config = json.load(f)

r = requests.get("http://api.jsonbin.io/b/{}/latest".format(config['jsonbin_key']))
data = json.loads(r.text)

def subprocess_execute(command, time_out=60):
    """executing the command with a watchdog"""

    # launching the command
    c = subprocess.Popen(command)

    # now waiting for the command to complete
    t = 0
    while t < time_out and c.poll() is None:
        time.sleep(1)  # (comment 1)
        t += 1

    # there are two possibilities for the while to have stopped:
    if c.poll() is None:
        # in the case the process did not complete, we kill it
        c.terminate()
        # and fill the return code with some error value
        returncode = -1  # (comment 2)

    else:                 
        # in the case the process completed normally
        returncode = c.poll()

    return returncode  

def path_dict(data):
    i = {}
    for d in data:
        i[d[0]] = d[4]
    return i

def transfer(source, path_dict):
    init_path = os.getcwd()
    os.chdir(source)
    files = os.listdir(os.getcwd())
    filepathlist = []
    for f in files:
        if ".!qB" not in f:
            ani = path_dict.keys()
            for a in ani:
                if a in f:
                    if not os.path.exists(path_dict[a]):
                        os.makedirs(path_dict[a])
                    shutil.move(f, path_dict[a] + "\\" + f)
                    filepathlist.append(path_dict[a])
                    notify.notify(f)
                    notify.notify_discord(f)
    os.chdir(init_path)
    return filepathlist

def refresh_plex(plexpath, filepathlist):
    init_path = os.getcwd()
    os.chdir(plexpath)
    for i in filepathlist:
        retval = subprocess_execute('"Plex Media Scanner" -s -r -x -d {}'.format(i), 300)
        print("Scan Finished with Code : {}".format(retval))
    os.chdir(init_path)

def main():
    fpl = transfer("F:\\RSSDownloads", path_dict(data))
    refresh_plex("C:\\Program Files (x86)\\Plex\\Plex Media Server", fpl)