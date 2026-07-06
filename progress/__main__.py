from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QSizePolicy, QPushButton
from PySide6.QtCore import QFile, QTextStream, Qt, QSize, QTimer
from PySide6.QtGui import QPixmap
from progress.ui.forms.main_window.ui_main_window import Ui_MainWindow
from progress.ui.pages.landing_page import LandingPage
from progress.ui.pages.solar_page import SolarPage
from progress.ui.pages.wind_page import WindPage
from progress.ui.pages.simulation_page import SimulationPage
from progress.ui.pages.results_page import ResultsPage
from progress.ui.pages.about_page import AboutPage
from progress.mod_sysdata import RASystemData
from progress.ui.utils.data_handler import DataHandler
from progress.mod_utilities import RAUtilities
from progress.ui.pages.log_window import LogWindow, get_log_window
from progress.paths import get_path
from progress.paths import BASE_DIR, DATA_DIR, SOLAR_DIR, SYSTEM_DIR, WIND_DIR, update_data_path, check_era_api_key_existence
import progress.resources_rc
import logging
import sys
import os

root = logging.getLogger()
for h in list(root.handlers):
    root.removeHandler(h)

os.makedirs(get_path() / "logs", exist_ok=True)
fh = logging.FileHandler(str(get_path() / "logs" / "progress_debug.log"))
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s"))
root.addHandler(fh)

ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
root.addHandler(ch)

