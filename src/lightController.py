from nanoleafapi import *
import colorConverter
import requests


class LightController:
    def __init__(self):
        self.nl = None
        self.notifier = None

    def initialize(self, ip, auth_token):
        self.nl = Nanoleaf(ip, auth_token)

    def setBrightness(self, value):
        if self.isDeviceConnected():
            self.nl.set_brightness(value)
            self.notifier.notify(message=f'Set brightness to {value}%')

    def setPower(self, value):
        if self.isDeviceConnected():
            if value:
                self.nl.power_on()
                self.notifier.notify(message='Set device on.')
            else:
                self.nl.power_off()
                self.notifier.notify(message='Set device off.')

    def setColor(self, color):
        if self.isDeviceConnected():
            self.nl.set_color(colorConverter.HEXtoRGB(color))
            self.notifier.notify(message=f'Set static color to {color}.', type='positive')

    def setEffect(self, effect):
        if self.isDeviceConnected():
            requests.put(self.nl.url + "/effects", data=effect)
            self.notifier.notify(message='Color effect applied.', type='positive')

    def identify(self):
        if self.isDeviceConnected():
            self.nl.identify()

    def isDeviceConnected(self):
        if self.nl is None:
            self.notifier.notify(message='No device connected. Please add a new device first.', type='negative')
            return False
        return True


    def setNotifier(self, notifier):
        self.notifier = notifier