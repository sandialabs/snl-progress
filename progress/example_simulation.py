import numpy as np
from time import perf_counter
from pyomo.environ import *
import copy
import pandas as pd
import os
import sys
import shutil
import yaml
import argparse
import logging
from pathlib import Path
from progress.mod_sysdata import RASystemData
from progress.mod_utilities import RAUtilities
from progress.mod_mcs_utils import MCS_utils, MCS_samples, MCS_hourly
from progress.mod_plot import RAPlotTools
from datetime import datetime, timedelta
from progress.mod_bus_statistics import bus_statistics

logger = logging.getLogger(__name__)


class StopSimulation(Exception):
    """Raised when the user requests the simulation to stop."""


def MCS(input_file, results_subdir, stop_event=None) :   
    '''This function performs mixed time sequential MCS using methods from the different RA modules'''
 
    # open configuration file
    with open(input_file, 'r') as f:
        config = yaml.safe_load(f)

    mcs_params = MCS_utils(config)
    bus_params, gen_params, line_params, load_all_regions, ess_params = mcs_params.initialize_params()

    #Extract some commonly used parameters
    samples = mcs_params.samples
    sim_hours = mcs_params.sim_hours
    ng = gen_params["ng"]
    nl = line_params["nl"]
    ness = ess_params["ness"]
    nz = mcs_params.bus_params["nz"]
    BMva = mcs_params.BMva
   
    optimization_period = mcs_params.optimization_period
    time_periods = mcs_params.time_periods
    network_model = mcs_params.network_model
    
    mcs_params.process_renewable_data()
    gen_mat, ch_mat, A_inc, curt_mat, indices_rec, LOL_track = mcs_params.process_matrices()

    # Instanciate commonly used classes
    raut = RAUtilities()

    tic = perf_counter()
        
    for s in range(samples):

        print(f'Sample: {s+1}')
        
        sample_instance= MCS_samples(mcs_params)
        sample_instance.initialize_sample_data()
        if optimization_period == "multi_period":
            holder_dict = sample_instance.holder_dict
            ess_smax_store = np.zeros((ness,sim_hours))

        # initalize sample components that will be modified within the hourly loop
        current_state = np.ones(ng + nl + ness) # all gens and TLs in up state at the start of the year
         # temp variables to be used for each sample
        var_s = {"t_min": 0, "LLD": 0, "curtailment": np.zeros(sim_hours), "label_LOLF": np.zeros(sim_hours), "freq_LOLF": 0, "LOL_days": 0, \
                 "outage_day": np.zeros(365)}
        # Initialize ESS SOC and duration which will be updated after dispatch and degradation evaluation in each hour
        SOC_old = 0.5*(np.multiply(np.multiply(ess_params["ess_pmax"], ess_params["ess_duration"]), ess_params["ess_socmax"]))/BMva
        ess_duration_temp = ess_params["ess_duration"].astype(float).copy()
        ESS_initial_capacities = ess_params["ess_pmax"].copy()
        
        for n in range(mcs_params.sim_hours):
            
            hourly_instance = MCS_hourly(sample_instance)
            # get current states(up/down) and capacities of all system components
            next_state, current_cap, var_s["t_min"] = raut.NextState(var_s["t_min"], ng, ness, nl, mcs_params.lambda_tot, mcs_params.mu_tot, \
                                                                     current_state, mcs_params.cap_max, mcs_params.cap_min, ess_params["ess_units"])
            current_state = copy.deepcopy(next_state)
            net_load, tot_ren, w_zones, s_zones = hourly_instance.get_net_load(n)
            
            # optimize dipatch and calculate load curtailment
            if optimization_period == "single_period":

                # calculate upper and lower bounds of gens and tls
                ess_smax, ess_smin, SOC_old = raut.updateSOC(ng, nl, current_cap, ess_params["ess_pmax"], ess_duration_temp, ess_params["ess_socmax"], ess_params["ess_socmin"], SOC_old)
                sample_instance.ess_smax_store[:, n] = ess_smax

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
            
                if network_model in ['Zonal', 'Nodal']:
                    load_curt, SOC_old, P_dis, P_ch, Pg, flow, curtbus = raut.OptDispatch(ng, nz, nl, ness, fb_ess, fb_soc, BMva, fb_Pg, fb_flow, A_inc, gen_mat, curt_mat, ch_mat, \
                                                        gen_params["gencost"], net_load, SOC_old, ess_params["ess_pmax"], ess_params["ess_eff"], ess_params["disch_cost"], ess_params["ch_cost"], copper_sheet = False)
                elif network_model == 'Copper Sheet':
                    load_curt, SOC_old, P_dis, P_ch, Pg, flow, curtbus = raut.OptDispatch(ng, nz, nl, ness, fb_ess, fb_soc, BMva, fb_Pg, fb_flow, A_inc, gen_mat, curt_mat, ch_mat,  \
                                                                    gen_params["gencost"], net_load, SOC_old, ess_params["ess_pmax"], ess_params["ess_eff"], ess_params["disch_cost"], ess_params["ch_cost"], copper_sheet = True)
                # Store hourly and outage-specific data
                hourly_instance.record_hourly_data(load_curt, SOC_old, P_dis, P_ch, Pg, curtbus, w_zones, s_zones, n, flow, None)
                # track loss of load states
                var_s, LOL_track = raut.TrackLOLStates(load_curt, BMva, var_s, LOL_track, s, n)

            if optimization_period  == "multi_period" and not mcs_params.enable_pcm:
                
                current_day,_ = divmod(n, 24)
                normalized_hour = n%time_periods

                ess_smax, ess_smin, _ = raut.updateSOC(ng, nl, current_cap, ess_params["ess_pmax"], ess_duration_temp, ess_params["ess_socmax"], ess_params["ess_socmin"], SOC_old)
                sample_instance.ess_smax_store[:, n] = ess_smax

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
                    
                    if network_model in ['Zonal', 'Nodal']:
                        
                        load_curt, SOC_profile, P_dis, P_ch, Pg, flow, curtbus = raut.OptDispatchMP(ng, nz, nl, ness, fb_ess, fb_soc, fb_ren, BMva, fb_Pg, fb_flow, \
                                                                                                    A_inc, gen_mat, curt_mat, ch_mat, gen_params["gencost"], holder_dict["net_load"], \
                                                                                                    SOC_old, ESS_initial_capacities, ess_params["ess_pmax"], ess_params["ess_eff"], \
                                                                                                    ess_params["disch_cost"], ess_params["ch_cost"], time_periods, copper_sheet = False)
                    elif network_model == 'Copper Sheet':
                        load_curt, SOC_profile, P_dis, P_ch, Pg, flow, curtbus = raut.OptDispatchMP(ng, nz, nl, ness, fb_ess, fb_soc, fb_ren, BMva, fb_Pg, fb_flow, A_inc, 
                                                                                                    gen_mat, curt_mat, ch_mat, gen_params["gencost"], holder_dict["net_load"], \
                                                                                                    SOC_old, ESS_initial_capacities, ess_params["ess_pmax"], ess_params["ess_eff"], \
                                                                                                    ess_params["disch_cost"], ess_params["ch_cost"], time_periods, copper_sheet = True)
                    
                    # record values for initilzing next optimiation period
                    SOC_old = SOC_profile[:,-1]
                    ESS_initial_capacities = current_cap["max"][ng + nl::]
                    sample_instance.initialize_holder_vars(holder_dict)
                    # Store hourly and outage-specific data
                    hourly_instance.record_hourly_data(load_curt, SOC_profile, P_dis, P_ch, Pg, curtbus, w_zones, s_zones, n, flow, current_day)
                    
                    # track loss of load states
                    for i in range(time_periods):
                        start_day = int(current_day+1-time_periods/24)
                        current_n = start_day * 24 + i
                        var_s, LOL_track = raut.TrackLOLStates(load_curt[i], BMva, var_s, LOL_track, s, current_n)
            
            if mcs_params.enable_pcm:
                ess_smax, ess_smin, _ = raut.updateSOC(ng, nl, current_cap, ess_params["ess_pmax"], ess_duration_temp, ess_params["ess_socmax"], ess_params["ess_socmin"], SOC_old)
                hourly_instance.populate_pcm_data(n, ng, nl, ness, current_cap, ess_smax, ess_smin, holder_dict)

            if mcs_params.evaluate_degradation == True and not mcs_params.enable_pcm:
                if (n+1)%time_periods == 0:
                    SOC_old, ess_duration_temp = hourly_instance.degradation_evaluation(n, ess_duration_temp, SOC_old)

            if (n+1)%100 == 0:
                logger.info(f'Hour {n + 1}')
        
        # setting up folder for saving results for each sample
        sample_subdir = os.path.join(results_subdir, f'Sample_{s + 1}')
        os.makedirs(sample_subdir, exist_ok=True)

        if mcs_params.enable_pcm:
            var_s, LOL_track = sample_instance.run_pcm(sample_subdir, holder_dict, s, var_s, LOL_track)

        # collect indices for all samples
        indices_rec = raut.UpdateIndexArrays(indices_rec, var_s, sim_hours, s)
        
        # check for convergence using LOLP and COV
        indices_rec["mLOLP_rec"][s] = np.mean(indices_rec["LOLP_rec"][0:s+1])
        var_LOLP = np.var(indices_rec["LOLP_rec"][0:s+1])
        indices_rec["COV_rec"][s] = np.sqrt(var_LOLP)/indices_rec["mLOLP_rec"][s]

        if not mcs_params.enable_pcm:
            sample_instance.export_sample_results(sample_subdir, s)

    # calculate reliability indices for the MCS
    indices = raut.GetReliabilityIndices(indices_rec, sim_hours, samples)

    # save indices calculated in csv file
    df = pd.DataFrame([indices])
    df.to_csv(f"{results_subdir}/indices.csv", index=False)

    if sim_hours == 8760:
        raut.OutageHeatMap(LOL_track, 1, samples, results_subdir)

    # save config file alongside results for reproducibility
    config_out = Path(results_subdir) / "config.txt"
    with open(input_file) as f_in, open(config_out, "w") as f_out:
        for line in f_in:
            stripped = line.lstrip()
            if stripped.startswith("#") or stripped.startswith("data:"):
                continue
            comment_pos = line.find(" #")
            if comment_pos != -1:
                line = line[:comment_pos] + "\n"
            f_out.write(line)

    toc = perf_counter()
    logger.info(f"Codes finished in {toc-tic} seconds")

    # get outage statistics for affected buses
    bus_statistics(results_subdir)

    return(indices, sim_hours, samples, indices_rec["mLOLP_rec"], indices_rec["COV_rec"])