root.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.frame_content.setMaximumHeight(16777215)
        self.ui.stackedWidget.setSizePolicy(
            self.ui.stackedWidget.sizePolicy().horizontalPolicy(),
            QSizePolicy.Ignored,
        )
        logger.info("Main window initialized")
        # Install app logger once the UI exists.
        # After this, logging and print output go to self.ui.log_window.
        # logs from the other pages get captured.
        self.data = DataHandler()
        self.sys_directory = str(SYSTEM_DIR)
        self.load_sys_data()

        self.landing_page = LandingPage()
        self.solar_page = SolarPage(data_handler=self.data)
        self.wind_page = WindPage(data_handler=self.data)
        self.simulation_page = SimulationPage()
        self.results_page = ResultsPage()
        self.about_page = AboutPage()
        # self.settings_page = SettingsPage()

        self._page_sequence = [
            self.ui.page_solar,
            self.ui.page_wind,
            self.ui.page_simulation,
            self.ui.page_results,
        ]

        # ERA5 API KEY CHECK
        api_key_exists = check_era_api_key_existence()
        if not api_key_exists:
            QMessageBox.critical(self, "ERA5 API KEY ISSUE", "Please check README instructions to get ERA5 API KEY")
            logging.error(f"api key DOESNT EXIST: {api_key_exists}")
        else:
            logging.info(f"api key exists: {api_key_exists}")

        self._mount_page(self.ui.page_landing, self.landing_page)
        self._mount_page(self.ui.page_solar, self.solar_page)
        self._mount_page(self.ui.page_wind, self.wind_page)
        self._mount_page(self.ui.page_simulation, self.simulation_page)
        self._mount_page(self.ui.page_results, self.results_page)
        self._mount_page(self.ui.page_about, self.about_page)
        # self._mount_page(self.ui.page_settings, self.settings_page)

        # signals and connections
        self.landing_page.getting_started_clicked.connect(self._handle_landing_getting_started)
        self.landing_page.documentation_clicked.connect(          
            lambda: self._go_to_page(self.ui.page_about)
        )
        self.solar_page.clusters_skipped.connect(
            lambda: self._go_to_page(self.ui.page_wind)
        )
        self.solar_page.clusters_generated.connect(
            lambda: self._update_navigation_ui(self.ui.stackedWidget.currentIndex())
        )
        self.solar_page.clusters_skipped.connect(
            lambda: self._update_navigation_ui(self.ui.stackedWidget.currentIndex())
        )
        self.wind_page.wind_ready.connect(
            lambda: self._update_navigation_ui(self.ui.stackedWidget.currentIndex())
        )
        self.ui.btn_prev.clicked.connect(self._go_previous_page)
        self.ui.btn_next.clicked.connect(self._go_next_page)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_landing)
        self.ui.stackedWidget.currentChanged.connect(self._update_navigation_ui)
        self._update_navigation_ui(self.ui.stackedWidget.currentIndex())

        self.ui.btn_home.clicked.connect(
            lambda checked=False: self._go_to_page(self.ui.page_landing)
        )
        self.ui.btn_solar.clicked.connect(
            lambda checked=False: self._go_to_page(self.ui.page_solar)
        )
        self.ui.btn_wind.clicked.connect(
            lambda checked=False: self._go_to_page(self.ui.page_wind)
        )
        self.ui.btn_simulation.clicked.connect(
            lambda checked=False: self._go_to_page(self.ui.page_simulation)
        )
        self.ui.btn_results.clicked.connect(
            lambda checked=False: self._go_to_page(self.ui.page_results)
        )

        self.ui.btn_about.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_about)
        )

        # Add Log Viewer button to sidebar
        self.ui.btn_log = QPushButton("Log Viewer", self.ui.frame_ribbon)
        self.ui.btn_log.setObjectName("btn_log")
        idx = self.ui.sidebarLayout.indexOf(self.ui.btn_about)
        self.ui.sidebarLayout.insertWidget(idx, self.ui.btn_log)

        # load theme (auto-detect system dark mode)
        self.load_stylesheet(self._detect_theme())

    def _mount_page(self, container, page_widget) -> None:
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
        layout.addWidget(page_widget)

    def _go_to_page(self, page) -> None:
        self.ui.stackedWidget.setCurrentWidget(page)

        # NAV LOGIC
    def _go_previous_page(self, checked: bool = False) -> None:
        current_page = self.ui.stackedWidget.currentWidget()
        if current_page in self._page_sequence:
            index = self._page_sequence.index(current_page)
            if index > 0:
                self.ui.stackedWidget.setCurrentWidget(self._page_sequence[index - 1])

    def _go_next_page(self, checked: bool = False) -> None:
        current_page = self.ui.stackedWidget.currentWidget()
        if current_page in self._page_sequence:
            index = self._page_sequence.index(current_page)
            if index < len(self._page_sequence) - 1:
                if current_page is self.ui.page_solar and not self.solar_page.is_ready_for_simulation():
                    QMessageBox.information(
                        self, "Clusters Required",
                        "Please generate or skip clustering before proceeding to the next step."
                    )
                    return
                if current_page is self.ui.page_wind and not self.wind_page.is_ready_for_simulation():
                    QMessageBox.information(
                        self, "Wind Data Required",
                        "Please process wind data to generate t_rate.xlsx before proceeding to simulation."
                    )
                    return
                self.ui.stackedWidget.setCurrentWidget(self._page_sequence[index + 1])

    def _update_navigation_ui(self, _index: int) -> None:
        current_page = self.ui.stackedWidget.currentWidget()
        on_landing = current_page is self.ui.page_landing

        self.ui.btn_prev.setVisible(not on_landing)
        self.ui.btn_next.setVisible(not on_landing)

        if on_landing:
            self.ui.btn_prev.setEnabled(False)
            self.ui.btn_next.setEnabled(False)
            return

        if current_page in self._page_sequence:
            seq_index = self._page_sequence.index(current_page)
            self.ui.btn_prev.setEnabled(seq_index > 0)
            can_next = seq_index < len(self._page_sequence) - 1
            if can_next:
                if current_page is self.ui.page_solar:
                    can_next = self.solar_page.is_ready_for_simulation()
                elif current_page is self.ui.page_wind:
                    can_next = self.wind_page.is_ready_for_simulation()
            self.ui.btn_next.setEnabled(can_next)
        else:
            self.ui.btn_prev.setEnabled(False)
            self.ui.btn_next.setEnabled(False)

    def _handle_landing_getting_started(self) -> None:
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_solar)

    def load_sys_data(self):
        try:
            rasd = RASystemData('single_period', 'Zonal')
            data_gen = self.sys_directory + '/gen.csv'
            data_branch = self.sys_directory + '/branch.csv'
            data_bus = self.sys_directory + '/bus.csv'
            data_load = self.sys_directory + '/load.csv'
            data_storage = self.sys_directory + '/storage.csv'

            genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost, genname = rasd.gen(data_gen)
            nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans, branchname = rasd.branch(data_branch, data_bus)
            bus_name, bus_no, nz = rasd.bus(data_bus)
            load_all_regions = rasd.load(bus_name, bus_no, data_load) 
            essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units, ess_chemistry = rasd.storage(data_storage)

            raut = RAUtilities()
            mu_tot, lambda_tot = raut.reltrates(
                MTTF_gen,
                MTTF_trans,
                MTTR_gen,
                MTTR_trans,
                MTTF_ess,
                MTTR_ess,
            )
            cap_max, cap_min = raut.capacities(
                nl,
                pmax,
                pmin,
                ess_pmax,
                ess_pmin,
                cap_trans,
            )

            # Set data in DataHandler
            self.data.genbus = genbus
            self.data.ng = ng
            self.data.pmax = pmax
            self.data.pmin = pmin
            self.data.FOR_gen = FOR_gen
            self.data.MTTF_gen = MTTF_gen
            self.data.MTTR_gen = MTTR_gen
            self.data.gencost = gencost
            self.data.nl = nl
            self.data.fb = fb
            self.data.tb = tb
            self.data.cap_trans = cap_trans
            self.data.MTTF_trans = MTTF_trans
            self.data.MTTR_trans = MTTR_trans
            self.data.bus_name = bus_name
            self.data.bus_no = bus_no
            self.data.nz = nz
            self.data.load_all_regions = load_all_regions
            self.data.essname = essname
            self.data.essbus = essbus
            self.data.ness = ness
            self.data.ess_pmax = ess_pmax
            self.data.ess_pmin = ess_pmin
            self.data.ess_duration = ess_duration
            self.data.ess_socmax = ess_socmax
            self.data.ess_socmin = ess_socmin
            self.data.ess_eff = ess_eff
            self.data.disch_cost = disch_cost
            self.data.ch_cost = ch_cost
            self.data.MTTF_ess = MTTF_ess
            self.data.MTTR_ess = MTTR_ess
            self.data.ess_units = ess_units
            self.data.mu_tot = mu_tot
            self.data.lambda_tot = lambda_tot
            self.data.cap_max = cap_max
            self.data.cap_min = cap_min
            self.data.raut = raut
            logger.info("System data loaded successfully")

        except Exception:
            logger.exception("Error loading system CSV data")

    @staticmethod
    def _detect_theme() -> str:
        try:
            scheme = QApplication.styleHints().colorScheme()
            if scheme == Qt.ColorScheme.Dark:
                return str(BASE_DIR / "resources" / "theme_dark.qss")
        except AttributeError:
            pass
        bg = QApplication.palette().window().color()
        if bg.lightness() < 128:
            return str(BASE_DIR / "resources" / "theme_dark.qss")
        return str(BASE_DIR / "resources" / "theme.qss")

    def load_stylesheet(self, filename):
        """Load a QSS stylesheet from a file."""
        file = QFile(filename)
        if file.open(QFile.ReadOnly):
            stylesheet = file.readAll().data().decode()
            self.setStyleSheet(stylesheet)
            file.close()


