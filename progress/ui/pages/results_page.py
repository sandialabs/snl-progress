from progress.ui.forms.results.ui_results import Ui_FilePreviewPage
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QScrollArea, QSizePolicy, QMenu, QTableWidget, QTableWidgetItem, QTreeView, QFileSystemModel, QVBoxLayout, QHeaderView, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtCore import QDir, Signal, QModelIndex
from progress.paths import RESULTS_DIR, HOME_DIR
from pathlib import Path
import pandas as pd
import logging
logger = logging.getLogger(__name__)


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

        # optional: only show dirs + supported files
        self.file_model.setFilter(
            QDir.Filter.AllDirs
            | QDir.Filter.Files
            | QDir.Filter.NoDotAndDotDot
        )
        self.file_model.setNameFilters(["*.csv", "*.pdf", "*.png"])
        self.file_model.setNameFilterDisables(False)
            
        # Hide Size, Type, and Date Modified columns
        self.ui.treeView_files.hideColumn(1)
        self.ui.treeView_files.hideColumn(2)
        self.ui.treeView_files.hideColumn(3)

        self.ui.treeView_files.setDragEnabled(True)
        self.ui.treeView_files.setAcceptDrops(True)
        self.ui.treeView_files.setDropIndicatorShown(True)
        self.ui.treeView_files.header().setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )
        self.ui.page_csv.setStyleSheet("background-color: white;")

        # Build preview widgets inside your stacked widget pages
        self._setup_csv_preview()
        self._setup_pdf_preview()
        self._setup_png_preview()

        # connections 
        self.ui.btn_home_dir.clicked.connect(self._set_file_paths_to_home)
        self.ui.btn_results_dir.clicked.connect(self._set_file_paths_to_result)
        self.ui.btn_clear_search.clicked.connect(
            lambda checked=False: self.ui.lineEdit_path.clear()
        )       
        self.ui.treeView_files.clicked.connect(self._on_file_clicked)

    def _setup_csv_preview(self) -> None:
        self.csv_table = self.ui.tableWidget_csv 
        self.csv_table.setAlternatingRowColors(True)
        self.csv_table.setSortingEnabled(True)

        self.csv_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #d0d0d0;
            }

            QTableWidget::item {
                background-color: white;
                color: black;
            }

            QTableWidget::item:selected {
                background-color: #3874f2;
                color: white;
            }

            QHeaderView::section {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #d0d0d0;
                padding: 4px;
            }
        """)

        self.csv_table.horizontalHeader().setStretchLastSection(True)
        self.csv_table.verticalHeader().setVisible(False)

    def _setup_pdf_preview(self) -> None:
        self.pdf_document = QPdfDocument(self)

        self.pdf_view = QPdfView(self.ui.page_pdf)
        self.pdf_view.setDocument(self.pdf_document)
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)

        layout = self.ui.page_pdf.layout()
        if layout is None:
            layout = QVBoxLayout(self.ui.page_pdf)

        layout.addWidget(self.pdf_view)

    def _setup_png_preview(self) -> None:
        self.png_label = QLabel(self.ui.page_image)
        self.png_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.png_label.setScaledContents(False)

        layout = self.ui.page_image.layout()
        if layout is None:
            layout = QVBoxLayout(self.ui.page_image)

        layout.addWidget(self.png_label)

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

    def _on_file_clicked(self, index: QModelIndex) -> None:
        if not index.isValid():
            return

        file_path_str = self.file_model.filePath(index)
        file_path = Path(file_path_str)

        if not file_path.is_file():
            return

        self.file_selected.emit(file_path_str)
        self._preview_file(file_path)


    def _preview_file(self, file_path: Path) -> None:
        suffix = file_path.suffix.lower()

        if suffix == ".csv":
            self._preview_csv(file_path)
            self.ui.stackedWidget_preview.setCurrentWidget(self.ui.page_csv)

        elif suffix == ".pdf":
            self._preview_pdf(file_path)
            self.ui.stackedWidget_preview.setCurrentWidget(self.ui.page_pdf)

        elif suffix == ".png":
            self._preview_png(file_path)
            self.ui.stackedWidget_preview.setCurrentWidget(self.ui.page_image)

        else:
            print(f"Unsupported file type: {suffix}")

    def _preview_csv(self, file_path: Path) -> None:
        try:
            logger.info(f"Loading CSV file: {file_path}")
            df = pd.read_csv(file_path)

            self.csv_table.setSortingEnabled(False)
            self.csv_table.clear()

            self.csv_table.setRowCount(len(df))
            self.csv_table.setColumnCount(len(df.columns))
            self.csv_table.setHorizontalHeaderLabels([str(col) for col in df.columns])

            for row_idx, row in df.iterrows():
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.csv_table.setItem(row_idx, col_idx, item)

            self.csv_table.resizeColumnsToContents()
            self.csv_table.setSortingEnabled(True)

            logger.info(f"CSV loaded successfully: {file_path}")

        except Exception as exc:
            logger.exception(f"Failed to load CSV file {file_path}: {exc}")

    def _preview_pdf(self, file_path: Path) -> None:
        try:
            self.pdf_document.load(str(file_path))
            self.pdf_view.setZoomMode(QPdfView.ZoomMode.FitInView)

        except Exception as exc:
            print(f"Failed to load PDF file {file_path}: {exc}")

    def _preview_png(self, file_path: Path) -> None:
        try:
            pixmap = QPixmap(str(file_path))

            if pixmap.isNull():
                print(f"Failed to load PNG file: {file_path}")
                return

            self.png_label.setPixmap(pixmap)

        except Exception as exc:
            print(f"Failed to load PNG file {file_path}: {exc}")
