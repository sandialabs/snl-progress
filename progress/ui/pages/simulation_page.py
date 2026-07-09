from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QFileDialog, QDialog, QPushButton
from PySide6.QtCore import QDate, QSettings, QTimer, Qt
from progress.ui.forms.simulation.ui_simulation import Ui_SimulationPage
from progress.ui.forms.simulation.ui_pcm_config import Ui_PCMConfigPage
from progress.ui.utils.worker import ProcessingThread
from progress.paths import get_path, get_results_path, load_config
from progress.example_simulation import MCS
from progress.ui.utils.data_handler import DataHandler
from dataclasses import dataclass
from pathlib import Path
import datetime
import logging
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import SingleQuotedScalarString
import yaml

logger = logging.getLogger(__name__)


class PCMConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)
        settings = QSettings("QuESt", "snl-progress")
        theme = settings.value("theme", "light")
        bg = "#1e293b" if theme == "dark" else "#ffffff"
        self.setStyleSheet(f"background-color: {bg};")
        self.ui = Ui_PCMConfigPage()
        self.ui.setupUi(self)
        self.setWindowTitle("PCM Configuration")
        self.setModal(True)

        self.ui.btn_save_config.clicked.connect(self._save_config)
        self.ui.btn_exit_config.clicked.connect(self.close)

        self.ui.btn_browse_venv = QPushButton("Browse...")
        self.ui.btn_browse_venv.setObjectName("btn_browse_venv")
        self.ui.horizontalLayout_14.insertWidget(2, self.ui.btn_browse_venv)
        self.ui.btn_browse_venv.clicked.connect(self._browse_venv)

        # info buttons
        self.ui.btn_info_venv.clicked.connect(self._display_venv_info)
        self.ui.btn_info_start_date.clicked.connect(self._display_start_date_info)
        self.ui.btn_info_solver.clicked.connect(self._display_solver_info)
        self.ui.btn_info_mipgap.clicked.connect(self._display_mipgap_info)
        self.ui.btn_info_pricing.clicked.connect(self._display_pricing_info)
        self.ui.btn_info_storage_mode.clicked.connect(self._display_storage_mode_info)

        self._load_from_yaml()

    def _browse_venv(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select PCM Python Executable",
            self.ui.lineEdit_pcm_venv.text() or str(Path.home()),
            "Python (python*);;All Files (*)")
        if path:
            self.ui.lineEdit_pcm_venv.setText(path)

    def _display_venv_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "PCM Venv Path", "Path to the Python executable of the virtual environment where PCM is installed.")

    def _display_start_date_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Start Date", "Start date for the PCM simulation in MM/DD/YYYY format. The end date is determined based on the total simulation hours.")

    def _display_solver_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Solver", "Solver to use for PCM optimization. Options include 'gurobi', 'cplex', 'cbc', etc.")

    def _display_mipgap_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "MIP Gap", "MIP gap tolerance for PCM optimization. Lower values yield more optimal solutions but increase computation time.")

    def _display_pricing_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Solve Pricing Problem", "Enable or disable solving the pricing problem in PCM. When enabled, generates LMPs, revenues, etc., but increases computation time.")

    def _display_storage_mode_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Storage AS Mode", "Enable or disable BESS participation in ancillary services within the PCM simulation.")

    def _load_from_yaml(self):
        config = load_config()
        pcm = config.get("pcm_parameters", {})
        self.ui.lineEdit_pcm_venv.setText(pcm.get("pcm_venv_path", ""))

        try:
            date_parts = pcm.get("start_date", "01/01/2020").split("/")
            d = QDate(int(date_parts[2]), int(date_parts[0]), int(date_parts[1]))
            self.ui.dateEdit_start_date.setDate(d)
        except (ValueError, IndexError):
            pass

        solver = pcm.get("solver", "")
        idx = self.ui.comboBox_solver.findText(solver, Qt.MatchFlag.MatchFixedString)
        if idx >= 0:
            self.ui.comboBox_solver.setCurrentIndex(idx)

        self.ui.doubleSpin_mini_gap.setValue(float(pcm.get("mipgap", 0.05)))

        solve_pricing = pcm.get("solve_pricing_problem", False)
        self.ui.radio_solve_pricing_true.setChecked(bool(solve_pricing))
        self.ui.radio_solve_pricing_false.setChecked(not bool(solve_pricing))

        storage_as = pcm.get("storage_AS_mode", True)
        self.ui.label_storage_mode_true.setChecked(bool(storage_as))
        self.ui.label_storage_mode_false.setChecked(not bool(storage_as))

    def _save_config(self):
        pcm_params = {
            "pcm_venv_path": self.ui.lineEdit_pcm_venv.text().strip(),
            "start_date": self.ui.dateEdit_start_date.date().toString("MM/dd/yyyy"),
            "solver": SingleQuotedScalarString(self.ui.comboBox_solver.currentText().strip()),
            "mipgap": self.ui.doubleSpin_mini_gap.value(),
            "solve_pricing_problem": self.ui.radio_solve_pricing_true.isChecked(),
            "storage_AS_mode": self.ui.label_storage_mode_true.isChecked(),
        }

        yaml_path = get_path() / "input.yaml"
        yaml = YAML()
        yaml.preserve_quotes = True
        with open(yaml_path) as f:
            data = yaml.load(f)
        pcm = data.get("pcm_parameters")
        if isinstance(pcm, dict):
            pcm.clear()
            pcm.update(pcm_params)
        else:
            data["pcm_parameters"] = pcm_params
        with open(yaml_path, "w") as f:
            yaml.dump(data, f)

        QMessageBox.information(self, "PCM Config", "PCM configuration saved!")


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

        self.ui.radio_use_pcm_true.clicked.connect(self._update_pcm_button_state)
        self.ui.radio_use_pcm_false.clicked.connect(self._update_pcm_button_state)
        self.ui.btn_pcm_config.clicked.connect(self._open_pcm_config_dialog)

        # info buttons
        self.ui.btn_info_samples.clicked.connect(self._display_samples_info)
        self.ui.btn_info_hours.clicked.connect(self._display_hours_info)
        self.ui.btn_info_load_factor.clicked.connect(self._display_load_factor_info)
        self.ui.btn_info_model_type.clicked.connect(self._display_model_info)
        self.ui.btn_info_opt_period.clicked.connect(self._display_opt_period_info)
        self.ui.btn_info_dc_load.clicked.connect(self._display_dc_load_info)
        self.ui.btn_info_degradation_eval.clicked.connect(self._display_degradation_eval_info)
        self.ui.btn_info_degradation_int.clicked.connect(self._display_degradation_int_info)
        self.ui.btn_info_detailed_model.clicked.connect(self._display_detailed_model_info)
        self.ui.btn_info_use_pcm.clicked.connect(self._display_use_pcm_info)

        self.ui.btn_stop_simulation.setEnabled(False)
        self.ui.btn_pcm_config.setEnabled(False)
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
        self.ui.radio_dc_load_true.setChecked(self.config.DC_load)
        self.ui.radio_dc_load_false.setChecked(not self.config.DC_load)

        config_data = load_config()
        use_pcm = config_data.get("use_pcm", False)
        self.ui.radio_use_pcm_true.setChecked(bool(use_pcm))
        self.ui.radio_use_pcm_false.setChecked(not bool(use_pcm))
        self._update_pcm_button_state()

    def _check_eval_degradation_selection(self) -> bool:
        return self.ui.radio_degradation_eval_true.isChecked()

    def _check_thermal_model_selection(self) -> bool:
        return self.ui.radio_detailed_model_true.isChecked()

    def _update_frame_visibility(self):
        is_visible = self._check_eval_degradation_selection()
        self.ui.frame_degradation_int.setVisible(is_visible)
        self.ui.frame_thermal_model.setVisible(is_visible)

    def _update_pcm_button_state(self):
        self.ui.btn_pcm_config.setEnabled(self.ui.radio_use_pcm_true.isChecked())

    def _display_samples_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Samples", "Number of Monte Carlo samples to run. Each sample represents one year of simulated operation.")

    def _display_hours_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Simulation Hours", "Total number of simulation hours for each sample. 1 non-leap year = 8760 hours.")

    def _display_load_factor_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Load Factor", "Multiplier applied to the base load at all buses to increase or decrease overall system demand. Default = 1.")

    def _display_model_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Network Model", "Select the network model fidelity: 'Copper Sheet' (no network constraints, lowest fidelity), 'Zonal' (nodes within a zone aggregated, medium fidelity), or 'Nodal' (full network representation, highest fidelity).")

    def _display_opt_period_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Optimization Period", "Optimization horizon in hours. Use 1 for reliability mode. Use multiples of 24 (e.g., 24, 48) for day-ahead hourly optimization. Recommended: 24.")

    def _display_dc_load_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "DC Load", "Enable or disable data center load integration. When enabled, random data center load profiles are added to the system load.")

    def _display_degradation_eval_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Degradation Evaluation", "Enable or disable battery degradation evaluation during the simulation. When enabled, BESS capacity fade is modeled over time.")

    def _display_degradation_int_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Degradation Interval", "Number of hours between successive BESS degradation evaluations. Recommended: 168 hours (1 week) or more.")

    def _display_detailed_model_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Detailed Thermal Model", "Use the detailed PyBAMM thermal model for BESS degradation. Enabled: higher accuracy but significantly longer computation. Disabled: constant 25°C temperature assumed.")

    def _display_use_pcm_info(self, checked: bool = False) -> None:
        QMessageBox.information(self, "Use PCM", "Enable or disable the PCM (Production Cost Model) co-simulation. PCM provides detailed unit commitment and economic dispatch for the simulated hours.")

    def _open_pcm_config_dialog(self):
        dialog = PCMConfigDialog(self)
        dialog.exec()

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
            DC_load=self.ui.radio_dc_load_true.isChecked(),
        )
        self.config = config
        config.save()
        yaml = YAML()
        yaml.preserve_quotes = True
        with open(get_path() / "input.yaml") as f:
            data = yaml.load(f)
        data["use_pcm"] = self.ui.radio_use_pcm_true.isChecked()
        with open(get_path() / "input.yaml", "w") as f:
            yaml.dump(data, f)
        return config

    def _on_save_config(self):
        if self._save_sim_configs() is not None:
            QMessageBox.information(self, "Simulation Input", "Input Saved!")
    


