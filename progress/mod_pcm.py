"""PCM integration utilities.

This module provides a helper class for exporting PCM YAML configuration,
converting it to PCM JSON input, modifying that JSON with progress model
results, running the PCM simulation, and extracting summary curtailment data.
"""

import logging
from datetime import datetime
import os
import subprocess
import tempfile
import textwrap
import pandas as pd
import numpy as np
import json

logger = logging.getLogger(__name__)

class PCM:
    """Wrapper for PCM model export, execution, and result extraction."""

    def __init__(self, sim_hours, pcm_config, input_directory, output_directory, progress_data, load_factor, network_model):
        """Initialize the PCM helper with configuration and simulation data.

        Parameters
        ----------
        sim_hours : int
            Total number of simulation hours.
        pcm_config : dict
            PCM configuration settings loaded from project configuration.
        input_directory : str
            Directory containing PCM input data files.
        output_directory : str
            Directory where PCM output will be saved.
        progress_data : dict
            Progress model data used to modify PCM JSON inputs.
        load_factor : float
            Load scaling factor to apply to PCM load profiles.
        network_model : str
            Network model type ('Copper Sheet', 'Zonal', or 'Nodal').
        """

        self.sim_hours = sim_hours
        self.pcm_venv_path = pcm_config["pcm_venv_path"]
        self.pcm_data_dir = input_directory
        self.pcm_config = pcm_config
        self.pcm_directory = output_directory
        os.makedirs(self.pcm_directory, exist_ok=True)
        self.progress_data = progress_data
        self.load_factor = load_factor
        self.network_model = network_model
        logger.info("PCM initialized for %d simulation hours", sim_hours)

    def export_pcm_yaml(self):
        """Export a PCM YAML configuration file for the configured simulation.

        The generated YAML is written to the output directory and used by PCM
        to create JSON input data for the day-ahead simulation.
        """
        pcm_yaml = {}
        pcm_yaml["solver"] = self.pcm_config["solver"]
        pcm_yaml["mipgap"] = self.pcm_config["mipgap"]
        pcm_yaml["baseMVA"] = 100.0
        load_data = pd.read_csv(os.path.join(self.pcm_data_dir, "System", "load.csv"), index_col=0)
        
        dt =  datetime.strptime(load_data.index[0], '%Y-%m-%d %H:%M:%S')
        pcm_yaml["start_date"] = dt.strftime('%m/%d/%Y')
        pcm_yaml["DA_lookahead_periods"] = self.pcm_config.get("lookahead_hours")
        start_dt = pd.to_datetime(pcm_yaml["start_date"], dayfirst=True)
        lookahead_pad_hours = int(np.ceil(self.pcm_config["lookahead_hours"] / 24) * 24)

        effective_hours = max(self.sim_hours - lookahead_pad_hours, 0)
        end_dt = start_dt + pd.Timedelta(hours=effective_hours - 1) 
        pcm_yaml["end_date"] = end_dt.strftime("%m/%d/%Y")
        pcm_yaml["simulate_DA_only"] = True
        
        pcm_yaml["RT_resolution"] = 60 
        pcm_yaml["RT_lookahead_periods"] = 1 
        pcm_yaml["run_RTSCED_as"] = "MILP" 
        pcm_yaml["branch_contingency"] = False
        pcm_yaml["solve_pricing_problem"] = self.pcm_config["solve_pricing_problem"] 
        pcm_yaml["load_timeseries_aggregation_level"] = "node"
        
        pcm_yaml["System Reserve"] = "None"
        pcm_yaml["Regulation Up"] = "timeseries"
        pcm_yaml["Regulation Down"] = "timeseries"
        pcm_yaml["Spinning Reserve"] = "timeseries"
        pcm_yaml["NonSpinning Reserve"] = "None"
        pcm_yaml["Supplemental Reserve"] = "None"
        pcm_yaml["Flexible Ramp Up"] = "timeseries"
        pcm_yaml["Flexible Ramp Down"] = "timeseries"

        pcm_yaml["storage_AS_participation_level"] = 4 if self.pcm_config["storage_AS_mode"] else 0 
        pcm_yaml["evaluate_degradation"] = True 

        pcm_yaml["output_interval"] = self.pcm_config["pcm_output_frequency"]
        pcm_yaml["plotly_plots"] = False 
        pcm_yaml["plot_ancillary_services"] = False
        pcm_yaml["plot_storage_details"] = True 

        self.input_yaml_dir = os.path.join(self.pcm_directory, "input_pcm.yaml")
        with open(self.input_yaml_dir, "w") as f:
            json.dump(pcm_yaml, f, indent=4)
        logger.info("PCM YAML exported to %s", self.input_yaml_dir)

    def export_PCM_json(self):
        """Generate PCM JSON input files from the exported YAML configuration.

        A temporary Python script is executed in the PCM virtual environment to
        invoke PCM's DataManager and export the DA input JSON files.
        """
        code = textwrap.dedent(f"""
        import logging
        from egret.common.log import logger as egret_logger
        from pcm.data_manager.data_main import DataManager

        egret_logger.setLevel(logging.ERROR)

        main_data_path = r"{self.pcm_data_dir}"
        yaml_path = r"{self.input_yaml_dir}"
        output_dir = r"{self.pcm_directory}"

        input_manager = DataManager(main_data_path, yaml_path, optional_json_dir=output_dir)
        input_manager.export_input_json()
        """)

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(code.encode("utf-8"))
            temp_script = f.name

        logger.info("Generating PCM JSON input files...")
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        proc = subprocess.Popen(
            [self.pcm_venv_path, temp_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        for line in proc.stdout:
            stripped = line.strip()
            if stripped and "HiGHS" not in stripped:
                logger.info(stripped)
        for line in proc.stderr:
            stripped = line.strip()
            if stripped:
                logger.error(stripped)
        proc.wait()
        os.remove(temp_script)
        logger.info("PCM JSON input files generated")

    def modify_pcm_json(self):
        """Modify the generated PCM JSON input file with progressive simulation data.

        This method updates generator commitment status, hydro/wind/solar limits,
        branch outages, load scaling, and storage limits based on the progress
        model outputs.
        """
        # Example of modifying the PCM input JSON file after it has been generated
        pcm_json_path = os.path.join(self.pcm_directory, "DA_data.json")
        logger.info("Modifying PCM JSON with progress model data...")
        with open(pcm_json_path, "r") as f:
            pcm_data = json.load(f)
        
       
        if self.network_model in {"Copper Sheet", "Zonal"}:
            new_buses = {}
            bus_to_zone_mapper = {}
            for bus_name, bus_details in pcm_data["elements"]["bus"].items():

                if self.network_model == "Copper Sheet":
                    new_bus_name = "1"
                else:  # Zonal
                    new_bus_name = bus_details["zone"]

                # Map every original bus to its new bus
                bus_to_zone_mapper[bus_name] = new_bus_name

                # Keep only one representative for each new bus
                if new_bus_name not in new_buses:
                    bus_details["bus_name"] = f"Zone_{new_bus_name}"
                    new_buses[new_bus_name] = bus_details

            pcm_data["elements"]["bus"] = new_buses
                
        for current_gen_name, current_gen_details in pcm_data["elements"]["generator"].items():

            if self.network_model in {"Copper Sheet", "Zonal"}:
                original_bus_name = current_gen_details["bus"]
                new_bus_name = bus_to_zone_mapper[original_bus_name]
                current_gen_details["bus"] = new_bus_name

            if current_gen_details["generator_type"] == "thermal":
                gen_status = self.progress_data["tg_status"][current_gen_name]
                gen_status = [None if x == 1 else x for x in gen_status]
                current_gen_details["fixed_commitment"] = {"data_type": "time_series",
                                                            "values": gen_status}
                
            if current_gen_details["category"] == "Hydro":
                gen_status = self.progress_data["tg_status"][current_gen_name]
                current_gen_details["p_max"]["values"] = [p * status for p, status in zip(current_gen_details["p_max"]["values"], gen_status)]

            if current_gen_details["category"] == "Solar PV":
                gen_limit = self.progress_data["solar_limit"][current_gen_name]
                current_gen_details["p_max"]["values"] = gen_limit

            if current_gen_details["category"] == "Wind":
                gen_limit = self.progress_data["wind_limit"][current_gen_name]
                current_gen_details["p_max"]["values"] = gen_limit
            if current_gen_details["category"] == "Wind":
                gen_limit = self.progress_data["wind_limit"][current_gen_name]
                current_gen_details["p_max"]["values"] = gen_limit
        
        if self.network_model == "Nodal":
            # Keep all branches
            for branch_name, branch_details in pcm_data["elements"]["branch"].items():
                branch_status = self.progress_data["line_status"][branch_name]
                branch_details["planned_outage"] = {
                    "data_type": "time_series",
                    "values": [1 - x for x in branch_status],
                }

        elif self.network_model == "Zonal":
            # Keep only interzonal branches
            new_branches = {}

            for branch_name, branch_details in pcm_data["elements"]["branch"].items():
                from_bus = bus_to_zone_mapper[branch_details["from_bus"]]
                to_bus = bus_to_zone_mapper[branch_details["to_bus"]]

                if from_bus == to_bus:
                    continue

                branch_status = self.progress_data["line_status"][branch_name]
                branch_details["planned_outage"] = {
                    "data_type": "time_series",
                    "values": [1 - x for x in branch_status],
                }
                branch_details["from_bus"] = from_bus
                branch_details["to_bus"] = to_bus

                new_branches[branch_name] = branch_details

            pcm_data["elements"]["branch"] = new_branches

        elif self.network_model == "Copper Sheet":
            # No transmission network
            pcm_data["elements"]["branch"] = {}

        if self.network_model == "Nodal":
            for load_element_name, load_element_details in pcm_data["elements"]["load"].items():
                bus_name = pcm_data["elements"]["bus"][load_element_name]["bus_name"]
                stored_load = self.progress_data["load"][bus_name]
                load_element_details["p_load"]["values"] = [p * self.load_factor for p in stored_load]
        elif self.network_model == "Zonal":
            pcm_data["elements"]["load"] = {}
            new_load_dict = {}
            for load_region, load_array in self.progress_data["load"].items():
                new_load_dict[load_region] = {
                    "bus": load_region,
                    "area"  : load_region,
                    "p_load": {"data_type": "time_series", "values": [p * self.load_factor for p in load_array]},
                }
            pcm_data["elements"]["load"] = new_load_dict
        elif self.network_model == "Copper Sheet":
            pcm_data["elements"]["load"] = {}
            new_load_dict = {}
            system_wide_load = np.sum([np.array(load_array) for load_array in self.progress_data["load"].values()], axis=0)
            new_load_dict["1"] = {
                "bus": "1",
                "area"  : "1",
                "p_load": {"data_type": "time_series", "values": [p * self.load_factor for p in system_wide_load]},
            }
            pcm_data["elements"]["load"] = new_load_dict

        for storage_name, storage_details in pcm_data["elements"]["storage"].items():
            if self.network_model in {"Copper Sheet", "Zonal"}:
                original_bus_name = storage_details["bus"]
                new_bus_name = bus_to_zone_mapper[original_bus_name]
                storage_details["bus"] = new_bus_name
            storage_details["ess_smax"]["values"] = self.progress_data["ess_smax_limit"][storage_name]
            storage_details["ess_smin"]["values"] = self.progress_data["ess_smin_limit"][storage_name]
            storage_details["ess_pmax"]["values"] = self.progress_data["ess_pmax_limit"][storage_name]

        if self.network_model == "Copper Sheet":
            pcm_data["elements"]["area"] = {}

        with open(pcm_json_path, "w") as f:
            json.dump(pcm_data, f, indent=4)
        logger.info("PCM JSON modification complete")

    def run_PCM(self):
        """Run the PCM market simulation and export results.

        A temporary Python script is executed in the PCM virtual environment to
        run the PCM market simulator and save results to the output directory.
        """
        code = textwrap.dedent(f"""
        import os
        import json
        import logging
        from egret.common.log import logger as egret_logger
        from pcm.data_manager.data_main import DataManager
        from pcm.market_manager.market_main import MarketSimulator
        from pcm.result_manager.result_main import ResultManager# %%

        egret_logger.setLevel(logging.ERROR)

        main_data_path = r"{self.pcm_data_dir}"
        yaml_path = r"{self.input_yaml_dir}"
        output_dir = r"{self.pcm_directory}"

        input_manager = DataManager(main_data_path, yaml_path, optional_json_dir = output_dir)
        simulator = MarketSimulator(input_manager)
        simulator.create_DA_RT_models()
        simulator.simulate_market() 

        result_processor = ResultManager(simulator, output_dir)
        result_processor.export_results()
        """)

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(code.encode("utf-8"))
            temp_script = f.name

        logger.info("Running PCM market simulation...")
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        proc = subprocess.Popen(
            [self.pcm_venv_path, temp_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        for line in proc.stdout:
            stripped = line.strip()
            if stripped and "HiGHS" not in stripped:
                logger.info(stripped)
        for line in proc.stderr:
            stripped = line.strip()
            if stripped:
                logger.error(stripped)
        proc.wait()
        os.remove(temp_script)
        logger.info("PCM market simulation complete")

    def extract_load_curtailment(self):
        """Extract the PCM load curtailment time series from simulation results.

        Returns
        -------
        numpy.ndarray
            Load curtailed values in MWh from the PCM simulation summary.
        """
        import glob
        logger.info("Extracting load curtailment from PCM results...")
        pcm_results_path = glob.glob(os.path.join(self.pcm_directory, "**", "simulation_summary.xlsx"), recursive=True)[0]
        df_curtailment = pd.read_excel(
            pcm_results_path,
            sheet_name="Curtailment Timestamp",
            engine="openpyxl"
        )
    
        return df_curtailment["Load Curtailed (MWh)"].values
