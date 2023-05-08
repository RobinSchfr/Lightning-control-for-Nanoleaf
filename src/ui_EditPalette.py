from nicegui import ui
from ui_ColorButton import Ui_ColorButton


class Ui_EditPalette:
    def __init__(self, effectFactory):
        self.effectFactory = effectFactory
        self.colorButtons = []
        self.container = ui.row()

    def addColor(self, color='#000000', updateEffect=True):
        if len(self.colorButtons) < 10:
            with self.container:
                cb = Ui_ColorButton(color, self)
                self.colorButtons.append(cb)
            if updateEffect:
                self.update()

    def clear(self, deepClear=False):
        self.container.clear()
        self.colorButtons.clear()
        if not deepClear:
            self.addColor(updateEffect=False)
            self.update()

    def remove(self):
        if len(self.colorButtons) > 1:
            self.colorButtons.pop(0)
            self.drawPalette()
            self.update()

    def shiftLeft(self, updateEffect=True):
        if len(self.colorButtons) > 1:
            leftColor = self.colorButtons[0].colorCode
            self.colorButtons.pop(0)
            self.addColor(leftColor, False)
            self.drawPalette()
            if updateEffect:
                self.update()

    def shiftRight(self):
        if len(self.colorButtons) > 1:
            for i in range(len(self.colorButtons) - 1):
                self.shiftLeft(False)
            self.drawPalette()
            self.update()

    def drawPalette(self):
        colors = self.colorButtons.copy()
        self.clear(True)
        for color in colors:
            with self.container:
                cb = Ui_ColorButton(color.colorCode, self)
                self.colorButtons.append(cb)

    def loadPalette(self, palette):
        self.clear(True)
        for color in palette:
            self.addColor(color, False)
        self.update()

    def update(self):
        self.effectFactory.colorPalette = self.getColorPalette()
        self.effectFactory.buildEffect()

    def getColorPalette(self):
        colorPalette = []
        for color in self.colorButtons:
            colorPalette.append(color.colorCode)
        return colorPalette