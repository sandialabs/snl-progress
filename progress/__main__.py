import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from progress.ui.forms.main_window.ui_mainwindow import Ui_MainWindow
from progress.mod_sysdata import RASystemData
from progress.mod_utilities import RAUtilities
from progress.ui.pages.landing_page import land_form
from progress.paths import get_path
base_dir = get_path()
from progress.ui.pages.results_page import results_form
from progress.ui.pages.about_page import MarkdownWidget
from progress.ui.pages.solar_page import solar_form
from progress.ui.pages.wind_page import wind_form
from progress.ui.pages.simulation_page import sim_form
from progress.ui.widgets.data_handler import DataHandler

class MainAppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainAppWindow, self).__init__(parent)
        self.setupUi(self)
        self.data_handler = DataHandler()

        #about page
        md_path = os.path.join(base_dir, '..', 'README.md')

        self.about_page_widget = MarkdownWidget(md_path)
        self.verticalLayout_63.addWidget(self.about_page_widget)

        # landing page
        self.tabWidget.setCurrentWidget(self.tab_7)
        self.landing_page = land_form()
        self.verticalLayout_7.addWidget(self.landing_page)
        self.results_page = results_form()
        self.verticalLayout_3.addWidget(self.results_page)

        self.landing_page.page_changer.connect(lambda: self.tabWidget.setCurrentWidget(self.solar_tab))
        self.stackedWidget.setCurrentIndex(1)

        #solar page
        self.solar_page = solar_form(self.data_handler)
        self.verticalLayout.addWidget(self.solar_page)
        self.solar_page.page_changer_next.connect(lambda: self.tabWidget.setCurrentWidget(self.wind_tab))
        self.solar_page.page_changer_previous.connect(lambda: self.tabWidget.setCurrentWidget(self.tab_7))

        # wind page
        self.wind_page = wind_form(self.data_handler)
        self.verticalLayout_2.addWidget(self.wind_page)
        self.wind_page.page_changer_next.connect(lambda: self.tabWidget.setCurrentWidget(self.sim_tab))
        self.wind_page.page_changer_previous.connect(lambda: self.tabWidget.setCurrentWidget(self.solar_tab))

        # sim page
        self.sim_page = sim_form(self.data_handler)
        self.verticalLayout_10.addWidget(self.sim_page)
        self.sim_page.page_changer_next.connect(lambda: (self.tabWidget.setCurrentWidget(self.results_tab), self.results_page.set_results_path()))
        self.sim_page.page_changer_previous.connect(lambda: self.tabWidget.setCurrentWidget(self.wind_tab))

        #setting up sys dir data
        self.sys_directory = os.path.join(base_dir, "Data", "System")
        self.load_sys_data()

        # load theme
        self.load_stylesheet(os.path.join(base_dir, "ui", "theme.qss"))

    def load_sys_data(self):
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

    app = QApplication(sys.argv)

    main_window = MainAppWindow()

    main_window.show()

    sys.exit(app.exec())



if __name__ == "__main__":
    main()