# import python modules
from pyomo.environ import *
import numpy as np
import pandas as pd
import calendar
import os
from datetime import datetime

class RAUtilities:
    """
    Contains utility methods required for performing mixed time sequential 
    Monte Carlo (MCS) simulations and evaluating reliability indices 
    in power systems.

    This class offers functions to:
      - Compute reliability transition rates for various components (generators, transmission lines, ESS).
      - Track and update component states (fail/repair) over simulated time.
      - Aggregate or compute net capacities, state of charge, and wind/solar generation.
      - Perform optimization-based dispatch (economic dispatch) in either a zonal or 
        copper-sheet model.
      - Compute final reliability indices (e.g., LOLP, EUE, LOLE) and handle parallel (MPI) processing steps.
    """
    def __init__(self):
        """
        Initializes the RAUtilities class.
        """
        pass

    def reltrates(self, MTTF_gen, MTTF_trans, MTTR_gen, MTTR_trans, MTTF_ess, MTTR_ess):
        """
        Computes repair and failure rates for generators, transmission lines, and ESS.

        :param MTTF_gen: Mean time to failure for generators (hours).
        :type MTTF_gen: np.ndarray
        :param MTTF_trans: Mean time to failure for transmission lines (hours).
        :type MTTF_trans: np.ndarray
        :param MTTR_gen: Mean time to repair for generators (hours).
        :type MTTR_gen: np.ndarray
        :param MTTR_trans: Mean time to repair for transmission lines (hours).
        :type MTTR_trans: np.ndarray
        :param MTTF_ess: Mean time to failure for energy storage systems (hours).
        :type MTTF_ess: np.ndarray
        :param MTTR_ess: Mean time to repair for energy storage systems (hours).
        :type MTTR_ess: np.ndarray

        :return:
            A 2-element tuple containing:

            * **mu_tot** (*np.ndarray*): Repair rates (1/MTTR) for all components (gen, trans, ESS).
            * **lambda_tot** (*np.ndarray*): Failure rates (1/MTTF) for all components.

        :rtype: tuple
        """


        self.MTTF_all = np.concatenate((MTTF_gen, MTTF_trans, MTTF_ess))
        self.MTTR_all = np.concatenate((MTTR_gen, MTTR_trans, MTTR_ess ))
        self.mu_tot = 1/self.MTTR_all # repair rates for all components
        self.lambda_tot = 1/self.MTTF_all # failure rates of all components

        return(self.mu_tot, self.lambda_tot)

    def capacities(self, nl, pmax, pmin, ess_pmax, ess_pmin, cap_trans):
        """
        Constructs arrays of maximum and minimum capacities for generators, lines, and ESS 
        for use in the MCS.

        :param nl: Number of transmission lines.
        :type nl: int
        :param pmax: Maximum capacities (MW) of each generator.
        :type pmax: np.ndarray
        :param pmin: Minimum capacities (MW) of each generator.
        :type pmin: np.ndarray
        :param ess_pmax: Maximum power outputs (MW) for each ESS.
        :type ess_pmax: np.ndarray
        :param ess_pmin: Minimum power outputs (MW) for each ESS.
        :type ess_pmin: np.ndarray
        :param cap_trans: Transmission capacities (MW) for each line.
        :type cap_trans: np.ndarray

        :return:
            A 2-element tuple containing:

            * **cap_max** (*np.ndarray*): Concatenated maximum capacities (generators + lines + ESS).
            * **cap_min** (*np.ndarray*): Concatenated minimum capacities (generators + lines + ESS).

        :rtype: tuple
        """


        self.cap_max = np.concatenate((pmax, cap_trans, ess_pmax))
        self.cap_min = np.concatenate((pmin, np.zeros(nl), ess_pmin))

        return(self.cap_max, self.cap_min)

    def NextState(self, t_min, ng, ness, nl, lambda_tot, mu_tot, current_state, cap_max, cap_min, ess_units):
        """
        Determines which component (gen/trans/ESS) transitions (fails or repairs) next 
        using exponential random draws, then updates system states and capacities.

        :param t_min: Time (hours) remaining until the next state transition event occurs.
        :type t_min: float
        :param ng: Number of conventional generators.
        :type ng: int
        :param ness: Number of energy storage systems.
        :type ness: int
        :param nl: Number of transmission lines.
        :type nl: int
        :param lambda_tot: Failure rates for all components (ordered: gen, lines, ESS).
        :type lambda_tot: np.ndarray
        :param mu_tot: Repair rates for all components (ordered: gen, lines, ESS).
        :type mu_tot: np.ndarray
        :param current_state: Current binary states of each component (1 = up, 0 = down). 
                             For ESS, each integer denotes how many are up among identical units.
        :type current_state: np.ndarray
        :param cap_max: Maximum capacities for each component type.
        :type cap_max: np.ndarray
        :param cap_min: Minimum capacities for each component type.
        :type cap_min: np.ndarray
        :param ess_units: Number of identical units for each ESS installation.
        :type ess_units: np.ndarray

        :return:
            A 3-element tuple containing:

            * **current_state** (*np.ndarray*): Updated states after one component fails/repairs.
            * **current_cap** (*dict*): Current maximum and minimum capacity arrays (accounting for the updated state).
            * **t_min** (*float*): Updated time to the next state transition.

        :rtype: tuple
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
        Adjusts the state-of-charge (SOC) for storage units to reflect any 
        failures/repairs that reduce or restore capacity.

        :param ng: Number of generators.
        :type ng: int
        :param nl: Number of lines.
        :type nl: int
        :param current_cap: Dictionary of current max and min capacities (from :meth:`NextState`).
        :type current_cap: dict
        :param ess_pmax: Original maximum power outputs for ESS (MW).
        :type ess_pmax: np.ndarray
        :param ess_duration: Duration (hours) of each ESS at rated power.
        :type ess_duration: np.ndarray
        :param ess_socmax: Maximum SOC fraction for each ESS.
        :type ess_socmax: np.ndarray
        :param ess_socmin: Minimum SOC fraction for each ESS.
        :type ess_socmin: np.ndarray
        :param SOC_old: Previous SOC values (in MWh).
        :type SOC_old: np.ndarray

        :return:
            A 3-element tuple containing:

            * **ess_smax** (*np.ndarray*): Maximum allowable SOC (in MWh) after accounting for failures/repairs.
            * **ess_smin** (*np.ndarray*): Minimum allowable SOC (in MWh).
            * **SOC_old** (*np.ndarray*): Updated SOC for each ESS.

        :rtype: tuple
        """

        self.ess_emax = np.multiply(current_cap["max"][ng + nl::], ess_duration) # maximum ess energy capacity
        self.ess_smax = np.multiply(self.ess_emax, ess_socmax) # maximum allowable SOC (as energy)
        self.ess_smin = np.multiply(self.ess_emax, ess_socmin) # minimum allowable SOC (as energy)
        SOC_old = current_cap["max"][ng + nl::]*SOC_old/ess_pmax # modify SOC_old based on current capacity of batteries

        return(self.ess_smax, self.ess_smin, SOC_old)


    def WindPower(self, nz, w_sites, zone_no, w_classes, r_cap, current_w_class, tr_mats, p_class, w_turbines, out_curve2, out_curve3):
        """
        Computes wind power generation by randomly transitioning wind speed classes, 
        then mapping each class to a turbine power output.

        :param nz: Number of zones in the system.
        :type nz: int
        :param w_sites: Number of wind farm sites.
        :type w_sites: int
        :param zone_no: Zone indices for each wind site.
        :type zone_no: np.ndarray
        :param w_classes: Total number of wind speed classes used.
        :type w_classes: int
        :param r_cap: Rated capacities (MW) of wind turbines at each site.
        :type r_cap: np.ndarray
        :param current_w_class: Current wind speed class for each site (1D array).
        :type current_w_class: np.ndarray
        :param tr_mats: 3D array of transition rate matrices for each site (dimensions: [site, w_classes, w_classes]).
        :type tr_mats: np.ndarray
        :param p_class: Array specifying the power curve classification type (e.g., 2 or 3) for each site.
        :type p_class: np.ndarray
        :param w_turbines: Number of turbines at each site.
        :type w_turbines: np.ndarray
        :param out_curve2: Power output curve for class 2 turbines (indexed by wind speed class).
        :type out_curve2: np.ndarray
        :param out_curve3: Power output curve for class 3 turbines (indexed by wind speed class).
        :type out_curve3: np.ndarray

        :return:
            A 2-element tuple containing:

            * **w_zones** (*np.ndarray*): Wind generation in each zone (size = nz).
            * **current_w_class** (*np.ndarray*): Updated wind speed classes for the next hour.

        :rtype: tuple
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
        Determines solar power output for each zone based on a randomly selected cluster/day/hour profile.

        :param n: Current hour in the overall MCS simulation.
        :type n: int
        :param nz: Number of zones.
        :type nz: int
        :param s_zone_no: Zone indices for each solar site.
        :type s_zone_no: np.ndarray
        :param solar_prob: Array of cluster probabilities (rows = clusters, columns = months).
        :type solar_prob: np.ndarray
        :param s_profiles: List of 3D arrays, each containing daily solar profiles for a cluster 
                           (dimensions: [days, 24 hours, sites]).
        :type s_profiles: list[np.ndarray]
        :param s_sites: Number of solar sites.
        :type s_sites: int
        :param s_max: Maximum capacity (MW) of each solar site.
        :type s_max: np.ndarray

        :return:
            A 2D NumPy array of shape (24, nz), giving solar generation (MW) for each zone over 24 hours. 
            Only the row corresponding to hour n%24 is relevant at time n, but the entire 2D block 
            is returned for convenience.

        :rtype: np.ndarray
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
        Formulates and solves an economic dispatch (transportation model) optimization 
        for a single hour, including line flow constraints, generation dispatch, 
        storage charging/discharging, and load curtailment.

        :param ng: Number of conventional generators.
        :type ng: int
        :param nz: Number of zones.
        :type nz: int
        :param nl: Number of lines.
        :type nl: int
        :param ness: Number of energy storage systems.
        :type ness: int
        :param fb_ess: Function specifying variable bounds for ESS charging power.
        :type fb_ess: function
        :param fb_soc: Function specifying variable bounds for ESS state of charge.
        :type fb_soc: function
        :param BMva: System base power (MVA).
        :type BMva: float
        :param fb_Pg: Function specifying variable bounds for generator and ESS discharge power.
        :type fb_Pg: function
        :param fb_flow: Function specifying variable bounds for line flow.
        :type fb_flow: function
        :param A_inc: Incidence matrix for lines.
        :type A_inc: np.ndarray
        :param gen_mat: Generation matrix indicating which bus/zone each generator belongs to.
        :type gen_mat: np.ndarray
        :param curt_mat: Matrix used for load curtailment variables (identity mapping to each zone).
        :type curt_mat: np.ndarray
        :param ch_mat: Matrix used for storage charging variables (which bus/zone each ESS belongs to).
        :type ch_mat: np.ndarray
        :param gencost: Per-unit fuel costs for conventional generators.
        :type gencost: np.ndarray
        :param net_load: Net load array (MW) per zone.
        :type net_load: np.ndarray
        :param SOC_old: Previous hour’s state-of-charge for each ESS (MWh).
        :type SOC_old: np.ndarray
        :param ess_pmax: Maximum power output (MW) for each ESS.
        :type ess_pmax: np.ndarray
        :param ess_eff: Round-trip efficiency (fraction) for each ESS.
        :type ess_eff: np.ndarray
        :param disch_cost: Discharge cost for each ESS.
        :type disch_cost: np.ndarray
        :param ch_cost: Charge cost for each ESS.
        :type ch_cost: np.ndarray

        :return:
            A 2-element tuple containing:

            * **load_curt** (*float*): Total load curtailment (MW) in this hour.
            * **SOC_old** (*np.ndarray*): Updated state-of-charge for each ESS after dispatch.

        :rtype: tuple
        """

        model = ConcreteModel() # declaring the model

        # declaring the variables
        model.flow = Var(range(nl), bounds = fb_flow) # line flow variables
        model.Pg = Var(range(ng + ness), bounds  = fb_Pg) # power output for conventional generators and ESS discharge
        model.Pc = Var(range(ness), bounds = fb_ess) # charge variables for ESS
        model.SOC = Var(range(ness), bounds = fb_soc) # state-of-charge variables for ESS
        model.curt = Var(range(nz), bounds = (0, None)) # load curtailment variables

        A_inc_t = np.transpose(A_inc) # transposing incedence matrix

        LOL_cost = 1000 # cost of lost load (set to very high so that system always tries to minimize loss)

        # power balance constraint
        def con_rule1(model,i):
            return(sum(A_inc_t[i, j]*model.flow[j] for j in range(nl))\
                    + sum(gen_mat[i,m]*model.Pg[m] for m in range(ng + ness)) \
                    + sum(ch_mat[i,m]*model.Pc[m] for m in range(ness)) \
            + sum(curt_mat[i,c]*model.curt[c] for c in range(nz)) >= net_load[i]/BMva)

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

        return(load_curt, SOC_old)

    def OptDispatchLite(self, ng, nz, ness, fb_ess, fb_soc, BMva, fb_Pg, A_inc, \
                    gencost, net_load, SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost):
        """
        Solves an economic dispatch problem ignoring line flow constraints (copper-sheet model). 
        This method is a simplified version of :meth:`OptDispatch`.

        :param ng: Number of conventional generators.
        :type ng: int
        :param nz: Number of zones.
        :type nz: int
        :param ness: Number of energy storage systems.
        :type ness: int
        :param fb_ess: Function specifying variable bounds for ESS charging power.
        :type fb_ess: function
        :param fb_soc: Function specifying variable bounds for ESS state-of-charge.
        :type fb_soc: function
        :param BMva: System base power (MVA).
        :type BMva: float
        :param fb_Pg: Function specifying variable bounds for generator and ESS discharge power.
        :type fb_Pg: function
        :param A_inc: Incidence matrix (not strictly used, but included for consistency).
        :type A_inc: np.ndarray
        :param gencost: Per-unit costs for conventional generators.
        :type gencost: np.ndarray
        :param net_load: Net load (MW) for the entire system (summed over all zones).
        :type net_load: np.ndarray
        :param SOC_old: Previous hour’s state-of-charge for each ESS (MWh).
        :type SOC_old: np.ndarray
        :param ess_pmax: Maximum power output for each ESS.
        :type ess_pmax: np.ndarray
        :param ess_eff: Round-trip efficiency for each ESS.
        :type ess_eff: np.ndarray
        :param disch_cost: Discharge cost for each ESS.
        :type disch_cost: np.ndarray
        :param ch_cost: Charge cost for each ESS.
        :type ch_cost: np.ndarray

        :return:
            A 2-element tuple containing:

            * **load_curt** (*float*): Total load curtailment (MW).
            * **SOC_old** (*np.ndarray*): Updated state-of-charge for each ESS.

        :rtype: tuple
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

        return(load_curt, SOC_old)

    def TrackLOLStates(self, load_curt, BMva, var_s, LOL_track, s, n):
        """
        Records whether load was curtailed at the current hour, and logs 
        loss-of-load days, frequencies, etc.

        :param load_curt: The amount of load curtailment (MW).
        :type load_curt: float
        :param BMva: System base power (MVA) for consistent unit conversions.
        :type BMva: float
        :param var_s: Dictionary of temporary simulation variables (e.g., 
                      curtailment array, LOL day counts).
        :type var_s: dict
        :param LOL_track: 2D array (shape: [samples, hours]) tracking which hours had loss of load.
        :type LOL_track: np.ndarray
        :param s: Current Monte Carlo sample index.
        :type s: int
        :param n: Current hour index.
        :type n: int

        :return:
            A 2-element tuple containing:

            * **var_s** (*dict*): Updated dictionary of simulation variables.
            * **LOL_track** (*np.ndarray*): Updated array marking loss-of-load hours.

        :rtype: tuple
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
        """
        Gathers partial results from all MPI processes and updates the 
        running mean and coefficient of variation (COV) for LOLP. 
        Used to track convergence during MCS.

        :param s: Current sample index.
        :type s: int
        :param LOLP_rec: Array of LOLP values recorded by the local process for each sample so far.
        :type LOLP_rec: np.ndarray
        :param comm: MPI communicator object.
        :type comm: mpi4py.MPI.Comm
        :param rank: MPI rank of this process.
        :type rank: int
        :param size: Total number of MPI processes.
        :type size: int
        :param mLOLP_rec: Array for storing the running mean of LOLP across samples.
        :type mLOLP_rec: np.ndarray
        :param COV_rec: Array for storing the coefficient of variation (COV) at each sample.
        :type COV_rec: np.ndarray

        :return:
            A 2-element tuple containing:

            * **mLOLP_rec** (*np.ndarray*): Updated array of mean LOLP values across processes.
            * **COV_rec** (*np.ndarray*): Updated array of COV values, checking for convergence.

        :rtype: tuple
        """
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
        Updates reliability index accumulators (LOLP, EUE, EPNS, LOLE, etc.) 
        after each sample is completed.

        :param indices_rec: Dictionary that stores reliability indices across samples.
        :type indices_rec: dict
        :param var_s: Dictionary of sample-specific tracking variables 
                      (curtailment array, LOL states, etc.).
        :type var_s: dict
        :param sim_hours: Number of hours in the current simulation (e.g., 8760 for a year).
        :type sim_hours: int
        :param s: Current sample index.
        :type s: int

        :return:
            **indices_rec** (*dict*): Updated dictionary containing reliability 
            index arrays for all samples.

        :rtype: dict
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
        Identifies the start and end of each outage (load-curtailed period) 
        from the binary LOL array and calculates their durations.

        :param var_s: Dictionary of sample-specific tracking variables (e.g., "label_LOLF").
        :type var_s: dict

        :return:
            1D array of outage durations (in hours).

        :rtype: np.ndarray
        """
        start_outages = np.where(np.diff(np.concatenate(([0], var_s["label_LOLF"], [0]))) == 1)[0]
        end_outages = np.where(np.diff(np.concatenate(([0], var_s["label_LOLF"], [0]))) == -1)[0]
        out_durations = end_outages - start_outages

        return(out_durations)

    def GetReliabilityIndices(self, indices_rec, sim_hours, samples):
        """
        Computes final reliability indices (LOLP, EUE, EPNS, LOLE, etc.) 
        by averaging over the recorded arrays.

        :param indices_rec: Dictionary with arrays of reliability indices 
                            (one entry per sample).
        :type indices_rec: dict
        :param sim_hours: Total number of hours (e.g., 8760) in the simulation horizon.
        :type sim_hours: int
        :param samples: Number of Monte Carlo samples performed.
        :type samples: int

        :return:
            A dictionary containing final reliability metrics such as LOLP, LOLH, EUE, EPNS, LOLE, etc.

        :rtype: dict
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

    def OutageHeatMap(self, LOL_track, size, samples, main_folder):
        """
        Aggregates hourly loss-of-load data into a monthly/hourly matrix and writes 
        the percentage of load-loss hours by month/hour to a CSV file. 
        Can be used later for creating heatmaps.

        :param LOL_track: 4D array of shape (size, samples, 365, 24) representing the LOL states.
        :type LOL_track: np.ndarray
        :param size: Total number of MPI processes.
        :type size: int
        :param samples: Number of Monte Carlo samples.
        :type samples: int
        :param main_folder: Directory path where results (CSV/plots) are saved.
        :type main_folder: str

        :return: None
        :rtype: None
        """
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
        
        pd.DataFrame((LOL_prob)*100/days_in_month[:, np.newaxis]).to_csv(f"{main_folder}/Results/LOL_perc_prob.csv")

    def ParallelProcessing(self, indices, LOL_track, comm, rank, size, samples, sim_hours):
        """
        Gathers reliability indices and the LOL tracker from all MPI processes to compute
        average indices over all ranks. Optionally saves final results and calls 
        :meth:`OutageHeatMap` if a full-year simulation is run.

        :param indices: Dictionary of reliability indices for the local rank.
        :type indices: dict
        :param LOL_track: 2D array of shape (samples, hours) tracking LOL states for the local rank.
        :type LOL_track: np.ndarray
        :param comm: MPI communicator object.
        :type comm: mpi4py.MPI.Comm
        :param rank: MPI rank of this process.
        :type rank: int
        :param size: Total number of MPI processes.
        :type size: int
        :param samples: Number of Monte Carlo samples performed.
        :type samples: int
        :param sim_hours: Number of hours in each sample (e.g., 8760).
        :type sim_hours: int

        :return:
            If rank=0, a dictionary containing aggregated reliability indices 
            (LOLP, EUE, etc.) across all ranks, else returns None.

        :rtype: dict or None
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

            main_folder = os.path.dirname(os.path.abspath(__file__))

            if not os.path.exists(f"{main_folder}/Results"):
                os.makedirs(f"{main_folder}/Results")

            df = pd.DataFrame([index_all])
            df.to_csv(f"{main_folder}/Results/indices.csv", index=False)

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

