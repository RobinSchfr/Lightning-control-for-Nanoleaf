from dotenv import load_dotenv
from nanoleafapi import *
import json
import os
import requests


load_dotenv()
ip = os.getenv('IP')
auth_token = os.getenv('AUTH_TOKEN')
nl = Nanoleaf(ip, auth_token)


def getAllEffects():
    return {
        "write": {
            "command": "requestPlugins",
            "version": "2.0"
        }
    }


def getSpecificEffect(effect):
    return {
        "write": {
            "command": "request",
            "animName": effect
        }
    }


command = getSpecificEffect('Aurora magic')
commandString = str(command).replace('\'', '\"')
response = requests.put(nl.url + '/effects', data=commandString)
jsonOut = json.loads(response.text)
print(json.dumps(jsonOut, indent=2))