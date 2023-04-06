from nicegui import ui


class Ui_ColorButton:
    def __init__(self, color, editPalette):
        self.colorCode = color
        self.editPalette = editPalette
        self.picker = ui.color_picker(on_pick=lambda e: self.changeColor(e.color))
        self.button = ui.button(on_click=self.picker.open).props('icon=colorize color=black').style('border: 2px solid #000; width: 38px; height: 38px;')
        self.changeColor(color, False)

    def changeColor(self, color, updateEffect=True):
        self.colorCode = color
        self.button.style(f'background-color:{color}!important')
        self.picker.set_color(color)
        if updateEffect:
            self.editPalette.update()