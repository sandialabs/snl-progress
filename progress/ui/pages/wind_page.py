from PySide6.QtWidgets import QWidget, QVBoxLayout
from progress.ui.forms.wind.ui_wind import Ui_WindPage

class WindPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindPage()
        self.ui.setupUi(self)

        self.ui.btn_process_wind.setVisible(False)
        self.ui.btn_download_wind.clicked.connect(self._display_process_data_btn)

    def _display_process_data_btn(self) -> None:
        self.ui.btn_process_wind.setVisible(True)


