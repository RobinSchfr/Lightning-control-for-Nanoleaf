from colors_1000 import palettes
from deviceInitializer import DeviceInitializer
from effectFactory import EffectFactory
from eventHandler import EventHandler
from nicegui import ui, app
from settings import Settings
from ui_AnnotatedSlider import Ui_AnnotatedSlider
from ui_EditPalette import Ui_EditPalette
from ui_EffectButtons import Ui_EffectButtons
from ui_EffectOptionsTab import Ui_EffectOptionsTab
from ui_Notifier import Notifier
from ui_Palette import Ui_Palette
import colorConverter
import matplotlib


class Ui_Structure:
    def __init__(self, light):
        self.eventHandler = EventHandler()
        self.effectFactory = None
        self.editPalette = None
        self.lightController = light
        self.notifier = Notifier()
        self.lightController.setNotifier(self.notifier)
        self.device = DeviceInitializer(self.notifier)
        self.currentPaletteId = 0
        with ui.row().style('width: 100%; display: flex;justify-content: space-between;align-items: flex-start;'):
            with ui.expansion(text='Colors', icon='palette').style('width: 30%;position: sticky;top: 0;'):
                with ui.tabs() as tabs:
                    ui.tab(name='Edit palette', icon='brush')
                    ui.tab(name='Choose palette', icon='table_rows').on('click', lambda: ui.open(f'#{self.currentPaletteId + 55}'))     # + 55, to skip every html element with an id which is not a color palette
                with ui.tab_panels(tabs=tabs, value='Choose palette'):
                    with ui.tab_panel(name='Edit palette'):
                        self.loadPaletteEditor()
                    with ui.tab_panel(name='Choose palette'):
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
            with ui.column().style('width: 30%;position: sticky;top: 0;'):
                with ui.expansion(text='Options', icon='edit').style('width: 100%;top: 0;'):
                    with ui.tabs() as tabs:
                        ui.tab(name='Effect options', icon='tune')
                        ui.tab(name='Settings', icon='settings')
                    with ui.tab_panels(tabs=tabs, value='Effect options'):
                        with ui.tab_panel(name='Effect options'):
                            with ui.expansion(text='Device settings', icon='lightbulb'):
                                self.powerSwitch = ui.switch(text='ON/OFF', value=True, on_change=lambda e: self.lightController.setPower(e.value)).props('icon=power_settings_new').style('margin-top: 5%;')
                                self.briSlider = Ui_AnnotatedSlider(min=0, max=100, value=0, description='Brightness:', lightController=self.lightController, checkBox=self.powerSwitch)
                            self.effectOptionsTab = Ui_EffectOptionsTab(self.eventHandler)
                            self.eventHandler.setEffectOptionsTab(self.effectOptionsTab)
                        with ui.tab_panel(name='Settings'):
                            with ui.column():
                                with ui.dialog().props('persistent') as dialog, ui.card():
                                    ui.label(text='Language:')
                                    ui.select(['English', 'German'], value='English')
                                    ui.button(text='Close', on_click=dialog.close)
                                ui.button('Language', on_click=dialog.open).props('icon=language').style('margin-top: 5%;')
                                with ui.dialog().props('persistent') as dialog, ui.card():
                                    ui.label(text='Appearance:')
                                    ui.select({1: 'Light mode', 2: 'Dark mode'}, value=2 if Settings.getValue("dark_mode") else 1, on_change=self.setColorMode)
                                    ui.color_input(label='Accent color', value=Settings.getValue("accent_color"), on_change=lambda e: self.setAccentColor(e.value))
                                    ui.button(text='Close', on_click=dialog.close)
                                ui.button(text='Appearance', on_click=dialog.open).props('icon=light_mode')
                                ui.link(text='GitHub', target='https://github.com/RobinSchfr/Lightning-control-for-Nanoleaf', new_tab=True)
                                with ui.dialog().props('persistent') as dialog, ui.card():
                                    self.ipInput = ui.input(label='IP address', on_change=lambda e: self.device.setIP(e.value))
                                    self.auth_tokenInput = ui.input(label='auth_token', password=True, password_toggle_button=True, on_change=lambda e: self.device.setAuthToken(e.value))
                                    ui.button(text='Get IP from device', on_click=self.getIPFromDevice).props('icon=add')
                                    ui.button(text='Create token', on_click=self.createAuthToken).props('icon=add')
                                    ui.button(text='Connect', on_click=self.connect).props('icon=link')
                                    ui.separator().style('margin-top: 5%')
                                    ui.button(text='Identify', on_click=self.lightController.identify)
                                    ui.button(text='Close', on_click=dialog.close)
                                ui.button(text='Developer options', on_click=dialog.open).props('icon=build color=red').style('margin-top: 15%;')
                with ui.expansion(text='Saved effects', icon='save').style('width: 100%;'):
                    ui.select({1: 'Device 1', 2: 'Device 2', 3: 'Device 3'}, value=1)
                    with ui.row().style('margin-top: 5%'):
                        ui.label(text='Effects stored on selected device: ').style('margin-top: 2%')
                        ui.circular_progress(max=50)
                    with ui.tabs().style('margin-top: 5%') as tabs:
                        ui.tab(name='Effect shortcuts', icon='bookmark')
                        ui.tab(name='Snapshot manager', icon='storage')
                    with ui.tab_panels(tabs=tabs, value='Effect shortcuts'):
                        with ui.tab_panel(name='Effect shortcuts'):
                            ui.button(text='Save current effect', on_click=None).props('icon=done').tooltip(text='Saves current effect as a shortcut (not on device)')
                            ui.separator().style('margin-top: 5%')
                        with ui.tab_panel(name='Snapshot manager'):
                            ui.button(text='Create snapshot', on_click=None).props('icon=create_new_folder').tooltip(text='Saves all local effects from a device')
                            ui.separator().style('margin-top: 5%')
        self.editPalette.addColor()
        self.loadCredentials()
        app.on_connect(lambda: self.updateValues())
        app.native.window_args['zoomable'] = True
        app.native.window_args['confirm_close'] = True
        app.native.window_args['min_size'] = (900, 550)
        ui.run(title='Lightning control for Nanoleaf - by Robin Schäfer', favicon='https://play-lh.googleusercontent.com/2WXa6Cwbvfrd6R1vvByeoQD5qa7zOr8g33vwxL-aPPRd9cIxZWNDqfUJQcRToz6A9Q', reload=False, dark=Settings.getValue("dark_mode"), window_size=(1600, 900) if Settings.getValue("native_mode") else None)

    def loadPalettes(self):
        ui.add_head_html('''<style>.palette:hover{border: 4px solid #000; box-sizing: border-box;}</style>''')
        with ui.element('div').style('overflow:auto; height:80vh;padding: 20px;'):
            for id, palette in enumerate(palettes):
                Ui_Palette(palette, id, self.editPalette, self)

    def loadPaletteEditor(self):
        self.effectFactory = EffectFactory(self.lightController, self.eventHandler)
        self.eventHandler.setEffectFactory(self.effectFactory)
        self.editPalette = Ui_EditPalette(self.effectFactory)
        ui.separator().style('margin-top: 5%')
        with ui.row().style('margin-top: 5%'):
            ui.button(on_click=lambda: self.editPalette.addColor()).props('icon=add').tooltip(text='Add new color (max. 10)')
            ui.button(on_click=lambda: self.editPalette.remove()).props('icon=remove').tooltip(text='Remove first color')
            ui.button(on_click=lambda: self.editPalette.clear()).props('icon=delete').tooltip(text='Clear palette')
        with ui.row().style('margin-top: 5%'):
            ui.button(on_click=lambda: self.editPalette.shiftLeft()).props('icon=arrow_left').tooltip(text='Shift palette one color to left')
            ui.button(on_click=lambda: self.editPalette.shiftRight()).props('icon=arrow_right').tooltip(text='Shift palette one color to right')
            ui.button(on_click=lambda: self.editPalette.shuffleColorPalette()).props('icon=shuffle').tooltip(text='Shuffle color palette')
        ui.separator().style('margin-top: 5%')
        with ui.column():
            secondaryColorCheckbox = ui.checkbox(text='Add secondary color (50% ratio)', on_change=lambda e: self.setSecondaryColor(e.value)).style('margin-top: 5%').tooltip(text='After each color of the palette the secondary color will be added')
            ui.color_input(label='Secondary color', value='#000000', on_change=lambda e: self.setSecondaryColor(True, e.value)).bind_visibility_from(secondaryColorCheckbox, 'value').props('color=black')
        with ui.column():
            colorShadesCheckbox = ui.checkbox(text='Create color shades').style('margin-top: 5%').tooltip(text='Creates 10 shades of a specific color')
            colorInput2 = ui.color_input(label='Color', value='#000000', on_change=None).bind_visibility_from(colorShadesCheckbox, 'value').props('color=black')
            ui.button(on_click=lambda e: self.createShades(colorInput2.value)).props('icon=add').tooltip('Create palette').bind_visibility_from(colorShadesCheckbox, 'value')
        with ui.column():
            colorGradientShadesCheckbox = ui.checkbox(text='Create gradient colors based on multiple input colors (less is more)').style('margin-top: 5%').tooltip(text='Creates 10 gradient shades of given colors (less is more)')
            ui.button(on_click=lambda e: self.createGradientShades()).props('icon=add').tooltip('Create palette').bind_visibility_from(colorGradientShadesCheckbox, 'value')
        with ui.column():
            spectralColorCheckbox = ui.checkbox(text='Create spectral colors (custom bri. & sat.)').style('margin-top: 5%').tooltip(text='Creates 10 spectral colors with specific brightness and saturation')
            colorInput3 = ui.color_input(label='Color', value='#ff0000', on_change=None).bind_visibility_from(spectralColorCheckbox, 'value').props('color=black')
            ui.button(on_click=lambda e: self.createSpectralColors(colorInput3.value)).props('icon=add').tooltip('Create palette').bind_visibility_from(spectralColorCheckbox, 'value')

    def createShades(self, color):
        h, s, l = colorConverter.HEXtoHSL(color)
        self.editPalette.clear(True)
        for l in range(95, 4, -10):
            self.editPalette.addColor(colorConverter.HSLtoHEX(h, s, l), False)
        self.editPalette.update()

    def createGradientShades(self):
        if len(self.editPalette.getColorPalette()) < 2:
            return
        colormap = matplotlib.colors.LinearSegmentedColormap.from_list(None, self.editPalette.getColorPalette())
        palette = []
        for i in range(5, 96, 10):
            palette.append(matplotlib.colors.rgb2hex(colormap(i * 0.01)))
        self.editPalette.loadPalette(palette)

    def createSpectralColors(self, color):
        h, s, l = colorConverter.HEXtoHSL(color)
        self.editPalette.clear(True)
        for h in range(0, 360, 36):
            self.editPalette.addColor(colorConverter.HSLtoHEX(h, s, l), False)
        self.editPalette.update()

    def setSecondaryColor(self, state, color='#000000'):
        if state:
            self.effectFactory.secondaryColor = color
        else:
            self.effectFactory.secondaryColor = None
        self.editPalette.update()

    def getIPFromDevice(self):
        self.device.getIPFromDevice()
        self.ipInput.set_value(self.device.ip)

    async def createAuthToken(self):
        await self.device.createAuthToken()
        self.auth_tokenInput.set_value(self.device.auth_token)

    def connect(self):
        try:
            self.lightController.initialize(self.ipInput.value, self.auth_tokenInput.value)
        except Exception:
            self.notifier.notify(message='Can\'t connect.', type='negative')
        else:
            Settings.setValue("ip", self.ipInput.value)
            Settings.setValue("auth_token", self.auth_tokenInput.value)
            self.notifier.notify(message='Device connected.', type='positive')

    def loadCredentials(self):
        ip = Settings.getValue("ip")
        auth_token = Settings.getValue("auth_token")
        if ip is not None and auth_token is not None:
            self.ipInput.set_value(ip)
            self.auth_tokenInput.set_value(auth_token)
            self.connect()

    async def updateValues(self):
        if self.lightController.isDeviceConnected():
            self.briSlider.slider.set_value(self.lightController.getBrightness())
            self.powerSwitch.set_value(self.lightController.getPower())
        ui.colors(primary=Settings.getValue("accent_color"))
        await self.setColorMode(False)

    @staticmethod
    def setAccentColor(color):
        Settings.setValue("accent_color", color)
        ui.colors(primary=color)

    @staticmethod
    async def setColorMode(toggle=True):
        darkMode = Settings.getValue("dark_mode")
        if toggle:
            darkMode = not darkMode
            Settings.setValue("dark_mode", darkMode)
        if darkMode:
            await ui.run_javascript('''
                Quasar.Dark.set(true);
                tailwind.config.darkMode = "class";
                document.body.classList.add("dark");
            ''', respond=False)
        else:
            await ui.run_javascript('''
                Quasar.Dark.set(false);
                tailwind.config.darkMode = "class"
                document.body.classList.remove("dark");
            ''', respond=False)