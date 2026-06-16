from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Signal
from progress.ui.forms.wind.ui_wind import Ui_WindPage

class WindPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_WindPage()
        self.ui.setupUi(self)

        self.ui.btn_process_wind.setVisible(False)
        self.ui.frame_date_range.setVisible(False)
        self.ui.frame_btns_data.setVisible(False)
        self.ui.btn_download_wind.clicked.connect(self._display_process_data_btn)
        self.ui.combo_data_source.currentIndexChanged.connect(self._on_data_source_changed)
        self.ui.btn_start_info.clicked.connect(self._display_start_year_info)
        self.ui.btn_end_info.clicked.connect(self._display_end_year_info)
        self.ui.btn_validate_own_data.clicked.connect(self._validate_user_data)
        self.ui.btn_process_wind.clicked.connect(self._display_processed_data)

    def _display_process_data_btn(self) -> None:
        self.ui.btn_process_wind.setVisible(True)

    def _validate_user_data(self, checked: bool = False) -> None:
        QMessageBox.information(self, "User Wind Data Validation", "User Wind Data is validated good to proceed.")

    def _display_start_year_info(self, checked: bool = False) -> None:
         QMessageBox.information(self, "ERA5 Start Year", "Start year for Wind data download.")

    def _display_end_year_info(self, checked: bool = False) -> None:
         QMessageBox.information(self, "ERA5 End Year", "End year for Wind data download.")

    def _display_processed_data(self, checked: bool = False) -> None:
        QMessageBox.information(self, "ERA5 Data Processed Alert", "Data processed and ready to go!")

    def _on_data_source_changed(self, _index: int) -> None:
        self._update_wind_page_options()

    def _update_wind_page_options(self) -> None:
        selection = self.ui.combo_data_source.currentText()

        if selection == "Use Your Own Data":
            self.ui.label_hint_selection.setVisible(False)
            self.ui.frame_date_range.setVisible(False)
            self.ui.frame_btns_data.setVisible(True)
            self.ui.btn_download_wind.setVisible(False)
            self.ui.btn_process_wind.setVisible(False)
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
