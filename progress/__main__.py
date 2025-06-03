import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from progress.App.main_window.ui_mainwindow import Ui_MainWindow
from progress.mod_sysdata import RASystemData
from progress.mod_utilities import RAUtilities
from progress.App.landing.landing_page import land_form
from progress.paths import get_path
base_dir = get_path()
from progress.App.results.results_view import results_form
from progress.App.about.about_md import MarkdownWidget
from progress.App.api.api_page import api_form
from progress.App.solar.solar_page import solar_form
from progress.App.wind.wind_page import wind_form
from progress.App.simulation.sim_page import sim_form
from progress.App.gui_tools.tools import DataHandler

class MainAppWindow(QMainWindow, Ui_MainWindow):
    """
    The main application window.

    Methods:
    - __init__(self, parent=None): Initializes the main window and connects UI elements to methods.
    - load_sys_data(self): Loads system data and calculates required variables.
    - load_stlesheets(self): Loads a qss stylesheet.
    - apply_dark_theme(self): Applies a dark theme to the app.
    - apply_light_theme(self): Applies a light theme to the app.
    """
    def __init__(self, parent=None):
        super(MainAppWindow, self).__init__(parent)
        # self.ui = Ui_MainWindow()
        self.setupUi(self)
          # Setup the UI using the imported class
        # data handler
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

        self.landing_page.page_changer.connect(lambda: self.tabWidget.setCurrentWidget(self.api_tab))
        self.stackedWidget.setCurrentIndex(1)

        #api page
        self.api_page = api_form(self.data_handler)
        self.verticalLayout_11.addWidget(self.api_page)
        self.api_page.page_changer_next.connect(lambda: self.tabWidget.setCurrentWidget(self.solar_tab))
        self.api_page.page_changer_previous.connect(lambda: self.tabWidget.setCurrentWidget(self.tab_7))

        #solar page
        self.solar_page = solar_form(self.data_handler)
        self.verticalLayout.addWidget(self.solar_page)
        self.solar_page.page_changer_next.connect(lambda: self.tabWidget.setCurrentWidget(self.wind_tab))
        self.solar_page.page_changer_previous.connect(lambda:self.tabWidget.setCurrentWidget(self.api_tab))

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

        # themes page
        self.light_button.clicked.connect(self.apply_light_theme)
        self.dark_button.clicked.connect(self.apply_dark_theme)
        self.apply_light_theme()

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

##### loading style sheets
    def load_stylesheet(self, filename):
        """Load a QSS stylesheet from a file."""
        file = QFile(filename)
        if file.open(QFile.ReadOnly):
            stylesheet = file.readAll().data().decode()
            self.setStyleSheet(stylesheet)
            file.close()

    def apply_dark_theme(self):
        """Apply the dark theme."""
        dark = os.path.join(base_dir,"App", "theme", "dark.qss")
        self.load_stylesheet(dark)

    def apply_light_theme(self):
        """Apply the light theme."""
        light = os.path.join(base_dir,"App", "theme", "light.qss")
        self.load_stylesheet(light)

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

    #### ---------------------- Extra Code ----------------------------

