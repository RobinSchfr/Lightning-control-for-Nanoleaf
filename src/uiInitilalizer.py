from filemanager import Filemanager, File
import colorConverter


class UiInitilalizer:
    def __init__(self, effectOptionsTab, editPalette, secondaryColorCheckbox, secondaryColorInput):
        self.effectOptionsTab = effectOptionsTab
        self.editPalette = editPalette
        self.secondaryColorCheckbox = secondaryColorCheckbox
        self.secondaryColorInput = secondaryColorInput
        currentEffect = Filemanager.getValue(File.EFFECTS, "current_effect")
        if currentEffect is not None:
            self.loadUI(currentEffect)

    def loadUI(self, effect):
        palette = self.getColors(effect)
        self.editPalette.loadPalette(palette)

    def getColors(self, effect):
        hsbColors = effect['write']['palette']
        palette = []
        for color in hsbColors:
            palette.append(colorConverter.HSBtoHEX(color['hue'], color['saturation'], color['brightness']))
        if len(palette) > 3:
            containsSecondaryColor = True
            comparator = palette[1]
            for i in range(3, len(palette), 2):
                if palette[i] != comparator:
                    containsSecondaryColor = False
                    break
            if containsSecondaryColor:
                palette = palette[::2]
                self.secondaryColorCheckbox.set_value(True)
                self.secondaryColorInput.set_value(comparator)
        return palette