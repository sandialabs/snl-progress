from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Signal
from progress.ui.utils.worker import WorkerThread, ProcessingThread
from progress.ui.forms.wind.ui_wind import Ui_WindPage
from progress.paths import get_path, load_config
from progress.mod_wind import Wind
from progress.ui.utils.data_handler import DataHandler
from progress.utils.data_validator import validate_domain
from pathlib import Path
import datetime
import pandas as pd
import numpy as np
import yaml
import logging

logger = logging.getLogger(__name__)

class WindPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindPage()
        self.ui.setupUi(self)
        self.data_handler = DataHandler
        self._wind: Wind | None = None

        self.ui.frame_process_wind.setVisible(False)
        self.ui.frame_date_range.setVisible(False)
        self.ui.frame_btns_data.setVisible(False)
        self.ui.btn_download_wind.clicked.connect(self._handle_download_wind)
        self.ui.btn_process_info.clicked.connect(self._display_wind_process_info)
        self.ui.combo_data_source.currentIndexChanged.connect(self._on_data_source_changed)
        self.ui.btn_start_info.clicked.connect(self._display_start_year_info)
        self.ui.btn_end_info.clicked.connect(self._display_end_year_info)
        self.ui.btn_validate_own_data.clicked.connect(self._validate_user_data)
        self.ui.btn_process_wind.clicked.connect(self._handle_process_wind)

        # ========= INIT VALUES =========
        self.start_year: int = 2020
        self.end_year: int = 2021

    # ========= DATA PAGE LOGIC =========

    def _display_start_year_info(self, checked: bool = False) -> None:
         QMessageBox.information(self, "ERA5 Start Year", "Start year for Wind data download.")

    def _display_end_year_info(self, checked: bool = False) -> None:
         QMessageBox.information(self, "ERA5 End Year", "End year for Wind data download.")

    def _display_wind_process_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Wind Process Help", "Wind speed data (downloaded or user-provided) is utilized to generate transition rate matrix in this step. You can skip this step if you already have the required matrix.")

    def _on_data_source_changed(self, _index: int) -> None:
        self._update_wind_page_options()

    def _update_wind_page_options(self) -> None:
        selection = self.ui.combo_data_source.currentText()

        if selection == "Use Your Own Data":
            self.ui.label_hint_selection.setVisible(False)
            self.ui.frame_date_range.setVisible(False)
            self.ui.frame_btns_data.setVisible(True)
            self.ui.frame_process_wind.setVisible(False)
            self.ui.btn_download_wind.setVisible(False)
            self.ui.btn_validate_own_data.setVisible(True)
        elif selection == "Download Wind Data from ERA5":
            self.ui.label_hint_selection.setVisible(False)
            self.ui.frame_btns_data.setVisible(True)
            self.ui.frame_date_range.setVisible(True)
            self.ui.btn_download_wind.setVisible(True)
            self.ui.btn_validate_own_data.setVisible(False)
        elif selection == "No Wind Data":
            self.ui.label_hint_selection.setVisible(False)
            self.ui.frame_btns_data.setVisible(False)
            self.ui.frame_date_range.setVisible(False)
        else:
            self.ui.label_hint_selection.setVisible(True)
            self.ui.frame_btns_data.setVisible(False)
            self.ui.frame_date_range.setVisible(False)
            self.ui.btn_download_wind.setVisible(False)
            self.ui.btn_validate_own_data.setVisible(False)

    def _handle_download_wind(self, checked=False) -> None:
        current_year = datetime.datetime.now().year
        try:
            self.start_year = int(self.ui.line_edit_start.text().strip())
        except ValueError:
            self.start_year = current_year
            logger.warning("Start year was empty or invalid. Defaulting to current year.")
            QMessageBox.critical(self, "Value Error", "End year was empty or invalid. Defaulting to current year, please enter a valid year.")
            return 

        try:
            self.end_year = int(self.ui.line_edit_end.text().strip())
            if self.end_year < self.start_year:
                logger.warning("End year was before start year. Defaulting to current year.")
                self.end_year = current_year
                QMessageBox.critical(self, "Value Error", "End year cannot be earlier than start year.")
                self.ui.line_edit_end.clear()
                return 

        except ValueError:
            self.end_year = current_year
            QMessageBox.critical(self, "Value Error", "End year was empty or invalid. Defaulting to current year, please enter a valid year.")
            logger.warning("End year was empty or invalid. Defaulting to current year, please enter a valid year.")
            return
        
        self.ui.btn_download_wind.setEnabled(False)
        self.ui.btn_download_wind.setText("Downloading...")

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Downloading Wind Data")
        msg.setText(
            "The latest wind data must be downloaded before continuing.\n\n"
            "We’re downloading the latest wind data. The app may pause briefly and will resume automatically when the download is complete.\n\n"
        )
        msg.setStandardButtons(QMessageBox.Ok)
        result = msg.exec_()

        if result == QMessageBox.Ok:
            self._run_wind_download(self.start_year, self.end_year)
        logger.info(f"Wind Start Year Value: {self.start_year}")
        logger.info(f"Wind End Year Value: {self.end_year}")

    def _run_wind_download(self, start_year: int, end_year: int) -> None:
        config = load_config()
        wind_dir = Path(config['data']) / 'Wind'
        self.data_handler.wind_directory = wind_dir
        self._wind = Wind(str(wind_dir))
        
        self._download_thread = WorkerThread(
            self._wind.DownloadWindData,
            start_year, 
            end_year
        )

        self._download_thread.success.connect(self._on_wind_download_success)
        self._download_thread.error.connect(self._on_wind_download_error)
        self._download_thread.start()

    def _on_wind_download_success(self) -> None:
        self.ui.btn_download_wind.setEnabled(True)
        self.ui.btn_download_wind.setText("Download Wind Data")
        self.ui.frame_process_wind.setVisible(True)
        self.ui.frame_date_range.setVisible(True)
        QMessageBox.critical(self, "Wind Data Download", f"Successfully downloaded data can proceed to process data")

    def _on_wind_download_error(self, error_msg: str) -> None:
        self.ui.btn_download_wind.setEnabled(True)
        self.ui.btn_download_wind.setText("Download Wind Data")
        QMessageBox.critical(self, "Download Error", f"Wind Data download failed:\n{error_msg}")

    def _handle_process_wind(self, checked=False) -> None:
        self.ui.btn_process_wind.setEnabled(False)
        self.ui.btn_process_wind.setText("Processing...")

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Processing Wind Data")
        msg.setText(
            "The wind data must be processed before continuing.\n\n"
        )
        msg.setStandardButtons(QMessageBox.Ok)
        result = msg.exec_()

        if result == QMessageBox.Ok:
            self._run_wind_process()

    def _run_wind_process(self):
        config = load_config()
        wind_dir = Path(config['data']) / 'Wind'
        self.data_handler.wind_directory = wind_dir
        self._wind = Wind(str(wind_dir))
        self.wind_sites: str = str(wind_dir / 'wind_sites.csv')
        self.wind_power_curves: str = str(wind_dir / 'w_power_curves.csv')
        self.windspeed_data: str = str(wind_dir / 'windspeed_data.csv')
        self.wind_tr_rate: str = str(wind_dir / 't_rate.xlsx')

        self._process_thread = WorkerThread(
            self._wind.CalWindTrRates,
            wind_dir,
            self.windspeed_data,
            self.wind_power_curves
        )

        self._process_thread.success.connect(
            lambda: self._on_wind_process_success(self.wind_tr_rate)
        )
        self._process_thread.error.connect(self._on_wind_process_error)
        self._process_thread.start()


    def _on_wind_process_success(self, wind_tr_rate: str) -> None:
        self.ui.btn_process_wind.setEnabled(True)
        self.ui.btn_process_wind.setText("Process Wind Data")
        tr_mats = pd.read_excel(wind_tr_rate, sheet_name=None)
        self.data_handler.tr_mats = np.array([tr_mats[sheet].to_numpy() for sheet in tr_mats])
        logger.info("Successfully processed data can proceed to simulation")
        QMessageBox.critical(self, "Wind Data Download", f"Successfully processed data can proceed to simulation")

    def _on_wind_process_error(self, error_msg: str) -> None:
        self.ui.btn_process_wind.setEnabled(True)
        self.ui.btn_process_wind.setText("Process Wind Data")
        QMessageBox.critical(self, "Process Error", f"Wind Data process failed:\n{error_msg}")

    def _validate_user_data(self, checked: bool = False) -> None:
        config = load_config()
        data_dir = Path(config['data'])
        errors, warnings = validate_domain(data_dir, "wind")

        if errors:
            msg = "Wind data validation failed:\n\n" + "\n".join(f"• {e}" for e in errors)
            if warnings:
                msg += "\n\nWarnings:\n" + "\n".join(f"• {w}" for w in warnings)
            QMessageBox.critical(self, "Wind Data Validation", msg)
            return

        if warnings:
            msg = "Wind data is valid with warnings:\n\n" + "\n".join(f"• {w}" for w in warnings)
            QMessageBox.warning(self, "Wind Data Validation", msg)
        else:
            QMessageBox.information(self, "Wind Data Validation", "Wind data is valid.")

        self.ui.frame_process_wind.setVisible(True)
    
    def _user_data_run_wind_process(self) -> None:
        config = load_config()
        wind_dir = Path(config['data']) / 'Wind'
        self.data_handler.wind_directory = wind_dir
        self._wind = Wind(str(wind_dir))
        self.wind_sites: str = str(wind_dir / 'wind_sites.csv')
        self.wind_power_curves: str = str(wind_dir / 'w_power_curves.csv')
        self.windspeed_data: str = str(wind_dir / 'windspeed_data.csv')
        self.wind_tr_rate: str = str(wind_dir / 't_rate.xlsx')

        self._process_thread = WorkerThread(
            self._wind.CalWindTrRates,
            wind_dir,
            self.windspeed_data,
            self.wind_power_curves
        )

        self._process_thread.success.connect(
            lambda: self._on_wind_process_user_data_success(self.wind_tr_rate)
        )
        self._process_thread.error.connect(self._on_wind_process_user_data_error)
        self._process_thread.start()

    def _on_wind_process_user_data_success(self, wind_tr_rate: str) -> None:
        self.ui.btn_process_wind.setEnabled(True)
        self.ui.btn_process_wind.setText("Process Wind Data")
        tr_mats = pd.read_excel(wind_tr_rate, sheet_name=None)
        self.data_handler.tr_mats = np.array([tr_mats[sheet].to_numpy() for sheet in tr_mats])
        QMessageBox.critical(self, "Wind Data Download", f"Successfully processed data can proceed to simulation")

    def _on_wind_process_user_data_error(self, error_msg: str) -> None:
        self.ui.btn_process_wind.setEnabled(True)
        self.ui.btn_process_wind.setText("Process Wind Data")
        QMessageBox.critical(self, "Process Error", f"Wind Data process failed:\n{error_msg}")
