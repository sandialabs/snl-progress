from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog
from progress.App.simulation.ui.ui_sim_gui import Ui_sim_widget
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from progress.paths import get_path
base_dir = get_path()
import os
from progress.App.gui_tools.tools import WorkerThread
from progress.mod_matrices import RAMatrices
from progress.mod_plot import RAPlotTools
import numpy as np
import pandas as pd
import copy
from datetime import datetime

class sim_form(QWidget, Ui_sim_widget):
    """Landing page widget."""

    page_changer_next = Signal()
    page_changer_previous = Signal()

    def __init__(self, data_handler, parent=None):
        """Sets up the UI file to show in the application"""
        super(sim_form, self).__init__(parent)
        self.setupUi(self)

        self.data_handler = data_handler

        self.pushButton_sim_previous.clicked.connect(lambda: self.page_changer_previous.emit())
        self.pushButton_6.clicked.connect(lambda: self.page_changer_next.emit())
        self.pushButton_5.clicked.connect(self.run)
        # self.sys_directory = os.path.join(base_dir, "Data", "System")
        # self.solar_directory = os.path.join(base_dir, "Data", "Solar")
        # self.wind_directory = os.path.join(base_dir, "Data", "Wind")

        self.plot_count = 0

    def handle_output(self, text_browser, text):
        # Update the GUI with the output text
        text_browser.append(text)

    def save_mcsinput(self):
        self.samples= int(self.lineEdit_4.text())
        self.sim_hours = int(self.lineEdit_5.text())
        self.load_factor = float(self.lineEdit_6.text())
        self.pushButton_5.setVisible(True)
        self.current_text = self.comboBox.currentText()
        QMessageBox.information(self, "Sim Input", "Input Saved!")

    def run(self):

        self.save_mcsinput()
        if self.current_text == "Zonal Model":
            self.worker_zonal = WorkerThread(self.MCS_zonal)

            #self.worker_zonal.output_updated.connect(self.handle_output)
            self.worker_zonal.output_updated.connect(lambda text: self.handle_output(self.textBrowser_2, text))
            self.worker_zonal.start()
            self.worker_zonal.finished.connect(self.plot)
        # self.output_window.show()

        elif self.current_text == "Copper Sheet Model":
            self.worker_copper= WorkerThread(self.MCS_cs)
            #self.worker_copper.output_updated.connect(self.handle_output)
            # Connect the output_updated signal to update the GUI
            self.worker_copper.output_updated.connect(lambda text: self.handle_output(self.textBrowser_2, text))

            self.worker_copper.start()
            self.worker_copper.finished.connect(self.plot)
        # self.output_window.show()

    def MCS_zonal(self):

        """
        Performs mixed time sequential Monte Carlo Simulation (MCS) to evaluate the reliability of a power system. Uses transportation model.

        Parameters:
        samples (int): Number of samples to simulate.
        sim_hours (int): Number of hours to simulate.
        system_directory (str): Path to the directory containing system data files.
        solar_directory (str or bool): Path to the directory containing solar data files or False if not used.
        wind_directory (str or bool): Path to the directory containing wind data files or False if not used.

        Returns:
        tuple: A tuple containing indices, rank, SOC records, curtailment records, renewable records, bus names, and ESS names.
        """

        BMva = 100

        # matrices required for optimization
        ramat = RAMatrices(self.data_handler.nz)
        gen_mat = ramat.genmat(self.data_handler.ng, self.data_handler.genbus, self.data_handler.ness, self.data_handler.essbus)
        ch_mat = ramat.chmat(self.data_handler.ness, self.data_handler.essbus, self.data_handler.nz)
        A_inc = ramat.Ainc(self.data_handler.nl, self.data_handler.fb, self.data_handler.tb)
        curt_mat = ramat.curtmat(self.data_handler.nz)

        # dictionary for storing temp. index values
        indices_rec = {"LOLP_rec": np.zeros(self.samples), "EUE_rec": np.zeros(self.samples), "MDT_rec": np.zeros(self.samples), \
                "LOLF_rec": np.zeros(self.samples), "EPNS_rec": np.zeros(self.samples), "LOLP_hr": np.zeros(self.sim_hours), \
                    "LOLE_rec": np.zeros(self.samples), "mLOLP_rec":np.zeros(self.samples), "COV_rec": np.zeros(self.samples)}

        LOL_track = np.zeros((self.samples, self.sim_hours))

        for s in range(self.samples):

            print(f'Sample: {s+1}')

            # temp variables to be used for each sample
            var_s = {"t_min": 0, "LLD": 0, "curtailment": np.zeros(self.sim_hours), "label_LOLF": np.zeros(self.sim_hours), "freq_LOLF": 0, "LOL_days": 0, \
                    "outage_day": np.zeros(365)}

            # current states of components
            current_state = np.ones(self.data_handler.ng + self.data_handler.nl + self.data_handler.ness) # all gens and TLs in up state at the start of the year

            if self.data_handler.wind_directory:
                current_w_class = np.floor(np.random.uniform(0, 1, self.data_handler.w_sites)*self.data_handler.w_classes).astype(int) # starting wind speed class for each site (random)

            # record data for plotting and exporting (optional)
            self.renewable_rec = {"wind_rec": np.zeros((self.data_handler.nz, self.sim_hours)), "solar_rec": np.zeros((self.data_handler.nz, self.sim_hours)), "congen_temp": 0, \
                            "rengen_temp": 0}

            SOC_old = 0.5*(np.multiply(np.multiply(self.data_handler.ess_pmax, self.data_handler.ess_duration), self.data_handler.ess_socmax))/BMva
            self.SOC_rec = np.zeros((self.data_handler.ness, self.sim_hours))
            self.curt_rec = np.zeros(self.sim_hours)
            # gen_rec = np.zeros((sim_hours, ng))

            for n in range(self.sim_hours):

                # get current states(up/down) and capacities of all system components
                next_state, current_cap, var_s["t_min"] = self.data_handler.raut.NextState(var_s["t_min"], self.data_handler.ng, self.data_handler.ness, self.data_handler.nl, \
                                                                        self.data_handler.lambda_tot, self.data_handler.mu_tot, current_state, self.data_handler.cap_max, self.data_handler.cap_min, self.data_handler.ess_units)
                current_state = copy.deepcopy(next_state)

                # update SOC based on failures in ESS
                ess_smax, ess_smin, SOC_old = self.data_handler.raut.updateSOC(self.data_handler.ng, self.data_handler.nl, current_cap, self.data_handler.ess_pmax, self.data_handler.ess_duration, self.data_handler.ess_socmax, \
                                                                self.data_handler.ess_socmin, SOC_old)

                # calculate upper and lower bounds of gens and tls
                gt_limits = {"g_lb": np.concatenate((current_cap["min"][0:self.data_handler.ng]/BMva, current_cap["min"][self.data_handler.ng + self.data_handler.nl::]/BMva)), \
                            "g_ub": np.concatenate((current_cap["max"][0:self.data_handler.ng]/BMva, current_cap["max"][self.data_handler.ng + self.data_handler.nl::]/BMva)), "tl": current_cap["max"][self.data_handler.ng:self.data_handler.ng + self.data_handler.nl]/BMva}

                def fb_Pg(model, i):
                    return (gt_limits["g_lb"][i], gt_limits["g_ub"][i])

                def fb_flow(model,i):
                    return (-gt_limits["tl"][i], gt_limits["tl"][i])

                def fb_ess(model, i):
                    return(-current_cap["max"][self.data_handler.ng + self.data_handler.nl::][i]/BMva, current_cap["min"][self.data_handler.ng + self.data_handler.nl::][i]/BMva)

                def fb_soc(model, i):
                    return(ess_smin[i]/BMva, ess_smax[i]/BMva)

                # get wind power output for all zones/areas
                if self.data_handler.wind_directory:
                    w_zones, current_w_class = self.data_handler.raut.WindPower(self.data_handler.nz, self.data_handler.w_sites, self.data_handler.zone_no, \
                    self.data_handler.w_classes, self.data_handler.r_cap, current_w_class, self.data_handler.tr_mats, self.data_handler.p_class, self.data_handler.w_turbines, self.data_handler.out_curve2, self.data_handler.out_curve3)

                # get solar power output for all zones/areas
                if self.data_handler.solar_directory:
                    s_zones = self.data_handler.raut.SolarPower(n, self.data_handler.nz, self.data_handler.s_zone_no, self.data_handler.solar_prob, self.data_handler.s_profiles, self.data_handler.s_sites, self.data_handler.s_max)

                # record wind and solar profiles for plotting (optional)
                if self.data_handler.wind_directory:
                    self.renewable_rec["wind_rec"][:, n] = w_zones

                if self.data_handler.solar_directory:
                    s_zones_t = np.transpose(s_zones)
                    self.renewable_rec["solar_rec"][:, n] = s_zones_t[:, n%24]

                # recalculate net load (for distribution side resources, optional)
                part_netload = self.load_factor*self.data_handler.load_all_regions

                if self.data_handler.solar_directory and self.data_handler.wind_directory:
                    net_load =  part_netload[n] - w_zones - s_zones[n%24]
                elif self.data_handler.solar_directory==False and self.data_handler.wind_directory:
                    net_load = part_netload[n] - w_zones
                elif self.data_handler.solar_directory and self.data_handler.wind_directory==False:
                    net_load = part_netload[n] - s_zones[n%24]
                elif self.data_handler.solar_directory==False and self.data_handler.wind_directory==False:
                    net_load = part_netload[n]

                # optimize dipatch and calculate load curtailment
                load_curt, SOC_old = self.data_handler.raut.OptDispatch(self.data_handler.ng, self.data_handler.nz, self.data_handler.nl, self.data_handler.ness, fb_ess, fb_soc, BMva, fb_Pg, fb_flow, A_inc, gen_mat, curt_mat, ch_mat, \
                                                    self.data_handler.gencost, net_load, SOC_old, self.data_handler.ess_pmax, self.data_handler.ess_eff, self.data_handler.disch_cost, self.data_handler.ch_cost)


                # record values for visualization purposes
                self.SOC_rec[:, n] = SOC_old*BMva
                self.curt_rec[n] = load_curt*BMva

                # track loss of load states
                var_s, LOL_track = self.data_handler.raut.TrackLOLStates(load_curt, BMva, var_s, LOL_track, s, n)

                if (n+1)%100 == 0:
                    print(f'Hour {n + 1}')

            # collect indices for all samples
            indices_rec = self.data_handler.raut.UpdateIndexArrays(indices_rec, var_s, self.sim_hours, s)

            # check for convergence using LOLP and COV
            indices_rec["mLOLP_rec"][s] = np.mean(indices_rec["LOLP_rec"][0:s+1])
            var_LOLP = np.var(indices_rec["LOLP_rec"][0:s+1])
            indices_rec["COV_rec"][s] = np.sqrt(var_LOLP)/indices_rec["mLOLP_rec"][s]

        # calculate reliability indices for the MCS
        indices = self.data_handler.raut.GetReliabilityIndices(indices_rec, self.sim_hours, self.samples)
        self.mLOLP_rec = indices_rec["mLOLP_rec"]
        self.COV_rec = indices_rec["COV_rec"]


        print("Simulation complete! You can view the results now by clicking next! Plots are also saved to the results folder.")
        self.pushButton_6.setVisible(True)

        self.main_folder = base_dir
        self.results_dir = os.path.join(self.main_folder, 'Results')

        if not os.path.exists(f"{self.main_folder}/Results"):
            os.makedirs(f"{self.main_folder}/Results")

        df = pd.DataFrame([indices])
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        results_subdir = os.path.join(self.main_folder, 'Results', timestamp)
        os.makedirs(results_subdir, exist_ok=True)
        df.to_csv(f"{results_subdir}/indices.csv", index=False)

        if self.sim_hours == 8760:
            self.data_handler.raut.OutageHeatMap(LOL_track, 1, self.samples, self.main_folder)

    def MCS_cs(self):

        """
        Performs mixed time sequential Monte Carlo Simulation (MCS) to evaluate the reliability of a power system. Uses copper sheet model.

        Parameters:
        samples (int): Number of samples to simulate.
        sim_hours (int): Number of hours to simulate.
        system_directory (str): Path to the directory containing system data files.
        solar_directory (str or bool): Path to the directory containing solar data files or False if not used.
        wind_directory (str or bool): Path to the directory containing wind data files or False if not used.

        Returns:
        tuple: A tuple containing indices, rank, SOC records, curtailment records, renewable records, bus names, and ESS names.
        """

        BMva = 100

        # matrices required for optimization
        ramat = RAMatrices(self.data_handler.nz)
        gen_mat = ramat.genmat(self.data_handler.ng, self.data_handler.genbus, self.data_handler.ness, self.data_handler.essbus)
        ch_mat = ramat.chmat(self.data_handler.ness, self.data_handler.essbus, self.data_handler.nz)
        A_inc = ramat.Ainc(self.data_handler.nl, self.data_handler.fb, self.data_handler.tb)
        curt_mat = ramat.curtmat(self.data_handler.nz)

        # dictionary for storing temp. index values
        indices_rec = {"LOLP_rec": np.zeros(self.samples), "EUE_rec": np.zeros(self.samples), "MDT_rec": np.zeros(self.samples), \
                "LOLF_rec": np.zeros(self.samples), "EPNS_rec": np.zeros(self.samples), "LOLP_hr": np.zeros(self.sim_hours), \
                    "LOLE_rec": np.zeros(self.samples), "mLOLP_rec":np.zeros(self.samples), "COV_rec": np.zeros(self.samples)}

        LOL_track = np.zeros((self.samples, self.sim_hours))

        for s in range(self.samples):

            print(f'Sample: {s+1}')

            # temp variables to be used for each sample
            var_s = {"t_min": 0, "LLD": 0, "curtailment": np.zeros(self.sim_hours), "label_LOLF": np.zeros(self.sim_hours), "freq_LOLF": 0, "LOL_days": 0, \
                    "outage_day": np.zeros(365)}

            # current states of components
            current_state = np.ones(self.data_handler.ng + self.data_handler.nl + self.data_handler.ness) # all gens and TLs in up state at the start of the year

            if self.data_handler.wind_directory:
                current_w_class = np.floor(np.random.uniform(0, 1, self.data_handler.w_sites)*self.data_handler.w_classes).astype(int) # starting wind speed class for each site (random)

            # record data for plotting and exporting (optional)
            self.renewable_rec = {"wind_rec": np.zeros((self.data_handler.nz, self.sim_hours)), "solar_rec": np.zeros((self.data_handler.nz, self.sim_hours)), "congen_temp": 0, \
                            "rengen_temp": 0}

            SOC_old = 0.5*(np.multiply(np.multiply(self.data_handler.ess_pmax, self.data_handler.ess_duration), self.data_handler.ess_socmax))/BMva
            self.SOC_rec = np.zeros((self.data_handler.ness, self.sim_hours))
            self.curt_rec = np.zeros(self.sim_hours)
            # gen_rec = np.zeros((sim_hours, ng))

            for n in range(self.sim_hours):

                # get current states(up/down) and capacities of all system components
                next_state, current_cap, var_s["t_min"] = self.data_handler.raut.NextState(var_s["t_min"], self.data_handler.ng, self.data_handler.ness, self.data_handler.nl, \
                                                                        self.data_handler.lambda_tot, self.data_handler.mu_tot, current_state, self.data_handler.cap_max, self.data_handler.cap_min, self.data_handler.ess_units)
                current_state = copy.deepcopy(next_state)

                # update SOC based on failures in ESS
                ess_smax, ess_smin, SOC_old = self.data_handler.raut.updateSOC(self.data_handler.ng, self.data_handler.nl, current_cap, self.data_handler.ess_pmax, self.data_handler.ess_duration, self.data_handler.ess_socmax, \
                                                                self.data_handler.ess_socmin, SOC_old)

                # calculate upper and lower bounds of gens and tls
                gt_limits = {"g_lb": np.concatenate((current_cap["min"][0:self.data_handler.ng]/BMva, current_cap["min"][self.data_handler.ng + self.data_handler.nl::]/BMva)), \
                            "g_ub": np.concatenate((current_cap["max"][0:self.data_handler.ng]/BMva, current_cap["max"][self.data_handler.ng + self.data_handler.nl::]/BMva)), "tl": current_cap["max"][self.data_handler.ng:self.data_handler.ng + self.data_handler.nl]/BMva}

                def fb_Pg(model, i):
                    return (gt_limits["g_lb"][i], gt_limits["g_ub"][i])

                def fb_flow(model,i):
                    return (-gt_limits["tl"][i], gt_limits["tl"][i])

                def fb_ess(model, i):
                    return(-current_cap["max"][self.data_handler.ng + self.data_handler.nl::][i]/BMva, current_cap["min"][self.data_handler.ng + self.data_handler.nl::][i]/BMva)

                def fb_soc(model, i):
                    return(ess_smin[i]/BMva, ess_smax[i]/BMva)

                # get wind power output for all zones/areas
                if self.data_handler.wind_directory:
                    w_zones, current_w_class = self.data_handler.raut.WindPower(self.data_handler.nz, self.data_handler.w_sites, self.data_handler.zone_no, \
                    self.data_handler.w_classes, self.data_handler.r_cap, current_w_class, self.data_handler.tr_mats, self.data_handler.p_class, self.data_handler.w_turbines, self.data_handler.out_curve2, self.data_handler.out_curve3)

                # get solar power output for all zones/areas
                if self.data_handler.solar_directory:
                    s_zones = self.data_handler.raut.SolarPower(n, self.data_handler.nz, self.data_handler.s_zone_no, self.data_handler.solar_prob, self.data_handler.s_profiles, self.data_handler.s_sites, self.data_handler.s_max)

                # record wind and solar profiles for plotting (optional)
                if self.data_handler.wind_directory:
                    self.renewable_rec["wind_rec"][:, n] = w_zones

                if self.data_handler.solar_directory:
                    s_zones_t = np.transpose(s_zones)
                    self.renewable_rec["solar_rec"][:, n] = s_zones_t[:, n%24]

                # recalculate net load (for distribution side resources, optional)
                part_netload = self.load_factor*self.data_handler.load_all_regions

                if self.data_handler.solar_directory and self.data_handler.wind_directory:
                    net_load =  part_netload[n] - w_zones - s_zones[n%24]
                elif self.data_handler.solar_directory==False and self.data_handler.wind_directory:
                    net_load = part_netload[n] - w_zones
                elif self.data_handler.solar_directory and self.data_handler.wind_directory==False:
                    net_load = part_netload[n] - s_zones[n%24]
                elif self.data_handler.solar_directory==False and self.data_handler.wind_directory==False:
                    net_load = part_netload[n]

                # optimize dipatch and calculate load curtailment
                load_curt, SOC_old = self.data_handler.raut.OptDispatchLite(self.data_handler.ng, self.data_handler.nz, self.data_handler.ness, fb_ess, fb_soc, BMva, fb_Pg, A_inc,\
                                                    self.data_handler.gencost, net_load, SOC_old, self.data_handler.ess_pmax, self.data_handler.ess_eff, self.data_handler.disch_cost, self.data_handler.ch_cost)

                # record values for visualization purposes
                self.SOC_rec[:, n] = SOC_old*BMva
                self.curt_rec[n] = load_curt*BMva
                # gen_rec[n] = gen[0:ng]

                # track loss of load states
                var_s, LOL_track = self.data_handler.raut.TrackLOLStates(load_curt, BMva, var_s, LOL_track, s, n)

                if (n+1)%100 == 0:
                    print(f'Hour {n + 1}')

            # collect indices for all samples
            indices_rec = self.data_handler.raut.UpdateIndexArrays(indices_rec, var_s, self.sim_hours, s)

            # check for convergence using LOLP and COV
            indices_rec["mLOLP_rec"][s] = np.mean(indices_rec["LOLP_rec"][0:s+1])
            var_LOLP = np.var(indices_rec["LOLP_rec"][0:s+1])
            indices_rec["COV_rec"][s] = np.sqrt(var_LOLP)/indices_rec["mLOLP_rec"][s]

        # calculate reliability indices for the MCS
        indices = self.data_handler.raut.GetReliabilityIndices(indices_rec, self.sim_hours, self.samples)
        self.mLOLP_rec = indices_rec["mLOLP_rec"]
        self.COV_rec = indices_rec["COV_rec"]

        print("Simulation complete! You can view the results now by clicking next! Plots are also saved to the results folder.")
        self.pushButton_6.setVisible(True)

        self.main_folder = base_dir
        self.results_dir = os.path.join(self.main_folder, 'Results')

        if not os.path.exists(f"{self.main_folder}/Results"):
            os.makedirs(f"{self.main_folder}/Results")

        df = pd.DataFrame([indices])
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        results_subdir = os.path.join(self.main_folder, 'Results', timestamp)
        os.makedirs(results_subdir, exist_ok=True)
        df.to_csv(f"{results_subdir}/indices.csv", index=False)

        if self.sim_hours == 8760:
            self.data_handler.raut.OutageHeatMap(LOL_track, 1, self.samples, self.main_folder)

    def plot(self):
        if self.plot_count == 0:
            self.plot_count = 1
        else:
            # Create a timestamp-based directory
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            results_subdir = os.path.join(self.main_folder, 'Results', timestamp)
            os.makedirs(results_subdir, exist_ok=True)

            # Initialize RAPlotTools
            rapt = RAPlotTools(self.main_folder)

            # Call plotting functions, passing the results_subdir
            rapt.PlotSolarGen(self.renewable_rec["solar_rec"], self.data_handler.bus_name, results_subdir)
            rapt.PlotWindGen(self.renewable_rec["wind_rec"], self.data_handler.bus_name, results_subdir)
            rapt.PlotSOC(self.SOC_rec, self.data_handler.essname, results_subdir)
            rapt.PlotLoadCurt(self.curt_rec, results_subdir)
            rapt.PlotLOLP(self.mLOLP_rec, self.samples, 1, results_subdir)
            rapt.PlotCOV(self.COV_rec, self.samples, 1, results_subdir)

            if self.sim_hours == 8760:
                rapt.OutageMap(f"{results_subdir}/LOL_perc_prob.csv", results_subdir)

            # Update plot count
            self.plot_count = 0

    # def plot(self):
    #     if self.plot_count == 0:
    #         self.plot_count = 1
    #     else:
    #         rapt = RAPlotTools(self.main_folder)
    #         rapt.PlotSolarGen(self.renewable_rec["solar_rec"], self.data_handler.bus_name)
    #         rapt.PlotWindGen(self.renewable_rec["wind_rec"], self.data_handler.bus_name)
    #         rapt.PlotSOC(self.SOC_rec, self.data_handler.essname)
    #         rapt.PlotLoadCurt(self.curt_rec)
    #         rapt.PlotLOLP(self.mLOLP_rec, self.samples, 1)
    #         rapt.PlotCOV(self.COV_rec, self.samples, 1)
    #         if self.sim_hours == 8760:
    #             rapt.OutageMap(f"{self.main_folder}/Results/LOL_perc_prob.csv")
    #         #self.ui.textBrowser_2.append("Plotting complete, view plots by clicking next. Plots are also saved in the Results folder.")
    #         #QMessageBox.information(self, "Plots", "Plotting complete, view plots in the Results folder.")
    #         #self.open_folder_in_explorer(self.results_dir)
    #         # self.load_plots()
    #         # self.load_csv_files()
    #         self.plot_count = 0