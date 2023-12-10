import json

def readConf():
    with open('config.json') as f:
        return json.load(f)