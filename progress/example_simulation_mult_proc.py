from networkx import config
import numpy as np
from time import perf_counter
from pyomo.environ import *
import copy
import pandas as pd
import os
from mpi4py import MPI
import yaml
from datetime import datetime
import argparse

from mod_sysdata import RASystemData
from mod_solar import Solar
from mod_wind import Wind
from mod_utilities import RAUtilities
from mod_matrices import RAMatrices
from mod_plot import RAPlotTools
from mod_kmeans import KMeans_Pipeline
from mod_degradation import BESS_Degradation

class ProgressMultiProcess:

    def __init__(self):
        
        # for parallel processing
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()

    def MCS(self, input_file, main_folder) :   
        '''This function performs mixed time sequential MCS using methods from the different RA modules'''

        # open configuration file
        with open(input_file, 'r') as f:
            config = yaml.safe_load(f)

        # data file locations
        system_directory = config['data'] + '/System'
        solar_directory = config['data'] + '/Solar'
        wind_directory = config['data'] + '/Wind'
        solar_dir_exists = os.path.exists(solar_directory)
        wind_dir_exists = os.path.exists(wind_directory)
        # Monte Carlo simulation parameters
        samples = config['samples']
        sim_hours = config['sim_hours']
        time_periods = config['optimization_period']
        if time_periods == 1:
            optimization_period = "single_period"
        else:
            optimization_period = "multi_period"
        evaluate_degradation = config['evaluate_degradation']
        detailed_thermal_model = config['detailed_thermal_model']
        degradation_interval = config['degradation_interval']

        # system data
        data_gen = system_directory + '/gen.csv'
        data_branch = system_directory + '/branch.csv'
        data_bus = system_directory + '/bus.csv'
        data_load = system_directory + '/load.csv'
        data_storage = system_directory + '/storage.csv'
        BMva = 100

        rasd = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = rasd.gen(data_gen)
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = rasd.branch(data_branch)
        bus_name, bus_no, nz = rasd.bus(data_bus)
        load_all_regions = rasd.load(bus_name, data_load)

        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
            disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units, ess_chemistry = rasd.storage(data_storage)
        ess_sbase = ess_pmax*ess_duration

        raut = RAUtilities()
        mu_tot, lambda_tot = raut.reltrates(MTTF_gen, MTTF_trans, MTTR_gen, MTTR_trans, MTTF_ess, MTTR_ess)
        cap_max, cap_min = raut.capacities(nl, pmax, pmin, ess_pmax, ess_pmin, cap_trans) # calling this function to get values of cap_max and cap_min

        # download and process wind data
        if wind_dir_exists:

            wind_sites = wind_directory + '/wind_sites.csv'
            wind_power_curves = wind_directory + '/w_power_curves.csv'
            # windspeed_data = wind_directory + '/windspeed_data.csv'
            wind_tr_rate = wind_directory + '/t_rate.xlsx'
            
            wind = Wind()
                
            w_sites, farm_name, zone_no, w_classes, w_turbines, r_cap, p_class, out_curve2, out_curve3,\
                start_speed = wind.WindFarmsData(wind_sites, wind_power_curves)

            tr_mats = pd.read_excel(wind_tr_rate, sheet_name=None)
            tr_mats = np.array([tr_mats[sheet_name].to_numpy() for sheet_name in tr_mats])

        # download and process solar data
        if solar_dir_exists:

            solar_site_data = solar_directory+"/solar_sites.csv"
            solar_prob_data = solar_directory+"/solar_probs.csv"

            solar = Solar(solar_site_data, solar_directory)

            s_sites, s_zone_no, s_max, s_profiles, solar_prob = solar.GetSolarProfiles(solar_prob_data)

        # matrices required for optimization
        ramat = RAMatrices(nz)
        gen_mat = ramat.genmat(ng, genbus, ness, essbus)
        ch_mat = ramat.chmat(ness, essbus, nz)
        A_inc = ramat.Ainc(nl, fb, tb)
        curt_mat = ramat.curtmat(nz)

        # dictionary for storing temp. index values
        indices_rec = {"LOLP_rec": np.zeros(samples), "EUE_rec": np.zeros(samples), "MDT_rec": np.zeros(samples), \
                        "LOLF_rec": np.zeros(samples), "EPNS_rec": np.zeros(samples), "LOLP_hr": np.zeros(sim_hours), \
                            "LOLE_rec": np.zeros(samples),"mLOLP_rec":np.zeros(samples), "COV_rec": np.zeros(samples)}
        
        LOL_track = np.zeros((samples, sim_hours))
            
        for s in range(samples):

            print(f'Sample: {s+1}, Process No.: {self.rank}')

            # temp variables to be used for each sample
            var_s = {"t_min": 0, "LLD": 0, "curtailment": np.zeros(sim_hours), "label_LOLF": np.zeros(sim_hours), "freq_LOLF": 0, "LOL_days": 0, \
                    "outage_day": np.zeros(365)}

            # current states of components
            current_state = np.ones(ng + nl + ness) # all gens and TLs in up state at the start of the year

            if wind_directory:
                current_w_class = np.floor(np.random.uniform(0, 1, w_sites)*w_classes).astype(int) # starting wind speed class for each site (random)

            # record data for plotting and exporting (optional)
            renewable_rec = {"wind_rec": np.zeros((nz, sim_hours)), "solar_rec": np.zeros((nz, sim_hours)), "congen_temp": 0, \
                            "rengen_temp": 0}

            SOC_old = 0.5*(np.multiply(np.multiply(ess_pmax, ess_duration), ess_socmax))/BMva
            SOC_rec = np.zeros((ness, sim_hours))
            Pdis_rec = np.zeros((ness, sim_hours))
            Pch_rec = np.zeros((ness, sim_hours))
            curt_rec = np.zeros(sim_hours)

            if optimization_period == "multi_period":
                def initialize_holder_vars(holder_dict):
                    holder_dict["g_limit"] = {}
                    holder_dict["capacity"] = {}
                    holder_dict["net_load"] = np.zeros((nz, time_periods))
                    holder_dict["ren_limit"] = np.zeros((nz, time_periods))
                    holder_dict["ess_min"] = np.zeros((ness, time_periods))
                    holder_dict["ess_max"] = np.zeros((ness, time_periods))
                holder_dict = {}
                initialize_holder_vars(holder_dict)
            ess_duration_temp = ess_duration.astype(float).copy()
            ess_smax_store = np.zeros((ness, sim_hours))

            # Form the degradation instances for all ESS
            degradation_instances = {}
            c_rate_holder = {}
            temp_holder = {}
            SOC_old_deg = {}
            if evaluate_degradation == True:
                for ess_name, ess_chem in zip(essname, ess_chemistry):
                    if ess_chem not in ["LFP", "NMC", "NCA", "LMO"]:
                        continue
                    degradation_instances[ess_name] = BESS_Degradation(ess_chem)
                    c_rate_holder[ess_name] = np.zeros(sim_hours)
                    temp_holder[ess_name] = np.zeros(sim_hours)
                    SOC_old_deg[ess_name] = 0.5

            for n in range(sim_hours):

                # get current states(up/down) and capacities of all system components
                next_state, current_cap, var_s["t_min"] = raut.NextState(var_s["t_min"], ng, ness, nl, \
                                                                        lambda_tot, mu_tot, current_state, cap_max, cap_min, ess_units)
                current_state = copy.deepcopy(next_state)
                
                # get wind power output for all zones/areas
                if wind_dir_exists:
                    w_zones, current_w_class = raut.WindPower(nz, w_sites, zone_no, \
                    w_classes, r_cap, current_w_class, tr_mats, p_class, w_turbines, out_curve2, out_curve3)

                # get solar power output for all zones/areas
                if solar_dir_exists:
                    s_zones = raut.SolarPower(n, nz, s_zone_no, solar_prob, s_profiles, s_sites, s_max)

                # record wind and solar profiles for plotting (optional)
                if wind_dir_exists:
                    renewable_rec["wind_rec"][:, n] = w_zones

                if solar_dir_exists:
                    s_zones_t = np.transpose(s_zones)
                    renewable_rec["solar_rec"][:, n] = s_zones_t[:, n%24]

                # recalculate net load (for distribution side resources, optional)
                part_netload = config['load_factor']*load_all_regions

                if solar_dir_exists and wind_dir_exists:
                    net_load =  part_netload[n] - w_zones - s_zones[n%24]
                    tot_ren = w_zones + s_zones[n%24]
                elif solar_dir_exists==False and wind_dir_exists:
                    net_load = part_netload[n] - w_zones
                    tot_ren = w_zones
                elif solar_dir_exists and wind_dir_exists==False:
                    net_load = part_netload[n] - s_zones[n%24]
                    tot_ren = s_zones[n%24]
                elif solar_dir_exists==False and wind_dir_exists==False:
                    net_load = part_netload[n]
                    tot_ren = np.zeros(nz)
            
                # optimize dipatch and calculate load curtailment

                if optimization_period == "single_period":
                    # update SOC based on failures in ESS
                    ess_smax, ess_smin, SOC_old = raut.updateSOC(ng, nl, current_cap, ess_pmax, ess_duration_temp, ess_socmax, ess_socmin, SOC_old)
                    ess_smax_store[:, n] = ess_smax
                    # calculate upper and lower bounds of gens and tls
                    gt_limits = {"g_lb": np.concatenate((current_cap["min"][0:ng]/BMva, current_cap["min"][ng + nl::]/BMva)), \
                                "g_ub": np.concatenate((current_cap["max"][0:ng]/BMva, current_cap["max"][ng + nl::]/BMva)), \
                                "tl": current_cap["max"][ng:ng + nl]/BMva}
                    
                    def fb_Pg(model, i):
                        return (0, gt_limits["g_ub"][i])

                    def fb_flow(model,i):
                        return (-gt_limits["tl"][i], gt_limits["tl"][i])
                    
                    def fb_ess(model, i):
                        return(-current_cap["max"][ng + nl::][i]/BMva, current_cap["min"][ng + nl::][i]/BMva)
                    
                    def fb_soc(model, i):
                        return(ess_smin[i]/BMva, ess_smax[i]/BMva)
                
                    if config['model'] == 'Zonal':
                        load_curt, SOC_old, P_dis, P_ch = raut.OptDispatch(ng, nz, nl, ness, fb_ess, fb_soc, BMva, fb_Pg, fb_flow, A_inc, gen_mat, curt_mat, ch_mat, \
                                                            gencost, net_load, SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost)
                    elif config['model'] == 'Copper Sheet':
                        load_curt, SOC_old, P_dis, P_ch = raut.OptDispatchLite(ng, nz, ness, fb_ess, fb_soc, BMva, fb_Pg, A_inc, \
                                                                        gencost, net_load, SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost)
                    
                    # record values for visualization purposes
                    SOC_rec[:, n] = SOC_old*BMva
                    Pdis_rec[:, n] = P_dis*BMva
                    Pch_rec[:, n] = P_ch*BMva
                    curt_rec[n] = load_curt*BMva

                    # track loss of load states
                    var_s, LOL_track = raut.TrackLOLStates(load_curt, BMva, var_s, LOL_track, s, n)

                if optimization_period  == "multi_period":
                    
                    current_day,_ = divmod(n, 24)
                    normalized_hour = n%time_periods

                    ess_smax, ess_smin, _ = raut.updateSOC(ng, nl, current_cap, ess_pmax, ess_duration_temp, ess_socmax, ess_socmin, SOC_old)
                    ess_smax_store[:, n] = ess_smax
                    
                    if (n+1)%time_periods == 0:
                        _ , _ , SOC_old = raut.updateSOC(ng, nl, current_cap, ess_pmax, ess_duration_temp, ess_socmax, ess_socmin, SOC_old)

                    holder_dict["g_limit"][normalized_hour] = {"g_lb": np.concatenate((current_cap["min"][0:ng]/BMva, current_cap["min"][ng + nl::]/BMva)), \
                                "g_ub": np.concatenate((current_cap["max"][0:ng]/BMva, current_cap["max"][ng + nl::]/BMva)), \
                                "tl": current_cap["max"][ng:ng + nl]/BMva}
                    holder_dict["capacity"][normalized_hour] = current_cap
                    holder_dict["net_load"][:, normalized_hour] = net_load
                    holder_dict["ess_min"][:, normalized_hour] = ess_smin
                    holder_dict["ess_max"][:, normalized_hour] = ess_smax
                    holder_dict["ren_limit"][:, normalized_hour] = tot_ren

                    if (n+1)%time_periods == 0:

                        def fb_Pg(model, i, t):
                            return (0, holder_dict["g_limit"][t]["g_ub"][i])

                        def fb_flow(model,i, t):
                            return (-holder_dict["g_limit"][t]["tl"][i], holder_dict["g_limit"][t]["tl"][i])

                        def fb_ess(model, i, t):
                            return(-holder_dict["capacity"][t]["max"][ng + nl::][i]/BMva, holder_dict["capacity"][t]["min"][ng + nl::][i]/BMva)

                        def fb_soc(model, i, t):
                            return(holder_dict["ess_min"][i,t]/BMva, holder_dict["ess_max"][i,t]/BMva)

                        def fb_ren(model, i, t):
                            return(0, holder_dict["ren_limit"][i,t]/BMva)
                        
                        if config['model'] == 'Zonal':
                            load_curt, SOC_profile, P_dis, P_ch = raut.OptDispatchMP(ng, nz, nl, ness, fb_ess, fb_soc, fb_ren, BMva, fb_Pg, fb_flow, A_inc, gen_mat, curt_mat, ch_mat, \
                                                            gencost, holder_dict["net_load"], SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost, time_periods, copper_sheet = False)
                        elif config['model'] == 'Copper Sheet':
                            load_curt, SOC_profile, P_dis, P_ch = raut.OptDispatchMP(ng, nz, nl, ness, fb_ess, fb_soc, fb_ren, BMva, fb_Pg, fb_flow, A_inc, gen_mat, curt_mat, ch_mat, \
                                                            gencost, holder_dict["net_load"], SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost, time_periods, copper_sheet = True)

                        # record values for visualization purposes
                        SOC_rec[:, n-time_periods+1:n+1] = SOC_profile*BMva
                        Pch_rec[:, n-time_periods+1:n+1] = P_ch*BMva
                        Pdis_rec[:, n-time_periods+1:n+1] = P_dis*BMva
                        curt_rec[n-time_periods+1:n+1] = load_curt*BMva
                        SOC_old = SOC_profile[:,-1]
                        initialize_holder_vars(holder_dict)

                        # track loss of load states
                        for i in range(time_periods):
                            start_day = int(current_day+1-time_periods/24)
                            current_n = start_day * 24 + i
                            var_s, LOL_track = raut.TrackLOLStates(load_curt[i], BMva, var_s, LOL_track, s, current_n)
                    if evaluate_degradation == True:
                        if (n+1)%degradation_interval == 0:

                            for ess_idx, ess_name in enumerate(essname):
                                if ess_chemistry[ess_idx] not in ["LFP", "NMC", "NCA", "LMO"]:
                                    continue
                                current_window_start = n + 1 - degradation_interval
                                current_deg_instance = degradation_instances[ess_name]

                                current_dis_Crates, current_overall_Crates = current_deg_instance.evaluate_C_rates(Pch_rec[ess_idx,current_window_start:n+1], 
                                                                                            Pdis_rec[ess_idx,current_window_start:n+1], 
                                                                                            ess_sbase[ess_idx], 
                                                                                            ess_eff[ess_idx]) 
                                if detailed_thermal_model == False:
                                    current_temp_profile = np.ones(len(current_overall_Crates))*25
                                else:
                                    current_temp_profile = current_deg_instance.evaluate_cell_temp(current_overall_Crates, SOC_old_deg[ess_name]) 
                                c_rate_holder[ess_name][current_window_start:n+1] = current_dis_Crates
                                temp_holder[ess_name][current_window_start:n+1] = current_temp_profile
                                soc_profile_norm = SOC_rec[ess_idx,:n+1]/ess_sbase[ess_idx]  
                                
                                current_deg_instance.update_instance(soc_profile_norm, c_rate_holder[ess_name][:n+1], temp_holder[ess_name][:n+1])
                                current_deg_instance.calculate_total_degradation()
                                ess_duration_temp[ess_idx] = ess_duration[ess_idx] * (1-current_deg_instance.L)
                                SOC_old[ess_idx] = SOC_old[ess_idx] * (1-current_deg_instance.L)
                                SOC_old_deg[ess_name] = soc_profile_norm[-1]

                    if (n+1)%1000 == 0:
                        print(f'Hour {n + 1}, Process No.: {self.rank}')

            # collect indices for all samples
            indices_rec = raut.UpdateIndexArrays(indices_rec, var_s, sim_hours, s)

            mLOLP_rec, COV_rec = raut.CheckConvergence(s, indices_rec["LOLP_rec"], self.comm, self.rank, self.size, \
                                  indices_rec["mLOLP_rec"], indices_rec["COV_rec"])
            # plot results for each sample
            sample_subdir = os.path.join(main_folder, f'Sample_{s+1}_Process_{self.rank}')
            os.makedirs(sample_subdir, exist_ok=False)
            rapt = RAPlotTools(sample_subdir)
            rapt.PlotSolarGen(renewable_rec["solar_rec"], bus_name, s)
            rapt.PlotWindGen(renewable_rec["wind_rec"], bus_name, s)
            rapt.PlotSOC(SOC_rec, essname, s)
            rapt.PlotESCap(ess_smax_store, essname, s)
            rapt.PlotLoadCurt(curt_rec, s)
            
        # calculate reliability indices for the MCS
        indices = raut.GetReliabilityIndices(indices_rec, sim_hours, samples)
        raut.ParallelProcessing(indices, LOL_track, self.comm, self.rank, self.size, samples, sim_hours,main_folder)

        return(self.rank, SOC_rec, curt_rec, renewable_rec, bus_name, essname, main_folder, \
               sim_hours, mLOLP_rec, COV_rec, samples, self.size)

