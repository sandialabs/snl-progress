from PySide6.QtWidgets import QWidget, QMessageBox
from progress.App.api.ui.ui_api_gui import Ui_api_widget
from PySide6.QtCore import Signal

class api_form(QWidget, Ui_api_widget):
    """Landing page widget."""

    page_changer_next = Signal()
    page_changer_previous = Signal()

    def __init__(self, data_handler, parent=None):
        """Sets up the UI file to show in the application"""
        super(api_form, self).__init__(parent)
        self.setupUi(self)
        self.data_handler = data_handler
        self.pushButton_DI_next_4.clicked.connect(self.next_page)
        self.pushButton_skip_API.clicked.connect(self.next_page)
        self.pushButton_DI_previous_4.clicked.connect(self.prev_page)
        self.pushButton_help_API.clicked.connect(self.show_help_api)
        self.pushButton_help_API_2.clicked.connect(self.show_help_name)
        self.pushButton_help_API_3.clicked.connect(self.show_skip_api)
        self.pushButton_save_solarinput.clicked.connect(self.save_api_input)
        self.pushButton_DI_next_4.setVisible(False)


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
        self.input_api = self.lineEdit_api.text()
        self.input_name = self.lineEdit_name.text()
        self.input_email = self.lineEdit_email.text()
        self.input_aff = self.lineEdit_aff.text()

        self.data_handler.set_input_api(self.input_api)
        self.data_handler.set_input_name(self.input_name)
        self.data_handler.set_input_email(self.input_email)
        self.data_handler.set_input_aff(self.input_aff)

        QMessageBox.information(self, "API information", "Saved!")

        self.pushButton_DI_next_4.setVisible(True)
        self.pushButton_skip_API.setVisible(False)
        self.pushButton_help_API_3.setVisible(False)

    def next_page(self):
        self.page_changer_next.emit()
    
    def prev_page(self):
        self.page_changer_previous.emit()