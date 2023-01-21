import json

def getConfig():

    with open('config.json', 'r') as f:
        config = json.load(f)

    return config

def get_watch_league():

    with open('config.json', 'r') as f:
        config = json.load(f)

    return config['watchlist']