##### possible docs comments #####

    # - handle_output(self, text): Updates the output window with text.

 
    # - show_help_solar(self): Displays a help message for the solar tab.
    # - open_solar_directory(self): Opens a dialog to select the solar directory.
    # - save_solarinput(self): Saves input data provided by the user in the solar tab.
    # - solar_data_process(self): Downloads and processes solar data.
    # - start_download_thread(self): Starts the download thread.
    # - start_gather_thread(self): Starts the gather thread.
    # - end_gather_thread(self): Handles the end of the gather thread.
    # - kmeans_eval(self): Evaluates clustering metrics.
    # - kmeans_gen(self): Generates clusters for solar data.
    # - save_windinput(self): Saves input data provided by the user in the wind tab.
    # - open_wind_directory(self): Opens a dialog to select the wind directory.
    # - download_wind_data(self): Downloads wind data.
    # - cal_wind_tr_rates(self, wind): Calculates wind transition rates.
    # - download_finished(self): Handles the completion of the download.
    # - save_mcsinput(self): Saves input data provided by the user in the simulation page.
    # - run(self): Runs the selected Monte Carlo Simulation (MCS) method.
    # - MCS_zonal(self): Performs MCS using the zonal model.
    # - MCS_cs(self): Performs MCS using the copper sheet model.
    # - plot(self): Plots the results of the simulation.

        # def kmeans_eval(self):

    #     self.solar_site_data = self.solar_directory+"/solar_sites.csv"
    #     self.solar_prob_data = self.solar_directory+"/solar_probs.csv"
    #     self.solar = Solar(self.solar_site_data, self.solar_directory)

    #     QMessageBox.information(self, "Clustering Metrics", "Press OK to continue. This may take a few minutes.")

    #     self.clust_eval = self.ui.lineEdit.text()

    #     self.pipeline = KMeans_Pipeline(self.solar_directory, self.solar_site_data)
    #     self.pipeline.test_metrics(int(self.clust_eval))

    #     #self.handle_kmeans_output(self.pipeline.test_metrics, int(self.clust_eval))

    #     QMessageBox.information(self, "Clustering Metrics", "Please look at SSE curve and silhouette score \
    #                             results to make an informed choice on the number of clusters.")
    #     self.display_text_file(self.cluster_results)
    #     self.display_png(self.pdf_path)
    #     #self.open_folder_in_explorer(self.solar_directory)
    #     #self.ui.widget_2.show()

        # def load_plots(self):
    #     pdf_files = [
    #         ("solar_generation.pdf", self.ui.verticalLayout_55),
    #         ("COV_track.pdf", self.ui.verticalLayout_46),
    #         ("loadcurt.pdf", self.ui.verticalLayout_49),
    #         ("LOLP_track.pdf", self.ui.verticalLayout_51),
    #         ("SOC.pdf", self.ui.verticalLayout_53),
    #         ("wind_generation.pdf", self.ui.verticalLayout_59),
    #         ("heatmap.pdf", self.ui.verticalLayout_47),
    #     ]

    #     for pdf_file, layout in pdf_files:
    #         file_path = os.path.join(base_dir, "Results", pdf_file)
    #         try:
    #             # Check if the file exists
    #             if os.path.exists(file_path):
    #                 pdf_viewer = PDFViewer(file_path)
    #                 layout.addWidget(pdf_viewer.get_pdf_view())
    #             else:
    #                 print(f"Warning: {file_path} does not exist.")  # Log the warning
    #                 QMessageBox.warning(self, "File Not Found", f"{pdf_file} does not exist.")
    #         except Exception as e:
    #             print(f"Error loading {pdf_file}: {e}")  # Log the error
    #             QMessageBox.critical(self, "Error", f"Failed to load {pdf_file}: {e}")
    # def load_plots(self):
    #     pdf_files = [
    #         ("solar_generation.pdf", self.ui.verticalLayout_55),
    #         ("COV_track.pdf", self.ui.verticalLayout_46),
    #         ("loadcurt.pdf", self.ui.verticalLayout_49),
    #         ("LOLP_track.pdf", self.ui.verticalLayout_51),
    #         ("SOC.pdf", self.ui.verticalLayout_53),
    #         ("wind_generation.pdf", self.ui.verticalLayout_59),
    #         ("heatmap.pdf", self.ui.verticalLayout_47),
    #     ]

    #     for pdf_file, layout in pdf_files:
    #         file_path = os.path.join(base_dir, "Results", pdf_file)
    #         try:
    #             if os.path.exists(file_path):
    #                 pdf_viewer = PDFViewer(file_path)
    #                 layout.addWidget(pdf_viewer.get_pdf_view())
    #             else:
    #                 print(f"Warning: {file_path} does not exist.")  # Log the warning
    #                 # Optionally, show a message box to inform the user
    #                # QMessageBox.warning(self, "File Not Found", f"{pdf_file} does not exist.")
    #         except Exception as e:
    #             print(f"Error loading {pdf_file}: {e}")  # Log the error
    #             # Optionally, show a message box to inform the user
    #           #  QMessageBox.critical(self, "Error", f"Failed to load {pdf_file}: {e}")

           # self.ui.stackedWidget.setCurrentIndex(0)


        # test_graph = os.path.join(base_dir, "Results", "solar_generation.pdf")
        # self.pdf_viewer = PDFViewer(test_graph)
        # self.ui.verticalLayout_46.addWidget(self.pdf_viewer.get_pdf_view())


        # test_graph1 = os.path.join(base_dir, "Results", "COV_track.pdf")
        # self.pdf_viewer1 = PDFViewer(test_graph1)
        # self.ui.verticalLayout_47.addWidget(self.pdf_viewer1.get_pdf_view())


        # test_graph2 = os.path.join(base_dir, "Results", "loadcurt.pdf")
        # self.pdf_viewer2 = PDFViewer(test_graph2)
        # self.ui.verticalLayout_49.addWidget(self.pdf_viewer2.get_pdf_view())


        # test_graph3 = os.path.join(base_dir, "Results", "LOLP_track.pdf")
        # self.pdf_viewer3 = PDFViewer(test_graph3)
        # self.ui.verticalLayout_51.addWidget(self.pdf_viewer3.get_pdf_view())


        # test_graph4 = os.path.join(base_dir, "Results", "SOC.pdf")
        # self.pdf_viewer4 = PDFViewer(test_graph4)
        # self.ui.verticalLayout_53.addWidget(self.pdf_viewer4.get_pdf_view())


        # test_graph5 = os.path.join(base_dir, "Results", "wind_generation.pdf")
        # self.pdf_viewer5 = PDFViewer(test_graph5)
        # self.ui.verticalLayout_55.addWidget(self.pdf_viewer5.get_pdf_view())

    # # open solar data directory
    # def open_solar_directory(self):
    #     self.solar_directory = QFileDialog.getExistingDirectory(self, "Select Directory", "")
    #     if self.solar_directory:
    #         self.ui.lineEdit_12.setText(self.solar_directory)
    #     self.ui.widget_14.show()