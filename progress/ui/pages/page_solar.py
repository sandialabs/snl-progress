from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QLabel, QSizePolicy
from progress.ui.forms.solar.ui_solar import Ui_SolarPage
from PySide6.QtCore import Signal, Qt
from progress.mod_solar import Solar
from progress.ui.widgets.worker import WorkerThread, StdoutBuffer
from progress.mod_kmeans import KMeans_Pipeline
from progress.paths import get_path
base_dir = get_path()
import os
from PySide6.QtGui import QPixmap

class solar_form(QWidget, Ui_SolarPage):
    """Solar page widget."""

    page_changer_next = Signal()
    page_changer_previous = Signal()

    def __init__(self, data_handler, parent=None):
        """Sets up the UI file to show in the application"""
        super(solar_form, self).__init__(parent)
        self.setupUi(self)

        self.btn_data_upload.hide()
