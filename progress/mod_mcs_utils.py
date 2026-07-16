"""Monte Carlo sequential simulation utilities for reliability assessment.

This module provides helper classes for initializing system and renewable
parameters, processing matrices, recording hourly sample data, and handling
optional PCM and degradation workflows used by the reliability assessment
simulation.
"""

import numpy as np
from time import perf_counter
from pyomo.environ import *
import copy
import pandas as pd
import os
import yaml
import argparse

from progress.mod_sysdata import RASystemData
from progress.mod_solar import Solar
from progress.mod_wind import Wind
from progress.mod_utilities import RAUtilities
from progress.mod_matrices import RAMatrices
from progress.mod_plot import RAPlotTools
from progress.mod_degradation import BESS_Degradation
from datetime import datetime, timedelta
from progress.mod_bus_statistics import bus_statistics
from progress.mod_pcm import PCM

class MCS_utils:
    """Collects and prepares system, renewable, and simulation parameters.

    This class is responsible for loading system data, renewable profiles,
    reliability parameters, and matrices required for Monte Carlo sequential
    simulation. It also maintains configuration state for PCM and degradation
    analysis.
    """

    def __init__(self, config):
        """Initialize simulation configuration and validate required options.

        Args:
            config (dict): Parsed configuration dictionary containing data
                directories, model type, sample settings, PCM options, and
                degradation settings.
        """

        # data dir
        self.data = config['data']

        # data file locations
        self.system_directory = config['data'] + '/System'
        self.solar_directory = config['data'] + '/Solar'
        self.wind_directory = config['data'] + '/Wind'
        self.solar_dir_exists = os.path.exists(self.solar_directory)
        self.wind_dir_exists = os.path.exists(self.wind_directory)

        # model Copper Sheet, Zonal, or Nodal
        self.network_model = config['model']

        # Monte Carlo simulation parameters
        self.samples = config['samples']
        self.time_periods = config['optimization_period']
        self.load_factor = config['load_factor']
        self.dispatch_solver = config.get('dispatch_solver', 'glpk')
        if self.time_periods == 1:
            self.optimization_period = "single_period"
        else:
            if self.time_periods % 24 != 0:
                raise ValueError("For multi-period optimization, the optimization_period should be a multiple of 24.")
            self.optimization_period = "multi_period"

        self.evaluate_degradation = config.get('evaluate_degradation', False)
        self.detailed_thermal_model = config.get('detailed_thermal_model', False)
        self.degradation_interval = config.get('degradation_interval', 168)

        self.DC_load_present = config.get('DC_load', False)

        self.enable_pcm = config["use_pcm"]
        if self.enable_pcm and self.network_model != "Nodal":
            raise ValueError("Currently, PCM model only supports Nodal network model.")
        if self.enable_pcm and self.time_periods != 24:
            raise ValueError("Currently, PCM only supports 24-hr multi-period model.")
        if self.enable_pcm:
            config["pcm_parameters"]["lookahead_hours"] = 6 #At least some lookahead is required to prevent errors
            self.sim_hours = config['sim_hours'] + int(np.ceil(config["pcm_parameters"]["lookahead_hours"] / 24) * 24 )
        else:
            self.sim_hours = config["sim_hours"]
        if self.enable_pcm and self.evaluate_degradation == True:
            raise ValueError("Currently, PCM does not enforce degradation.")
        
        self.pcm_parameters =  config.get('pcm_parameters', {})


    def initialize_params(self) :   
        """Load system details and reliability data.

        This method reads generator, branch, bus, load, and storage definitions
        from the system data directory. It also computes base capacities and
        failure/repair rates needed for reliability assessment.

        Returns:
            tuple: bus_params, gen_params, line_params, load_all_regions, ess_params
        """

        data_gen = self.system_directory + '/gen.csv'
        data_branch = self.system_directory + '/branch.csv'
        data_bus = self.system_directory + '/bus.csv'
        data_load = self.system_directory + '/load.csv'
        data_storage = self.system_directory + '/storage.csv'
        self.BMva = 100

        rasd = RASystemData(self.optimization_period, self.network_model)
        self.gen_params = {}

        self.gen_params["genbus"], self.gen_params["ng"], self.gen_params["pmax"], self.gen_params["pmin"], self.gen_params["FOR_gen"], \
        self.gen_params["MTTF_gen"], self.gen_params["MTTR_gen"], self.gen_params["gencost"], self.gen_params["genname"] = rasd.gen(data_gen)
        
        self.line_params = {}
        self.line_params["nl"], self.line_params["fb"], self.line_params["tb"], self.line_params["cap_trans"], self.line_params["MTTF_trans"], \
            self.line_params["MTTR_trans"], self.line_params["branchname"] = rasd.branch(data_branch, data_bus)
        
        self.bus_params = {}
        self.bus_params["busname"], self.bus_params["bus_no"], self.bus_params["nz"] = rasd.bus(data_bus)

        self.load_all_regions = rasd.load(self.bus_params["busname"], self.bus_params["bus_no"], data_load)
        
        self.ess_params = {}
        self.ess_params["essname"], self.ess_params["essbus"], self.ess_params["ness"], self.ess_params["ess_pmax"], self.ess_params["ess_pmin"], \
            self.ess_params["ess_duration"], self.ess_params["ess_socmax"], self.ess_params["ess_socmin"], self.ess_params["ess_eff"], \
            self.ess_params["disch_cost"], self.ess_params["ch_cost"], self.ess_params["MTTF_ess"], self.ess_params["MTTR_ess"], \
            self.ess_params["ess_units"], self.ess_params["ess_chemistry"] = rasd.storage(data_storage)
        self.ess_params["ess_sbase"] = self.ess_params["ess_pmax"]*self.ess_params["ess_duration"]
        
        self.raut = RAUtilities(dispatch_solver=self.dispatch_solver)
        self.cap_max, self.cap_min = self.raut.capacities(self.line_params["nl"], self.gen_params["pmax"], self.gen_params["pmin"], self.ess_params["ess_pmax"], self.ess_params["ess_pmin"], self.line_params["cap_trans"]) # calling this function to get values of cap_max and cap_min
        self.mu_tot, self.lambda_tot = self.raut.reltrates(self.gen_params["MTTF_gen"], self.line_params["MTTF_trans"], self.gen_params["MTTR_gen"], self.line_params["MTTR_trans"], self.ess_params["MTTF_ess"], self.ess_params["MTTR_ess"])
        
        if self.DC_load_present == True and self.network_model == "Zonal":
            self.raut.DC_zonal(self.system_directory)
        return self.bus_params, self.gen_params, self.line_params, self.load_all_regions, self.ess_params

    def process_renewable_data(self):
        """Load and process renewable resource data for wind and solar.

        Reads renewable input files from the configured data directories and
        initializes wind and solar parameter dictionaries used during simulation.
        For wind, it also generates or loads transition rate matrices required
        for stochastic wind resource modeling.
        """
        # download and process wind data
        if self.wind_dir_exists:

            wind_sites = self.wind_directory + '/wind_sites.csv'
            wind_power_curves = self.wind_directory + '/w_power_curves.csv'
            windspeed_data = self.wind_directory + '/windspeed_data.csv'
            wind_tr_rate = self.wind_directory + '/t_rate.xlsx'
            
            self.wind_params = {}
            wind = Wind(self.wind_directory)
            self.wind_params["w_sites"], self.wind_params["farm_name"], self.wind_params["zone_no"], self.wind_params["w_classes"], \
                self.wind_params["w_turbines"], self.wind_params["r_cap"], self.wind_params["p_class"], self.wind_params["out_curve2"], \
                self.wind_params["out_curve3"], self.wind_params["start_speed"] = wind.WindFarmsData(wind_sites, wind_power_curves, self.network_model)

            # calculate transition rates 
            if not os.path.exists(wind_tr_rate):
                wind.CalWindTrRates(self.wind_directory, windspeed_data, wind_sites, wind_power_curves)

            tr_mats = pd.read_excel(wind_tr_rate, sheet_name=None)
            self.wind_params["tr_mats"] = np.array([tr_mats[sheet_name].to_numpy() for sheet_name in tr_mats])

        # download and process solar data
        if self.solar_dir_exists:

            solar_prob_data = self.solar_directory+"/solar_probs.csv"

            solar = Solar(self.solar_directory, self.network_model)
            self.solar_params = {}
            self.solar_params["farm_name"] = solar.names
            self.solar_params["s_sites"], self.solar_params["s_zone_no"], self.solar_params["s_max"], self.solar_params["s_profiles"], \
                self.solar_params["solar_prob"] = solar.GetSolarProfiles(solar_prob_data)

    def process_matrices(self):
        """Build power system matrices and initialize sample index buffers.

        This method creates the generator dispatch matrix, ESS charge/discharge
        matrix, incidence matrix for network connectivity, and curtailment
        matrix. It also initializes arrays used to record reliability indices
        across the Monte Carlo samples.

        Returns:
            tuple: gen_mat, ch_mat, A_inc, curt_mat, indices_rec, LOL_track
        """
        # matrices required for optimization
        ramat = RAMatrices(self.bus_params["nz"])
        self.gen_mat = ramat.genmat(self.gen_params["ng"], self.gen_params["genbus"], self.ess_params["ness"], self.ess_params["essbus"])
        self.ch_mat = ramat.chmat(self.ess_params["ness"], self.ess_params["essbus"], self.bus_params["nz"])
        self.A_inc = ramat.Ainc(self.line_params["nl"], self.line_params["fb"], self.line_params["tb"])
        self.curt_mat = ramat.curtmat(self.bus_params["nz"])

        # dictionary for storing temp. index values
        self.indices_rec = {"LOLP_rec": np.zeros(self.samples), "EUE_rec": np.zeros(self.samples), "MDT_rec": np.zeros(self.samples), \
                        "LOLF_rec": np.zeros(self.samples), "EPNS_rec": np.zeros(self.samples), "LOLP_hr": np.zeros(self.sim_hours), \
                            "LOLE_rec": np.zeros(self.samples),"mLOLP_rec":np.zeros(self.samples), "COV_rec": np.zeros(self.samples)}
        
        self.LOL_track = np.zeros((self.samples, self.sim_hours))

        return self.gen_mat, self.ch_mat, self.A_inc, self.curt_mat, self.indices_rec, self.LOL_track