# =========================================================================================
#                                      SIMULATION 
# =========================================================================================
if __name__ == "__main__":
     # --- Force logging to stdout so terminal shows progress ---
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    root.addHandler(handler)
    root.setLevel(logging.INFO)
    # --- Parse CLI args ---
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to YAML configuration file. Default: input.yaml")
    parser.add_argument("--out", help="Optional: output directory. If not provided, a new Results_<timestamp> folder will be created.")
    args = parser.parse_args()

    # --- Determine input YAML ---
    if args.config:
        config_file = os.path.abspath(args.config)
    else:
        config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "input.yaml"))

    # --- Determine output folder ---
    if args.out:
        main_folder = os.path.abspath(args.out)
        results_subdir = main_folder
    else:
        main_folder = os.path.dirname(os.path.abspath(__file__))
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        results_subdir = os.path.join(main_folder, 'Results', timestamp)
        os.makedirs(results_subdir, exist_ok=True)
        
    # run MCS
    indices, sim_hours, samples, mLOLP_rec, COV_rec = MCS(config_file, results_subdir)
    
    # open configuration file
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    network_model = config['model']
    
    # plot indices for all samples after MCS is complete
    rapt = RAPlotTools(config["data"], results_subdir, network_model)
    if samples > 1 and sum(mLOLP_rec) > 0:
        rapt.PlotLOLP(mLOLP_rec, samples, 1)
        rapt.PlotCOV(COV_rec, samples, 1)
    if sim_hours == 8760:
        rapt.OutageMap(f"{results_subdir}/LOL_perc_prob.csv")

    # get outage statistics for affected buses
    # bus_statistics(results_subdir)
