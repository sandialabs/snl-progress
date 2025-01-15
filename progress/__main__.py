import sys
import os
import io
import copy
import numpy as np
import pandas as pd

from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog, QMessageBox, QTextEdit, QVBoxLayout, QDialog, QSplashScreen, QTableWidget, QTableWidgetItem, QScrollArea, QLabel, QSizePolicy
from PySide6.QtCore import Signal, QThread, QUrl, Qt
from progress.App.MainWindow import Ui_MainWindow
from PySide6.QtGui import QPixmap

from progress.mod_sysdata import RASystemData
from progress.mod_utilities import RAUtilities
from progress.mod_solar import Solar
from progress.mod_kmeans import KMeans_Pipeline
from progress.mod_wind import Wind
from progress.mod_matrices import RAMatrices
from progress.mod_plot import RAPlotTools
from progress.paths import get_path
from progress.App.landing.land import LeafAnimation
base_dir = get_path()
from progress.App.results.results_view import results_form


from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView

# class PDFViewer(QWidget):
#     def __init__(self, pdf_path=None):
#         super().__init__()

#         # Create a QPdfView instance
#         self.pdf_view = QPdfView(self)

#         # Create a layout and add the QPdfView to it
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.pdf_view)
#         self.setLayout(layout)

#         # Load the PDF file if a path is provided
#         if pdf_path:
#             self.load_pdf(pdf_path)

#     def load_pdf(self, pdf_path):
#         # Print the provided path for debugging
#         #print(f"Provided PDF path: {pdf_path}")

#         # Get the absolute path and print it for debugging
#         abs_path = os.path.abspath(pdf_path)
#         #print(f"Absolute PDF path: {abs_path}")

#         # Check if the PDF file exists
#         if not os.path.exists(abs_path):
#             print("The specified PDF file does not exist.")
#             return

#         #print(f"Attempting to load PDF from: {abs_path}")  # Debugging output

#         # Create a QPdfDocument instance
#         self.pdf_document = QPdfDocument()
#         load_error = self.pdf_document.load(abs_path)  # Load the PDF document
#         self.pdf_view.setDocument(self.pdf_document)
#         # # Check if the PDF loaded successfully
#         # if load_error == QPdfDocument.NoError:  # NoError indicates success
#         #     self.pdf_view.setDocument(self.pdf_document)
#         # else:
#         #     print("Failed to load PDF document. Error code:", load_error)

#     def get_pdf_view(self):
#         """Returns the QPdfView instance for adding to other layouts."""
#         return self.pdf_view

# class OutputWindow(QDialog):
#     """
#     A dialog window for displaying output text.

#     Methods:
#     - __init__(self, parent=None): Initializes the output window.
#     - update_output(self, text): Appends text to the output display.
#     """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("QuESt Reliability Processes")

#         self.output_text = QTextEdit()
#         self.output_text.setMinimumSize(700, 600)
#         self.output_text.setReadOnly(True)

#         layout = QVBoxLayout()
#         layout.addWidget(self.output_text)

#         self.setLayout(layout)

#     def update_output(self, text):
#         self.output_text.append(text)

class WorkerThread(QThread):
    """
    A worker thread for running long-running methods in the background.

    Signals:
    - finished: Emitted when the thread finishes execution.
    - output_updated: Emitted when the output is updated.

    Methods:
    - __init__(self, method, *args): Initializes the worker thread with a method and its arguments.
    - run(self): Redirects stdout, runs the method, restores stdout, and emits the finished signal.
    """
    finished = Signal()
    output_updated = Signal(str)

    def __init__(self, method, *args):
        super().__init__()
        self.method = method
        self.args = args

    def run(self):
        # Redirect stdout to a buffer
        stdout_buffer = StdoutBuffer(self)
        sys.stdout = stdout_buffer

        # Execute the long-running method
        self.method(*self.args)

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Emit the finished signal when the process completes
        self.finished.emit()

class StdoutBuffer:
    """
    A buffer for capturing and emitting stdout text.

    Methods:
    - __init__(self, worker_thread): Initializes the buffer with a worker thread.
    - write(self, text): Captures and emits text.
    - flush(self): No-op for compatibility.
    """
    def __init__(self, worker_thread):
        self.worker_thread = worker_thread
        self.buffer = ""

    def write(self, text):
        self.buffer += text
        lines = self.buffer.split("\n")
        for line in lines[:-1]:
            self.worker_thread.output_updated.emit(line)
        self.buffer = lines[-1]

    def flush(self):
        pass

