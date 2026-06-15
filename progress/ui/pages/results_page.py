from progress.ui.forms.results.ui_results import Ui_FilePreviewPage
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QScrollArea, QSizePolicy, QMenu, QTableWidget, QTableWidgetItem, QTreeView, QFileSystemModel, QVBoxLayout, QHeaderView, QSizePolicy
from PySide6.QtCore import QDir, Signal, QModelIndex
from progress.paths import RESULTS_DIR, HOME_DIR
from pathlib import Path


class ResultsPage(QWidget):
    file_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_FilePreviewPage()
        self.ui.setupUi(self)

        self.file_model = QFileSystemModel(self)
        self.file_model.setRootPath(str(RESULTS_DIR))
        self.ui.treeView_files.setModel(self.file_model)
        root_index = self.file_model.index(str(RESULTS_DIR))
        self.ui.treeView_files.setRootIndex(root_index)
            
        # Hide Size, Type, and Date Modified columns
        self.ui.treeView_files.hideColumn(1)
        self.ui.treeView_files.hideColumn(2)
        self.ui.treeView_files.hideColumn(3)

        # Let the filename column use available horizontal space
        self.ui.treeView_files.header().setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        # connections 
        self.ui.btn_home_dir.clicked.connect(self._set_file_paths_to_home)
        self.ui.btn_results_dir.clicked.connect(self._set_file_paths_to_result)
        self.ui.btn_clear_search.clicked.connect(
            lambda checked=False: self.ui.lineEdit_path.clear()
        )       

    def _set_file_paths_to_home(self) -> None:
        home_path = str(HOME_DIR)
        self.file_model.setRootPath(home_path)
        root_index = self.file_model.index(home_path)
        self.ui.treeView_files.setRootIndex(root_index)

    def _set_file_paths_to_result(self) -> None:
        results_path = str(RESULTS_DIR)
        self.file_model.setRootPath(results_path)
        root_index = self.file_model.index(results_path)
        self.ui.treeView_files.setRootIndex(root_index)

    def _on_file_clicked(self, index: QModelIndex):
        if not index.isValid():
            return

        file_path_str = self.file_model.filePath(index)
        file_path = Path(file_path_str)

        if file_path.is_file():
            self.file_selected.emit(file_path_str)
