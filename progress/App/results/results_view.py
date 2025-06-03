from PySide6.QtWidgets import QWidget
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtCore import Signal, Qt

from progress.App.results.ui.ui_results_viewer import Ui_results_widget
from progress.App.results.drag_widget import FileBrowser, ImageGrid
from progress.paths import get_path
base_dir = get_path()
import os

class results_form(QWidget, Ui_results_widget):
    """Results viewing widget."""
    # Define a custom signal
    # change_page = Signal(int)

    def __init__(self, parent=None):
        """Sets up the UI file to show in the application"""
        super(results_form, self).__init__(parent)
        self.setupUi(self)

        # Initialize widgets 
        self.image_grid = ImageGrid()
        self.file_browser = FileBrowser()
        self.pdf_document = QPdfDocument(self)
        self.pdf_viewer = QPdfView(self)
        self.pdf_viewer.setDocument(self.pdf_document)
        self.pdf_viewer.setVisible(False)
        self.pdf_viewer.setZoomMode(QPdfView.ZoomMode.FitInView)

        # Add widgets to layouts
        self.verticalLayout.addWidget(self.file_browser)
        self.verticalLayout_2.addWidget(self.image_grid)
        self.verticalLayout_2.addWidget(self.pdf_viewer)

        # internal state
        self.png_counter = 0

        # connect signals
        self.file_min.clicked.connect(self.png_toggle)
        self.file_browser.file_selected.connect(self.display_file)

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
            results_folder = os.path.join(base_dir, "Results")
            self.file_browser.setRootPath(results_folder)
        except Exception as e:
            print(f"Failed to set results path: {e}")

    def display_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            self.image_grid.setVisible(False)
            self.pdf_viewer.setVisible(True)
            self.pdf_document.load(file_path)
        elif ext in [".png", ".jpg", ".jpeg", ".bmp"]:
            self.pdf_viewer.setVisible(False)
            self.image_grid.setVisible(True)
            self.image_grid.display_image(file_path)  # you must ensure this method exists in ImageGrid
        else:
            print("Unsupported file type:", ext)