from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from progress.ui.forms.simulation.ui_simulation import Ui_SimulationPage


class SimulationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SimulationPage()
        self.ui.setupUi(self)

        self.ui.radio_degradation_eval_true.clicked.connect(self._update_frame_visibility)
        self.ui.radio_degradation_eval_false.clicked.connect(self._update_frame_visibility)

        self.ui.btn_run_simulation.clicked.connect(self._display_sim_results)


        self._update_frame_visibility()

    def _check_eval_degradation_selection(self) -> bool:
        return self.ui.radio_degradation_eval_true.isChecked()

    def _update_frame_visibility(self):
        is_visible = self._check_eval_degradation_selection()
        
        self.ui.frame_degradation_int.setVisible(is_visible)
        self.ui.frame_thermal_model.setVisible(is_visible)

    def _display_sim_results(self):
        QMessageBox.information(self, "Simulation Input", "Input Saved!")
