from nanoleafapi import *
import json
import requests


ip = 'ip'
auth_token = 'auth_token'
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