import json


class Settings:
    @staticmethod
    def setValue(key, value):
        with open('settings.json', 'r') as settingsFile:
            settings = json.load(settingsFile)
        settings[key] = value
        with open('settings.json', 'w') as settingsFile:
            json.dump(settings, settingsFile, indent=4)

    @staticmethod
    def getValue(key):
        with open('settings.json', 'r') as settingsFile:
            settings = json.load(settingsFile)
        return settings[key]

    @staticmethod
    def createSettingsFile():
        try:
            Settings.getValue("ip")
        except FileNotFoundError:
            settings = {"ip": None, "auth_token": None, "dark_mode": True, "accent_color": "#4500db", "language": "english", "native_mode": False}
            with open('settings.json', 'w') as settingsFile:
                json.dump(settings, settingsFile, indent=4)