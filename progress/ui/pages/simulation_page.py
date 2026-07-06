from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QFileDialog
from PySide6.QtCore import QTimer
from progress.ui.forms.simulation.ui_simulation import Ui_SimulationPage
from progress.ui.utils.worker import ProcessingThread
from progress.paths import get_path, get_results_path, load_config
from progress.example_simulation import MCS
from progress.ui.utils.data_handler import DataHandler
from dataclasses import dataclass
from pathlib import Path
import datetime
import logging
from ruamel.yaml import YAML
import yaml

logger = logging.getLogger(__name__)

@dataclass
class MCSConfig:
    samples: int = 5
    sim_hours: int = 8760
    load_factor: float = 1.15
    model: str = 'Zonal'
    optimization_period: int = 24
    evaluate_degradation: bool = False
    degradation_interval: int = 1000
    detailed_thermal_model: bool = False
    DC_load: bool = True

    @classmethod
    def from_yaml(cls):
        data = load_config()
        field_names = cls.__dataclass_fields__.keys()
        filtered = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered)

    def save(self, path=None):
        """Write MCSConfig fields into the YAML config file, preserving comments and non-config keys.

        Uses ruamel.yaml to perform a round-trip update of input.yaml. Only the 9 fields
        defined on MCSConfig are overwritten; all other keys (data, download_w, n_clusters,
        etc.) and any YAML comments remain untouched.

        Parameters
        ----------
        path : str or Path, optional
            Path to the YAML file. Defaults to progress/input.yaml.
        """
        yaml_path = path or (get_path() / "input.yaml")
        yaml = YAML()
        yaml.preserve_quotes = True
        with open(yaml_path) as f:
            data = yaml.load(f)
        for field in self.__dataclass_fields__:
            data[field] = getattr(self, field)
        with open(yaml_path, "w") as f:
            yaml.dump(data, f)

MODEL_MAP = {
    "Zonal Model": "Zonal",
    "Copper Sheet Model": "Copper Sheet",
    "Nodal": "Nodal",
}
MODEL_MAP_REV = {v: k for k, v in MODEL_MAP.items()}

class SimulationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SimulationPage()
        self.ui.setupUi(self)
        self.setMaximumHeight(16777215)
        self.config = MCSConfig.from_yaml()
        self._sim_stopped = False
        self.setMinimumHeight(0)

        # ==== connections ====
        self.ui.radio_degradation_eval_true.clicked.connect(self._update_frame_visibility)
        self.ui.radio_degradation_eval_false.clicked.connect(self._update_frame_visibility)
        self.ui.btn_run_simulation.clicked.connect(self._display_sim_results)
        self.ui.btn_stop_simulation.clicked.connect(self._stop_simulation)
        self.ui.btn_save_config.clicked.connect(self._on_save_config)

        self.ui.btn_stop_simulation.setEnabled(False)
        self._populate_gui()
        self._update_frame_visibility()

    def _populate_gui(self):
        self.ui.lineEdit_samples.setText(str(self.config.samples))
        self.ui.lineEdit_hours.setText(str(self.config.sim_hours))
        self.ui.lineEdit_load_factor.setText(str(self.config.load_factor))
        self.ui.comboBox_model_type.setCurrentText(MODEL_MAP_REV[self.config.model])
        self.ui.lineEdit_opt_period.setText(str(self.config.optimization_period))
        self.ui.radio_degradation_eval_false.setChecked(not self.config.evaluate_degradation)
        self.ui.lineEdit_degradation_int.setText(str(self.config.degradation_interval))
        self.ui.radio_detailed_model_true.setChecked(self.config.detailed_thermal_model)
        self.ui.radio_detailed_model_false.setChecked(not self.config.detailed_thermal_model)

    def _check_eval_degradation_selection(self) -> bool:
        return self.ui.radio_degradation_eval_true.isChecked()

    def _check_thermal_model_selection(self) -> bool:
        return self.ui.radio_detailed_model_true.isChecked()

    def _update_frame_visibility(self):
        is_visible = self._check_eval_degradation_selection()
        self.ui.frame_degradation_int.setVisible(is_visible)
        self.ui.frame_thermal_model.setVisible(is_visible)

    def _display_sim_results(self):
        if self._save_sim_configs() is None:
            return
        yaml_path = get_path() / "input.yaml"
        results_dir = get_results_path() / datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        results_dir.mkdir(parents=True, exist_ok=True)
        self._sim_stopped = False
        self._sim_thread = ProcessingThread(MCS, str(yaml_path), str(results_dir))
        self.ui.btn_run_simulation.setText("Running...")
        self.ui.btn_run_simulation.setEnabled(False)
        self.ui.btn_stop_simulation.setEnabled(True)
        self._sim_thread.start()
        self._poll_timer = QTimer()
        self._poll_timer.timeout.connect(self._check_sim_done)
        self._poll_timer.start(500)

    def _stop_simulation(self):
        self._sim_stopped = True
        self._sim_thread.stop()
        self.ui.btn_stop_simulation.setEnabled(False)

    def _check_sim_done(self):
        if self._sim_thread.isFinished():
            self._poll_timer.stop()
            self.ui.btn_run_simulation.setText("Run Simulation")
            self.ui.btn_run_simulation.setEnabled(True)
            if self._sim_stopped:
                QMessageBox.information(self, "Simulation Stopped", "Simulation was cancelled by user.")
            else:
                QMessageBox.information(self, "Simulation Complete", "Simulation ran successfully and results saved.")

    def _save_sim_configs(self) -> MCSConfig | None:
        try:
            samples = int(self.ui.lineEdit_samples.text().strip())
            sim_hours = int(self.ui.lineEdit_hours.text().strip())
            load_factor = float(self.ui.lineEdit_load_factor.text().strip())
            model = MODEL_MAP[self.ui.comboBox_model_type.currentText()]
            optimization_period = int(self.ui.lineEdit_opt_period.text().strip())
            degradation_interval = int(self.ui.lineEdit_degradation_int.text().strip())
        except (ValueError, KeyError) as e:
            QMessageBox.critical(self, "Invalid Input", f"Invalid value: {e}")
            return None

        config = MCSConfig(
            samples=samples,
            sim_hours=sim_hours,
            load_factor=load_factor,
            model=model,
            optimization_period=optimization_period,
            evaluate_degradation=self._check_eval_degradation_selection(),
            degradation_interval=degradation_interval,
            detailed_thermal_model=self._check_thermal_model_selection(),
            DC_load=False,
        )
        self.config = config
        config.save()
        return config

    def _on_save_config(self):
        if self._save_sim_configs() is not None:
            QMessageBox.information(self, "Simulation Input", "Input Saved!")
    


