from effectList import effects
from nicegui import ui
from ui_AnnotatedSlider import Ui_AnnotatedSlider
from ui_AnnotatedToggle import Ui_AnnotatedToggle
from ui_DoubleSlider import Ui_DoubleSlider


class Ui_EffectOptionsTab:
    def __init__(self, eventHandler):
        self.eventHandler = eventHandler
        self.effectFactory = self.eventHandler.effectFactory
        with ui.row():
            ui.label('Current Effect:')
            self.currentEffect = ui.label()
            ui.separator().style('margin-top: 5%')
        self.delayTime = Ui_DoubleSlider('Delay Time:', self.effectFactory)
        self.transTime = Ui_DoubleSlider('Transition Time:', self.effectFactory)
        self.linDirection = Ui_AnnotatedToggle({1: 'Right', 2: 'Left', 3: 'Up', 4: 'Down'}, value=1, description='Direction:', effectFactory=self.effectFactory)
        self.mainColorProb = Ui_AnnotatedSlider(min=0, max=100, value=50, description='Main Color Probability:', effectFactory=self.effectFactory)
        self.evolutionSpeed = Ui_AnnotatedSlider(min=0, max=100, value=50, description='Evolution Speed:', effectFactory=self.effectFactory)
        self.scale = Ui_AnnotatedSlider(min=0, max=100, value=50, description='Scale:', effectFactory=self.effectFactory)
        self.stretch = Ui_AnnotatedSlider(min=0, max=100, value=50, description='Stretch:', effectFactory=self.effectFactory)
        self.nColorsPerFrame = Ui_AnnotatedSlider(min=2, max=10, value=2, description='n Colors per frame:', effectFactory=self.effectFactory)
        self.info = ui.label('No further settings available for this effect.').style('margin-top: -20%;')
        self.setEffect('Random')

    def setEffect(self, effect):
        self.currentEffect.set_text(effect)
        self.hideOptions()
        self.effectFactory.pluginType, effect = self.getEffectProps(effect)
        self.effectFactory.currentEffect = effect
        props = effect[1]
        if 'delayTime' in props:
            self.delayTime.widget.setVisibility(True)
        if 'transTime' in props:
            self.transTime.widget.setVisibility(True)
        if 'linDirection' in props:
            self.linDirection.widget.setVisibility(True)
        if 'mainColorProb' in props:
            self.mainColorProb.widget.setVisibility(True)
        if 'evolutionSpeed' in props:
            self.evolutionSpeed.widget.setVisibility(True)
        if 'scale' in props:
            self.scale.widget.setVisibility(True)
        if 'stretch' in props:
            self.stretch.widget.setVisibility(True)
        if 'nColorsPerFrame' in props:
            self.nColorsPerFrame.widget.setVisibility(True)
        if len(props) == 0:
            self.info.set_visibility(True)

    def hideOptions(self):
        for element in [self.delayTime, self.transTime, self.linDirection, self.mainColorProb, self.evolutionSpeed, self.scale, self.stretch, self.nColorsPerFrame]:
            element.widget.setVisibility(False)
        self.info.set_visibility(False)

    @staticmethod
    def getEffectProps(effect):
        for key in effects.keys():
            try:
                return key, effects[key][effect]
            except KeyError:
                pass