# =========================================================================================
#                                      SIMULATION 
# =========================================================================================

if __name__ == "__main__":
    # --- Parse CLI args ---
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to YAML configuration file. Default: ./progress/input.yaml")
    parser.add_argument("--out", help="Optional: output directory. If not provided, a new Results_<timestamp> folder will be created.")
    parser.add_argument("--optimization_period", default="multi_period")
    parser.add_argument("--time_periods", type=int, default=24)
    args = parser.parse_args()

    # --- Determine input YAML ---
    if args.config:
        config_file = os.path.abspath(args.config)
    else:
        config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "input.yaml"))

    # --- Initialize MPI-enabled class ---
    pmp = ProgressMultiProcess()
    rank = pmp.comm.Get_rank()

    # --- Determine output folder ---
    if args.out:
        main_folder = os.path.abspath(args.out)
        results_subdir = main_folder
    else:
        main_folder = os.path.dirname(os.path.abspath(__file__))
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        results_subdir = os.path.join(main_folder, "Results", timestamp)

    # --- Create directory (rank 0 only) ---
    if rank == 0:
        os.makedirs(results_subdir, exist_ok=True)
    pmp.comm.Barrier()  # wait for directory creation

    # run MCS
    rank, SOC_rec, curt_rec, renewable_rec, bus_name, essname, main_folder, sim_hours, \
          mLOLP_rec, COV_rec, samples, size = pmp.MCS(config_file, results_subdir)
    
    if rank == 0:
        # plot results
        rapt = RAPlotTools(main_folder)
        rapt.PlotLOLP(mLOLP_rec, samples, size)
        rapt.PlotCOV(COV_rec, samples, size)
        if sim_hours == 8760:
            rapt.OutageMap(f"{main_folder}/LOL_perc_prob.csv")

