from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QApplication
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QPixmap
from progress.ui.forms.solar.ui_solar import Ui_SolarPage 
from progress.ui.forms.solar.ui_solar_results import Ui_SolarResults 
from progress.ui.utils.worker import WorkerThread, ProcessingThread
from progress.paths import get_path, load_config
from progress.mod_solar import Solar
from progress.mod_kmeans import KMeans_Pipeline
from typing import Optional
from progress.ui.utils.data_handler import DataHandler
from progress.utils.data_validator import validate_domain
from progress.ui import msgbox
import yaml
import os
from pathlib import Path
import logging
import datetime

logger = logging.getLogger(__name__)

class SolarResultsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SolarResults()
        self.ui.setupUi(self)

class SolarPage(QWidget):
    clusters_skipped = Signal()
    clusters_generated = Signal()

    def __init__(self, data_handler: DataHandler):
        super().__init__()
        self.ui = Ui_SolarPage()
        self.results_window = SolarResultsPage()
        self.ui.setupUi(self)
        self.data_handler = data_handler
        self._solar: Optional[Solar] = None
        self._kmeans_pipeline: Optional[KMeans_Pipeline] = None
        self._active_threads: list[WorkerThread] = []

        # STATE FLAGS
        self._cluster_page_unlocked = False
        self._clusters_ready = False
        self._processing = False

        # UI initialization
        self.ui.spin_box_num_cluster.setValue(0)
        self.ui.solarStackedWidget.setCurrentIndex(0)
        self.ui.label_hint_selection.setVisible(False)
        self.ui.frame_btns_data.setVisible(False)
        self.ui.frame_data_range.setVisible(False)
        self.ui.frame_data_nav.setVisible(False)
        self.ui.btn_validate_own_data.setVisible(False)
        self.ui.combo_data_source.setCurrentText("-- Select Option --")
        self.ui.label_hint_selection.setVisible(True)

        self.destroyed.connect(self._cleanup_worker_threads)

        # ========= CONNECTIONS =========
        # ---- data page connections ----
        self.ui.solarStackedWidget.currentChanged.connect(self._update_page_navigation_ui)
        self._update_page_navigation_ui(self.ui.solarStackedWidget.currentIndex())
        self.ui.btn_download_solar.clicked.connect(self._handle_download_solar)
        self.ui.btn_validate_own_data.clicked.connect(self._validate_user_data)
        self.ui.btn_data_page.clicked.connect(self._switch_to_data_page)
        self.ui.combo_data_source.currentIndexChanged.connect(self._on_data_source_changed)
        self.ui.btn_clusters_page.clicked.connect(self._switch_to_cluster_page)

        # ---- cluster page connections ----
        self.ui.btn_eval_cluster.clicked.connect(self._evaluate_clusters)
        self.ui.btn_gen_cluster.clicked.connect(self._generate_clusters)
        self.ui.btn_open_results.clicked.connect(self._open_cluster_results)
        self.ui.btn_skip.clicked.connect(self._skip_clustering)
        self.ui.btn_start_info.clicked.connect(self._display_start_year_info)
        self.ui.btn_end_info.clicked.connect(self._display_end_year_info)
        self.ui.btn_info_num_cluster.clicked.connect(self._display_cluster_help)
        self.ui.btn_info_final_num_cluster.clicked.connect(self._display_cluster_final_help)
        self.ui.btn_info_skip.clicked.connect(self._display_skip_btn_info)

        # ========= INIT VALUES =========
        self.start_year: int = 2020
        self.end_year: int = 2021
        self.num_clusters: int = 0
        self.final_num_clusters:int = 0

    # ========= NAVIGATION =========
    def _switch_to_cluster_page(self, checked: bool = False) -> None:
        self.ui.solarStackedWidget.setCurrentWidget(self.ui.page_cluster)

    def _switch_to_data_page(self, checked: bool = False) -> None:
        self.ui.solarStackedWidget.setCurrentWidget(self.ui.page_data)
    
    # ========= CLUSTER PAGE LOGIC =========
    def _open_cluster_results(self, checked: bool = False) -> None:
        self.results_window.show()

    def _evaluate_clusters(self, checked: bool = False) -> None:
        clust_eval = self.ui.spin_box_num_cluster.value()
        if clust_eval <= 0:
            msgbox.critical(self, "Value Error", "Number of clusters to evaluate must be greater than 0.")
            return

        if not self.data_handler.solar_directory:
            msgbox.critical(self, "No Solar Data", "Please download or provide solar data first.")
            return

        if self._kmeans_pipeline is None:
            site_csv = self.data_handler.solar_directory / 'solar_sites.csv'
            if not site_csv.exists():
                msgbox.critical(self, "File Not Found", f"Cannot find solar site data at:\n{site_csv}")
                return
            self._kmeans_pipeline = KMeans_Pipeline(self.data_handler.solar_directory, site_csv)

        self.ui.btn_eval_cluster.setEnabled(False)
        self.ui.btn_eval_cluster.setText("Evaluating...")
        QApplication.processEvents()

        self._eval_thread = WorkerThread(self._kmeans_pipeline.test_metrics, clust_eval)
        self._eval_thread.success.connect(self._on_eval_done)
        self._eval_thread.error.connect(self._on_eval_error)
        self._eval_thread.start()

    def _on_eval_done(self) -> None:
        self._on_thread_finished("btn_eval_cluster", "Evaluate")
        sse_path = self.data_handler.solar_directory / 'SSE_Curve.png'
        if sse_path.exists():
            pixmap = QPixmap(sse_path)
            self.results_window.ui.label_solar_plot.setPixmap(pixmap)
        results_path = self.data_handler.solar_directory / 'clustering_results.txt'
        if results_path.exists():
            with open(results_path) as f:
                text = f.read()
            self.results_window.ui.text_solar_results.setPlainText(text)
        self.results_window.show()

    def _on_eval_error(self, error_msg: str) -> None:
        self._on_thread_finished("btn_eval_cluster", "Evaluate")
        msgbox.critical(self, "Evaluation Error", f"Clustering evaluation failed:\n{error_msg}")

    def _generate_clusters(self, checked: bool = False) -> None:
        n_clusters = self.ui.spin_box_final_num_cluster.value()
        if n_clusters <= 0:
            msgbox.critical(self, "Value Error", "Number of clusters to generate must be greater than 0.")
            return

        if self._kmeans_pipeline is None:
            msgbox.critical(self, "No Pipeline", "Please run the evaluation step first.")
            return

        if self._solar is None:
            msgbox.critical(self, "No Solar Instance", "Solar data has not been processed. Please download or provide solar data first.")
            return

        self.ui.btn_gen_cluster.setEnabled(False)
        self.ui.btn_gen_cluster.setText("Generating...")
        QApplication.processEvents()

        def generate_wrapper():
            self._kmeans_pipeline.run(n_clusters=n_clusters)
            self._kmeans_pipeline.calculate_cluster_probability()
            self._kmeans_pipeline.split_and_cluster_data()
            solar_prob_path = self.data_handler.solar_directory / 'solar_probs.csv'
            self._solar.GetSolarProfiles(solar_prob_path)

        self._gen_thread = WorkerThread(generate_wrapper)
        self._gen_thread.success.connect(self._on_gen_done)
        self._gen_thread.error.connect(self._on_gen_error)
        self._gen_thread.start()

    def _on_gen_done(self) -> None:
        self._on_thread_finished("btn_gen_cluster", "Generate")
        self._clusters_ready = True
        self.clusters_generated.emit()
        msgbox.information(self, "Clustering Complete", "Clustering has been completed successfully.")

    def _on_gen_error(self, error_msg: str) -> None:
        self._on_thread_finished("btn_gen_cluster", "Generate")
        msgbox.critical(self, "Generation Error", f"Clustering generation failed:\n{error_msg}")

    def _on_thread_finished(self, btn_name: str, btn_text: str) -> None:
        btn = getattr(self.ui, btn_name, None)
        if btn is not None:
            btn.setEnabled(True)
            btn.setText(btn_text)

    def _check_clusters_exist(self) -> bool:
        solar_dir = self.data_handler.solar_directory
        if not solar_dir:
            return False
        clusters_dir = solar_dir / 'Clusters'
        if not clusters_dir.exists() or not clusters_dir.is_dir():
            return False
        try:
            return any(clusters_dir.iterdir())
        except (PermissionError, OSError):
            return False

    def _skip_clustering(self, checked: bool = False) -> None:
        reply = msgbox.question(
            self, "Skip Clustering",
            "Are you sure you want to skip clustering?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            if not self._check_clusters_exist():
                msgbox.critical(
                    self, "Clusters Not Found",
                    "Cannot skip clustering. No pre-existing cluster data was found.\n\n"
                    "Please generate clusters first, or place your existing cluster files "
                    "in the 'Clusters' directory under your solar data folder."
                )
                return
            self._clusters_ready = True
            self.clusters_skipped.emit()

    # ========= THREAD LIFECYCLE HELPERS =========
    def _track_thread(self, thread: WorkerThread) -> None:
        self._active_threads.append(thread)
        thread.finished.connect(lambda t=thread: self._active_threads.remove(t))

    def _stop_thread(self, thread: Optional[WorkerThread]) -> None:
        if thread is not None and thread.isRunning():
            thread.quit()
            thread.wait(3000)

    def _cleanup_worker_threads(self) -> None:
        for t in list(self._active_threads):
            if t.isRunning():
                t.quit()
                t.wait(3000)

    # ========= DATA PAGE LOGIC =========
    def _handle_download_solar(self, checked=False) -> None:
        self.ui.frame_data_nav.setVisible(True)
        self._processing = True

        current_year = datetime.datetime.now().year
        try:
            self.start_year = int(self.ui.line_edit_start.text().strip())
        except ValueError:
            self.start_year = current_year
            logger.warning("Start year was empty or invalid. Defaulting to current year.")
            msgbox.critical(self, "Value Error", "End year was empty or invalid. Defaulting to current year, please enter a valid year.")
            return 

        try:
            self.end_year = int(self.ui.line_edit_end.text().strip())
            if self.end_year < self.start_year:
                logger.warning("End year was before start year. Defaulting to current year.")
                self.end_year = current_year
                msgbox.critical(self, "Value Error", "End year cannot be earlier than start year.")
                self.ui.line_edit_end.clear()
                return 

        except ValueError:
            self.end_year = current_year
            msgbox.critical(self, "Value Error", "End year was empty or invalid. Defaulting to current year, please enter a valid year.")
            logger.warning("End year was empty or invalid. Defaulting to current year, please enter a valid year.")
            return

        self.ui.btn_download_solar.setEnabled(False)
        self.ui.btn_download_solar.setText("Downloading...")
        QApplication.processEvents()

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Downloading Solar Data")
        msg.setText(
            "We're downloading the requested solar data. The app may pause briefly and will resume automatically when the download is complete.\n\n"
        )
        msg.setStandardButtons(QMessageBox.Ok)
        style = msgbox._current_style()
        if style:
            msg.setStyleSheet(style)
        result = msg.exec_()

        if result == QMessageBox.Ok:
            self._run_solar_download(self.start_year, self.end_year)
        logger.info(f"Solar Start Year Value: {self.start_year}")
        logger.info(f"Solar End Year Value: {self.end_year}")

    def _run_solar_download(self, start_year: int, end_year: int) -> None:
        config = load_config()
        solar_dir = Path(config['data']) / 'Solar'
        self._solar = Solar(str(solar_dir), config['model'])
        self.data_handler.solar_directory = solar_dir

        self._stop_thread(getattr(self, '_download_thread', None))
        self._download_thread = WorkerThread(self._solar.run_pipeline, start_year, end_year)
        self._download_thread.success.connect(self._on_download_success)
        self._download_thread.error.connect(self._on_download_error)
        self._track_thread(self._download_thread)
        self._download_thread.start()


    def _on_download_success(self) -> None:
        self._processing = False
        self._cluster_page_unlocked = True
        self._update_page_navigation_ui(self.ui.solarStackedWidget.currentIndex())
        self.ui.btn_download_solar.setEnabled(True)
        self.ui.btn_download_solar.setText("Download Solar Data")
        msgbox.information(self, "Solar Data Download", "Successfully downloaded and processed solar data. Ready to proceed to the clustering page.")

    def _on_download_error(self, error_msg: str) -> None:
        self._processing = False
        self.ui.btn_download_solar.setEnabled(True)
        self.ui.btn_download_solar.setText("Download Solar Data")
        msgbox.critical(self, "Download Error", f"Solar data download failed:\n{error_msg}")

    def _update_page_navigation_ui(self, _index: int) -> None:
        current_page = self.ui.solarStackedWidget.currentWidget()

        self.ui.btn_data_page.setEnabled(current_page is not self.ui.page_data)
        self.ui.btn_clusters_page.setEnabled(
            self._cluster_page_unlocked and not self._processing and current_page is not self.ui.page_cluster
        )
    def is_ready_for_simulation(self) -> bool:
        if self._processing:
            return False
        selection = self.ui.combo_data_source.currentText()
        if selection == "No Solar Data":
            return True
        return self._clusters_ready

    def _on_data_source_changed(self, _index: int) -> None:
        self._update_solar_page_options()
        if self.ui.combo_data_source.currentText() == "No Solar Data":
            self.clusters_generated.emit()

    def _validate_user_data(self, checked: bool = False) -> None:
        config = load_config()
        data_dir = Path(config['data'])
        errors, warnings = validate_domain(data_dir, "solar")

        if errors:
            msg = "Solar data validation failed:\n\n" + "\n".join(f"• {e}" for e in errors)
            if warnings:
                msg += "\n\nWarnings:\n" + "\n".join(f"• {w}" for w in warnings)
            msgbox.critical(self, "Solar Data Validation", msg)
            return

        if warnings:
            msg = "Solar data is valid with warnings:\n\n" + "\n".join(f"• {w}" for w in warnings)
            msgbox.warning(self, "Solar Data Validation", msg)

        solar_dir = data_dir / 'Solar'
        gen_all_sites_path = solar_dir / 'gen_all_sites.csv'

        if gen_all_sites_path.exists():
            self._solar = Solar(str(solar_dir), config['model'])
            self.data_handler.solar_directory = solar_dir
            self._cluster_page_unlocked = True
            self._update_page_navigation_ui(self.ui.solarStackedWidget.currentIndex())
            msgbox.information(self, "Solar Data Validation",
                "Solar data is valid.\n\nSolar generation data (gen_all_sites.csv) already exists. Ready to proceed to clustering.")
            return

        weather_dir = solar_dir / 'solar_weather_data'
        has_weather_data = weather_dir.exists() and any(weather_dir.glob('*.csv'))

        if has_weather_data:
            msgbox.information(self, "Solar Data Validation",
                "Solar data is valid.\n\nProcessing weather data into solar generation profiles. Please wait for the process to complete, then proceed to the clustering page.")
            self._processing = True
            self._update_page_navigation_ui(self.ui.solarStackedWidget.currentIndex())
            self._run_solar_processing()
        else:
            msgbox.warning(self, "Solar Data Validation",
                "Solar data is valid, but solar generation data (gen_all_sites.csv) was not found and "
                "no weather data is available to generate it.\n\n"
                "Please either:\n"
                "• Download weather data using 'Download Solar Data', or\n"
                "• Place gen_all_sites.csv directly in the Solar directory.")

    def _run_solar_processing(self) -> None:
        config = load_config()
        solar_dir = Path(config['data']) / 'Solar'
        self._solar = Solar(str(solar_dir), config['model'])
        self.data_handler.solar_directory = solar_dir

        self._stop_thread(getattr(self, '_processing_thread', None))
        self._processing_thread = WorkerThread(self._solar.run_pipeline_gui)
        self._processing_thread.success.connect(self._on_processing_success)
        self._processing_thread.error.connect(self._on_processing_error)
        self._track_thread(self._processing_thread)
        self._processing_thread.start()

    def _on_processing_success(self) -> None:
        self._processing = False
        self._cluster_page_unlocked = True
        self._update_page_navigation_ui(self.ui.solarStackedWidget.currentIndex())
        msgbox.information(self, "Solar Processing", "Solar data processing completed.")

    def _on_processing_error(self, error_msg: str) -> None:
        self._processing = False
        msgbox.critical(self, "Solar Processing Error",
            f"Solar data processing failed:\n{error_msg}\n\n"
            "This typically means weather data files (solar_weather_data/*_gen.csv) are missing. "
            "Please download weather data first using 'Download Solar Data'.")

    def _display_start_year_info(self, checked: bool = False) -> None:
         msgbox.information(self, "ERA5 Start Year", "Start year for Solar data download.")

    def _display_end_year_info(self, checked: bool = False) -> None:
         msgbox.information(self, "ERA5 End Year", "End year for Solar data download.")

    def _display_cluster_help(self):
        msgbox.information(self, "Clusters Help", "This step finds the optimum number of clusters to evaluate.")

    def _display_cluster_final_help(self):
        msgbox.information(self, "Clusters Final Help", "This step allows you to save the optimum number of clusters to evaluate you observe from the results.")

    def _display_skip_btn_info(self):
        msgbox.information(self, "Solar Help", "You can skip this step if your solar power generation data has previously been clustered.")

    def _update_solar_page_options(self) -> None:
        selection = self.ui.combo_data_source.currentText()
    
        if selection == "Use Your Own Data":
            self.ui.label_hint_selection.setVisible(False)
            self.ui.frame_btns_data.setVisible(False)
            self.ui.frame_data_range.setVisible(False)
            self.ui.frame_data_nav.setVisible(True)
            self.ui.btn_validate_own_data.setVisible(True)
        elif selection == "Download Solar Data from ERA5":
            self.ui.label_hint_selection.setVisible(False)
            self.ui.frame_btns_data.setVisible(True)
            self.ui.frame_data_range.setVisible(True)
            self.ui.frame_data_nav.setVisible(True)
            self.ui.btn_validate_own_data.setVisible(False)
        elif selection == "No Solar Data":
            self.ui.label_hint_selection.setVisible(False)
            self.ui.frame_btns_data.setVisible(False)
            self.ui.frame_data_range.setVisible(False)
            self.ui.frame_data_nav.setVisible(False)
            self.ui.btn_validate_own_data.setVisible(False)
            self._cluster_page_unlocked = False
        else:
            self.ui.label_hint_selection.setVisible(True)
            self.ui.frame_data_nav.setVisible(False)
            self.ui.frame_btns_data.setVisible(False)
            self.ui.frame_data_range.setVisible(False)
            self.ui.btn_validate_own_data.setVisible(False)
            self._cluster_page_unlocked = False

        self._update_page_navigation_ui(self.ui.solarStackedWidget.currentIndex())
