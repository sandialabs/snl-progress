from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QSettings
from progress.ui.forms.settings.ui_settings import Ui_SettingsPage

THEME_MAP = {0: "light", 1: "dark"}

class SettingsPage(QWidget):
    def __init__(self, theme_switch_callback=None):
        super().__init__()
        self.ui = Ui_SettingsPage()
        self.ui.setupUi(self)
        self._theme_switch_callback = theme_switch_callback
        self._updating = False

        self.settings = QSettings("QuESt", "snl-progress")
        self.ui.comboBox_theme.currentIndexChanged.connect(self._on_theme_changed)

    def sync_from_settings(self):
        theme = self.settings.value("theme", "light")
        idx = 0 if theme == "light" else 1
        self._updating = True
        self.ui.comboBox_theme.setCurrentIndex(idx)
        self._updating = False

    def _on_theme_changed(self, index):
        if self._updating:
            return
        theme = THEME_MAP.get(index, "light")
        self.settings.setValue("theme", theme)
        if self._theme_switch_callback:
            self._theme_switch_callback(theme)

