import colorConverter
import copy


class EffectFactory:
    BASE_EFFECT = {
        "write": {"command": "display", "version": "2.0", "animType": "plugin", "colorType": "HSB",
                  "palette": [],
                  "pluginType": "", "pluginUuid": "",
                  "pluginOptions": []}}

    def __init__(self, lightController, eventHandler):
        self.lightController = lightController
        self.eventHandler = eventHandler
        self.currentEffect = list()
        self.colorPalette = None
        self.secondaryColor = None
        self.pluginType = ''
        self.delayTime = 10
        self.transTime = 10
        self.linDirection = 'right'
        self.mainColorProb = 50
        self.evolutionSpeed = 50
        self.scale = 50
        self.stretch = 50
        self.nColorsPerFrame = 2
        self.propValues = None
        self.updatePropValues()

    def updatePropValues(self):
        self.propValues = {'delayTime': self.delayTime,
                           'transTime': self.transTime,
                           'linDirection': self.linDirection,
                           'mainColorProb': self.mainColorProb,
                           'evolutionSpeed': self.evolutionSpeed,
                           'scale': self.scale,
                           'stretch': self.stretch,
                           'nColorsPerFrame': self.nColorsPerFrame
                           }

    def buildEffect(self):
        if self.colorPalette is None:
            return
        elif self.currentEffect[0] is None:
            self.lightController.setColor(self.colorPalette[0])
        else:
            effectJson = copy.deepcopy(self.BASE_EFFECT)
            if self.secondaryColor is not None:
                secondaryH, secondaryS, secondaryB = colorConverter.HEXtoHSB(self.secondaryColor)
            for color in self.colorPalette:
                h, s, b = colorConverter.HEXtoHSB(color)
                effectJson['write']['palette'].append({"hue": h, "saturation": s, "brightness": b})
                if self.secondaryColor is not None:
                    effectJson['write']['palette'].append({"hue": secondaryH, "saturation": secondaryS, "brightness": secondaryB})
            effectJson["write"].update({"pluginType": self.pluginType})
            effectJson["write"].update({"pluginUuid": self.currentEffect[0]})
            self.updatePropValues()
            for prop in self.currentEffect[1]:
                effectJson['write']['pluginOptions'].append({"name": prop, "value": self.propValues[prop]})
            effectString = str(effectJson).replace('\'', '\"')
            self.lightController.setEffect(effectString)
        self.eventHandler.effectOptionsTab.infoAlert()