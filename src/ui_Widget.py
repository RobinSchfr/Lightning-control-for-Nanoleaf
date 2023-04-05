class Ui_Widget:
    def __init__(self, childWidgets):
        self.childWidgets = childWidgets

    def setVisibility(self, visible=True):
        for widget in self.childWidgets:
            widget.set_visibility(visible)