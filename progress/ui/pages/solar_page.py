from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from progress.ui.forms.solar.ui_solar import Ui_SolarPage 
from progress.ui.forms.solar.ui_solar_results import Ui_SolarResults 
from progress.ui.utils.worker import WorkerThread, ProcessingThread
from progress.paths import get_path, load_config
from progress.mod_solar import Solar
from progress.mod_kmeans import KMeans_Pipeline
from progress.ui.utils.data_handler import DataHandler
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
    def __init__(self, data_handler: DataHandler):
        super().__init__()
        self.ui = Ui_SolarPage()
        self.results_window = SolarResultsPage()
        self.ui.setupUi(self)
        self.data_handler = data_handler
        self._solar: Solar | None = None
        self._kmeans_pipeline: KMeans_Pipeline | None = None

        # STATE FLAG for download solar data to download
        self._cluster_page_unlocked = False

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
            QMessageBox.critical(self, "Value Error", "Number of clusters to evaluate must be greater than 0.")
            return

        if not self.data_handler.solar_directory:
            QMessageBox.critical(self, "No Solar Data", "Please download or provide solar data first.")
            return

        if self._kmeans_pipeline is None:
            site_csv = self.data_handler.solar_directory / 'solar_sites.csv'
            if not site_csv.exists():
                QMessageBox.critical(self, "File Not Found", f"Cannot find solar site data at:\n{site_csv}")
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
        QMessageBox.critical(self, "Evaluation Error", f"Clustering evaluation failed:\n{error_msg}")

    def _generate_clusters(self, checked: bool = False) -> None:
        n_clusters = self.ui.spin_box_final_num_cluster.value()
        if n_clusters <= 0:
            QMessageBox.critical(self, "Value Error", "Number of clusters to generate must be greater than 0.")
            return

        if self._kmeans_pipeline is None:
            QMessageBox.critical(self, "No Pipeline", "Please run the evaluation step first.")
            return

        if self._solar is None:
            QMessageBox.critical(self, "No Solar Instance", "Solar data has not been processed. Please download or provide solar data first.")
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
        QMessageBox.information(self, "Clustering Complete", "Clustering has been completed successfully.")

    def _on_gen_error(self, error_msg: str) -> None:
        self._on_thread_finished("btn_gen_cluster", "Generate")
        QMessageBox.critical(self, "Generation Error", f"Clustering generation failed:\n{error_msg}")

    def _on_thread_finished(self, btn_name: str, btn_text: str) -> None:
        btn = getattr(self.ui, btn_name, None)
        if btn is not None:
            btn.setEnabled(True)
            btn.setText(btn_text)

    def _skip_clustering(self, checked: bool = False) -> None:
        reply = QMessageBox.question(
            self, "Skip Clustering",
            "Are you sure you want to skip clustering?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self._switch_to_data_page()

    # ========= DATA PAGE LOGIC =========
    def _handle_download_solar(self, checked=False) -> None:
        # download logic here
        self._cluster_page_unlocked = True
        self._update_page_navigation_ui(self.ui.solarStackedWidget.currentIndex())
        self.ui.frame_data_nav.setVisible(True)

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

        self.ui.btn_download_solar.setEnabled(False)
        self.ui.btn_download_solar.setText("Downloading...")
        QApplication.processEvents()

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Downloading Solar Data")
        msg.setText(
            "The latest solar data must be downloaded before continuing.\n\n"
            "We’re downloading the latest solar data. The app may pause briefly and will resume automatically when the download is complete.\n\n"
        )
        msg.setStandardButtons(QMessageBox.Ok)
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

        self._download_thread = WorkerThread(self._solar.run_pipeline, start_year, end_year)
        self._download_thread.start()

        self._download_thread.success.connect(self._on_download_success)
        self._download_thread.error.connect(self._on_download_error)


    def _on_download_success(self) -> None:
        self._cluster_page_unlocked = True
        self._update_page_navigation_ui(self.ui.solarStackedWidget.currentIndex())
        self.ui.btn_download_solar.setEnabled(True)
        self.ui.btn_download_solar.setText("Download Solar Data")
        QMessageBox.information(self, "Solar Data Download", "Successfully downloaded/processed data can proceed to clustering page if needed")

    def _on_download_error(self, error_msg: str) -> None:
        self.ui.btn_download_solar.setEnabled(True)
        self.ui.btn_download_solar.setText("Download Solar Data")
        QMessageBox.critical(self, "Download Error", f"Solar data download failed:\n{error_msg}")

    def _update_page_navigation_ui(self, _index: int) -> None:
        current_page = self.ui.solarStackedWidget.currentWidget()

        self.ui.btn_data_page.setEnabled(current_page is not self.ui.page_data)
        self.ui.btn_clusters_page.setEnabled(
            self._cluster_page_unlocked and current_page is not self.ui.page_cluster
        )
    def _on_data_source_changed(self, _index: int) -> None:
        self._update_solar_page_options()

    def _validate_user_data(self, checked: bool = False) -> None:
        QMessageBox.information(self, "User Solar Data Validation", "User Solar Data is validated good to proceed.")
        self._cluster_page_unlocked = True
        self._update_page_navigation_ui(self.ui.solarStackedWidget.currentIndex())
        self._run_solar_processing()   

    def _run_solar_processing(self) -> None:
        config = load_config()
        solar_dir = Path(config['data']) / 'Solar'
        self._solar = Solar(str(solar_dir), config['model'])
        self.data_handler.solar_directory = solar_dir
        self._processing_thread = WorkerThread(self._solar.run_pipeline_gui)
        self._processing_thread.start()

    def _display_start_year_info(self, checked: bool = False) -> None:
         QMessageBox.information(self, "ERA5 Start Year", "Start year for Solar data download.")

    def _display_end_year_info(self, checked: bool = False) -> None:
         QMessageBox.information(self, "ERA5 End Year", "End year for Solar data download.")

    def _display_cluster_help(self):
        QMessageBox.information(self, "Clusters Help", "This step finds the optimum number of clusters to evaluate.")

    def _display_cluster_final_help(self):
        QMessageBox.information(self, "Clusters Final Help", "This step allows you to save the optimum number of clusters to evaluate you observe from the results.")

    def _display_skip_btn_info(self):
        QMessageBox.information(self, "Solar Help", "You can skip this step if your solar power generation data has previously been clustered.")

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
