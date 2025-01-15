from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QSizePolicy, QFrame, QVBoxLayout, QHBoxLayout

from PySide6.QtCore import Signal

from progress.App.results.ui.ui_results_viewer import Ui_results_widget
from progress.App.results.drag_widget import FileBrowser, ImageGrid
from progress.paths import get_path
base = get_path()
import os

class results_form(QWidget, Ui_results_widget):
    """Results viewing widget."""
    # Define a custom signal
    change_page = Signal(int)

    def __init__(self, parent=None):
        """Sets up the UI file to show in the application"""
        super(results_form, self).__init__(parent)
        self.setupUi(self)
        self.image_grid1 = ImageGrid()
        self.image_grid2 = ImageGrid()
        self.image_grid3 = ImageGrid()
        self.file_browser = FileBrowser()
        self.verticalLayout.addWidget(self.file_browser)
        self.verticalLayout_2.addWidget(self.image_grid1)
        self.verticalLayout_3.addWidget(self.image_grid2)
        self.verticalLayout_4.addWidget(self.image_grid3)
        self.png_counter = 0
        self.file_min.clicked.connect(self.png_toggle)

    def png_toggle(self):
        if self.png_counter==0:

            self.frame.setMinimumWidth(0)
            self.frame.setMaximumWidth(0)
            self.png_counter = 1
        else:
            
            self.frame.setMinimumWidth(230)
            self.frame.setMaximumWidth(230)
            self.png_counter = 0

    def set_results_path(self):
        try:
            results_folder = os.path.join(base, "Results")
            self.file_browser.setRootPath(results_folder)
        except:
            pass