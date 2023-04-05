from nanoleafapi import *
import colorConverter
import requests
import credentials


class LightController:
    def __init__(self):
        self.ip = credentials.ip
        self.auth_token = credentials.auth_token
        self.nl = Nanoleaf(self.ip, self.auth_token)

    def setBrightness(self, value):
        self.nl.set_brightness(value)

    def setPower(self, value):
        if value:
            self.nl.power_on()
        else:
            self.nl.power_off()

    def setColor(self, color):
        self.nl.set_color(colorConverter.HEXtoRGB(color))

    def setEffect(self, effect):
        requests.put(self.nl.url + "/effects", data=effect)

    def identify(self):
        self.nl.identify()