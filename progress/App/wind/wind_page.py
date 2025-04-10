from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog
from progress.App.wind.ui.ui_wind_gui import Ui_wind_widget
from PySide6.QtCore import Signal
from progress.mod_wind import Wind
import pandas as pd
import numpy as np
import os
from progress.App.gui_tools.tools import WorkerThread, StdoutBuffer

from progress.paths import get_path
base_dir = get_path()

class wind_form(QWidget, Ui_wind_widget):
    """Landing page widget."""

    page_changer_next = Signal()
    page_changer_previous = Signal()

    def __init__(self, data_handler, parent=None):
        """Sets up the UI file to show in the application"""
        super(wind_form, self).__init__(parent)
        self.setupUi(self)

        self.data_handler = data_handler
        # # button connections in tab widget "wind"
        self.pushButton_DI_next_3.clicked.connect(lambda: self.page_changer_next.emit())
        self.pushButton_DI_previous_3.clicked.connect(lambda: self.page_changer_previous.emit())
        self.widget_9.setVisible(False)
        self.pushButton_4.setVisible(False)
        self.pushButton_7.setVisible(False)
        self.textBrowser_3.setVisible(False)
        self.pushButton_wind_upload.setVisible(False)
        self.pushButton_DI_next_3.setVisible(False)
        self.pushButton_help_wind.setVisible(False)
        self.comboBox_3.currentIndexChanged.connect(self.wind_cb_changed)
        self.pushButton_wind_upload.clicked.connect(self.upload_wind_data)
        self.pushButton_help_wind.clicked.connect(self.wind_process_help)
        self.pushButton_4.clicked.connect(self.download_wind_data)
        self.pushButton_7.clicked.connect(self.process_existing_wdata)
        self.wind_directory = os.path.join(base_dir, "Data", "Wind")
        self.data_handler.set_wind_directory(self.wind_directory)

    def wind_cb_changed(self, index):
        if index == 1:
            self.widget_9.setVisible(True)
            self.pushButton_4.setVisible(True)
            self.pushButton_7.setVisible(False)
        elif index == 2:
            self.pushButton_help_wind.setVisible(True)
            self.pushButton_DI_next_3.setVisible(True)
            self.widget_9.setVisible(False)
            self.pushButton_4.setVisible(False)
            self.pushButton_wind_upload.setVisible(True)
        elif index == 3:
            self.data_handler.set_wind_directory(False)
            self.pushButton_DI_next_3.setVisible(True)

    def upload_wind_data(self):

        self.wind_directory = QFileDialog.getExistingDirectory(self, "Select Directory", base_dir)
        self.data_handler.set_wind_directory(self.wind_directory)
        self.wind_site_data = self.wind_directory+"/wind_sites.csv"
        self.pcurve_data = self.wind_directory+"/w_power_curves.csv"
        wind = Wind()
        self.w_sites, self.farm_name, self.zone_no, self.w_classes, self.w_turbines, self.r_cap, self.p_class, \
            self.out_curve2, self.out_curve3, self.start_speed = wind.WindFarmsData(self.wind_site_data, self.pcurve_data)

        self.data_handler.set_w_sites(self.w_sites)
        self.data_handler.set_farm_name(self.farm_name)
        self.data_handler.set_zone_no(self.zone_no)
        self.data_handler.set_w_classes(self.w_classes)
        self.data_handler.set_w_turbines(self.w_turbines)
        self.data_handler.set_r_cap(self.r_cap)
        self.data_handler.set_p_class(self.p_class)
        self.data_handler.set_out_curve2(self.out_curve2)
        self.data_handler.set_out_curve3(self.out_curve3)
        self.data_handler.set_start_speed(self.start_speed)

        wind_tr_rate = self.wind_directory + '/t_rate.xlsx'

        if os.path.exists(wind_tr_rate):
            self.tr_mats = pd.read_excel(wind_tr_rate, sheet_name=None)
            self.tr_mats = np.array([self.tr_mats[sheet_name].to_numpy() for sheet_name in self.tr_mats])
            self.data_handler.set_tr_mats(self.tr_mats)
        else:
            QMessageBox.information(self, "Transition Matrix", "Transition rate matrix does not exist. Please process wind speed data first.")

        QMessageBox.information(self, "Wind Upload", "Wind data uploaded and saved!")

        self.pushButton_7.setVisible(True)
        self.pushButton_DI_next_3.setVisible(True)

    def wind_process_help(self):

        QMessageBox.information(self, "Wind Process Help", "Wind speed data (downloaded or user-provided) is utilized to generate transition rate matrix in this step. You can skip this step if you already have the required matrix.")


    def download_wind_data(self):

        self.textBrowser_3.setVisible(True)

        self.input_starty_w = int(self.lineEdit_22.text())
        self.input_endy_w = int(self.lineEdit_23.text())

        self.wind_site_data = self.wind_directory+"/wind_sites.csv"
        self.pcurve_data = self.wind_directory+"/w_power_curves.csv"

        wind = Wind()
        self.w_sites, self.farm_name, self.zone_no, self.w_classes, self.w_turbines, self.r_cap, self.p_class, \
            self.out_curve2, self.out_curve3, self.start_speed = wind.WindFarmsData(self.wind_site_data, self.pcurve_data)

        self.data_handler.set_w_sites(self.w_sites)
        self.data_handler.set_farm_name(self.farm_name)
        self.data_handler.set_zone_no(self.zone_no)
        self.data_handler.set_w_classes(self.w_classes)
        self.data_handler.set_w_turbines(self.w_turbines)
        self.data_handler.set_r_cap(self.r_cap)
        self.data_handler.set_p_class(self.p_class)
        self.data_handler.set_out_curve2(self.out_curve2)
        self.data_handler.set_out_curve3(self.out_curve3)
        self.data_handler.set_start_speed(self.start_speed)

        # Create a worker thread for the DownloadWindData method
        self.download_thread = WorkerThread(wind.DownloadWindData, self.wind_directory, self.wind_site_data, self.data_handler.input_api, self.data_handler.input_email, \
                                            self.data_handler.input_aff, self.input_starty_w, self.input_endy_w)

        self.download_thread.output_updated.connect(lambda text: self.handle_output(self.textBrowser_3, text))
        # Connect the finished signal to handle thread completion
        self.download_thread.finished.connect(lambda: self.cal_wind_tr_rates())

        # Start the worker thread
        self.download_thread.start()

        self.pushButton_DI_next_3.setVisible(True)
        self.pushButton_7.setVisible(True)

    def cal_wind_tr_rates(self):
        self.windspeed_data = self.wind_directory+"/windspeed_data.csv"
        self.wind_site_data = self.wind_directory+"/wind_sites.csv"
        self.pcurve_data = self.wind_directory+"/w_power_curves.csv"
        wind = Wind()
        self.w_sites, self.farm_name, self.zone_no, self.w_classes, self.w_turbines, self.r_cap, self.p_class, \
            self.out_curve2, self.out_curve3, self.start_speed = wind.WindFarmsData(self.wind_site_data, self.pcurve_data)

        self.data_handler.set_w_sites(self.w_sites)
        self.data_handler.set_farm_name(self.farm_name)
        self.data_handler.set_zone_no(self.zone_no)
        self.data_handler.set_w_classes(self.w_classes)
        self.data_handler.set_w_turbines(self.w_turbines)
        self.data_handler.set_r_cap(self.r_cap)
        self.data_handler.set_p_class(self.p_class)
        self.data_handler.set_out_curve2(self.out_curve2)
        self.data_handler.set_out_curve3(self.out_curve3)
        self.data_handler.set_start_speed(self.start_speed)

        # calculate transition rates
        wind.CalWindTrRates(self.wind_directory, self.windspeed_data, self.wind_site_data, self.pcurve_data)

        # QMessageBox.information(self, "Processing Complete", "Wind data processing complete!")

        # self.pushButton_DI_next_3.setVisible(True)

    def download_finished(self):
        wind_tr_rate = self.wind_directory + '/t_rate.xlsx'
        self.tr_mats = pd.read_excel(wind_tr_rate, sheet_name=None)
        self.tr_mats = np.array([self.tr_mats[sheet_name].to_numpy() for sheet_name in self.tr_mats])
        self.data_handler.set_tr_mats(self.tr_mats)
        self.pushButton_DI_next_3.setVisible(True)

    def process_existing_wdata(self):

        self.textBrowser_3.setVisible(False)
        self.cal_wind_tr_rates()
        self.download_finished()
        QMessageBox.information(self, "Existing Wind Data", "Processed!")
        self.pushButton_DI_next_3.setVisible(True)

    def handle_output(self, text_browser, text):
        # Update the GUI with the output text
        text_browser.append(text)
