import numpy as np
from time import perf_counter
from pyomo.environ import *
import copy
import pandas as pd
import os
import yaml

from .mod_sysdata import RASystemData
from .mod_solar import Solar
from .mod_wind import Wind
from .mod_utilities import RAUtilities
from .mod_matrices import RAMatrices
from .mod_plot import RAPlotTools
from .mod_kmeans import KMeans_Pipeline
from datetime import datetime

def MCS(input_file):
    """
    Executes a Mixed Time Sequential Monte Carlo Simulation (MCS) for reliability analysis using data from various RA modules.

    **Overview of the Process**:

    1. **Configuration & Setup**:
       - Reads simulation parameters (e.g., number of samples, simulation hours, file locations) from a YAML file.
       - Initializes paths for system data, wind data, and solar data.
    
    2. **System Data & Preprocessing**:
       - Creates instances of :class:`RASystemData <.mod_sysdata.RASystemData>` and :class:`RAUtilities <.mod_utilities.RAUtilities>` to read generator, branch, bus, load, and storage data, along with their reliability parameters (Mean Time To Failure, Mean Time To Repair, etc.).
       - Computes total transition rates and capacities for generation and transmission.

    3. **Wind & Solar Integration** (if specified):
       - Invokes :class:`Wind <.mod_wind.Wind>` and :class:`Solar <.mod_solar.Solar>` classes to download/process wind or solar data, build transition rate matrices, and retrieve probability distributions or generation profiles.

    4. **Matrices & Optimization Setup**:
       - Uses :class:`RAMatrices <.mod_matrices.RAMatrices>` to construct key model matrices (generator matrix, charging matrix, incidence matrix, curtailment matrix).
       - Defines internal bounds and callbacks for optimization variables.

    5. **Monte Carlo Simulation**:
       - For each sample (from 1 to ``samples``), simulates a full year (``sim_hours`` hours), updating component states (up/down) based on reliability transitions.
       - Recalculates available capacities, updates energy storage states, and computes net load after accounting for wind/solar generation.
       - Performs an optimization-based economic dispatch (Zonal or Copper Sheet approach) to serve load while minimizing curtailment, capturing load loss events as needed.
       - Tracks reliability indices, state-of-charge, and curtailment for output.

    6. **Index Calculation & Convergence**:
       - Accumulates reliability indices (e.g., LOLP, EUE) and checks partial convergence by computing the Coefficient of Variation (COV) of LOLP across samples.
       - Writes final reliability metrics to a CSV file and optionally produces an outage heat map if a full-year simulation (8760 hours) is performed.

    :param input_file: Path to the YAML configuration file that provides simulation settings.
    :type input_file: str

    :return:
        A tuple containing:

        * **indices** (*dict*): Final dictionary of reliability indices for the entire simulation.

        * **SOC_rec** (*np.ndarray*): Hourly state-of-charge records for each storage unit.

        * **curt_rec** (*np.ndarray*): Hourly load curtailment records for the system.

        * **renewable_rec** (*dict*): Wind and solar generation records for visualization.

        * **bus_name** (*list[str]*): Names of each bus in the system model.

        * **essname** (*list[str]*): Names of each energy storage unit.

        * **main_folder** (*str*): Absolute path to the directory containing this script.

        * **sim_hours** (*int*): Number of hours in the simulated year (e.g., 8760).

        * **samples** (*int*): Number of Monte Carlo samples iterated over.

        * **mLOLP_rec** (*np.ndarray*): Running mean of Loss of Load Probability across samples.

        * **COV_rec** (*np.ndarray*): Coefficient of Variation array used to check convergence.

    :rtype: tuple

    :raises FileNotFoundError: If the YAML config file or any required data file is not found.
    :raises ValueError: If the YAML config data has invalid or missing fields.
    :raises RuntimeError: If optimization fails or the underlying solver cannot converge.
    """

    # open configuration file
    with open(input_file, 'r') as f:
        config = yaml.safe_load(f)

    # data file locations
    system_directory = config['data'] + '/System'
    solar_directory = config['data'] + '/Solar'
    wind_directory = config['data'] + '/Wind'

    # Monte Carlo simulation parameters
    samples = config['samples']
    sim_hours = config['sim_hours']
    
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
        disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = rasd.storage(data_storage)

    raut = RAUtilities()
    mu_tot, lambda_tot = raut.reltrates(MTTF_gen, MTTF_trans, MTTR_gen, MTTR_trans, MTTF_ess, MTTR_ess)
    cap_max, cap_min = raut.capacities(nl, pmax, pmin, ess_pmax, ess_pmin, cap_trans) # calling this function to get values of cap_max and cap_min

    # download and process wind data
    if wind_directory:

        wind_sites = wind_directory + '/wind_sites.csv'
        wind_power_curves = wind_directory + '/w_power_curves.csv'
        windspeed_data = wind_directory + '/windspeed_data.csv'
        wind_tr_rate = wind_directory + '/t_rate.xlsx'
        
        wind = Wind()
        w_sites, farm_name, zone_no, w_classes, w_turbines, r_cap, p_class, out_curve2, out_curve3,\
            start_speed = wind.WindFarmsData(wind_sites, wind_power_curves)

        # calculate transition rates 
        wind.CalWindTrRates(wind_directory, windspeed_data, wind_sites, wind_power_curves)

        tr_mats = pd.read_excel(wind_tr_rate, sheet_name=None)
        tr_mats = np.array([tr_mats[sheet_name].to_numpy() for sheet_name in tr_mats])

    # download and process solar data
    if solar_directory:

        solar_site_data = solar_directory+"/solar_sites.csv"
        solar_prob_data = solar_directory+"/solar_probs.csv"

        solar = Solar(solar_site_data, solar_directory)
        
        s_sites, s_zone_no, s_max, s_profiles, solar_prob = solar.GetSolarProfiles(solar_prob_data)

        # print("Solar data processing complete!")

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

    tic = perf_counter()
        
    for s in range(samples):

        print(f'Sample: {s+1}')

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
        curt_rec = np.zeros(sim_hours)
        # gen_rec = np.zeros((sim_hours, ng))

        for n in range(sim_hours):

            # get current states(up/down) and capacities of all system components
            next_state, current_cap, var_s["t_min"] = raut.NextState(var_s["t_min"], ng, ness, nl, \
                                                                     lambda_tot, mu_tot, current_state, cap_max, cap_min, ess_units)
            current_state = copy.deepcopy(next_state)
            
            # update SOC based on failures in ESS
            ess_smax, ess_smin, SOC_old = raut.updateSOC(ng, nl, current_cap, ess_pmax, ess_duration, ess_socmax, ess_socmin, SOC_old)

            # calculate upper and lower bounds of gens and tls
            gt_limits = {"g_lb": np.concatenate((current_cap["min"][0:ng]/BMva, current_cap["min"][ng + nl::]/BMva)), \
                         "g_ub": np.concatenate((current_cap["max"][0:ng]/BMva, current_cap["max"][ng + nl::]/BMva)), "tl": current_cap["max"][ng:ng + nl]/BMva}
            
            def fb_Pg(model, i):
                return (gt_limits["g_lb"][i], gt_limits["g_ub"][i])

            def fb_flow(model,i):
                return (-gt_limits["tl"][i], gt_limits["tl"][i])
            
            def fb_ess(model, i):
                return(-current_cap["max"][ng + nl::][i]/BMva, current_cap["min"][ng + nl::][i]/BMva)
            
            def fb_soc(model, i):
                return(ess_smin[i]/BMva, ess_smax[i]/BMva)
            
            # get wind power output for all zones/areas
            if wind_directory:
                w_zones, current_w_class = raut.WindPower(nz, w_sites, zone_no, \
                w_classes, r_cap, current_w_class, tr_mats, p_class, w_turbines, out_curve2, out_curve3)

            # get solar power output for all zones/areas
            if solar_directory:
                s_zones = raut.SolarPower(n, nz, s_zone_no, solar_prob, s_profiles, s_sites, s_max)

            # record wind and solar profiles for plotting (optional)
            if wind_directory:
                renewable_rec["wind_rec"][:, n] = w_zones

            if solar_directory:
                s_zones_t = np.transpose(s_zones)
                renewable_rec["solar_rec"][:, n] = s_zones_t[:, n%24]

            # recalculate net load (for distribution side resources, optional)
            part_netload = config['load_factor']*load_all_regions

            if solar_directory and wind_directory:
                net_load =  part_netload[n] - w_zones - s_zones[n%24]
            elif solar_directory==False and wind_directory:
                net_load = part_netload[n] - w_zones
            elif solar_directory and wind_directory==False:
                net_load = part_netload[n] - s_zones[n%24]
            elif solar_directory==False and wind_directory==False:
                net_load = part_netload[n]
        
            # optimize dipatch and calculate load curtailment

            if config['model'] == 'Zonal':
                load_curt, SOC_old = raut.OptDispatch(ng, nz, nl, ness, fb_ess, fb_soc, BMva, fb_Pg, fb_flow, A_inc, gen_mat, curt_mat, ch_mat, \
                                                    gencost, net_load, SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost)
            elif config['model'] == 'Copper Sheet':
                load_curt, SOC_old = raut.OptDispatchLite(ng, nz, ness, fb_ess, fb_soc, BMva, fb_Pg, A_inc, \
                                                                gencost, net_load, SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost)
            
            # record values for visualization purposes
            SOC_rec[:, n] = SOC_old*BMva
            curt_rec[n] = load_curt*BMva

            # track loss of load states
            var_s, LOL_track = raut.TrackLOLStates(load_curt, BMva, var_s, LOL_track, s, n)

            if (n+1)%100 == 0:
                print(f'Hour {n + 1}')

        # collect indices for all samples
        indices_rec = raut.UpdateIndexArrays(indices_rec, var_s, sim_hours, s)

        # check for convergence using LOLP and COV
        indices_rec["mLOLP_rec"][s] = np.mean(indices_rec["LOLP_rec"][0:s+1])
        var_LOLP = np.var(indices_rec["LOLP_rec"][0:s+1])
        indices_rec["COV_rec"][s] = np.sqrt(var_LOLP)/indices_rec["mLOLP_rec"][s]

        # setting up folder for saving results for each sample
        if s == 0:
            main_folder = os.path.dirname(os.path.abspath(__file__))
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            results_subdir = os.path.join(main_folder, 'Results', timestamp)
            os.makedirs(results_subdir, exist_ok=True)
        
        sample_subdir = os.path.join(results_subdir, f'Sample {s + 1}')
        os.makedirs(sample_subdir, exist_ok=True)

        # plot results for each sample
        rapt = RAPlotTools(sample_subdir)
        rapt.PlotSolarGen(renewable_rec["solar_rec"], bus_name, s)
        rapt.PlotWindGen(renewable_rec["wind_rec"], bus_name, s)
        rapt.PlotSOC(SOC_rec, essname, s)
        rapt.PlotLoadCurt(curt_rec, s)

    # calculate reliability indices for the MCS
    indices = raut.GetReliabilityIndices(indices_rec, sim_hours, samples)

    # create folder for saving results for all samples
    all_subdir = os.path.join(results_subdir, 'Indices')
    os.makedirs(all_subdir, exist_ok=True)

    # save indices calculated in csv file
    df = pd.DataFrame([indices])
    df.to_csv(f"{all_subdir}/indices.csv", index=False)

    if sim_hours == 8760:
        raut.OutageHeatMap(LOL_track, 1, samples, all_subdir)

    toc = perf_counter()
    print(f"Codes finished in {toc-tic} seconds")

    return(indices, SOC_rec, curt_rec, renewable_rec, bus_name, essname, results_subdir, all_subdir, sim_hours, \
           samples, indices_rec["mLOLP_rec"], indices_rec["COV_rec"])

# =========================================================================================
#                                      SIMULATION 
# =========================================================================================

if __name__ == "__main__":
    
    # run MCS
    indices, SOC_rec, curt_rec, renewable_rec, bus_name, essname, results_subdir, all_subdir, sim_hours, \
        samples, mLOLP_rec, COV_rec = MCS('input.yaml')
    
    # plot indices for all samples after MCS is complete
    rapt = RAPlotTools(all_subdir)
    rapt.PlotLOLP(mLOLP_rec, samples, 1)
    rapt.PlotCOV(COV_rec, samples, 1)
    if sim_hours == 8760:
        rapt.OutageMap(f"{all_subdir}/LOL_perc_prob.csv")

