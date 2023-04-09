from dotenv import load_dotenv
from nanoleafapi import *
import colorConverter
import os
import requests


class LightController:
    def __init__(self):
        load_dotenv()
        self.ip = os.getenv('IP')
        self.auth_token = os.getenv('AUTH_TOKEN')
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