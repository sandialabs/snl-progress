from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class settings_form(QWidget):
    def __init__(self, parent=None):
        super(settings_form, self).__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Settings")
        layout.addWidget(label)
