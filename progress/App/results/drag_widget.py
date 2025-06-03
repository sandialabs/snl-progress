import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QScrollArea, QSizePolicy, QMenu, QTableWidget, QTableWidgetItem, QTreeView, QFileSystemModel
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QMouseEvent, QCursor, QAction
from PySide6.QtCore import Qt, QUrl, QPoint, QMimeData, Signal, QModelIndex
import csv

class DraggableResizableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFixedSize(500, 300)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.content_widget = None

        self.setMouseTracking(True)
        self.resizing = False
        self.dragging = False
        self.offset = None

    def set_content(self, content_widget):
        if self.content_widget:
            self.content_widget.setParent(None)
        self.content_widget = content_widget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.content_widget)
        self.setLayout(layout)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if self.is_in_resize_area(event.position().toPoint()):
                self.resizing = True
                self.offset = event.position().toPoint()
            else:
                self.dragging = True
                self.offset = event.position().toPoint()
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.resizing:
            new_width = max(event.position().toPoint().x(), 10)  # Ensure minimum width
            new_height = max(event.position().toPoint().y(), 10)  # Ensure minimum height
            self.setFixedSize(new_width, new_height)
            if self.content_widget:
                self.content_widget.setFixedSize(new_width, new_height)
        elif self.dragging:
            self.move(self.mapToParent(event.position().toPoint() - self.offset))
        else:
            if self.is_in_resize_area(event.position().toPoint()):
                self.setCursor(QCursor(Qt.SizeFDiagCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.resizing = False
        self.dragging = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def is_in_resize_area(self, pos):
        return pos.x() > self.width() - 10 and pos.y() > self.height() - 10

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.delete_widget)
        context_menu.addAction(delete_action)
        context_menu.exec(position)

    def delete_widget(self):
        self.deleteLater()

class ImageGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.scrollArea = QScrollArea(self)
        #self.scrollArea.setStyleSheet("border: 2px;")
        self.scrollArea.setFrameShape(QScrollArea.NoFrame)
        self.scrollArea.setViewportMargins(0, 0, 0, 0)
        self.containerWidget = QWidget()

        #self.containerWidget.setStyleSheet("border: 1px solid rgb(60, 60, 60); border-radius: 5px; padding: 5px; background-color: rgb(40, 40, 40); color: rgb(200, 200, 200);")
        self.scrollArea.setWidget(self.containerWidget)
        self.scrollArea.setWidgetResizable(True)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.scrollArea)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        position = event.position().toPoint()
        widget_position = self.containerWidget.mapFrom(self, position)

        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(('.png', '.jpeg', '.jpg', '.svg')):
                self.add_image(file_path, widget_position)
            elif file_path.endswith('.csv'):
                self.add_csv(file_path, widget_position)

    def add_image(self, file_path, position):
        pixmap = QPixmap(file_path)
        label = QLabel()
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        widget = DraggableResizableWidget(self.containerWidget)
        widget.set_content(label)
        widget.move(position)
        widget.show()

    def add_csv(self, file_path, position):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        table_widget = QTableWidget()
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]) if data else 0)
        for row_idx, row in enumerate(data):
            for col_idx, cell in enumerate(row):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(cell))

        table_widget.horizontalHeader().setVisible(False)
        table_widget.verticalHeader().setVisible(False)
        #table_widget.setHorizontalScrollMode(QTableWidget.ScrollPerpixel)
        #table_widget.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_widget.setMinimumSize(200, 200)
        table_widget.setStyleSheet("""
        QTableWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            gridline-color: #444444;
            border: 3px solid #444444;
        }

        QTableWidget::item {
            background-color: #2b2b2b;
            color: #ffffff;
        }

        QTableWidget::item:selected {
            background-color: #3d3d3d;
            color: #ffffff;
        }

        QHeaderView::section {
            background-color: #3d3d3d;
            color: #ffffff;
            border: 1px solid #444444;
        }

        QTableCornerButton::section {
            background-color: #3d3d3d;
            border: 1px solid #444444;
        }

        # QScrollBar:vertical {
        #     border: 1px solid #444444;
        #     background: #2b2b2b;
        #     width: 15px;
        #     margin: 22px 0 22px 0;
        # }

        # QScrollBar::handle:vertical {
        #     background: #3d3d3d;
        #     min-height: 20px;
        # }

        # QScrollBar::add-line:vertical {
        #     border: 1px solid #444444;
        #     background: #3d3d3d;
        #     height: 20px;
        #     subcontrol-position: bottom;
        #     subcontrol-origin: margin;
        # }

        # QScrollBar::sub-line:vertical {
        #     border: 1px solid #444444;
        #     background: #3d3d3d;
        #     height: 20px;
        #     subcontrol-position: top;
        #     subcontrol-origin: margin;
        # }

        # QScrollBar:horizontal {
        #     border: 1px solid #444444;
        #     background: #2b2b2b;
        #     height: 15px;
        #     margin: 0 22px 0 22px;
        # }

        # QScrollBar::handle:horizontal {
        #     background: #3d3d3d;
        #     min-width: 20px;
        # }

        # QScrollBar::add-line:horizontal {
        #     border: 1px solid #444444;
        #     background: #3d3d3d;
        #     width: 20px;
        #     subcontrol-position: right;
        #     subcontrol-origin: margin;
        # }

        # QScrollBar::sub-line:horizontal {
        #     border: 1px solid #444444;
        #     background: #3d3d3d;
        #     width: 20px;
        #     subcontrol-position: left;
        #     subcontrol-origin: margin;
        # }
        """)

        widget = DraggableResizableWidget(self.containerWidget)
        widget.set_content(table_widget)
        widget.move(position)
        widget.show()

