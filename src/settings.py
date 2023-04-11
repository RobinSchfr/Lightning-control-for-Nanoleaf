import json


class Settings:
    @staticmethod
    def setValue(key, value):
        with open('../settings.json', 'r') as settingsFile:
            settings = json.load(settingsFile)
        settings[key] = value
        with open('../settings.json', 'w') as settingsFile:
            json.dump(settings, settingsFile)

    @staticmethod
    def getValue(key):
        with open('../settings.json', 'r') as settingsFile:
            settings = json.load(settingsFile)
        return settings[key]