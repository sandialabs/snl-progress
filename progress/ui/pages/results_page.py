from PySide6.QtWidgets import QWidget, QVBoxLayout
from progress.ui.forms.results.ui_results import Ui_FilePreviewPage


class ResultsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FilePreviewPage()
        self.ui.setupUi(self)
