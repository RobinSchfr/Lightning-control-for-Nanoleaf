from nicegui import ui
from colors_1000 import palettes
from ui_AnnotatedSlider import Ui_AnnotatedSlider
from ui_Palette import Ui_Palette
from ui_EditPalette import Ui_EditPalette
import colorConverter
from effectFactory import EffectFactory
from ui_EffectButtons import Ui_EffectButtons
from ui_EffectOptionsTab import Ui_EffectOptionsTab
from eventHandler import EventHandler


class Ui_Structure:
    def __init__(self, light):
        self.eventHandler = EventHandler()
        self.effectFactory = None
        self.editPalette = None
        self.lightController = light
        with ui.row().style('width: 100%; display: flex;justify-content: space-between;align-items: flex-start;'):
            with ui.expansion(text='Colors', icon='palette').style('width: 30%;position: sticky;top: 0;'):
                pass
                with ui.tabs() as tabs:
                    ui.tab(name='Edit pallete', icon='brush')
                    ui.tab(name='Choose pallete', icon='table_rows')
                with ui.tab_panels(tabs=tabs, value='Choose pallete'):
                    with ui.tab_panel(name='Edit pallete'):
                        self.loadPaletteEditor()
                    with ui.tab_panel(name='Choose pallete'):
                        self.loadPalettes()
            with ui.expansion(text='Effects', icon='auto_awesome').style('width: 30%;position: sticky;top: 0;'):
                self.effectButtons = Ui_EffectButtons(self.eventHandler)
                with ui.tabs() as tabs:
                    ui.tab(name='Basic', icon='invert_colors')
                    ui.tab(name='Sound', icon='music_note')
                with ui.tab_panels(tabs=tabs, value='Basic'):
                    with ui.tab_panel(name='Basic'):
                        self.effectButtons.loadEffects(effectType='color')
                    with ui.tab_panel(name='Sound'):
                        self.effectButtons.loadEffects(effectType='rhythm')
            with ui.expansion(text='Options', icon='edit').style('width: 30%;position: sticky;top: 0;'):
                with ui.tabs() as tabs:
                    ui.tab(name='Effect options', icon='tune')
                    ui.tab(name='Settings', icon='settings')
                with ui.tab_panels(tabs=tabs, value='Effect options'):
                    with ui.tab_panel(name='Effect options'):
                        self.effectOptionsTab = Ui_EffectOptionsTab(self.eventHandler)
                        self.eventHandler.setEffectOptionsTab(self.effectOptionsTab)
                    with ui.tab_panel(name='Settings'):
                        self.powerSwitch = ui.switch(text='ON/OFF', value=True, on_change=lambda e: self.lightController.setPower(e.value)).props('icon=power_settings_new')
                        self.briSlider = Ui_AnnotatedSlider(min=0, max=100, value=100, description='Brightness:', lightController=self.lightController)
                        with ui.expansion(text='System settings', icon='settings').style('margin-top: 10%;'):
                            with ui.column():
                                with ui.dialog().props('persistent') as dialog, ui.card():
                                    ui.label(text='Language:')
                                    ui.select(['English', 'German'], value='English')
                                    ui.button(text='Close', on_click=dialog.close)
                                ui.button('Language', on_click=dialog.open).props('icon=language').style('margin-top: 5%;')
                                with ui.dialog().props('persistent') as dialog, ui.card():
                                    ui.label(text='Appearance:')
                                    ui.select({1: 'Light mode', 2: 'Dark mode'}, value=2, on_change=lambda e: self.toggleDarkMode(e.value))
                                    ui.button(text='Close', on_click=dialog.close)
                                ui.button(text='Appearance', on_click=dialog.open).props('icon=dark_mode')
                                with ui.dialog().props('persistent') as dialog, ui.card():
                                    ui.input(label='IP address')
                                    ui.input(label='auth_token', password=True, password_toggle_button=True)
                                    ui.button(text='Identify', on_click=self.lightController.identify())
                                    ui.button(text='Close', on_click=dialog.close)
                                ui.button(text='Developer options', on_click=dialog.open).props('icon=build color=red').style('margin-top: 15%;')
        self.editPalette.addColor()
        ui.colors(primary='#6400ff')    # green: #58b947
        ui.run(title='Lightning control for Nanoleaf - by Robin Schäfer', favicon='https://play-lh.googleusercontent.com/2WXa6Cwbvfrd6R1vvByeoQD5qa7zOr8g33vwxL-aPPRd9cIxZWNDqfUJQcRToz6A9Q', show=False, dark=True)

    def loadPalettes(self):
        ui.add_head_html('''<style>.palette:hover{border: 4px solid #000; box-sizing: border-box;}</style>''')
        with ui.element('div').style('overflow:auto; height:80vh;padding: 20px;'):
            for palette in palettes:
                Ui_Palette(palette, self.editPalette)

    def loadPaletteEditor(self):
        self.effectFactory = EffectFactory(self.lightController, self.eventHandler)
        self.eventHandler.setEffectFactory(self.effectFactory)
        self.editPalette = Ui_EditPalette(self.effectFactory)
        ui.separator().style('margin-top: 5%')
        with ui.row().style('margin-top: 5%'):
            ui.button(on_click=lambda: self.editPalette.addColor()).props('icon=add').tooltip(text='Add new color')
            ui.button(on_click=lambda: self.editPalette.remove()).props('icon=remove').tooltip(text='Remove first color')
            ui.button(on_click=lambda: self.editPalette.clear()).props('icon=delete').tooltip(text='Clear palette')
        with ui.row().style('margin-top: 5%'):
            ui.button(on_click=lambda: self.editPalette.shiftLeft()).props('icon=arrow_left').tooltip(text='Shift palette one color to left')
            ui.button(on_click=lambda: self.editPalette.shiftRight()).props('icon=arrow_right').tooltip(text='Shift palette one color to right')
        with ui.row().style('margin-top: 5%'):
            ui.button(on_click=lambda: None).props('icon=favorite').tooltip('Save this palette to favorites')
        ui.separator().style('margin-top: 5%')
        with ui.column():
            checkbox = ui.checkbox(text='Add secondary color (50% ratio)').style('margin-top: 5%').tooltip(text='After each color of the palette the secondary color will be added')
            colorInput = ui.color_input(label='Secondary color', value='#000000', on_change=None).bind_visibility_from(checkbox, 'value').props('color=black')
        with ui.column():
            checkbox2 = ui.checkbox(text='Create color shades').style('margin-top: 5%').tooltip(text='Creates 10 shades of a specific color')
            colorInput2 = ui.color_input(label='Color', value='#000000', on_change=None).bind_visibility_from(checkbox2, 'value').props('color=black')
            ui.button(on_click=lambda e: self.createShades(colorInput2.value)).props('icon=add').tooltip('Create palette').bind_visibility_from(checkbox2, 'value')
        ui.separator().style('margin-top: 5%')
        with ui.row().style('margin-top: 5%'):
            ui.button(text='Update', on_click=lambda: self.editPalette.update()).props('icon=sync')


    def createShades(self, color):
        h, s, l = colorConverter.HEXtoHSL(color)
        self.editPalette.clear(True)
        for l in range(95, 4, -10):
            self.editPalette.addColor(colorConverter.HSLtoHEX(h, s, l), False)

    @staticmethod
    def toggleDarkMode(newValue):
        darkMode = True
        if newValue == 1:
            darkMode = False
        ui.run(dark=darkMode)
        ui.notify(message='Press F5 to apply', type='info')