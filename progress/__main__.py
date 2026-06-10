from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QFile, QTextStream, Qt, QSize, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtPdfWidgets import QPdfView
from progress.ui.forms.main_window.ui_main_window import Ui_MainWindow
from progress.ui.pages.landing_page import LandingPage
from progress.ui.pages.solar_page import SolarPage
from progress.ui.pages.wind_page import WindPage
from progress.ui.pages.simulation_page import SimulationPage
from progress.ui.pages.results_page import ResultsPage
from progress.mod_sysdata import RASystemData
from progress.ui.widgets.data_handler import DataHandler
from progress.ui.pages.about_page import MarkdownWidget
from progress.mod_utilities import RAUtilities
from progress.paths import BASE_DIR, DATA_DIR, SOLAR_DIR, SYSTEM_DIR, WIND_DIR, update_data_path
import progress.resources_rc
import sys
import os



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

        #setting up sys dir data
        self.sys_directory = str(SYSTEM_DIR)
        self.load_sys_data()

        # load theme
        # self.load_stylesheet(str(base_dir / "resources" / "theme.qss"))

    def _mount_page(self, container, page_widget) -> None:
        layout = container.layout()
        if layout is None:
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
        layout.addWidget(page_widget)



    def load_sys_data(self):
        try:
            rasd = RASystemData()
            data_gen = self.sys_directory + '/gen.csv'
            data_branch = self.sys_directory + '/branch.csv'
            data_bus = self.sys_directory + '/bus.csv'
            data_load = self.sys_directory + '/load.csv'
            data_storage = self.sys_directory + '/storage.csv'

            genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = rasd.gen(data_gen)
            nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = rasd.branch(data_branch)
            bus_name, bus_no, nz = rasd.bus(data_bus)
            load_all_regions = rasd.load(bus_name, data_load)
            essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = rasd.storage(data_storage)

            raut = RAUtilities()
            mu_tot, lambda_tot = raut.reltrates(MTTF_gen, MTTF_trans, MTTR_gen, MTTR_trans, MTTF_ess, MTTR_ess)
            cap_max, cap_min = raut.capacities(nl, pmax, pmin, ess_pmax, ess_pmin, cap_trans)

            # Set data in DataHandler
            self.data_handler.set_genbus(genbus)
            self.data_handler.set_ng(ng)
            self.data_handler.set_pmax(pmax)
            self.data_handler.set_pmin(pmin)
            self.data_handler.set_FOR_gen(FOR_gen)
            self.data_handler.set_MTTF_gen(MTTF_gen)
            self.data_handler.set_MTTR_gen(MTTR_gen)
            self.data_handler.set_gencost(gencost)
            self.data_handler.set_nl(nl)
            self.data_handler.set_fb(fb)
            self.data_handler.set_tb(tb)
            self.data_handler.set_cap_trans(cap_trans)
            self.data_handler.set_MTTF_trans(MTTF_trans)
            self.data_handler.set_MTTR_trans(MTTR_trans)
            self.data_handler.set_bus_name(bus_name)
            self.data_handler.set_bus_no(bus_no)
            self.data_handler.set_nz(nz)
            self.data_handler.set_load_all_regions(load_all_regions)
            self.data_handler.set_essname(essname)
            self.data_handler.set_essbus(essbus)
            self.data_handler.set_ness(ness)
            self.data_handler.set_ess_pmax(ess_pmax)
            self.data_handler.set_ess_pmin(ess_pmin)
            self.data_handler.set_ess_duration(ess_duration)
            self.data_handler.set_ess_socmax(ess_socmax)
            self.data_handler.set_ess_socmin(ess_socmin)
            self.data_handler.set_ess_eff(ess_eff)
            self.data_handler.set_disch_cost(disch_cost)
            self.data_handler.set_ch_cost(ch_cost)
            self.data_handler.set_MTTF_ess(MTTF_ess)
            self.data_handler.set_MTTR_ess(MTTR_ess)
            self.data_handler.set_ess_units(ess_units)
            self.data_handler.set_mu_tot(mu_tot)
            self.data_handler.set_lambda_tot(lambda_tot)
            self.data_handler.set_cap_max(cap_max)
            self.data_handler.set_cap_min(cap_min)
            self.data_handler.set_raut(raut)
        except Exception as e:
            print("ERROR LOADING CSV")

    def load_stylesheet(self, filename):
        """Load a QSS stylesheet from a file."""
        file = QFile(filename)
        if file.open(QFile.ReadOnly):
            stylesheet = file.readAll().data().decode()
            self.setStyleSheet(stylesheet)
            file.close()


def main():
    """
    The main entry point for the application.
    Initializes the QApplication, creates and shows the main window, and starts the event loop.
    """
    update_data_path()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()

