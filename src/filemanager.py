from enum import Enum
import json


class File(Enum):
    SETTINGS = 'settings.json'
    EFFECTS = 'effects.json'


class Filemanager:
    @staticmethod
    def setValue(file, key, value):
        with open(file.value, 'r') as settingsFile:
            settings = json.load(settingsFile)
        settings[key] = value
        with open(file.value, 'w') as settingsFile:
            json.dump(settings, settingsFile, indent=4)

    @staticmethod
    def getValue(file, key):
        with open(file.value, 'r') as settingsFile:
            settings = json.load(settingsFile)
        return settings[key]

    @staticmethod
    def createFiles():
        try:
            Filemanager.getValue(File.SETTINGS, "ip")
        except FileNotFoundError:
            settings = {"ip": None, "auth_token": None, "dark_mode": True, "accent_color": "#4500db", "language": "english", "native_mode": False}
            with open(File.SETTINGS.value, 'w') as settingsFile:
                json.dump(settings, settingsFile, indent=4)
        try:
            Filemanager.getValue(File.EFFECTS, "current_effect")
        except FileNotFoundError:
            effects = {"current_effect": None}
            with open(File.EFFECTS.value, 'w') as effectsFile:
                json.dump(effects, effectsFile, indent=4)