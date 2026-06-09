import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import QFile, QTextStream
from PySide6.QtPdfWidgets import QPdfView
import progress.resources_rc
from progress.tests.ui.ui_solar import Ui_SolarPage
from progress.tests.ui.ui_wind import Ui_WindPage

class SolarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SolarPage()
        self.ui.setupUi(self)

        # self.ui.btn_download_solar.hide()
        self.ui.btn_download_solar.setText("Upload Data")

        # Initialize at 0 to display the special value text
        self.ui.spin_box_num_cluster.setValue(0)
        self.ui.solarStackedWidget.setCurrentIndex(0)
        self.ui.btn_next_page_data.clicked.connect(self._switch_to_cluster_page)
        self.ui.btn_prev_page_data.clicked.connect(self._switch_to_data_page)
        self.ui.btn_prev_page_cluster.clicked.connect(self._switch_to_data_page)
        self.ui.btn_next_page_cluster.clicked.connect(self._switch_to_data_page)
        self.ui.btn_eval_cluster.clicked.connect(self._open_cluster_results)


    def _switch_to_cluster_page(self) -> None:
        self.ui.solarStackedWidget.setCurrentIndex(1)

    def _switch_to_data_page(self) -> None:
        self.ui.solarStackedWidget.setCurrentIndex(0)

    def _open_cluster_results(self) -> None:
        pass




class WindWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindPage()
        self.ui.setupUi(self)

class AppController:
    """Manages and displays both windows simultaneously."""
    def __init__(self):
        # Storing them as attributes keeps them alive in memory
        self.window_one = SolarWindow()
        self.window_two = WindWindow()

    def show_all(self):
        # Call .show() on both instances to display them together
        self.window_one.show()
        self.window_two.show()



app = QApplication(sys.argv)
# Initialize the controller and open the windows
controller = AppController()
controller.show_all()

sys.exit(app.exec())
