
from PySide6.QtWidgets import QWidget, QVBoxLayout
from progress.ui.forms.simulation.ui_simulation import Ui_SimulationPage


class SimulationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SimulationPage()
        self.ui.setupUi(self)

        self.ui.radio_degradation_eval_true.clicked.connect(self._update_frame_visibility)
        self.ui.radio_degradation_eval_false.clicked.connect(self._update_frame_visibility)

        self._update_frame_visibility()

    def _check_eval_degradation_selection(self) -> bool:
        return self.ui.radio_degradation_eval_true.isChecked()

    def _update_frame_visibility(self):
        is_visible = self._check_eval_degradation_selection()
        
        self.ui.frame_degradation_int.setVisible(is_visible)
        self.ui.frame_thermal_model.setVisible(is_visible)

