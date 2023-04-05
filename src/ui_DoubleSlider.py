from nicegui import ui
from ui_Widget import Ui_Widget


class Ui_DoubleSlider:
    class Value:
        def __init__(self):
            self.smallVal = 1
            self.bigVal = 0

        def getValue(self):
            return self.smallVal + self.bigVal

    def __init__(self, description, effectFactory):
        self.v = self.Value()
        self.description = description
        self.effectFactory = effectFactory
        with ui.row().style('margin-top: 10px;'):
            self.label = ui.label(description).style('margin-top: 10px;')
            self.labelVal = ui.label().style('margin-top: 10px;')
        self.bigValSlider = ui.slider(min=0, max=59, step=1, on_change=self.updateValue).props('label-always').bind_value(self.v, 'bigVal').style('margin-top: 10%;')
        self.smallValSlider = ui.slider(min=0.1, max=1, step=0.1, on_change=self.updateValue).props('label-always').bind_value(self.v, 'smallVal').style('margin-top: 10%;')
        self.sep = ui.separator().style('margin-top: 5%')
        self.widget = Ui_Widget([self.label, self.labelVal, self.bigValSlider, self.smallValSlider, self.sep])

    def updateValue(self):
        self.labelVal.set_text(f'{self.v.getValue()} seconds')
        if self.description == 'Delay Time:':
            self.effectFactory.delayTime = self.v.getValue() * 10
        else:
            self.effectFactory.transTime = self.v.getValue() * 10
        self.effectFactory.buildEffect()