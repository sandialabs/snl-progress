from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Signal
from progress.ui.forms.landing.ui_landing import Ui_LandingPage
from progress.dpi import is_windows

class LandingPage(QWidget):
    getting_started_clicked = Signal()
    documentation_clicked = Signal()


    def __init__(self):
        super().__init__()
        self.ui = Ui_LandingPage()
        self.ui.setupUi(self)
        self._current_theme = "light"

        self._progress_logo_icon = QSvgRenderer(":/logos/Images/logos/progress_bold_s.svg")
        self.ui.label_progress_logo.setAlignment(Qt.AlignCenter)
        font_pt = 18 if is_windows() else 33
        self.ui.label_progress_desc.setStyleSheet(f"font-size: {font_pt}pt;")
        self.ui.frame_2.setMinimumHeight(150)

        self._update_logo()
        self._update_footer_logos()

        self.ui.btn_getting_started.clicked.connect(self._on_getting_started_clicked)
        self.ui.btn_documentation.clicked.connect(self._on_documentation_clicked)

    def set_theme(self, theme: str):
        self._current_theme = theme
        self._update_footer_logos()

    def _update_logo(self):
        label = self.ui.label_progress_logo
        label_size = label.size()

        render_size = label_size
        if render_size.height() < 150:
            render_size.setHeight(150)

        svg_size = self._progress_logo_icon.defaultSize()
        scaled = svg_size.scaled(render_size, Qt.KeepAspectRatio)

        pixmap = QPixmap(render_size)
        pixmap.fill(Qt.transparent)

        x = (render_size.width() - scaled.width()) // 2
        y = (render_size.height() - scaled.height()) // 2
        target_rect = QRectF(x, y, scaled.width(), scaled.height())

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        self._progress_logo_icon.render(painter, target_rect)
        painter.end()

        label.setPixmap(pixmap)

    def update_footer_logos(self):
        self._update_footer_logos()

    def _update_footer_logos(self):
        if self._current_theme == "dark":
            self.ui.label_doe_logo.setPixmap(QPixmap(":/logos/Images/logos/DOE_inverted.png"))
            self.ui.label_snl_logo.setPixmap(QPixmap(":/logos/Images/logos/SNL_logo_inverted.png"))
        else:
            self.ui.label_doe_logo.setPixmap(QPixmap(":/logos/Images/logos/DOE_transparent.png"))
            self.ui.label_snl_logo.setPixmap(QPixmap(":/logos/Images/logos/SNL_logo.png"))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_logo()

    def showEvent(self, event):
        super().showEvent(event)
        self._update_logo()

    def _on_getting_started_clicked(self, checked: bool = False) -> None:
        self.getting_started_clicked.emit()

    def _on_documentation_clicked(self, checked: bool = False) -> None:
        self.documentation_clicked.emit()
