from PySide6.QtWidgets import QWidget
from progress.App.landing.ui.ui_landing import Ui_land
from PySide6.QtCore import Signal
class land_form(QWidget, Ui_land):
    """Landing page widget."""

    page_changer = Signal()
    def __init__(self, parent=None):
        """Sets up the UI file to show in the application"""
        super(land_form, self).__init__(parent)
        self.setupUi(self)
        self.get_started_button.clicked.connect(self.on_get_started_clicked)

    def on_get_started_clicked(self):
        self.page_changer.emit()