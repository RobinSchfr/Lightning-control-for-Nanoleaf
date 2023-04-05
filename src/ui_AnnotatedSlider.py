from typing import Optional
from nicegui import ui
from ui_Widget import Ui_Widget


class Ui_AnnotatedSlider:
    def __init__(self, *, min: float, max: float, step: float = 1.0, value: Optional[float] = None, description: str = '', effectFactory: Optional = None, lightController: Optional = None) -> None:
        self.effectFactory = effectFactory
        self.lightController = lightController
        self.description = description
        with ui.row().style('margin-top: 20px;'):
            self.label = ui.label(description).style('margin-top: 20px;')
            self.slider = ui.slider(min=min, max=max, step=step, value=value, on_change=self.updateValue).style('width: 50%;margin-top: 18px;').props('label-always')
            self.sep = ui.separator().style('margin-top: 5%')
            self.widget = Ui_Widget([self.label, self.slider, self.sep])

    def updateValue(self):
        match self.description:
            case 'Main Color Probability:':
                self.effectFactory.mainColorProb = self.slider.value
                self.effectFactory.buildEffect()
            case 'Evolution Speed:':
                self.effectFactory.evolutionSpeed = self.slider.value
                self.effectFactory.buildEffect()
            case 'Scale:':
                self.effectFactory.scale = self.slider.value
                self.effectFactory.buildEffect()
            case 'Stretch:':
                self.effectFactory.stretch = self.slider.value
                self.effectFactory.buildEffect()
            case 'n Colors per frame:':
                self.effectFactory.nColorsPerFrame = self.slider.value
                self.effectFactory.buildEffect()
            case 'Brightness:':
                if self.lightController is not None:
                    self.lightController.setBrightness(self.slider.value)