import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QFile, QTextStream, Qt, QSize, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtPdfWidgets import QPdfView
import progress.resources_rc
from progress.tests.ui.ui_main_window import Ui_MainWindow
from progress.tests.ui.ui_solar import Ui_SolarPage
from progress.tests.ui.ui_wind import Ui_WindPage
from progress.tests.ui.ui_solar_results import Ui_SolarResults
from progress.tests.ui.ui_simulation import Ui_SimulationPage 
from progress.tests.ui.ui_landing import Ui_LandingPage
from progress.tests.ui.ui_results import Ui_FilePreviewPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.landing_page = LandingPage()
        self.solar_page = SolarPage()
        self.wind_page = WindPage()
        self.simulation_page = SimulationPage()
        self.results_page = ResultsPage()
        # self.settings_page = SettingsPage()
        # self.about_page = AboutPage()

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_landing)

        self._mount_page(self.ui.page_landing, self.landing_page)
        self._mount_page(self.ui.page_solar, self.solar_page)
        self._mount_page(self.ui.page_wind, self.wind_page)
        self._mount_page(self.ui.page_simulation, self.simulation_page)
        self._mount_page(self.ui.page_results, self.results_page)
        # self._mount_page(self.ui.page_settings, self.settings_page)
        # self._mount_page(self.ui.page_about, self.about_page)

        self.ui.btn_home.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_landing)
        )
        self.ui.btn_solar.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_solar)
        )
        self.ui.btn_wind.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_wind)
        )
        self.ui.btn_simulation.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_simulation)
        )
        self.ui.btn_results.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_results)
        )
        # self.ui.btn_settings.clicked.connect(
        #     lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)
        # )
        # self.ui.btn_about.clicked.connect(
        #     lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_about)
        # )


    def _mount_page(self, container, page_widget) -> None:
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
        layout.addWidget(page_widget)


class SolarPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SolarPage()
        self.results_window = SolarResultsPage()
        self.ui.setupUi(self)

        # self.ui.btn_download_solar.hide()
        # self.ui/btn_download_solar.setVisible(False)
        self.ui.btn_download_solar.setText("Upload Data")

        # UI initialization
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
        self.results_window.show()

class LandingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LandingPage()
        self.ui.setupUi(self)

        self._progress_logo_pixmap = QPixmap(":/logos/Images/logos/progress_transparent_alt.png")
        self.ui.label_progress_logo.setAlignment(Qt.AlignCenter)

class SimulationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SimulationPage()
        self.ui.setupUi(self)

class SolarResultsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SolarResults()
        self.ui.setupUi(self)

class WindPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindPage()
        self.ui.setupUi(self)

        self.ui.btn_process_wind.setVisible(False)
        self.ui.btn_download_wind.clicked.connect(self._display_process_data_btn)

    def _display_process_data_btn(self) -> None:
        self.ui.btn_process_wind.setVisible(True)


class SimulationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SimulationPage()
        self.ui.setupUi(self)


class ResultsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FilePreviewPage()
        self.ui.setupUi(self)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
