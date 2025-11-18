# import python modules
from pyomo.environ import *
import numpy as np
import pandas as pd
import calendar
import os
from datetime import datetime

#np.random.seed(42)  
class RAUtilities:
    '''
    This class contains the different methods required for performing mixed time sequential Monte Carlo simulation and evaluate the reliability indices of a power system.
    '''
    def __init__(self):
        """
        Initializes the RAUtilities class.
        """
        pass

    def reltrates(self, MTTF_gen, MTTF_trans, MTTR_gen, MTTR_trans, MTTF_ess, MTTR_ess):
        """
        Calculates failure and repair rates for all conventional generators and transmission lines.

        Parameters:
            MTTF_gen (array): Mean time to failure for generators.
            MTTF_trans (array): Mean time to failure for transmission lines.
            MTTR_gen (array): Mean time to repair for generators.
            MTTR_trans (array): Mean time to repair for transmission lines.
            MTTF_ess (array): Mean time to failure for energy storage systems.
            MTTR_ess (array): Mean time to repair for energy storage systems.

        Returns:
            tuple: Repair rates and failure rates for all components.
        """

        self.MTTF_all = np.concatenate((MTTF_gen, MTTF_trans, MTTF_ess))
        self.MTTR_all = np.concatenate((MTTR_gen, MTTR_trans, MTTR_ess ))
        self.mu_tot = 1/self.MTTR_all # repair rates for all components
        self.lambda_tot = 1/self.MTTF_all # failure rates of all components

        return(self.mu_tot, self.lambda_tot)

    def capacities(self, nl, pmax, pmin, ess_pmax, ess_pmin, cap_trans):
        """
        Concatenates capacities of generators and transmission lines for use in the MCS.

        Parameters:
            nl (int): Number of lines.
            pmax (array): Maximum capacities of generators.
            pmin (array): Minimum capacities of generators.
            ess_pmax (array): Maximum capacities of energy storage systems.
            ess_pmin (array): Minimum capacities of energy storage systems.
            cap_trans (array): Transmission capacities.

        Returns:
            tuple: Maximum and minimum capacities of all components.
        """

        self.cap_max = np.concatenate((pmax, cap_trans, ess_pmax))
        self.cap_min = np.concatenate((pmin, np.zeros(nl), ess_pmin))

        return(self.cap_max, self.cap_min)

    def NextState(self, t_min, ng, ness, nl, lambda_tot, mu_tot, current_state, cap_max, cap_min, ess_units):
        """
        Generates random numbers to calculate the time to the next state for generators and transmission lines.

        Parameters:
            t_min (float): Minimum time.
            ng (int): Number of generators.
            ness (int): Number of energy storage systems.
            nl (int): Number of lines.
            lambda_tot (array): Failure rates.
            mu_tot (array): Repair rates.
            current_state (array): Current states of components.
            cap_max (array): Maximum capacities of components.
            cap_min (array): Minimum capacities of components.
            ess_units (array): Units of energy storage systems.

        Returns:
            tuple: Current state, current capacity, and minimum time.
        """
        self.t_min = t_min
        if self.t_min <= 0:
            self.U = np.random.uniform(0, 1, ng + nl) # this should be for gt only
            self.time_gt = np.zeros(ng + nl)
            for u in range(ng + nl):
                if current_state[u] == 1:
                    self.time_gt[u] = -np.log(self.U[u])/lambda_tot[u]
                else:
                    self.time_gt[u] = -np.log(self.U[u])/mu_tot[u]

            # calculate time for ess states here (for all ess): 2 numbers for each ess, choose minimum
            self.V_fail = np.random.uniform(0, 1, ness)
            self.V_repair = np.random.uniform(0, 1, ness)
            self.time_ess_fail = np.zeros(ness)
            self.time_ess_repair = np.ones(ness)*1e7
            for v in range(ness):
                self.time_ess_fail[v] = -np.log(self.V_fail[v])/lambda_tot[ng + nl + v]
                if current_state[ng + nl + v] < 1:
                    self.time_ess_repair[v] = -np.log(self.V_repair[v])/mu_tot[ng + nl + v]

            self.time_ess = np.vstack((self.time_ess_fail, self.time_ess_repair))
            self.t_min_ess = self.time_ess.min()
            self.t_min_ess_index = np.unravel_index(np.argmin(self.time_ess), self.time_ess.shape)

            # augment with t_min of gt
            self.time_all = np.append(self.time_gt, self.t_min_ess)
            self.t_min = min(self.time_all) # calculate shortest time; the component with the shortest time will fail first
            self.index_min = np.argmin(self.time_all) # component with the shortest time

            self.temp_ess_ind = self.time_all.size - 1

        self.t_min -= 1

        # change component states based on time to next event
        if self.t_min <= 0 and self.index_min != self.temp_ess_ind: # if failure/repair is for gen/TLs
            if current_state[self.index_min] == 1:
                current_state[self.index_min] = 0
            elif current_state[self.index_min] == 0:
                current_state[self.index_min] = 1
        elif self.t_min <= 0 and self.index_min == self.temp_ess_ind: # if failure/repair is for ESS
            if self.t_min_ess_index[0] == 0: # if ESS failure
                self.ess_failed = self.t_min_ess_index[1]
                if current_state[ng + nl + self.ess_failed] >= 1/ess_units[self.ess_failed]:
                    current_state[ng + nl + self.ess_failed] = current_state[ng + nl + self.ess_failed] - 1/ess_units[self.ess_failed]
            else: # if ESS repair
                 self.ess_repaired = self.t_min_ess_index[1]
                 if current_state[ng + nl + self.ess_repaired] < 1:
                    current_state[ng + nl + self.ess_repaired] = current_state[ng + nl + self.ess_repaired] + 1/ess_units[self.ess_repaired]

        current_cap = {"max": np.multiply(current_state, cap_max), "min": np.multiply(current_state, cap_min)} # calculate current capacity of all components
        return(current_state, current_cap, self.t_min)

    def updateSOC(self, ng, nl, current_cap, ess_pmax, ess_duration, ess_socmax, ess_socmin, SOC_old):
        """
        Updates the state of charge (SOC) based on failures in energy storage systems.

        Parameters:
            ng (int): Number of generators.
            nl (int): Number of lines.
            current_cap (dict): Current capacities of components.
            ess_pmax (array): Maximum power outputs of energy storage systems.
            ess_duration (array): Durations of energy storage systems.
            ess_socmax (array): Maximum state of charge of energy storage systems.
            ess_socmin (array): Minimum state of charge of energy storage systems.
            SOC_old (array): Previous state of charge.

        Returns:
            tuple: Maximum and minimum SOC, and updated SOC.
        """

        self.ess_emax = np.multiply(current_cap["max"][ng + nl::], ess_duration) # maximum ess energy capacity
        self.ess_smax = np.multiply(self.ess_emax, ess_socmax) # maximum allowable SOC (as energy)
        self.ess_smin = np.multiply(self.ess_emax, ess_socmin) # minimum allowable SOC (as energy)
        SOC_old = current_cap["max"][ng + nl::]*SOC_old/ess_pmax # modify SOC_old based on current capacity of batteries

        return(self.ess_smax, self.ess_smin, SOC_old)


    def WindPower(self, nz, w_sites, zone_no, w_classes, r_cap, current_w_class, tr_mats, p_class, w_turbines, out_curve2, out_curve3):
        """
        Calculates the wind power generation for each hour at each site.

        Parameters:
            nz (int): Number of zones.
            w_sites (int): Number of wind sites.
            zone_no (array): Zone numbers.
            w_classes (int): Number of wind speed classes.
            r_cap (array): Rated capacities of wind turbines.
            current_w_class (array): Current wind speed classes.
            tr_mats (array): Transition matrices.
            p_class (array): Power classes.
            w_turbines (array): Number of wind turbines.
            out_curve2 (array): Output curve for class 2 turbines.
            out_curve3 (array): Output curve for class 3 turbines.

        Returns:
            tuple: Wind power generation at each zone and updated wind speed classes.
        """

        # generate random numbers for each class in each site
        self.W = np.random.uniform(0, 1, (w_sites, w_classes))

        # change zeroes in tr_mats to very low values
        tr_mats[tr_mats == 0] = 1e-10

        # calculate minimum time to next state for each site
        self.time_wind = np.zeros((w_sites, w_classes))
        for w in range(w_sites):
            for c in range(w_classes):
                if current_w_class[w] == c:
                    self.time_wind[w, :] = -np.log(self.W[w, :])/tr_mats[w, c, :]
                    break

        temp = np.matrix(self.time_wind)
        tmin_wind = temp.argmin(1)
        current_w_class = tmin_wind # change wind speed class depending on minimum time calculation

        # calculate wind power generation at each site
        self.w_power = np.zeros(w_sites)
        for w in range(w_sites):
            if p_class[w] == 2:
                self.w_power[w] = out_curve2[tmin_wind[w]]*w_turbines[w]*r_cap[w]
            else:
                self.w_power[w] = out_curve3[tmin_wind[w]]*w_turbines[w]*r_cap[w]

        # aggregate wind power generation from different sites at each zone
        self.w_zones = np.zeros(nz)

        for b in range(nz):
            for z in range(len(zone_no)):
                if b == zone_no[z] - 1:
                    self.w_zones[b] += self.w_power[z]

        return(self.w_zones, current_w_class)

    def SolarPower(self, n, nz, s_zone_no, solar_prob, s_profiles, s_sites, s_max):
        """
        Calculates solar power generation for each hour at each site.

        Parameters:
            n (int): Current hour.
            nz (int): Number of zones.
            s_zone_no (array): Zone numbers for solar sites.
            solar_prob (array): Solar probability data.
            s_profiles (array): Solar profiles.
            s_sites (int): Number of solar sites.
            s_max (array): Maximum capacities of solar sites.

        Returns:
            numpy.ndarray: Solar power generation at each zone.
        """

        if n%24 == 0:

            self.month = np.floor(n/731).astype(int) # which month are we in?
            self.prob_col = solar_prob[:, self.month]
            self.prob_index = np.array(list(zip(self.prob_col, range(len(self.prob_col))))) # create a tuple with the each element and its index
            self.sorted_prob = self.prob_index[self.prob_index[:, 0].argsort()] # sort the tuples
            self.sorted_prob[:, 0] = np.cumsum(self.sorted_prob[:, 0])
            self.rand_clust = np.random.uniform(0, 1)

            for i in range(len(self.sorted_prob)):
                if i == 0 and self.rand_clust < self.sorted_prob[i, 0]:
                    self.clust = int(self.sorted_prob[i, 1])
                    break
                elif i > 0 and self.sorted_prob[i - 1, 0] < self.rand_clust < self.sorted_prob[i, 0]:
                    self.clust = int(self.sorted_prob[i, 1])
                    break

            self.solar_dim = s_profiles[self.clust].shape
            self.days = self.solar_dim[0]


            self.rand_day = np.floor(np.random.uniform(0, 1)*self.days).astype(int)
            sgen_sites = np.zeros((s_sites, 24))

            for sg in range(s_sites):

                sgen_sites[sg] = s_profiles[self.clust][self.rand_day, :, sg]*s_max[sg]

            self.s_zones = np.zeros((nz, 24))

            for b in range(nz):
                for z in range(len(s_zone_no)):
                    if b == s_zone_no[z] - 1:
                        self.s_zones[b] += sgen_sites[z]


        return(np.transpose(self.s_zones))


    def OptDispatch(self, ng, nz, nl, ness, fb_ess, fb_soc, BMva, fb_Pg, fb_flow, A_inc, gen_mat, curt_mat, ch_mat, \
                    gencost, net_load, SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost):
        """
        Achieves economic dispatch for a particular hour using optimization. Transportation model is used.

        Parameters:
            ng (int): Number of generators.
            nz (int): Number of zones.
            nl (int): Number of lines.
            ness (int): Number of energy storage systems.
            fb_ess (function): Function for bounds of ESS variables.
            fb_soc (function): Function for bounds of SOC variables.
            BMva (float): Base power in MVA.
            fb_Pg (function): Function for bounds of generation variables.
            fb_flow (function): Function for bounds of flow variables.
            A_inc (array): Incidence matrix.
            gen_mat (array): Generation matrix.
            curt_mat (array): Curtailment matrix.
            ch_mat (array): Charging matrix.
            gencost (array): Generation costs.
            net_load (array): Net load.
            SOC_old (array): Previous state of charge.
            ess_pmax (array): Maximum power outputs of energy storage systems.
            ess_eff (array): Efficiencies of energy storage systems.
            disch_cost (array): Discharge costs.
            ch_cost (array): Charge costs.

        Returns:
            tuple: Load curtailment and updated state of charge.
        """

        model = ConcreteModel() # declaring the model

        # declaring the variables
        model.flow = Var(range(nl), bounds = fb_flow) # line flow variables
        model.Pg = Var(range(ng + ness), bounds  = fb_Pg) # power output for conventional generators and ESS discharge
        model.Pc = Var(range(ness), bounds = fb_ess) # charge variables for ESS
        model.SOC = Var(range(ness), bounds = fb_soc) # state-of-charge variables for ESS
        model.curt = Var(range(nz), bounds = (0, None)) # load curtailment variables
        model.renewable_curt = Var(range(nz), bounds = (0, None)) # renewable load curtailment variables
        A_inc_t = np.transpose(A_inc) # transposing incedence matrix

        LOL_cost = 1000 # cost of lost load (set to very high so that system always tries to minimize loss)

        # power balance constraint
        def con_rule1(model,i):
            return(sum(A_inc_t[i, j]*model.flow[j] for j in range(nl))\
                    + sum(gen_mat[i,m]*model.Pg[m] for m in range(ng + ness)) \
                    + sum(ch_mat[i,m]*model.Pc[m] for m in range(ness)) \
                    + sum(curt_mat[i,c]*model.curt[c] for c in range(nz)) == model.renewable_curt[i] + net_load[i]/BMva)

        model.equality = Constraint(range(nz), rule = con_rule1)

        # soc update constraint
        def con_rule2(model, i):
            return(model.SOC[i] == SOC_old[i] - ess_eff[i]*model.Pc[i] - model.Pg[ng + i])

        model.soc_constraint = Constraint(range(ness), rule = con_rule2)

        # charge discharge constraint for the soc
        def con_rule3(model, i):
            return(-model.Pc[i] + model.Pg[ng + i] <= ess_pmax[i]/BMva)

        model.chdis_constraint = Constraint(range(ness), rule = con_rule3)

        # Objective ----> minimize total cost (cost of gen + cost of storage + cost of lost load)
        '''Relative fuels costs are used here. Loss of load is penalized heavily to encourage ESS discharge
        for supporting demand. ESS discharge is made more expensive than conv. gen so that ESS is only used
        when no generators are available to meet additional load (reliability application). ESS charging is
        incentivized so that ESS charges whenever it is not being used.'''
        model.objective = Objective(expr = sum(model.curt[i] for i in range(nz))*LOL_cost + \
                                    sum(gencost[i]*model.Pg[i] for i in range(ng)) + \
                                    sum(disch_cost[i]*model.Pg[ng + i] for i in range(ness)) + \
                                    sum(ch_cost[i]*model.Pc[i] for i in range(ness)))

        opt = SolverFactory('glpk')
        opt.solve(model)
        load_curt = sum(np.array(list(model.curt.get_values().values())))
        # gen = np.array(list(model.Pg.get_values().values()))

        SOC_old = np.array(list(model.SOC.get_values().values()))
        P_dis = np.array(list(model.Pg.get_values().values()))[ng::]
        P_ch = np.array(list(model.Pc.get_values().values()))
        return(load_curt, SOC_old, P_dis, P_ch)

    def OptDispatchMP(self, ng, nz, nl, ness, fb_ess, fb_soc, fb_ren, BMva, fb_Pg, fb_flow, A_inc, gen_mat, curt_mat, ch_mat, \
                    gencost, net_load, SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost, time_period, copper_sheet = False):
       
        model = ConcreteModel() # declaring the model

        # declaring the variables
        T = range(time_period)
        model.flow = Var(range(nl), T, bounds = fb_flow) # line flow variables
        model.Pg = Var(range(ng + ness), T, bounds  = fb_Pg) # power output for conventional generators and ESS discharge
        model.Pc = Var(range(ness), T, bounds = fb_ess) # charge variables for ESS
        model.SOC = Var(range(ness), T, bounds = fb_soc) # state-of-charge variables for ESS
        model.curt = Var(range(nz), T, bounds = (0, None)) # load curtailment variables
        model.ren_curt = Var(range(nz), T, bounds = fb_ren)

        A_inc_t = np.transpose(A_inc) # transposing incedence matrix

        LOL_cost = 100000000 # cost of lost load (set to very high so that system always tries to minimize loss)

        # power balance constraint
        if copper_sheet == False:
            def con_rule1(model,i,t):
                return(sum(A_inc_t[i, j]*model.flow[j,t] for j in range(nl))\
                        + sum(gen_mat[i,m]*model.Pg[m,t] for m in range(ng + ness)) \
                        + sum(ch_mat[i,m]*model.Pc[m,t] for m in range(ness)) \
                + sum(curt_mat[i,c]*model.curt[c,t] for c in range(nz)) == model.ren_curt[i,t] + net_load[i,t]/BMva)

            model.equality = Constraint(range(nz), T, rule = con_rule1)

        if copper_sheet == True:
            for i in range(nl):
                for t in T:
                    model.flow[i, t].fix(0.0)
                    
            def con_rule1(model, t):
                return(sum(model.Pg[m,t] for m in range(ng + ness)) \
                      + sum(model.Pc[m,t] for m in range(ness)) \
                      + sum(model.curt[c,t] for c in range(nz)) == sum(model.ren_curt[i,t] for i in range(nz)) 
                      + sum(net_load[:,t])/BMva)

            model.equality = Constraint(T, rule = con_rule1)

        # soc update constraint
        def con_rule2(model, i,t):
            if t == 0:
                return(model.SOC[i,t] == SOC_old[i] - ess_eff[i]*model.Pc[i,t] - model.Pg[ng + i,t])
            else: 
                return(model.SOC[i,t] == model.SOC[i,t-1] - ess_eff[i]*model.Pc[i,t] - model.Pg[ng + i,t])

        model.soc_constraint = Constraint(range(ness), T, rule = con_rule2)

        def soc_rule_EoD(model,i,t):
            if (t + 1)%24 == 0:
                return(model.SOC[i,t] >= SOC_old[i])
            else:
                return Constraint.Skip
        model.soc_neutrality = Constraint(range(ness), T, rule = soc_rule_EoD)

        # charge discharge constraint for the soc
        def con_rule3(model, i,t):
            return(-model.Pc[i,t] + model.Pg[ng + i,t] <= ess_pmax[i]/BMva)

        model.chdis_constraint = Constraint(range(ness), T, rule = con_rule3)

        # Objective ----> minimize total cost (cost of gen + cost of storage + cost of lost load)
        model.objective = Objective( expr = sum(model.curt[i, t] * LOL_cost for i in range(nz) for t in T)
                                    + sum(gencost[i] * model.Pg[i, t] * BMva for i in range(ng) for t in T)
                                    + sum(disch_cost[i] * model.Pg[ng + i, t] * BMva for i in range(ness) for t in T)
                                    + sum(ch_cost[i] * -model.Pc[i, t] * BMva for i in range(ness) for t in T))
        
        opt = SolverFactory('glpk')
        res = opt.solve(model, tee = False)

        load_curt = np.zeros(len(T))
        for t in T:
            current_curtail = 0
            for z in range(nz):
                current_curtail += model.curt[z, t].value
            load_curt[t] = current_curtail
        soc_profile = np.zeros((ness, len(T)))
        p_discharge = np.zeros((ness, len(T)))
        p_charge = np.zeros((ness, len(T)))
        for i in range(ness):
            for t in T:
                soc_profile[i, t] = model.SOC[i, t].value
                p_discharge[i, t] = model.Pg[ng + i, t].value
                p_charge[i, t] = model.Pc[i, t].value

        return load_curt, soc_profile, p_discharge, p_charge

    def OptDispatchLite(self, ng, nz, ness, fb_ess, fb_soc, BMva, fb_Pg, A_inc, \
                    gencost, net_load, SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost):
        """
        Achieves economic dispatch for a particular hour using optimization. Copper sheet model is used, i.e., flow constraints are ignored.

        Parameters:
            ng (int): Number of generators.
            nz (int): Number of zones.
            nl (int): Number of lines.
            ness (int): Number of energy storage systems.
            fb_ess (function): Function for bounds of ESS variables.
            fb_soc (function): Function for bounds of SOC variables.
            BMva (float): Base power in MVA.
            fb_Pg (function): Function for bounds of generation variables.
            fb_flow (function): Function for bounds of flow variables.
            A_inc (array): Incidence matrix.
            gen_mat (array): Generation matrix.
            curt_mat (array): Curtailment matrix.
            ch_mat (array): Charging matrix.
            gencost (array): Generation costs.
            net_load (array): Net load.
            SOC_old (array): Previous state of charge.
            ess_pmax (array): Maximum power outputs of energy storage systems.
            ess_eff (array): Efficiencies of energy storage systems.
            disch_cost (array): Discharge costs.
            ch_cost (array): Charge costs.

        Returns:
            tuple: Load curtailment and updated state of charge.
        """

        model = ConcreteModel() # declaring the model

        # declaring the variables
        model.Pg = Var(range(ng + ness), bounds  = fb_Pg) # power output for conventional generators and ESS discharge
        model.Pc = Var(range(ness), bounds = fb_ess) # discharge variables for ESS
        model.SOC = Var(range(ness), bounds = fb_soc) # state-of-charge variables for ESS
        model.curt = Var(range(nz), bounds = (0, None)) # load curtailment variables

        A_inc_t = np.transpose(A_inc) # transposing incedence matrix

        LOL_cost = 1000 # cost of lost load (set to very high so that system always tries to minimize loss)

        def con_rule1(model):
            return(sum(model.Pg[m] for m in range(ng + ness)) + sum(model.Pc[m] for m in range(ness)) \
                   + sum(model.curt[c] for c in range(nz)) >= sum(net_load)/BMva)

        model.equality = Constraint(rule = con_rule1)

        # soc update constraint
        def con_rule2(model, i):
            return(model.SOC[i] == SOC_old[i] - ess_eff[i]*model.Pc[i] - model.Pg[ng + i])

        model.soc_constraint = Constraint(range(ness), rule = con_rule2)

        # charge discharge constraint for the soc
        def con_rule3(model, i):
            return(-model.Pc[i] + model.Pg[ng + i] <= ess_pmax[i]/BMva)

        model.chdis_constraint = Constraint(range(ness), rule = con_rule3)

        # Objective ----> minimize total cost (cost of gen + cost of storage + cost of lost load)
        '''Relative fuels costs are used here. Loss of load is penalized heavily to encourage ESS discharge
        for supporting demand. ESS discharge is made more expensive than conv. gen so that ESS is only used
        when no generators are available to meet additional load (reliability application). ESS charging is
        incentivized so that ESS charges whenever it is not being used.'''
        model.objective = Objective(expr = sum(model.curt[i] for i in range(nz))*LOL_cost + \
                                    sum(gencost[i]*model.Pg[i] for i in range(ng)) + \
                                    sum(disch_cost[i]*model.Pg[ng + i] for i in range(ness)) + \
                                    sum(ch_cost[i]*model.Pc[i] for i in range(ness)))

        opt = SolverFactory('glpk')
        opt.solve(model)
        load_curt = sum(np.array(list(model.curt.get_values().values())))

        SOC_old = np.array(list(model.SOC.get_values().values()))
        P_dis = np.array(list(model.Pg.get_values().values()))[ng::]
        P_ch = np.array(list(model.Pc.get_values().values()))
        return(load_curt, SOC_old, P_dis, P_ch)

    def TrackLOLStates(self, load_curt, BMva, var_s, LOL_track, s, n):
        """
        Tracks the loss of load states.

        Parameters:
            load_curt (float): Load curtailment.
            BMva (float): Base power in MVA.
            var_s (dict): Dictionary of temporary variables.
            LOL_track (array): Array to track loss of load.
            s (int): Current sample.
            n (int): Current hour.

        Returns:
            tuple: Updated variables and loss of load tracker.
        """
        if load_curt > 0:
            var_s["LLD"] += 1 # starts at 0 for each year, adds 1 whenever there is a loss of load hour
            var_s["curtailment"][n] = load_curt*BMva # starts at 0 for each year, tracks total load curtailed over a year
            var_s["label_LOLF"][n] = 1 # binary array, = 1 if load curtailed, 0 otherwise
            LOL_track[s][n] = 1
        if n > 0 and var_s["label_LOLF"][n] == 1 and var_s["label_LOLF"][n-1] == 0:
            var_s["freq_LOLF"] += 1
        if (n+1)%24 == 0:
            LOLE_temp = sum(var_s["label_LOLF"][(n-23):(n+1)])
            var_s['outage_day'][int((n+1)/24) - 1] = LOLE_temp
            if LOLE_temp > 0:
                var_s["LOL_days"] += 1

        return(var_s, LOL_track)
    
    def CheckConvergence(self, s, LOLP_rec, comm, rank, size, mLOLP_rec, COV_rec):

        self.LOLP_len = np.size(LOLP_rec)

        self.sendbuf_LOLP = LOLP_rec
        self.recvbuf_LOLP = None

        if rank==0:
            self.recvbuf_LOLP = np.empty([size, self.LOLP_len])
        
        comm.Gather(self.sendbuf_LOLP, self.recvbuf_LOLP, root=0)

        if rank==0:
            self.temp_mat = self.recvbuf_LOLP[:, 0:s+1]
            mLOLP_rec[s] = np.mean(self.temp_mat)
            var_LOLP = np.var(self.temp_mat)
            COV_rec[s] = np.sqrt(var_LOLP)/mLOLP_rec[s]

        return(mLOLP_rec, COV_rec)


    def UpdateIndexArrays(self, indices_rec, var_s, sim_hours, s):
        """
        Stores the index values for all samples.

        Parameters:
            indices_rec (dict): Dictionary of indices to be recorded.
            var_s (dict): Dictionary of temporary variables.
            sim_hours (int): Number of simulation hours.
            s (int): Current sample.

        Returns:
            dict: Updated indices recorder.
        """
        indices_rec["LOLP_rec"][s] = var_s["LLD"]/sim_hours
        indices_rec["EUE_rec"][s] = sum(var_s["curtailment"])
        if var_s["LLD"] > 0:
            indices_rec["EPNS_rec"][s] = sum(var_s["curtailment"])/var_s["LLD"]
        indices_rec["LOLF_rec"][s] = var_s["freq_LOLF"]
        if  indices_rec["LOLF_rec"][s] > 0:
           indices_rec["MDT_rec"][s] = var_s["LLD"]/indices_rec["LOLF_rec"][s]
        indices_rec["LOLE_rec"][s] = var_s["LOL_days"]
        indices_rec["LOLP_hr"] += var_s["label_LOLF"] # hourly LOLP

        return(indices_rec)

    def OutageAnalysis(self, var_s):
        """
        Analyzes outages based on loss of load states.

        Parameters:
            var_s (dict): Dictionary of temporary variables.

        Returns:
            numpy.ndarray: Array of outage durations.
        """
        start_outages = np.where(np.diff(np.concatenate(([0], var_s["label_LOLF"], [0]))) == 1)[0]
        end_outages = np.where(np.diff(np.concatenate(([0], var_s["label_LOLF"], [0]))) == -1)[0]
        out_durations = end_outages - start_outages

        return(out_durations)

    def GetReliabilityIndices(self, indices_rec, sim_hours, samples):
        """
        Calculates the reliability indices.

        Parameters:
            indices_rec (dict): Dictionary of indices to be recorded.
            sim_hours (int): Number of simulation hours.
            samples (int): Number of samples.

        Returns:
            dict: Dictionary of calculated reliability indices.
        """
        self.LOLP = np.mean(indices_rec["LOLP_rec"])
        self.LOLH = self.LOLP*sim_hours
        self.EUE = np.mean(indices_rec["EUE_rec"])
        self.EPNS = np.mean(indices_rec["EPNS_rec"])
        self.LOLF = np.mean(indices_rec["LOLF_rec"]) # Loss of Load Frequency (occ/year)
        self.MDT = np.mean(indices_rec["MDT_rec"])
        self.LOLE = np.mean(indices_rec["LOLE_rec"])
        # self.LOLP_hr = indices_rec["LOLP_hr"]/samples

        self.indices = {"LOLP": self.LOLP, "LOLH": self.LOLH,"EUE": self.EUE, "EPNS": self.EPNS, "LOLF": self.LOLF, "MDT": self.MDT, "LOLE": self.LOLE}

        return(self.indices)

    def OutageHeatMap(self, LOL_track, size, samples, all_subdir):
            
            LOL_temp  = np.reshape(LOL_track, (size*samples, 365, 24))
            LOL_temp = np.sum(LOL_temp, axis=0)
            days_in_month = np.array([calendar.monthrange(2022, month)[1] for month in range(1, 13)])
            LOL_prob = np.zeros((12, 24))
            start_index = 0

            for month, month_days in enumerate(days_in_month):
                end_index = start_index + month_days
                LOL_prob[month, :] = LOL_temp[start_index:end_index, :].sum(axis = 0)
                start_index = end_index

            LOL_prob = LOL_prob/(size*samples)

            # timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            # results_subdir = os.path.join(main_folder, 'Results', timestamp)
            pd.DataFrame((LOL_prob)*100/days_in_month[:, np.newaxis]).to_csv(f"{all_subdir}/LOL_perc_prob.csv")

    def ParallelProcessing(self, indices, LOL_track, comm, rank, size, samples, sim_hours, main_folder):
        """
        Performs parallel processing to gather results from different processes.

        Parameters:
            indices (dict): Dictionary of calculated reliability indices.
            LOL_track (array): Array to track loss of load.
            comm (MPI.Comm): MPI communicator.
            rank (int): Rank of the current process.
            size (int): Total number of processes.
            samples (int): Number of samples.

        Returns:
            dict: Dictionary of aggregated reliability indices for all processes or a rank message.
        """
        self.indices_np = np.array([indices["LOLP"], indices["LOLH"], indices["EUE"], indices["EPNS"], indices["LOLF"], indices["MDT"], indices["LOLE"]])
        self.ind_len = np.size(self.indices_np)
        LOL_track = LOL_track.flatten()
        self.LOL_len = np.size(LOL_track)

        self.sendbuf_ind = self.indices_np
        self.sendbuf_LOL = LOL_track
        self.recvbuf_ind = None
        self.recvbuf_LOL = None

        if rank == 0:
            self.recvbuf_ind = np.empty([size, self.ind_len])
            self.recvbuf_LOL = np.empty([size, self.LOL_len])

        comm.Gather(self.sendbuf_ind, self.recvbuf_ind, root=0)
        comm.Gather(self.sendbuf_LOL, self.recvbuf_LOL, root=0)

        if rank == 0:
            self.LOLP_allp = np.mean(self.recvbuf_ind[:, 0]) # LOLP for all processes
            self.LOLH_allp = np.mean(self.recvbuf_ind[:, 1])
            self.EUE_allp = np.mean(self.recvbuf_ind[:, 2])
            self.EPNS_allp = np.mean(self.recvbuf_ind[:, 3])
            self.LOLF_allp = np.mean(self.recvbuf_ind[:, 4])
            self.MDT_allp = np.mean(self.recvbuf_ind[:, 5])
            self.LOLE_allp = np.mean(self.recvbuf_ind[:, 6])

            index_all = {"LOLP": self.LOLP_allp, "LOLH": self.LOLH_allp, "EUE": self.EUE_allp, "EPNS": self.EPNS_allp, "LOLF": self.LOLF_allp, \
                         "MDT": self.MDT_allp, "LOLE": self.LOLE_allp}

            df = pd.DataFrame([index_all])
            df.to_csv(f"{main_folder}/indices.csv", index=False)

            if sim_hours == 8760:
                self.recvbuf_LOL = self.recvbuf_LOL.reshape(size, samples, 365, 24)
                self.OutageHeatMap(self.recvbuf_LOL, size, samples, main_folder)
        
############ EXTRA CODE FOR ADDING OTHER RESOURCES BESIDES WIND AND SOLAR ######################

    # def PartNetLoad(self, CSP_all_buses, RTPV_all_buses, load_all_regions):
    #     '''Calculates partial net load by subtracting RTPV and CSP from total load.
    #        Solar PV and Wind are adjusted later.
    #     '''
    #     self.CSP_all_buses = CSP_all_buses
    #     self.RTPV_all_buses = RTPV_all_buses
    #     self.load_all_regions = load_all_regions
    #     self.part_netload = self.load_all_regions - (self.CSP_all_buses + self.RTPV_all_buses)
    #     # self.part_netload = 2*self.part_netload

    #     return(self.part_netload)