class MCS_samples():
    """Stores sample-level data and provides utilities for each Monte Carlo sample.

    This class wraps an MCS_utils instance and extends it with data structures
    that track hourly results, outage records, renewable generation profiles,
    and optional degradation state for each Monte Carlo sample.
    """

    def __init__(self, mcs_utils):
        """Create a new sample handler that delegates to a shared MCS utility object."""
        self._mcs = mcs_utils

    def __getattr__(self, name):
        """Delegate attribute access to the underlying MCS_utils instance."""
        return getattr(self._mcs, name)
    
    def initialize_holder_vars(self, holder_dict):
        """Initialize dictionaries used to store PCM and outage tracking values."""
        holder_dict["g_limit"] = {}
        holder_dict["capacity"] = {}
        holder_dict["net_load"] = np.zeros((self.bus_params["nz"], self.time_periods))
        holder_dict["ren_limit"] = np.zeros((self.bus_params["nz"], self.time_periods))
        holder_dict["ess_min"] = np.zeros((self.ess_params["ness"], self.time_periods))
        holder_dict["ess_max"] = np.zeros((self.ess_params["ness"], self.time_periods))

        holder_dict["tg_status"] = {}
        for gen_name in self.gen_params["genname"].values:
            holder_dict["tg_status"][gen_name] =[]
        holder_dict["line_status"] = {}
        for line_name in self.line_params["branchname"].values:
            holder_dict["line_status"][line_name] = []
        if self.solar_dir_exists:
            holder_dict["solar_limit"] = {}
            for solar_name in self.solar_params["farm_name"].values:
                holder_dict["solar_limit"][solar_name] = []
        if self.wind_dir_exists:
            holder_dict["wind_limit"] = {}
            for wind_name in self.wind_params["farm_name"].values:
                holder_dict["wind_limit"][wind_name] = []
        holder_dict["ess_pmax_limit"] = {}
        holder_dict["ess_smax_limit"] = {}
        holder_dict["ess_smin_limit"] = {}
        for ess_name in self.ess_params["essname"].values:
            holder_dict["ess_pmax_limit"][ess_name] = []
            holder_dict["ess_smax_limit"][ess_name] = []
            holder_dict["ess_smin_limit"][ess_name] = []
        holder_dict["load"] = {}
        for bus_name in self.bus_params["busname"].values:
            holder_dict["load"][bus_name] = []

    def initialize_sample_data(self):
        """Initialize arrays and lists used to record sample-level hourly results."""

        if self.wind_dir_exists:
            self.current_w_class = self.raut.InitializeWindClasses(self.wind_params["w_sites"], self.wind_params["w_classes"])

        # record data for plotting and exporting (optional)
        self.renewable_rec = {"wind_rec": np.zeros((self.bus_params["nz"], self.sim_hours)), "solar_rec": np.zeros((self.bus_params["nz"], self.sim_hours)), "congen_temp": 0, \
                        "rengen_temp": 0}

        ESS_initial_capacities = copy.deepcopy(self.ess_params["ess_pmax"])
        self.SOC_rec = np.zeros((self.ess_params["ness"], self.sim_hours))
        self.Pdis_rec = np.zeros((self.ess_params["ness"], self.sim_hours))
        self.Pch_rec = np.zeros((self.ess_params["ness"], self.sim_hours))
        self.curt_rec = np.zeros(self.sim_hours)

        # the following lists will be used to record data during hours of outage
        self.out_hours = []
        self.Pg_rec = []
        self.flow_rec = []
        self.curtbus_rec = []
        self.ESS_rec = []
        self.wind_rec = []
        self.solar_rec = []

        if self.optimization_period == "multi_period":
            self.holder_dict = {}
            self.initialize_holder_vars(self.holder_dict)

        self.ess_smax_store = np.zeros((self.ess_params["ness"], self.sim_hours))
        # Form the degradation instances for all ESS
        self.degradation_instances = {}
        self.c_rate_holder = {}
        self.temp_holder = {}
        self.SOC_old_deg = {}
        if self.evaluate_degradation == True:
            for ess_name, ess_chem in zip(self.ess_params["essname"], self.ess_params["ess_chemistry"]):
                if ess_chem not in ["LFP", "NMC", "NCA", "LMO"]:
                    continue
                self.degradation_instances[ess_name] = BESS_Degradation(ess_chem)
                self.c_rate_holder[ess_name] = np.zeros(self.sim_hours)
                self.temp_holder[ess_name] = np.zeros(self.sim_hours)
                self.SOC_old_deg[ess_name] = 0.5
        # Read any data-center load
        if self.DC_load_present:
            self.load_plus_dc = self.raut.data_center_load(self.load_all_regions, self.system_directory, self.network_model)
        else:
            self.load_plus_dc = self.load_all_regions

    def run_pcm(self, sample_subdir, holder_dict, sample_no, var_s, LOL_track):
        """Execute PCM workflow and update curtailment tracking.

        Args:
            sample_subdir (str): Output directory for the current sample.
            holder_dict (dict): PCM state dictionary storing generation and limits.
            sample_no (int): Current Monte Carlo sample index.
            var_s: Current LOL state used by the tracking logic.
            LOL_track: Array tracking LOL state across samples and hours.

        Returns:
            tuple: updated var_s, updated LOL_track
        """
        
        pcm_obj = PCM(self.sim_hours, self.pcm_parameters, self.data, sample_subdir, holder_dict, self.load_factor)
        pcm_obj.export_pcm_yaml()
        pcm_obj.export_PCM_json()
        pcm_obj.modify_pcm_json()
        pcm_obj.run_PCM()
        load_curtailment_pcm = pcm_obj.extract_load_curtailment()
        for n in range(len(load_curtailment_pcm)):
            load_curt = load_curtailment_pcm[n]
            self.curt_rec[n] = load_curt
            var_s_new, LOL_track_new = self.raut.TrackLOLStates(load_curt, 1, var_s, LOL_track, sample_no, n)
        return var_s_new, LOL_track_new
    
    def export_sample_results(self, sample_subdir, s):
        """Export sample results to plots, CSV files, and outage records.

        Args:
            sample_subdir (str): Output directory for the current sample.
            s (int): Sample index used for file naming and plot labels.
        """
        # Plot ESS SOC, max capacity, and load curtailment
        rapt = RAPlotTools(self.data, sample_subdir, self.network_model)
        rapt.PlotSOC(self.SOC_rec, self.ess_params["essname"], s)
        if self.evaluate_degradation == True:
            rapt.PlotESCap(self.ess_smax_store, self.ess_params["essname"], s)
        rapt.PlotLoadCurt(self.curt_rec, s)

        # print solar gen, wind gen, and ESS SOC in csv files
        timestamps = pd.date_range(start="2026-01-01 00:00",
                                    periods=self.renewable_rec["solar_rec"].T.shape[0],
                                    freq="h")
        row_names = " " + timestamps.strftime("%m/%d %H:%M")
        df_solar_csv = pd.DataFrame(self.renewable_rec["solar_rec"].T, columns= self.bus_params["busname"], index=row_names)
        df_solar_csv.to_csv(f"{sample_subdir}/solar_gen.csv", index=True)
        df_wind_csv = pd.DataFrame(self.renewable_rec["wind_rec"].T, columns=self.bus_params["busname"], index=row_names)
        df_wind_csv.to_csv(f"{sample_subdir}/wind_gen.csv", index=True)
        df_SOC_csv = pd.DataFrame(self.SOC_rec.T, columns = self.ess_params["essname"], index=row_names)
        df_SOC_csv.to_csv(f"{sample_subdir}/ESS_SOC.csv", index=True)

        # save outage hour data to excel file
        if sum(self.curt_rec) > 0:
            df_Pg = pd.DataFrame(np.transpose(np.vstack(self.Pg_rec)), index=list(self.gen_params["genname"]))
            df_Pg.columns = self.out_hours

            if self.network_model in ['Zonal', 'Nodal']:
                df_flow = pd.DataFrame(np.transpose(np.vstack(self.flow_rec)), index=list(self.line_params["branchname"]))
                df_flow.columns = self.out_hours

            df_curt= pd.DataFrame(np.transpose(np.vstack(self.curtbus_rec)), index=list(self.bus_params["busname"]))
            df_curt.columns = self.out_hours

            df_ESS= pd.DataFrame(np.transpose(np.vstack(self.ESS_rec)), index=list(self.ess_params["essname"]))
            df_ESS.columns = self.out_hours

            df_wind= pd.DataFrame(np.transpose(np.vstack(self.wind_rec)), index=list(self.bus_params["busname"]))
            df_wind = df_wind[(df_wind != 0).any(axis=1)]
            df_wind.columns = self.out_hours

            df_solar= pd.DataFrame(np.transpose(np.vstack(self.solar_rec)), index=list(self.bus_params["busname"]))
            df_solar = df_solar[(df_solar != 0).any(axis=1)]
            df_solar.columns = self.out_hours

            with pd.ExcelWriter(f"{sample_subdir}/Outage_Records_Sample_{s+1}.xlsx", engine="openpyxl") as writer:
                df_Pg.to_excel(writer, sheet_name="conv_gen_MW")
                if self.network_model in ['Zonal', 'Nodal']:
                    df_flow.to_excel(writer, sheet_name="branch_loading_perc")
                df_curt.to_excel(writer, sheet_name="loadcurt_bus")
                df_ESS.to_excel(writer, sheet_name="ESS_net_exchange")
                df_wind.to_excel(writer, sheet_name="wind_gen_MW")
                df_solar.to_excel(writer, sheet_name="solar_gen")

                for ws in writer.book.worksheets:
                    for col in ws.columns:
                        max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col)
                        ws.column_dimensions[col[0].column_letter].width = max_len + 2

