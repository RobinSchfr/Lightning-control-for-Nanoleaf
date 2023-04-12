from lightController import LightController
from settings import Settings
from ui_Structure import Ui_Structure


Settings.createSettingsFile()
light = LightController()
ui = Ui_Structure(light)