class AppController:
    """Manages and displays both windows simultaneously."""
    def __init__(self):
        # Storing them as attributes keeps them alive in memory
        self.log_window = LogWindow()
        self.main_window = MainWindow()
        self.main_window.ui.btn_log.clicked.connect(self._toggle_log_window)

    def _toggle_log_window(self):
        if self.log_window.isVisible():
            self.log_window.hide()
        else:
            self.log_window.show()
            self.log_window.raise_()
            self.log_window.activateWindow()

    def show_all(self):
        # Enable log window capture so all subsequent output goes to the GUI log.
        # Startup output (imports, init) still printed to terminal.
        # keep this code when you add log window
        log_controller = get_log_window()
        if log_controller is not None:
            log_controller.enable_capture()

        # Call .show() on both instances to display them together
        screen = QApplication.primaryScreen()
        available = screen.availableGeometry()

        screen_x = available.x()
        screen_y = available.y()
        screen_w = available.width()
        screen_h = available.height()

        gap = 20

        main_w = int(screen_w * 0.65)
        log_w = screen_w - main_w - gap
        height = int(screen_h * 0.9)

        self.main_window.setGeometry(
            screen_x,
            screen_y,
            main_w,
            height,
        )

        self.log_window.setGeometry(
            screen_x + main_w + gap,
            screen_y,
            log_w,
            height,
        )

        self.main_window.show()
        self.log_window.show()

def main():
    """
    The main entry point for the application.
    Initializes the QApplication, creates and shows the main window, and starts the event loop.
    """
    app = QApplication(sys.argv)
    window = AppController()
    update_data_path()
    window.show_all()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
