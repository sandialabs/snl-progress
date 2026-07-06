from progress.ui.forms.results.ui_results import Ui_FilePreviewPage
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QScrollArea, QSizePolicy, QMenu, QTableWidget, QTableWidgetItem,
    QTreeView, QFileSystemModel, QVBoxLayout, QHeaderView, QSizePolicy,
    QPlainTextEdit, QComboBox)
from PySide6.QtGui import QPixmap
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtCore import Qt, QDir, Signal, QModelIndex, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
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
        self.file_model.setNameFilters(["*.csv", "*.pdf", "*.png", "*.txt", "*.xlsx", "*.html", "*.json"])
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
            QHeaderView.ResizeMode.Stretch
        )
        # self.ui.page_csv.setStyleSheet("background-color: white;")

        # Build preview widgets inside your stacked widget pages
        self._setup_csv_preview()
        self._setup_pdf_preview()
        self._setup_png_preview()
        self._setup_txt_preview()
        self._setup_xlsx_preview()
        self._setup_html_preview()

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

        # Table styling handled via theme.qss

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
        self.ui.scrollArea_image.setVisible(False)
        self.ui.label_image_title.setVisible(False)
        self.ui.verticalLayout_image.setContentsMargins(0, 0, 0, 0)
        self.ui.verticalLayout_image.setSpacing(0)
        self.png_label = QLabel(self.ui.page_image)
        self.png_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.png_label.setScaledContents(False)
        self.png_label.setMinimumSize(400, 300)
        layout = self.ui.page_image.layout()
        if layout is None:
            layout = QVBoxLayout(self.ui.page_image)
        layout.addWidget(self.png_label)

    def _setup_txt_preview(self) -> None:
        self.page_txt = QWidget()
        self.ui.stackedWidget_preview.addWidget(self.page_txt)

        self.txt_edit = QPlainTextEdit(self.page_txt)
        self.txt_edit.setReadOnly(True)
        self.txt_edit.setStyleSheet("background-color: white; color: black; font-family: monospace;")

        layout = QVBoxLayout(self.page_txt)
        layout.addWidget(self.txt_edit)

    def _setup_xlsx_preview(self) -> None:
        self.xlsx_table = self.ui.tableWidget_xslx
        self.xlsx_table.setAlternatingRowColors(True)
        self.xlsx_table.setSortingEnabled(True)
        self.xlsx_table.horizontalHeader().setStretchLastSection(True)
        self.xlsx_table.verticalHeader().setVisible(False)

        self.xlsx_sheet_combo = QComboBox()
        self.xlsx_sheet_combo.setMaximumHeight(30)
        self.xlsx_sheet_combo.setVisible(False)
        idx = self.ui.verticalLayout.indexOf(self.xlsx_table)
        self.ui.verticalLayout.insertWidget(idx, self.xlsx_sheet_combo)
        self.xlsx_sheet_combo.currentTextChanged.connect(self._on_xlsx_sheet_changed)

        self._xlsx_sheets = {}

    def _setup_html_preview(self) -> None:
        self.page_html = QWidget()
        self.ui.stackedWidget_preview.addWidget(self.page_html)

        self.label_html_title = QLabel("Plotly Preview")
        self.label_html_title.setStyleSheet("font-size: 14px; font-weight: bold; padding: 8px;")
        self.label_html_title.setVisible(False)

        self.html_view = QWebEngineView(self.page_html)

        layout = QVBoxLayout(self.page_html)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.label_html_title)
        layout.addWidget(self.html_view)

    def _preview_txt(self, file_path: Path) -> None:
        try:
            text = file_path.read_text(encoding="utf-8")
            self.txt_edit.setPlainText(text)
            logger.info(f"Text file loaded: {file_path}")
        except Exception as exc:
            logger.exception(f"Failed to load text file {file_path}: {exc}")

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

        elif suffix in (".txt", ".json"):
            self._preview_txt(file_path)
            self.ui.stackedWidget_preview.setCurrentWidget(self.page_txt)

        elif suffix == ".xlsx":
            self._preview_xlsx(file_path)
            self.ui.stackedWidget_preview.setCurrentWidget(self.ui.page_xlsx)

        elif suffix == ".html":
            self._preview_html(file_path)
            self.ui.stackedWidget_preview.setCurrentWidget(self.page_html)

        else:
            print(f"Unsupported file type: {suffix}")

    def _on_xlsx_sheet_changed(self, sheet_name: str) -> None:
        if sheet_name in self._xlsx_sheets:
            self._populate_xlsx_table(self._xlsx_sheets[sheet_name])

    def _populate_xlsx_table(self, df: pd.DataFrame) -> None:
        self.xlsx_table.setSortingEnabled(False)
        self.xlsx_table.clear()
        self.xlsx_table.setRowCount(len(df))
        self.xlsx_table.setColumnCount(len(df.columns))
        self.xlsx_table.setHorizontalHeaderLabels([str(col) for col in df.columns])
        for row_idx, (_, row) in enumerate(df.iterrows()):
            for col_idx, value in enumerate(row):
                self.xlsx_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        self.xlsx_table.resizeColumnsToContents()
        self.xlsx_table.setSortingEnabled(True)

    def _preview_xlsx(self, file_path: Path) -> None:
        try:
            logger.info(f"Loading XLSX file: {file_path}")
            xls = pd.ExcelFile(file_path, engine="openpyxl")
            self._xlsx_sheets = {name: xls.parse(name) for name in xls.sheet_names}

            self.xlsx_sheet_combo.blockSignals(True)
            self.xlsx_sheet_combo.clear()
            self.xlsx_sheet_combo.addItems(xls.sheet_names)
            self.xlsx_sheet_combo.setVisible(len(xls.sheet_names) > 1)
            self.xlsx_sheet_combo.blockSignals(False)

            self._populate_xlsx_table(self._xlsx_sheets[xls.sheet_names[0]])
            logger.info(f"XLSX loaded successfully: {file_path}")

        except Exception as exc:
            logger.exception(f"Failed to load XLSX file {file_path}: {exc}")

    def _preview_csv(self, file_path: Path) -> None:
        try:
            logger.info(f"Loading CSV file: {file_path}")
            df = pd.read_csv(file_path)

            self.csv_table.setSortingEnabled(False)
            self.csv_table.clear()

            self.csv_table.setRowCount(len(df))
            self.csv_table.setColumnCount(len(df.columns))
            self.csv_table.setHorizontalHeaderLabels([str(col) for col in df.columns])

            for row_idx, (_, row) in enumerate(df.iterrows()):
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

            scaled = pixmap.scaled(
                self.png_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.png_label.setPixmap(scaled)

        except Exception as exc:
            print(f"Failed to load PNG file {file_path}: {exc}")

    def _preview_html(self, file_path: Path) -> None:
        try:
            self.html_view.load(QUrl.fromLocalFile(str(file_path)))
        except Exception as exc:
            print(f"Failed to load HTML file {file_path}: {exc}")
