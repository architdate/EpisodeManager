# Misc Plex Functions

import json
import requests
from plexapi.myplex import MyPlexAccount
import os
import sys

MOVIELIB = "Films"
ANIMELIB = "Anime"
TVLIB = "TV programmes"

with open('config.json', 'r') as f:
    config = json.load(f)

def login_account(username, password):
    return MyPlexAccount(username, password)

def login_server(account, servername):
    return account.resource(servername).connect()

def get_user_list(server):
    return [c.title for c in server.clients()]

def scan_movies(server):
    movies = server.library.section(MOVIELIB)
    movies.update()

def scan_tv(server):
    tv = server.library.section(TVLIB)
    tv.update()

def scan_anime(server):
    anime = server.library.section(ANIMELIB)
    anime.update()

def get_users(account):
    friends = []
    pending = []
    for i in account.users():
        if i.friend:
            friends.append(i.username)
        else:
            pending.append(i.username)
    return {'friends': friends, 'pending': pending}
        
# Placeholder file