class MainAppWindow(QMainWindow):
    """
    The main application window.

    Methods:
    - __init__(self, parent=None): Initializes the main window and connects UI elements to methods.
    - switch_to_home_page(self): Switches to the home page.
    - switch_to_DI_page(self): Switches to the data input page.
    - switch_to_system_page(self): Switches to the system tab.
    - switch_to_solar_page(self): Switches to the solar tab.
    - switch_to_wind_page(self): Switches to the wind tab.
    - switch_to_sim_page(self): Switches to the simulation page.
    - handle_output(self, text): Updates the output window with text.
    - open_folder_in_explorer(self, path): Opens a folder in the system's file explorer.
    - open_sys_directory(self): Opens a dialog to select the system directory.
    - load_sys_data(self): Loads system data and calculates required variables.
    - show_help_solar(self): Displays a help message for the solar tab.
    - open_solar_directory(self): Opens a dialog to select the solar directory.
    - save_solarinput(self): Saves input data provided by the user in the solar tab.
    - solar_data_process(self): Downloads and processes solar data.
    - start_download_thread(self): Starts the download thread.
    - start_gather_thread(self): Starts the gather thread.
    - end_gather_thread(self): Handles the end of the gather thread.
    - kmeans_eval(self): Evaluates clustering metrics.
    - kmeans_gen(self): Generates clusters for solar data.
    - save_windinput(self): Saves input data provided by the user in the wind tab.
    - open_wind_directory(self): Opens a dialog to select the wind directory.
    - download_wind_data(self): Downloads wind data.
    - cal_wind_tr_rates(self, wind): Calculates wind transition rates.
    - download_finished(self): Handles the completion of the download.
    - save_mcsinput(self): Saves input data provided by the user in the simulation page.
    - run(self): Runs the selected Monte Carlo Simulation (MCS) method.
    - MCS_zonal(self): Performs MCS using the zonal model.
    - MCS_cs(self): Performs MCS using the copper sheet model.
    - plot(self): Plots the results of the simulation.
    """
    def __init__(self, parent=None):
        super(MainAppWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
          # Setup the UI using the imported class

        self.ui.tabWidget.setCurrentWidget(self.ui.tab_7)
        #self.output_window = OutputWindow()
        self.landing_page = LeafAnimation()
        self.ui.verticalLayout_7.addWidget(self.landing_page)
        self.results_page = results_form()
        self.ui.verticalLayout_3.addWidget(self.results_page)
        # button connections in the landing page (stacked widget #1)
        # self.ui.pushButton_getStarted.clicked.connect(self.switch_to_DI_page)
        self.landing_page.page_changer.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.api_tab))
        self.ui.actionHome_Page.triggered.connect(self.switch_to_home_page)
        self.ui.stackedWidget.setCurrentIndex(1)

        # button connections in the data input page (stacked widget #2)
        #self.ui.pushButton_DI_previous.clicked.connect(self.switch_to_home_page)
        self.ui.pushButton_help_API.clicked.connect(self.show_help_api)
        self.ui.pushButton_help_API_2.clicked.connect(self.show_help_name)
        self.ui.pushButton_help_API_3.clicked.connect(self.show_skip_api)
        self.ui.pushButton_save_solarinput.clicked.connect(self.save_api_input)
        self.ui.pushButton_DI_next_4.setVisible(False)

        # button connections in tab widget "solar"
        self.ui.widget_5.setVisible(False)
        self.ui.textBrowser_4.setVisible(False)
        self.ui.pushButton_solar_dl.setVisible(False)
        self.ui.pushButton_DI_next_2.setVisible(False)
        self.ui.pushButton_DI_next_5.setVisible(False)
        self.ui.pushButton_solar_upload.setVisible(False)
        self.ui.comboBox_2.currentIndexChanged.connect(self.solar_cb_changed)
        self.ui.pushButton_solar_upload.clicked.connect(self.upload_solar_data)
        self.ui.pushButton_help_solar.clicked.connect(self.show_help_solar)
        self.ui.textBrowser_6.setVisible(False)
        self.ui.textBrowser_5.setVisible(False)
        self.ui.pushButton_solar_dl.clicked.connect(self.solar_data_process)
        self.ui.pushButton_2.clicked.connect(self.kmeans_eval)
        self.ui.pushButton_3.clicked.connect(self.kmeans_gen)
        self.ui.pushButton.clicked.connect(self.save_solar_data)

        # # button connections in tab widget "wind"
        self.ui.widget_9.setVisible(False)
        self.ui.pushButton_4.setVisible(False)
        self.ui.pushButton_7.setVisible(False)
        self.ui.textBrowser_3.setVisible(False)
        self.ui.pushButton_wind_upload.setVisible(False)
        self.ui.pushButton_DI_next_3.setVisible(False)
        self.ui.pushButton_help_wind.setVisible(False)
        self.ui.comboBox_3.currentIndexChanged.connect(self.wind_cb_changed)
        self.ui.pushButton_wind_upload.clicked.connect(self.upload_wind_data)
        self.ui.pushButton_help_wind.clicked.connect(self.wind_process_help)
        self.ui.pushButton_4.clicked.connect(self.download_wind_data)
        self.ui.pushButton_7.clicked.connect(self.process_existing_wdata)

        self.ui.pushButton_5.clicked.connect(self.run)

        #define data paths
        self.sys_directory = os.path.join(base_dir, "Data", "System")
        self.load_sys_data()
        self.solar_directory = os.path.join(base_dir, "Data", "Solar")
        self.wind_directory = os.path.join(base_dir, "Data", "Wind")
        self.cluster_results = os.path.join(base_dir, "Data", "Solar", "clustering_results.txt")
        self.pdf_path = os.path.join(base_dir, "Data", "Solar", "SSE_Curve.png")

        #self.ui.pushButton_getStarted.clicked.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.api_tab))
        self.ui.pushButton_skip_API.clicked.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.solar_tab))
        self.ui.pushButton_DI_next_4.clicked.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.solar_tab))
        self.ui.pushButton_DI_previous_2.clicked.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.api_tab))

        self.ui.pushButton_DI_next_2.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_DI_previous_4.clicked.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.tab_7))

        self.ui.pushButton.clicked.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.wind_tab))
        self.ui.pushButton_DI_next_5.clicked.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.wind_tab))
        self.ui.pushButton_DI_previous_5.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))

        self.ui.pushButton_DI_next_3.clicked.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.sim_tab))
        self.ui.pushButton_DI_previous_3.clicked.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.solar_tab))

        self.ui.pushButton_sim_previous.clicked.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.wind_tab))
        self.ui.pushButton_6.clicked.connect(lambda: self.ui.tabWidget.setCurrentWidget(self.ui.results_tab))
        self.ui.pushButton_6.clicked.connect(self.results_page.set_results_path)


        self.counter = 0
        self.plot_count = 0
        self.tester=0
        self.png_count = 0

    def switch_to_home_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def switch_to_DI_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def switch_to_system_page(self):
        self.ui.tabWidget.setCurrentIndex(0)

    def switch_to_solar_page(self):
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.tab_2.setEnabled(True)

    def switch_to_wind_page(self):
        self.ui.tabWidget.setCurrentIndex(2)
        self.ui.tab_3.setEnabled(True)

    def switch_to_sim_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def handle_output(self, text_browser, text):
        # Update the GUI with the output text
        text_browser.append(text)

    def open_folder_in_explorer(self, path):
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            os.system(f"open {path}")
        else:
            os.system(f"xdg-open {path}")

    def open_sys_directory(self):
        sys_directory = QFileDialog.getExistingDirectory(self, "Select Directory", "")
        if sys_directory:
            self.ui.lineEdit_3.setText(sys_directory)
            self.sys_directory = sys_directory

    # load system data and calculate required variables
    def load_sys_data(self):
        rasd = RASystemData()
        self.data_gen = self.sys_directory + '/gen.csv'
        self.data_branch = self.sys_directory + '/branch.csv'
        self.data_bus = self.sys_directory + '/bus.csv'
        self.data_load = self.sys_directory + '/load.csv'
        self.data_storage = self.sys_directory + '/storage.csv'

        self.genbus, self.ng, self.pmax, self.pmin, self.FOR_gen, self.MTTF_gen, self.MTTR_gen, self.gencost = rasd.gen(self.data_gen)
        self.nl, self.fb, self.tb, self.cap_trans, self.MTTF_trans, self.MTTR_trans = rasd.branch(self.data_branch)
        self.bus_name, self.bus_no, self.nz = rasd.bus(self.data_bus)
        self.load_all_regions = rasd.load(self.bus_name, self.data_load)
        self.essname, self.essbus, self.ness, self.ess_pmax, self.ess_pmin, self.ess_duration, self.ess_socmax, self.ess_socmin, \
               self.ess_eff, self.disch_cost, self.ch_cost, self.MTTF_ess, self.MTTR_ess, self.ess_units = rasd.storage(self.data_storage)

        self.raut = RAUtilities()
        self.mu_tot, self.lambda_tot = self.raut.reltrates(self.MTTF_gen, self.MTTF_trans, self.MTTR_gen, self.MTTR_trans, self.MTTF_ess, self.MTTR_ess)
        self.cap_max, self.cap_min = self.raut.capacities(self.nl,self.pmax, self.pmin, self.ess_pmax, self.ess_pmin, self.cap_trans) # calling this function to get values of cap_max and cap_min

    # Open help message box in the "solar" tab
    def show_help_api(self):
        QMessageBox.information(self, "API Help 1", "Signup for API key: https://developer.nrel.gov/signup/")

    # Open help message box in the "solar" tab
    def show_help_name(self):
        QMessageBox.information(self, "API Help 2", "Use '+' instead of space for name and affiliation, e.g., john+doe.")

    def show_skip_api(self):
        QMessageBox.information(self, "API Help 3", "You can skip this step if you are using your own data.")

    # save input data provided by the user in the solar tab
    def save_api_input(self):
        # save user input
        self.input_api = self.ui.lineEdit_api.text()
        self.input_name = self.ui.lineEdit_name.text()
        self.input_email = self.ui.lineEdit_email.text()
        self.input_aff = self.ui.lineEdit_aff.text()

        self.input_api_w = self.input_api
        self.input_email_w = self.input_email
        self.input_aff_w = self.input_aff

        QMessageBox.information(self, "API information", "Saved!")

        self.ui.pushButton_DI_next_4.setVisible(True)
        self.ui.pushButton_skip_API.setVisible(False)
        self.ui.pushButton_help_API_3.setVisible(False)

    # Open help message box in the "solar" tab
    def show_help_solar(self):
        QMessageBox.information(self, "Solar Help", "You can skip this step if your solar power generation data has previously been clustered.")

    def solar_cb_changed(self, index):
        if index == 1:
            self.ui.textBrowser_4.setVisible(True)
            self.ui.widget_5.setVisible(True)
            self.ui.pushButton_solar_dl.setVisible(True)
            self.ui.pushButton_solar_upload.setVisible(False)
        elif index == 2:
            self.ui.pushButton_solar_upload.setVisible(True)
            self.ui.textBrowser_4.setVisible(False)
            self.ui.widget_5.setVisible(False)
            self.ui.pushButton_solar_dl.setVisible(False)
            # self.ui.pushButton_DI_next_2.setVisible(True)

    def upload_solar_data(self):

        self.solar_directory = QFileDialog.getExistingDirectory(self, "Select Directory", "")

        QMessageBox.information(self, "Solar Upload", "Solar data uploaded and saved!")

        self.ui.pushButton_DI_next_2.setVisible(True)

    # download weather data and convert to solar generation data for all sites
    def solar_data_process(self):
        self.ui.textBrowser_4.append("Downloading solar data...")
        self.input_starty = int(self.ui.lineEdit_starty.text())
        self.input_endy = int(self.ui.lineEdit_endy.text())
        self.solar_site_data = self.solar_directory+"/solar_sites.csv"
        self.solar_prob_data = self.solar_directory+"/solar_probs.csv"
        self.solar = Solar(self.solar_site_data, self.solar_directory)

        # Create worker threads for download and gather processes
        self.download_thread = WorkerThread(self.solar.SolarGen, self.input_api, self.input_name, \
                                            self.input_aff, self.input_email, self.input_starty, self.input_endy)
        self.gather_thread = WorkerThread(self.solar.SolarGenGather, self.input_starty, self.input_endy)

        self.start_download_thread()

        # Connect the output_updated signal to update the GUI
        self.download_thread.output_updated.connect(lambda text: self.handle_output(self.ui.textBrowser_4, text))

        # Connect the finished signal of download_thread to start the gather_thread
        self.download_thread.finished.connect(self.start_gather_thread)

        # Connect the output_updated signal to update the GUI
        self.gather_thread.output_updated.connect(lambda text: self.handle_output(self.ui.textBrowser_4, text))

        # Connect the finished signal of gather_thread to handle thread completion
        self.gather_thread.finished.connect(self.end_gather_thread)

        self.ui.pushButton_DI_next_2.setVisible(True)

    def start_download_thread(self):
        # start download thread
        self.download_thread.start()
        #self.ui.textBrowser_4.append("Downloading solar data please wait until the process has finished.")
        #self.output_window.show()

    def start_gather_thread(self):
        # Start the gather_thread
        self.gather_thread.start()

    def end_gather_thread(self):
        pass

    def kmeans_eval(self):

        if hasattr(self, 'label_sse'):
            self.label_sse.setVisible(False)
            self.ui.horizontalLayout_23.removeWidget(self.label_sse)
        self.ui.textBrowser_6.setVisible(True)
        self.ui.textBrowser_5.setVisible(True)
        self.solar_site_data = self.solar_directory + "/solar_sites.csv"
        self.solar_prob_data = self.solar_directory + "/solar_probs.csv"
        self.solar = Solar(self.solar_site_data, self.solar_directory)

        QMessageBox.information(self, "Clustering Metrics", "Press OK to continue. This may take a few minutes.")

        self.clust_eval = self.ui.lineEdit.text()

        # Create a worker thread for the instantiation of KMeans_Pipeline
        self.worker_pipeline = WorkerThread(self.create_pipeline)
        self.worker_pipeline.output_updated.connect(lambda text: self.handle_output(self.ui.textBrowser_6, text))
        #self.worker_pipeline.finished.connect(self.start_test_metrics)
        self.worker_pipeline.finished.connect(self.checker)
        # Start the worker thread for pipeline instantiation
        self.worker_pipeline.start()

    def checker(self):
        if self.counter==0:
            # print(self.counter)
            self.counter = 1
            # print(self.counter)
        else:
            self.start_test_metrics()
            self.counter = 0

    def create_pipeline(self):
        self.pipeline = KMeans_Pipeline(self.solar_directory, self.solar_site_data)

    def start_test_metrics(self):
        # Check if worker_pipeline has completed
        if hasattr(self, 'worker_pipeline') and self.worker_pipeline.isFinished():
            # Create worker threads for the pipeline methods
            self.worker1 = WorkerThread(self.pipeline.test_metrics, int(self.clust_eval))
            self.worker2 = WorkerThread(self.display_text_file, self.cluster_results)

            # Connect signals
            self.worker1.output_updated.connect(lambda text: self.handle_output(self.ui.textBrowser_6, text))
            self.worker1.finished.connect(self.start_worker2)
            self.worker2.output_updated.connect(lambda text: self.handle_output(self.ui.textBrowser_5, text))
            self.worker2.finished.connect(self.on_workers_finished)

            # Start the first worker
            self.worker1.start()
        else:
            print("worker_pipeline has not finished yet.")

    def start_worker2(self):
        if self.tester==0:
            self.tester=1
        else:
            self.worker2.start()
            self.tester=0

    def display_text_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.ui.textBrowser_5.append(content)  # Append the content to the QTextBrowser
        except Exception as e:
            self.ui.textBrowser_5.append(f"Error loading file: {e}")


    def display_png(self, file_path):
        if os.path.isfile(file_path):  # Check if the file exists
            pixmap = QPixmap(file_path)

            if not pixmap.isNull():
                # Hide the QTextBrowser
                if self.png_count == 0:
                    self.png_count = 1
                elif self.png_count ==1 :
                    self.ui.textBrowser_6.hide()

                    # Create a QLabel to display the image
                    self.label_sse = QLabel()
                    self.label_sse.setPixmap(pixmap)
                    self.label_sse.setPixmap(pixmap.scaled(self.ui.textBrowser_6.width(), self.ui.textBrowser_6.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    self.label_sse.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                    self.ui.horizontalLayout_23.insertWidget(0, self.label_sse)
                    self.png_count = 0

                    # label.setAlignment(Qt.AlignCenter)
                    # label.setGeometry(self.ui.textBrowser_6.geometry())
                    # label.show()

                #print('Image displayed successfully.')
            else:
                self.ui.textBrowser_6.setText("Failed to load image.")
                self.ui.textBrowser_6.show()
                print("Failed to load image.")
        else:
            self.ui.textBrowser_6.setText("File does not exist.")
            self.ui.textBrowser_6.show()
            print("File does not exist.")

    # def display_png(self, file_path):
    #     if os.path.isfile(file_path):  # Check if the file exists
    #         url = QUrl.fromLocalFile(file_path)  # Convert the file path to a URL
    #         html_content = f'<img src="{url.toString()}" />'
    #         self.ui.textBrowser_6.setHtml(html_content)  # Load the image in the QTextBrowser
    #         print('Image displayed successfully.')
    #     else:
    #         self.ui.textBrowser_6.setText("File does not exist.")
    #         print("File does not exist.")

    def on_workers_finished(self):
        # QMessageBox.information(self, "Clustering Metrics", "Please look at SSE curve and silhouette score results to make an informed choice on the number of clusters.")
        self.display_png(self.pdf_path)
        # self.display_text_file(self.cluster_results)

    def kmeans_gen(self):
        # self.ui.textBrowser_5.setVisible(False)
        self.clust_gen = self.ui.lineEdit_2.text()
        self.pipeline.run(n_clusters = int(self.clust_gen))
        self.pipeline.calculate_cluster_probability()
        self.pipeline.split_and_cluster_data()

        self.s_sites, self.s_zone_no, self.s_max, self.s_profiles, self.solar_prob = self.solar.GetSolarProfiles(self.solar_prob_data)

        QMessageBox.information(self, "Clustering Complete", "Clustering of solar data complete!")

        self.ui.pushButton_DI_next_5.setVisible(True)

    def save_solar_data(self):
        solar_site_data = self.solar_directory+"/solar_sites.csv"
        solar_prob_data = self.solar_directory+"/solar_probs.csv"

        solar = Solar(solar_site_data, self.solar_directory)

        self.s_sites, self.s_zone_no, self.s_max, self.s_profiles, self.solar_prob = solar.GetSolarProfiles(solar_prob_data)

    def wind_cb_changed(self, index):
        if index == 1:
            self.ui.widget_9.setVisible(True)
            self.ui.pushButton_4.setVisible(True)
            self.ui.pushButton_7.setVisible(False)
        elif index == 2:
            self.ui.pushButton_help_wind.setVisible(True)
            self.ui.pushButton_DI_next_3.setVisible(True)
            self.ui.widget_9.setVisible(False)
            self.ui.pushButton_4.setVisible(False)
            self.ui.pushButton_wind_upload.setVisible(True)

    def upload_wind_data(self):

        self.wind_directory = QFileDialog.getExistingDirectory(self, "Select Directory", "")
        self.wind_site_data = self.wind_directory+"/wind_sites.csv"
        self.pcurve_data = self.wind_directory+"/w_power_curves.csv"
        wind = Wind()
        self.w_sites, self.farm_name, self.zone_no, self.w_classes, self.w_turbines, self.r_cap, self.p_class, \
            self.out_curve2, self.out_curve3, self.start_speed = wind.WindFarmsData(self.wind_site_data, self.pcurve_data)

        wind_tr_rate = self.wind_directory + '/t_rate.xlsx'
        if os.path.exists(wind_tr_rate):
            self.tr_mats = pd.read_excel(wind_tr_rate, sheet_name=None)
            self.tr_mats = np.array([self.tr_mats[sheet_name].to_numpy() for sheet_name in self.tr_mats])
        else:
            QMessageBox.information(self, "Transition Matrix", "Transition rate matrix does not exist. Please process wind speed data first.")

        QMessageBox.information(self, "Wind Upload", "Wind data uploaded and saved!")

        self.ui.pushButton_7.setVisible(True)
        self.ui.pushButton_DI_next_3.setVisible(True)

    def wind_process_help(self):

        QMessageBox.information(self, "Wind Process Help", "Wind speed data (downloaded or user-provided) is utilized to generate transition rate matrix in this step. You can skip this step if you already have the required matrix.")


    def download_wind_data(self):

        self.ui.textBrowser_3.setVisible(True)

        self.input_starty_w = int(self.ui.lineEdit_22.text())
        self.input_endy_w = int(self.ui.lineEdit_23.text())

        self.wind_site_data = self.wind_directory+"/wind_sites.csv"
        self.pcurve_data = self.wind_directory+"/w_power_curves.csv"

        wind = Wind()
        self.w_sites, self.farm_name, self.zone_no, self.w_classes, self.w_turbines, self.r_cap, self.p_class, \
            self.out_curve2, self.out_curve3, self.start_speed = wind.WindFarmsData(self.wind_site_data, self.pcurve_data)

        # Create a worker thread for the DownloadWindData method
        self.download_thread = WorkerThread(wind.DownloadWindData, self.wind_directory, self.wind_site_data, self.input_api_w, self.input_email_w, \
                                            self.input_aff_w, self.input_starty_w, self.input_endy_w)

        self.download_thread.output_updated.connect(lambda text: self.handle_output(self.ui.textBrowser_3, text))
        # Connect the finished signal to handle thread completion
        self.download_thread.finished.connect(lambda: self.cal_wind_tr_rates())

        # Start the worker thread
        self.download_thread.start()

        self.ui.pushButton_DI_next_3.setVisible(True)
        self.ui.pushButton_7.setVisible(True)

    def cal_wind_tr_rates(self):
        self.windspeed_data = self.wind_directory+"/windspeed_data.csv"
        self.wind_site_data = self.wind_directory+"/wind_sites.csv"
        self.pcurve_data = self.wind_directory+"/w_power_curves.csv"
        wind = Wind()
        self.w_sites, self.farm_name, self.zone_no, self.w_classes, self.w_turbines, self.r_cap, self.p_class, \
            self.out_curve2, self.out_curve3, self.start_speed = wind.WindFarmsData(self.wind_site_data, self.pcurve_data)

        # calculate transition rates
        wind.CalWindTrRates(self.wind_directory, self.windspeed_data, self.wind_site_data, self.pcurve_data)

        # QMessageBox.information(self, "Processing Complete", "Wind data processing complete!")

        # self.ui.pushButton_DI_next_3.setVisible(True)

    def download_finished(self):
        wind_tr_rate = self.wind_directory + '/t_rate.xlsx'
        self.tr_mats = pd.read_excel(wind_tr_rate, sheet_name=None)
        self.tr_mats = np.array([self.tr_mats[sheet_name].to_numpy() for sheet_name in self.tr_mats])
        self.ui.pushButton_DI_next_3.setVisible(True)

    def process_existing_wdata(self):

        self.ui.textBrowser_3.setVisible(False)
        self.cal_wind_tr_rates()
        self.download_finished()
        QMessageBox.information(self, "Existing Wind Data", "Processed!")
        self.ui.pushButton_DI_next_3.setVisible(True)


    def save_mcsinput(self):
        self.samples= int(self.ui.lineEdit_4.text())
        self.sim_hours = int(self.ui.lineEdit_5.text())
        self.load_factor = float(self.ui.lineEdit_6.text())
        self.ui.pushButton_5.setVisible(True)
        self.current_text = self.ui.comboBox.currentText()
        QMessageBox.information(self, "Sim Input", "Input Saved!")

    def run(self):

        self.save_mcsinput()
        if self.current_text == "Zonal Model":
            self.worker_zonal = WorkerThread(self.MCS_zonal)

            #self.worker_zonal.output_updated.connect(self.handle_output)
            self.worker_zonal.output_updated.connect(lambda text: self.handle_output(self.ui.textBrowser_2, text))
            self.worker_zonal.start()
            self.worker_zonal.finished.connect(self.plot)
           # self.output_window.show()

        elif self.current_text == "Copper Sheet Model":
            self.worker_copper= WorkerThread(self.MCS_cs)
            #self.worker_copper.output_updated.connect(self.handle_output)
            # Connect the output_updated signal to update the GUI
            self.worker_copper.output_updated.connect(lambda text: self.handle_output(self.ui.textBrowser_2, text))

            self.worker_copper.start()
            self.worker_copper.finished.connect(self.plot)
           # self.output_window.show()

    def MCS_zonal(self):

        """
        Performs mixed time sequential Monte Carlo Simulation (MCS) to evaluate the reliability of a power system. Uses transportation model.

        Parameters:
        samples (int): Number of samples to simulate.
        sim_hours (int): Number of hours to simulate.
        system_directory (str): Path to the directory containing system data files.
        solar_directory (str or bool): Path to the directory containing solar data files or False if not used.
        wind_directory (str or bool): Path to the directory containing wind data files or False if not used.

        Returns:
        tuple: A tuple containing indices, rank, SOC records, curtailment records, renewable records, bus names, and ESS names.
        """

        BMva = 100

        # matrices required for optimization
        ramat = RAMatrices(self.nz)
        gen_mat = ramat.genmat(self.ng, self.genbus, self.ness, self.essbus)
        ch_mat = ramat.chmat(self.ness, self.essbus, self.nz)
        A_inc = ramat.Ainc(self.nl, self.fb, self.tb)
        curt_mat = ramat.curtmat(self.nz)

        # dictionary for storing temp. index values
        indices_rec = {"LOLP_rec": np.zeros(self.samples), "EUE_rec": np.zeros(self.samples), "MDT_rec": np.zeros(self.samples), \
                "LOLF_rec": np.zeros(self.samples), "EPNS_rec": np.zeros(self.samples), "LOLP_hr": np.zeros(self.sim_hours), \
                    "LOLE_rec": np.zeros(self.samples), "mLOLP_rec":np.zeros(self.samples), "COV_rec": np.zeros(self.samples)}

        LOL_track = np.zeros((self.samples, self.sim_hours))

        for s in range(self.samples):

            print(f'Sample: {s+1}')

            # temp variables to be used for each sample
            var_s = {"t_min": 0, "LLD": 0, "curtailment": np.zeros(self.sim_hours), "label_LOLF": np.zeros(self.sim_hours), "freq_LOLF": 0, "LOL_days": 0, \
                    "outage_day": np.zeros(365)}

            # current states of components
            current_state = np.ones(self.ng + self.nl + self.ness) # all gens and TLs in up state at the start of the year

            if self.wind_directory:
                current_w_class = np.floor(np.random.uniform(0, 1, self.w_sites)*self.w_classes).astype(int) # starting wind speed class for each site (random)

            # record data for plotting and exporting (optional)
            self.renewable_rec = {"wind_rec": np.zeros((self.nz, self.sim_hours)), "solar_rec": np.zeros((self.nz, self.sim_hours)), "congen_temp": 0, \
                            "rengen_temp": 0}

            SOC_old = 0.5*(np.multiply(np.multiply(self.ess_pmax, self.ess_duration), self.ess_socmax))/BMva
            self.SOC_rec = np.zeros((self.ness, self.sim_hours))
            self.curt_rec = np.zeros(self.sim_hours)
            # gen_rec = np.zeros((sim_hours, ng))

            for n in range(self.sim_hours):

                # get current states(up/down) and capacities of all system components
                next_state, current_cap, var_s["t_min"] = self.raut.NextState(var_s["t_min"], self.ng, self.ness, self.nl, \
                                                                        self.lambda_tot, self.mu_tot, current_state, self.cap_max, self.cap_min, self.ess_units)
                current_state = copy.deepcopy(next_state)

                # update SOC based on failures in ESS
                ess_smax, ess_smin, SOC_old = self.raut.updateSOC(self.ng, self.nl, current_cap, self.ess_pmax, self.ess_duration, self.ess_socmax, \
                                                                  self.ess_socmin, SOC_old)

                # calculate upper and lower bounds of gens and tls
                gt_limits = {"g_lb": np.concatenate((current_cap["min"][0:self.ng]/BMva, current_cap["min"][self.ng + self.nl::]/BMva)), \
                            "g_ub": np.concatenate((current_cap["max"][0:self.ng]/BMva, current_cap["max"][self.ng + self.nl::]/BMva)), "tl": current_cap["max"][self.ng:self.ng + self.nl]/BMva}

                def fb_Pg(model, i):
                    return (gt_limits["g_lb"][i], gt_limits["g_ub"][i])

                def fb_flow(model,i):
                    return (-gt_limits["tl"][i], gt_limits["tl"][i])

                def fb_ess(model, i):
                    return(-current_cap["max"][self.ng + self.nl::][i]/BMva, current_cap["min"][self.ng + self.nl::][i]/BMva)

                def fb_soc(model, i):
                    return(ess_smin[i]/BMva, ess_smax[i]/BMva)

                # get wind power output for all zones/areas
                if self.wind_directory:
                    w_zones, current_w_class = self.raut.WindPower(self.nz, self.w_sites, self.zone_no, \
                    self.w_classes, self.r_cap, current_w_class, self.tr_mats, self.p_class, self.w_turbines, self.out_curve2, self.out_curve3)

                # get solar power output for all zones/areas
                if self.solar_directory:
                    s_zones = self.raut.SolarPower(n, self.nz, self.s_zone_no, self.solar_prob, self.s_profiles, self.s_sites, self.s_max)

                # record wind and solar profiles for plotting (optional)
                if self.wind_directory:
                    self.renewable_rec["wind_rec"][:, n] = w_zones

                if self.solar_directory:
                    s_zones_t = np.transpose(s_zones)
                    self.renewable_rec["solar_rec"][:, n] = s_zones_t[:, n%24]

                # recalculate net load (for distribution side resources, optional)
                part_netload = self.load_factor*self.load_all_regions

                if self.solar_directory and self.wind_directory:
                    net_load =  part_netload[n] - w_zones - s_zones[n%24]
                elif self.solar_directory==False and self.wind_directory:
                    net_load = part_netload[n] - w_zones
                elif self.solar_directory and self.wind_directory==False:
                    net_load = part_netload[n] - s_zones[n%24]
                elif self.solar_directory==False and self.wind_directory==False:
                    net_load = part_netload[n]

                # optimize dipatch and calculate load curtailment
                load_curt, SOC_old = self.raut.OptDispatch(self.ng, self.nz, self.nl, self.ness, fb_ess, fb_soc, BMva, fb_Pg, fb_flow, A_inc, gen_mat, curt_mat, ch_mat, \
                                                    self.gencost, net_load, SOC_old, self.ess_pmax, self.ess_eff, self.disch_cost, self.ch_cost)


                # record values for visualization purposes
                self.SOC_rec[:, n] = SOC_old*BMva
                self.curt_rec[n] = load_curt*BMva

                # track loss of load states
                var_s, LOL_track = self.raut.TrackLOLStates(load_curt, BMva, var_s, LOL_track, s, n)

                if (n+1)%100 == 0:
                    print(f'Hour {n + 1}')

            # collect indices for all samples
            indices_rec = self.raut.UpdateIndexArrays(indices_rec, var_s, self.sim_hours, s)

            # check for convergence using LOLP and COV
            indices_rec["mLOLP_rec"][s] = np.mean(indices_rec["LOLP_rec"][0:s+1])
            var_LOLP = np.var(indices_rec["LOLP_rec"][0:s+1])
            indices_rec["COV_rec"][s] = np.sqrt(var_LOLP)/indices_rec["mLOLP_rec"][s]

        # calculate reliability indices for the MCS
        indices = self.raut.GetReliabilityIndices(indices_rec, self.sim_hours, self.samples)
        self.mLOLP_rec = indices_rec["mLOLP_rec"]
        self.COV_rec = indices_rec["COV_rec"]


        print("Simulation complete! You can view the results now by clicking next! Plots are also saved to the results folder.")
        self.ui.pushButton_6.setVisible(True)

        self.main_folder = os.path.dirname(os.path.abspath(__file__))
        self.results_dir = os.path.join(self.main_folder, 'Results')

        if not os.path.exists(f"{self.main_folder}/Results"):
            os.makedirs(f"{self.main_folder}/Results")

        df = pd.DataFrame([indices])
        df.to_csv(f"{self.main_folder}/Results/indices.csv", index=False)
        if self.sim_hours == 8760:
            self.raut.OutageHeatMap(LOL_track, 1, self.samples, self.main_folder)

    def MCS_cs(self):

        """
        Performs mixed time sequential Monte Carlo Simulation (MCS) to evaluate the reliability of a power system. Uses copper sheet model.

        Parameters:
        samples (int): Number of samples to simulate.
        sim_hours (int): Number of hours to simulate.
        system_directory (str): Path to the directory containing system data files.
        solar_directory (str or bool): Path to the directory containing solar data files or False if not used.
        wind_directory (str or bool): Path to the directory containing wind data files or False if not used.

        Returns:
        tuple: A tuple containing indices, rank, SOC records, curtailment records, renewable records, bus names, and ESS names.
        """

        BMva = 100

        # matrices required for optimization
        ramat = RAMatrices(self.nz)
        gen_mat = ramat.genmat(self.ng, self.genbus, self.ness, self.essbus)
        ch_mat = ramat.chmat(self.ness, self.essbus, self.nz)
        A_inc = ramat.Ainc(self.nl, self.fb, self.tb)
        curt_mat = ramat.curtmat(self.nz)

        # dictionary for storing temp. index values
        indices_rec = {"LOLP_rec": np.zeros(self.samples), "EUE_rec": np.zeros(self.samples), "MDT_rec": np.zeros(self.samples), \
                "LOLF_rec": np.zeros(self.samples), "EPNS_rec": np.zeros(self.samples), "LOLP_hr": np.zeros(self.sim_hours), \
                    "LOLE_rec": np.zeros(self.samples), "mLOLP_rec":np.zeros(self.samples), "COV_rec": np.zeros(self.samples)}

        LOL_track = np.zeros((self.samples, self.sim_hours))

        for s in range(self.samples):

            print(f'Sample: {s+1}')

            # temp variables to be used for each sample
            var_s = {"t_min": 0, "LLD": 0, "curtailment": np.zeros(self.sim_hours), "label_LOLF": np.zeros(self.sim_hours), "freq_LOLF": 0, "LOL_days": 0, \
                    "outage_day": np.zeros(365)}

            # current states of components
            current_state = np.ones(self.ng + self.nl + self.ness) # all gens and TLs in up state at the start of the year

            if self.wind_directory:
                current_w_class = np.floor(np.random.uniform(0, 1, self.w_sites)*self.w_classes).astype(int) # starting wind speed class for each site (random)

            # record data for plotting and exporting (optional)
            self.renewable_rec = {"wind_rec": np.zeros((self.nz, self.sim_hours)), "solar_rec": np.zeros((self.nz, self.sim_hours)), "congen_temp": 0, \
                            "rengen_temp": 0}

            SOC_old = 0.5*(np.multiply(np.multiply(self.ess_pmax, self.ess_duration), self.ess_socmax))/BMva
            self.SOC_rec = np.zeros((self.ness, self.sim_hours))
            self.curt_rec = np.zeros(self.sim_hours)
            # gen_rec = np.zeros((sim_hours, ng))

            for n in range(self.sim_hours):

                # get current states(up/down) and capacities of all system components
                next_state, current_cap, var_s["t_min"] = self.raut.NextState(var_s["t_min"], self.ng, self.ness, self.nl, \
                                                                        self.lambda_tot, self.mu_tot, current_state, self.cap_max, self.cap_min, self.ess_units)
                current_state = copy.deepcopy(next_state)

                # update SOC based on failures in ESS
                ess_smax, ess_smin, SOC_old = self.raut.updateSOC(self.ng, self.nl, current_cap, self.ess_pmax, self.ess_duration, self.ess_socmax, \
                                                                  self.ess_socmin, SOC_old)

                # calculate upper and lower bounds of gens and tls
                gt_limits = {"g_lb": np.concatenate((current_cap["min"][0:self.ng]/BMva, current_cap["min"][self.ng + self.nl::]/BMva)), \
                            "g_ub": np.concatenate((current_cap["max"][0:self.ng]/BMva, current_cap["max"][self.ng + self.nl::]/BMva)), "tl": current_cap["max"][self.ng:self.ng + self.nl]/BMva}

                def fb_Pg(model, i):
                    return (gt_limits["g_lb"][i], gt_limits["g_ub"][i])

                def fb_flow(model,i):
                    return (-gt_limits["tl"][i], gt_limits["tl"][i])

                def fb_ess(model, i):
                    return(-current_cap["max"][self.ng + self.nl::][i]/BMva, current_cap["min"][self.ng + self.nl::][i]/BMva)

                def fb_soc(model, i):
                    return(ess_smin[i]/BMva, ess_smax[i]/BMva)

                # get wind power output for all zones/areas
                if self.wind_directory:
                    w_zones, current_w_class = self.raut.WindPower(self.nz, self.w_sites, self.zone_no, \
                    self.w_classes, self.r_cap, current_w_class, self.tr_mats, self.p_class, self.w_turbines, self.out_curve2, self.out_curve3)

                # get solar power output for all zones/areas
                if self.solar_directory:
                    s_zones = self.raut.SolarPower(n, self.nz, self.s_zone_no, self.solar_prob, self.s_profiles, self.s_sites, self.s_max)

                # record wind and solar profiles for plotting (optional)
                if self.wind_directory:
                    self.renewable_rec["wind_rec"][:, n] = w_zones

                if self.solar_directory:
                    s_zones_t = np.transpose(s_zones)
                    self.renewable_rec["solar_rec"][:, n] = s_zones_t[:, n%24]

                # recalculate net load (for distribution side resources, optional)
                part_netload = 1.25*self.load_all_regions

                if self.solar_directory and self.wind_directory:
                    net_load =  part_netload[n] - w_zones - s_zones[n%24]
                elif self.solar_directory==False and self.wind_directory:
                    net_load = part_netload[n] - w_zones
                elif self.solar_directory and self.wind_directory==False:
                    net_load = part_netload[n] - s_zones[n%24]
                elif self.solar_directory==False and self.wind_directory==False:
                    net_load = part_netload[n]

                # optimize dipatch and calculate load curtailment
                load_curt, SOC_old = self.raut.OptDispatchLite(self.ng, self.nz, self.ness, fb_ess, fb_soc, BMva, fb_Pg, A_inc,\
                                                    self.gencost, net_load, SOC_old, self.ess_pmax, self.ess_eff, self.disch_cost, self.ch_cost)

                # record values for visualization purposes
                self.SOC_rec[:, n] = SOC_old*BMva
                self.curt_rec[n] = load_curt*BMva
                # gen_rec[n] = gen[0:ng]

                # track loss of load states
                var_s, LOL_track = self.raut.TrackLOLStates(load_curt, BMva, var_s, LOL_track, s, n)

                if (n+1)%100 == 0:
                    print(f'Hour {n + 1}')

            # collect indices for all samples
            indices_rec = self.raut.UpdateIndexArrays(indices_rec, var_s, self.sim_hours, s)

            # check for convergence using LOLP and COV
            indices_rec["mLOLP_rec"][s] = np.mean(indices_rec["LOLP_rec"][0:s+1])
            var_LOLP = np.var(indices_rec["LOLP_rec"][0:s+1])
            indices_rec["COV_rec"][s] = np.sqrt(var_LOLP)/indices_rec["mLOLP_rec"][s]

        # calculate reliability indices for the MCS
        indices = self.raut.GetReliabilityIndices(indices_rec, self.sim_hours, self.samples)
        self.mLOLP_rec = indices_rec["mLOLP_rec"]
        self.COV_rec = indices_rec["COV_rec"]

        print("Simulation complete! You can view the results now by clicking next! Plots are also saved to the results folder.")
        self.ui.pushButton_6.setVisible(True)

        self.main_folder = os.path.dirname(os.path.abspath(__file__))
        self.results_dir = os.path.join(self.main_folder, 'Results')

        if not os.path.exists(f"{self.main_folder}/Results"):
            os.makedirs(f"{self.main_folder}/Results")

        df = pd.DataFrame([indices])
        df.to_csv(f"{self.main_folder}/Results/indices.csv", index=False)

        if self.sim_hours == 8760:
            self.raut.OutageHeatMap(LOL_track, 1, self.samples, self.main_folder)

    def plot(self):
        if self.plot_count == 0:

            self.plot_count = 1
        else:
            rapt = RAPlotTools(self.main_folder)
            rapt.PlotSolarGen(self.renewable_rec["solar_rec"], self.bus_name)
            rapt.PlotWindGen(self.renewable_rec["wind_rec"], self.bus_name)
            rapt.PlotSOC(self.SOC_rec, self.essname)
            rapt.PlotLoadCurt(self.curt_rec)
            rapt.PlotLOLP(self.mLOLP_rec, self.samples, 1)
            rapt.PlotCOV(self.COV_rec, self.samples, 1)
            if self.sim_hours == 8760:
                rapt.OutageMap(f"{self.main_folder}/Results/LOL_perc_prob.csv")
            #self.ui.textBrowser_2.append("Plotting complete, view plots by clicking next. Plots are also saved in the Results folder.")
            #QMessageBox.information(self, "Plots", "Plotting complete, view plots in the Results folder.")
            #self.open_folder_in_explorer(self.results_dir)
            # self.load_plots()
            # self.load_csv_files()
            self.plot_count = 0

    # def load_plots(self):
    #     # List of test graphs and their corresponding layout
    #     graphs = [
    #         ("solar_generation.pdf", self.ui.verticalLayout_55),
    #         ("COV_track.pdf", self.ui.verticalLayout_46),
    #         ("loadcurt.pdf", self.ui.verticalLayout_49),
    #         ("LOLP_track.pdf", self.ui.verticalLayout_51),
    #         ("SOC.pdf", self.ui.verticalLayout_53),
    #         ("wind_generation.pdf", self.ui.verticalLayout_59),
    #         ("heatmap.pdf", self.ui.verticalLayout_47),
    #     ]
    #     # Remove existing PDF viewers if they exist
    #     for graph_name, layout in graphs:
    #         viewer_attr_name = f"pdf_viewer_{graph_name.split('.')[0]}"
    #         if hasattr(self, viewer_attr_name):
    #             viewer = getattr(self, viewer_attr_name)
    #             layout.removeWidget(viewer.get_pdf_view())

    #     # Load new plots
    #     for graph_name, layout in graphs:
    #         test_graph = os.path.join(base_dir, "Results", graph_name)

    #         try:
    #             # Create a new PDFViewer instance and add it to the layout
    #             viewer = PDFViewer(test_graph)
    #             layout.addWidget(viewer.get_pdf_view())
    #             setattr(self, f"pdf_viewer_{graph_name.split('.')[0]}", viewer)
    #         except Exception as e:
    #             print(f"Failed to load {graph_name}: {e}")


    # def load_csv_files(self):

    #     csv_files = [
    #         os.path.join(base_dir, "Results", "indices.csv")
    #         # os.path.join(base_dir, "Results", "LOL_perc_prob.csv"),
    #     ]

    #     for file_path in csv_files:
    #         try:
    #             if os.path.exists(file_path):
    #                 self.load_csv_to_table(file_path)
    #             else:
    #                 print(f"Warning: {file_path} does not exist.")  # Log the warning
    #                 #QMessageBox.warning(self, "File Not Found", f"{file_path} does not exist.")
    #         except Exception as e:
    #             print(f"Error loading {file_path}: {e}")
    #             #QMessageBox.critical(self, "Error", f"Failed to load {file_path}: {e}")

    # def load_csv_to_table(self, file_path):
    #     # Generate a dynamic attribute name based on the file name
    #     table_attr_name = f"table_{os.path.basename(file_path).split('.')[0]}"

    #     # Check if the table already exists and remove it if it does
    #     if hasattr(self, table_attr_name):
    #         existing_table = getattr(self, table_attr_name)
    #         self.ui.verticalLayout_61.removeWidget(existing_table)

    #     # Create a new table for the CSV file
    #     table = QTableWidget()

    #     # Load the CSV file into a pandas DataFrame
    #     df = pd.read_csv(file_path)

    #     # Set the table row and column count
    #     table.setRowCount(df.shape[0])
    #     table.setColumnCount(df.shape[1])

    #     # Set the table headers
    #     table.setHorizontalHeaderLabels(df.columns.tolist())

    #     # Populate the table with data
    #     for row in range(df.shape[0]):
    #         for col in range(df.shape[1]):
    #             item = QTableWidgetItem(str(df.iat[row, col]))
    #             table.setItem(row, col, item)

    #     # Add the new table to the layout
    #     self.ui.verticalLayout_61.addWidget(table)

    #     # Store the new table in the instance for future reference
    #     setattr(self, table_attr_name, table)

    # def load_csv_to_table(self, file_path):
    #     # Create a new table for each CSV file
    #     table = QTableWidget()

    #     # Load the CSV file into a pandas DataFrame
    #     df = pd.read_csv(file_path)

    #     # Set the table row and column count
    #     table.setRowCount(df.shape[0])
    #     table.setColumnCount(df.shape[1])

    #     # Set the table headers
    #     table.setHorizontalHeaderLabels(df.columns.tolist())

    #     # Populate the table with data
    #     for row in range(df.shape[0]):
    #         for col in range(df.shape[1]):
    #             item = QTableWidgetItem(str(df.iat[row, col]))
    #             table.setItem(row, col, item)

    #     # Add the table to the layout
    #     self.ui.verticalLayout_61.addWidget(table)

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