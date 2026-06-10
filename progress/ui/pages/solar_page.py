from PySide6.QtWidgets import QWidget, QVBoxLayout
from progress.ui.forms.solar.ui_solar import Ui_SolarPage 
from progress.ui.forms.solar.ui_solar_results import Ui_SolarResults 

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

        # self.ui.btn_download_solar.hide()
        # self.ui/btn_download_solar.setVisible(False)
        self.ui.btn_download_solar.setText("Upload Data")

        # UI initialization
        self.ui.spin_box_num_cluster.setValue(0)
        self.ui.solarStackedWidget.setCurrentIndex(0)
        self.ui.btn_eval_cluster.clicked.connect(self._open_cluster_results)


    def _switch_to_cluster_page(self) -> None:
        self.ui.solarStackedWidget.setCurrentIndex(1)

    def _switch_to_data_page(self) -> None:
        self.ui.solarStackedWidget.setCurrentIndex(0)

    def _open_cluster_results(self) -> None:
        self.results_window.show()
