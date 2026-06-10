from PySide6.QtWidgets import QWidget, QVBoxLayout
from progress.ui.forms.simulation.ui_simulation import Ui_SimulationPage


class SimulationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SimulationPage()
        self.ui.setupUi(self)

