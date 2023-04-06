from nicegui import ui
from typing import Any, Dict, List, Union
from ui_Widget import Ui_Widget


class Ui_AnnotatedToggle:
    def __init__(self, options: Union[List, Dict], *, value: Any = None, description: str = '', effectFactory) -> None:
        self.effectFactory = effectFactory
        with ui.row().style('margin-top: 20px;'):
            self.label = ui.label(description).style('margin-top: 20px;')
            self.slider = ui.toggle(options, value=value, on_change=self.updateValue).style('width: 50%;margin-top: 14px;')
            self.sep = ui.separator().style('margin-top: 5%')
            self.widget = Ui_Widget([self.label, self.slider, self.sep])

    def updateValue(self):
        self.effectFactory.linDirection = str(self.slider.options[self.slider.value]).lower()
        self.effectFactory.buildEffect()