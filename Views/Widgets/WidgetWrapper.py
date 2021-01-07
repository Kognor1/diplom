from PyQt5.QtWidgets import QWidget


class WidgetWrapper(QWidget):
    def __init__(self, hbox):
        super().__init__()
        self.setLayout(hbox)

