from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Signal
from progress.ui.forms.solar.ui_solar import Ui_SolarPage 
from progress.ui.forms.solar.ui_solar_results import Ui_SolarResults 
from enum import Enum 

class SolarResultsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SolarResults()
        self.ui.setupUi(self)

class SolarPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SolarPage()
        self.results_window = SolarResultsPage()
        self.ui.setupUi(self)

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
        # connections
        self.ui.solarStackedWidget.currentChanged.connect(self._update_page_navigation_ui)
        self._update_page_navigation_ui(self.ui.solarStackedWidget.currentIndex())
        self.ui.btn_download_solar.clicked.connect(self._handle_download_solar)
        self.ui.btn_eval_cluster.clicked.connect(self._open_cluster_results)
        self.ui.btn_data_page.clicked.connect(self._switch_to_data_page)
        self.ui.btn_clusters_page.clicked.connect(self._switch_to_cluster_page)
        self.ui.combo_data_source.currentIndexChanged.connect(self._on_data_source_changed)
        self.ui.btn_start_info.clicked.connect(self._display_start_year_info)
        self.ui.btn_end_info.clicked.connect(self._display_end_year_info)
        self.ui.btn_info_num_cluster.clicked.connect(self._display_cluster_help)
        self.ui.btn_info_final_num_cluster.clicked.connect(self._display_cluster_final_help)
        self.ui.btn_info_skip.clicked.connect(self._display_skip_btn_info)
        self.ui.btn_validate_own_data.clicked.connect(self._validate_user_data)

    def _switch_to_cluster_page(self, checked: bool = False) -> None:
        self.ui.solarStackedWidget.setCurrentWidget(self.ui.page_cluster)

    def _switch_to_data_page(self, checked: bool = False) -> None:
        self.ui.solarStackedWidget.setCurrentWidget(self.ui.page_data)
    
    def _open_cluster_results(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Clustering Metrics", "Press OK to continue. This may take a few minutes.")
        self.results_window.show()

    def _handle_download_solar(self, checked=False) -> None:
        # download logic here
        self._cluster_page_unlocked = True
        self._update_page_navigation_ui(self.ui.solarStackedWidget.currentIndex())
        self.ui.frame_data_nav.setVisible(True)

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
