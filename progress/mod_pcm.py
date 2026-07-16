"""PCM integration utilities.

This module provides a helper class for exporting PCM YAML configuration,
converting it to PCM JSON input, modifying that JSON with progress model
results, running the PCM simulation, and extracting summary curtailment data.
"""

import logging
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

    def __init__(self, sim_hours, pcm_config, input_directory, output_directory, progress_data, load_factor):
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
        """

        self.sim_hours = sim_hours
        self.pcm_venv_path = pcm_config["pcm_venv_path"]
        self.pcm_data_dir = input_directory
        self.pcm_config = pcm_config
        self.pcm_directory = output_directory
        os.makedirs(self.pcm_directory, exist_ok=True)
        self.progress_data = progress_data
        self.load_factor = load_factor
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
        pcm_yaml["start_date"] = self.pcm_config["start_date"]
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
        
        pcm_yaml["System Reserve"] = "percentage"
        pcm_yaml["Regulation Up"] = "timeseries"
        pcm_yaml["Regulation Down"] = "timeseries"
        pcm_yaml["Spinning Reserve"] = "timeseries"
        pcm_yaml["NonSpinning Reserve"] = "None"
        pcm_yaml["Supplemental Reserve"] = "None"
        pcm_yaml["Flexible Ramp Up"] = "timeseries"
        pcm_yaml["Flexible Ramp Down"] = "timeseries"

        pcm_yaml["storage_AS_participation_level"] = 4 if self.pcm_config["storage_AS_mode"] else 0 
        pcm_yaml["evaluate_degradation"] = True 

        pcm_yaml["output_interval"] = "weekly" 
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
        result = subprocess.run([self.pcm_venv_path, temp_script], check=True,
                                capture_output=True, text=True)
        os.remove(temp_script)
        if result.stdout.strip():
            for line in result.stdout.strip().splitlines():
                if "DATA Warning" in line:
                    logger.debug(line)
                else:
                    logger.info(line)
        if result.stderr.strip():
            logger.debug("PCM export JSON stderr: %s", result.stderr.strip())
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
        
        for current_gen_name, current_gen_details in pcm_data["elements"]["generator"].items():
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
        
        for current_branch_name, current_branch_details in pcm_data["elements"]["branch"].items():
            branch_status = self.progress_data["line_status"][current_branch_name]
            branch_status_bool =  [int(1-x) for x in branch_status]
            current_branch_details["planned_outage"] = {"data_type": "time_series",
                                                        "values": branch_status_bool}

        for load_element_name, load_element_details in pcm_data["elements"]["load"].items():
            bus_name = pcm_data["elements"]["bus"][load_element_name]["bus_name"]
            stored_load = self.progress_data["load"][bus_name]
            load_element_details["p_load"]["values"] = [p * self.load_factor for p in stored_load]

        for storage_name, storage_details in pcm_data["elements"]["storage"].items():
            storage_details["ess_smax"]["values"] = self.progress_data["ess_smax_limit"][storage_name]
            storage_details["ess_smin"]["values"] = self.progress_data["ess_smin_limit"][storage_name]
            storage_details["ess_pmax"]["values"] = self.progress_data["ess_pmax_limit"][storage_name]

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
        result = subprocess.run([self.pcm_venv_path, temp_script], check=True,
                                capture_output=True, text=True)
        os.remove(temp_script)
        if result.stdout.strip():
            for line in result.stdout.strip().splitlines():
                logger.info(line)
        if result.stderr.strip():
            logger.error("PCM simulation stderr: %s", result.stderr.strip())
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
