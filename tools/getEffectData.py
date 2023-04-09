from src.lightController import LightController
import json
import requests


lc = LightController()


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
response = requests.put(lc.nl.url + '/effects', data=commandString)
jsonOut = json.loads(response.text)
print(json.dumps(jsonOut, indent=2))