class FileBrowser(QTreeView):

    file_selected = Signal(str)

    def __init__(self):
        super().__init__()

        # Setup file system model
        self.model = QFileSystemModel()
        self.model.setRootPath('')  # Accept all roots
        self.setModel(self.model)

        # View configuration (applied to 'self')
        self.setRootIndex(self.model.index(os.path.expanduser("~")))
        self.setAnimated(True)
        self.setSortingEnabled(True)

        # connect click signal
        self.clicked.connect(self.on_file_clicked)

        # Enable drag-and-drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)

    def setRootPath(self, path):
        self.model.setRootPath(path)
        self.setRootIndex(self.model.index(path))

    def mimeData(self, indexes):
        mime_data = QMimeData()
        file_paths = [self.model.filePath(index) for index in indexes]
        mime_data.setUrls([QUrl.fromLocalFile(path) for path in file_paths])
        return mime_data
    
    def on_file_clicked(self, index: QModelIndex):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            self.file_selected.emit(file_path) 


# class WebEngineView(QWebEngineView):
#     def __init__(self):
#         super().__init__()
#         self.setAcceptDrops(True)

#     def dragEnterEvent(self, event):
#         if event.mimeData().hasUrls():
#             event.acceptProposedAction()

#     def dragMoveEvent(self, event):
#         if event.mimeData().hasUrls():
#             event.acceptProposedAction()

#     def dropEvent(self, event):
#         if event.mimeData().hasUrls():
#             for url in event.mimeData().urls():
#                 if url.isLocalFile() and url.toLocalFile().endswith('.html'):
#                     self.load_html_with_js(url.toLocalFile())
#                     break

#     def load_html_with_js(self, file_path):
#         with open(file_path, 'r') as file:
#             html_content = file.read()

#         # Inject the necessary JavaScript libraries
#         injected_html = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <title>Generated HTML</title>
#             <meta charset="utf-8" />
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
#         </head>
#         <body>
#             {html_content}
#             <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
#         </body>
#         </html>
#         """

#         self.setHtml(injected_html)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Draggable and Resizable Widgets")
        self.setGeometry(100, 100, 800, 600)
        self.imageGrid = ImageGrid()
        self.setCentralWidget(self.imageGrid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
