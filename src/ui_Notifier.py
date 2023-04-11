from nicegui import ui


class Notifier:
    @staticmethod
    def notify(message, type=None):
        ui.notify(message=message, type=type)