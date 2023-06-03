from lightController import LightController
from filemanager import Filemanager
from ui_Structure import Ui_Structure


Filemanager.createFiles()
light = LightController()
ui = Ui_Structure(light)