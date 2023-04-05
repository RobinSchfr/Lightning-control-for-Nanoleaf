from nicegui import ui


class Ui_Palette:
    def __init__(self, palette, editPalette):
        self.palette = palette
        self.editPalette = editPalette
        uiPalette = ui.html(f'<div class="palette" style="display: flex; flex-direction: row;margin-top: 10px;filter: none;"><div style="width: 20%; height: 100px; background-color: {palette[0]};"></div><div style="width: 20%; height: 100px; background-color: {palette[1]};"></div><div style="width: 20%; height: 100px; background-color: {palette[2]};"></div><div style="width: 20%; height: 100px; background-color: {palette[3]};"></div><div style="width: 20%; height: 100px; background-color: {palette[4]};"></div></div>')
        uiPalette.on('click', lambda:  self.editPalette.loadPalette(self.palette))