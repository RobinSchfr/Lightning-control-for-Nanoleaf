from nicegui import ui


class Ui_DeviceInitializerDialog:

    @staticmethod
    async def show():
        with ui.dialog() as dialog, ui.card():
            ui.label(text='The power button on the device should be held for 5-7 seconds, then you need to press "Create token" within 30 seconds.')
            ui.button(text='Create token', on_click=lambda: dialog.submit(True))
        await dialog