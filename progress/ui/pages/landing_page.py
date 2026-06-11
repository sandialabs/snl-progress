from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from progress.ui.forms.landing.ui_landing import Ui_LandingPage
from PySide6.QtCore import Signal

class LandingPage(QWidget):
    getting_started_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_LandingPage()
        self.ui.setupUi(self)

        self._progress_logo_pixmap = QPixmap(":/logos/Images/logos/progress_transparent_alt.png")
        self.ui.label_progress_logo.setAlignment(Qt.AlignCenter)

        self.ui.btn_getting_started.clicked.connect(self._on_getting_started_clicked)

    def _on_getting_started_clicked(self, checked: bool = False) -> None:
        self.getting_started_clicked.emit()