class MCS_hourly(MCS_samples):
    """Provides per-hour net load, renewable dispatch, and recording utilities.

    This class extends sample-level storage with hourly computations for net
    load, renewable generation, load curtailment recording, PCM data population,
    and battery degradation evaluation.
    """

    def __init__(self, mcs_samples):
        """Wrap an MCS_samples instance so hourly methods can access sample state."""
        self._mcs = mcs_samples

    def __getattr__(self, name):
        return getattr(self._mcs, name)

    def get_net_load(self, hour):
        """Compute net load and renewable outputs for a single hour.

        Args:
            hour (int): Hour index in the simulation horizon.

        Returns:
            tuple: net_load, total_renewable, wind_output, solar_output
        """
        # get wind power output for all zones/areas
        if self.wind_dir_exists:
            w_zones, self.current_w_class = self.raut.WindPower(self.bus_params["nz"], self.wind_params["w_sites"], self.wind_params["zone_no"], 
                                            self.wind_params["w_classes"], self.wind_params["r_cap"], self.current_w_class, self.wind_params["tr_mats"], self.wind_params["p_class"], 
                                            self.wind_params["w_turbines"], self.wind_params["out_curve2"], self.wind_params["out_curve3"])

        # get solar power output for all zones/areas
        if self.solar_dir_exists:
            s_zones = self.raut.SolarPower(hour, self.bus_params["nz"], self.solar_params["s_zone_no"], self.solar_params["solar_prob"], self.solar_params["s_profiles"], 
                                      self.solar_params["s_sites"], self.solar_params["s_max"])

        # record wind and solar profiles for plotting (optional)
        if self.wind_dir_exists:
            self.renewable_rec["wind_rec"][:, hour] = w_zones

        if self.solar_dir_exists:
            s_zones_t = np.transpose(s_zones)
            self.renewable_rec["solar_rec"][:, hour] = s_zones_t[:, hour%24]

        # recalculate net load (for distribution side resources, optional)
        part_netload = self.load_factor*self.load_plus_dc.values

        if self.solar_dir_exists and self.wind_dir_exists:
            net_load =  part_netload[hour] - w_zones - s_zones[hour%24]
            tot_ren = w_zones + s_zones[hour%24]
        elif self.solar_dir_exists==False and self.wind_dir_exists:
            net_load = part_netload[hour] - w_zones
            tot_ren = w_zones
        elif self.solar_dir_exists and self.wind_dir_exists==False:
            net_load = part_netload[hour] - s_zones[hour%24]
            tot_ren = s_zones[hour%24]
        elif self.solar_dir_exists==False and self.wind_dir_exists==False:
            net_load = part_netload[hour]
            tot_ren = np.zeros(self.bus_params["nz"])

        return net_load, tot_ren, w_zones, s_zones
    
    def record_hourly_data(self, load_curt, SOC_profile, P_dis, P_ch, Pg, curtbus, w_zones, s_zones_t, hour, flow, current_day):
        """Record hourly state and outage information for the current simulation step.

        Args:
            load_curt: Load curtailment vector or scalar for the current hour.
            SOC_profile: ESS state of charge profile.
            P_dis: ESS discharge power.
            P_ch: ESS charge power.
            Pg: Generator dispatch matrix or vector.
            curtbus: Load curtailment by bus.
            w_zones: Wind generation by zone.
            s_zones_t: Solar generation time-series transpose matrix.
            hour (int): Current hour index.
            flow: Branch flow data for the current hour (optional).
            current_day: Current day index for multi-period recording (optional).
        """
        
        time_periods = self.time_periods
        if self.optimization_period == "single_period":
            self.SOC_rec[:, hour] = SOC_profile*self.BMva
            self.Pdis_rec[:, hour] = P_dis*self.BMva
            self.Pch_rec[:, hour] = P_ch*self.BMva
            self.curt_rec[hour] = load_curt*self.BMva

            if load_curt > 0:
                self.out_hours.append((datetime(2001,1,1) + timedelta(hours=hour)).strftime("%b %d %H:%M"))
                self.Pg_rec.append(Pg * self.BMva)

                if self.network_model in ['Zonal', 'Nodal']:
                    self.flow_rec.append(flow*self.BMva/self.line_params["cap_trans"]*100)

                self.curtbus_rec.append(curtbus*self.BMva)
                self.ESS_rec.append((P_dis + P_ch)*self.BMva)
                self.wind_rec.append(w_zones)
                self.solar_rec.append(s_zones_t[:, hour%24])
        
        if self.optimization_period == "multi_period":
            self.SOC_rec[:, hour-time_periods+1:hour+1] = SOC_profile*self.BMva
            self.Pch_rec[:, hour-time_periods+1:hour+1] = P_ch*self.BMva
            self.Pdis_rec[:, hour-time_periods+1:hour+1] = P_dis*self.BMva
            self.curt_rec[hour-time_periods+1:hour+1] = load_curt*self.BMva
            if np.any(load_curt):
                curt_hours = np.where(load_curt != 0)[0]
                curt_actual = current_day * 24 + curt_hours

                for i, h in enumerate(curt_actual):
                    self.out_hours.append(
                        (datetime(2001,1,1) + timedelta(hours=int(h))).strftime("%b %d %H:%M")
                    )

                    ch = curt_hours[i]

                    self.Pg_rec.append(Pg[:, ch] * self.BMva)

                    if self.network_model in ['Zonal', 'Nodal']:
                        self.flow_rec.append(flow[:, ch] * self.BMva/self.line_params["cap_trans"]*100)

                    self.curtbus_rec.append(curtbus[:, ch] * self.BMva)
                    self.ESS_rec.append((P_dis[:, ch] + P_ch[:, ch]) * self.BMva)
                    self.wind_rec.append(self.renewable_rec["wind_rec"][:, h])
                    self.solar_rec.append(self.renewable_rec["solar_rec"][:, h])

    def populate_pcm_data(self, hour, ng, nl, ness, current_cap, ess_smax, ess_smin, holder_dict):
        """Populate PCM tracking dictionaries with current capacity and renewable limits.

        Args:
            hour (int): Current simulation hour.
            ng (int): Number of conventional generators.
            nl (int): Number of transmission lines.
            ness (int): Number of ESS units.
            current_cap: Current component capacity limits.
            ess_smax: Current ESS maximum energy capacity limits.
            holder_dict (dict): PCM data structure for limits and status.
        """

        for i in range(ng + nl + ness):
            if i < ng:
                gen_name = self.gen_params["genname"].loc[i]
                holder_dict["tg_status"][gen_name].append(current_cap["max"][i]/self.gen_params["pmax"][i])
            elif i >= ng and i < ng + nl:
                line_name = self.line_params["branchname"].loc[i-ng]
                holder_dict["line_status"][line_name].append(current_cap["max"][i]/self.line_params["cap_trans"][i-ng])
            elif i >= ng + nl and i < ng + nl + ness:
                ess_name = self.ess_params["essname"].loc[i-ng-nl]
                holder_dict["ess_pmax_limit"][ess_name].append(current_cap["max"][i])
                holder_dict["ess_smax_limit"][ess_name].append(ess_smax[i-ng-nl])
                holder_dict["ess_smin_limit"][ess_name].append(ess_smin[i-ng-nl])
        if self.wind_dir_exists:
            w_zones, current_w_class = self.raut.WindPower(self.bus_params["nz"], self.wind_params["w_sites"], self.wind_params["zone_no"], 
                                            self.wind_params["w_classes"], self.wind_params["r_cap"], self.current_w_class, self.wind_params["tr_mats"], self.wind_params["p_class"], 
                                            self.wind_params["w_turbines"], self.wind_params["out_curve2"], self.wind_params["out_curve3"])
            for i in range(self.wind_params["w_sites"]):
                site_name = self.wind_params["farm_name"].loc[i]
                holder_dict["wind_limit"][site_name].append(self.raut.w_power[i])
        if self.solar_dir_exists:
            if hour%24 == 0:
                s_zones, s_gen_sites = self.raut.SolarPower(hour, self.bus_params["nz"], self.solar_params["s_zone_no"], self.solar_params["solar_prob"], self.solar_params["s_profiles"], 
                                      self.solar_params["s_sites"], self.solar_params["s_max"], return_site_gen = True)
                for i in range(self.solar_params["s_sites"]):
                    site_name = self.solar_params["farm_name"].loc[i]
                    holder_dict["solar_limit"][site_name].extend(list(s_gen_sites[i, :]))
        for bus_name in self.bus_params["busname"].values:
            holder_dict["load"][bus_name].append(self.load_plus_dc.loc[hour, bus_name])
            
    def degradation_evaluation(self, n, ess_duration_temp, SOC_old):
        """Evaluate battery degradation at configured degradation intervals.

        This method computes C-rate profiles, temperature profiles, and updates
        state of charge and duration deratings for ESS units when the current
        hour reaches a degradation checkpoint.

        Args:
            n (int): Current hour index in the simulation.
            ess_duration_temp: Array of ESS durations subject to degradation.
            SOC_old: Previous SOC values used for degradation tracking.

        Returns:
            tuple: updated SOC_old, updated ess_duration_temp
        """
        if (n+1)%self.degradation_interval == 0:

            for ess_idx, ess_name in enumerate(self.ess_params["essname"]):
                if self.ess_params["ess_chemistry"][ess_idx] not in ["LFP", "NMC", "NCA", "LMO"]:
                    continue
                current_window_start = n + 1 - self.degradation_interval
                current_deg_instance = self.degradation_instances[ess_name]

                current_dis_Crates, current_overall_Crates = current_deg_instance.evaluate_C_rates(self.Pch_rec[ess_idx,current_window_start:n+1], 
                                                                            self.Pdis_rec[ess_idx,current_window_start:n+1], 
                                                                            self.ess_params["ess_sbase"][ess_idx], 
                                                                            self.ess_params["ess_eff"][ess_idx]) 
                if self.detailed_thermal_model == False:
                    current_temp_profile = np.ones(len(current_overall_Crates))*25
                else:
                    current_temp_profile = current_deg_instance.evaluate_cell_temp(current_overall_Crates, self.SOC_old_deg[ess_name]) 
                self.c_rate_holder[ess_name][current_window_start:n+1] = current_dis_Crates
                self.temp_holder[ess_name][current_window_start:n+1] = current_temp_profile
                soc_profile_norm = self.SOC_rec[ess_idx,:n+1]/self.ess_params["ess_sbase"][ess_idx]  
                
                current_deg_instance.update_instance(soc_profile_norm, self.c_rate_holder[ess_name][:n+1], self.temp_holder[ess_name][:n+1])
                current_deg_instance.calculate_total_degradation()
                ess_duration_temp[ess_idx] = self.ess_params["ess_duration"][ess_idx] * (1-current_deg_instance.L)
                SOC_old[ess_idx] = SOC_old[ess_idx] * (1-current_deg_instance.L)
                self.SOC_old_deg[ess_name] = soc_profile_norm[-1]

        return SOC_old, ess_duration_temp

                