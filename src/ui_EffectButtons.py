from nicegui import ui
from effectList import effects
from ui_EffectButton import Ui_EffectButton


class Ui_EffectButtons:
    def __init__(self, eventHandler):
        self.selectedEffect = 'Static'
        self.eventHandler = eventHandler

    def loadEffects(self, effectType):
        with ui.row():
            for effect in effects[effectType]:
                Ui_EffectButton(effect, self.eventHandler)