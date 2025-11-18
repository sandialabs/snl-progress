import pandas as pd
import numpy as np

class RASystemData:
    '''This class extracts, modifies and returns the system data required for resource adequacy assessment'''

    # def __init__(self, nh):
    #     '''Hours of data available'''
    #     self.nh = nh

    def branch(self, data_branch):
        """
        Extracts and returns all system branch data.

        Parameters:
            data_branch (str): Path to the CSV file containing branch data.

        Returns:
            tuple: A tuple containing the number of lines, from buses, to buses, transmission capacities, MTTF, and MTTR.
        """

        self.branch = pd.read_csv(data_branch)
        self.fb = self.branch['From Bus'].values
        self.tb = self.branch['To Bus'].values
        self.nl = len(self.tb)
        self.r = self.branch['R'].values
        self.x = self.branch['X'].values
        self.b = self.branch['B'].values
        self.cap_trans = self.branch['Rating'].values
        self.MTTR_trans = self.branch['MTTR'].values
        self.MTTF_trans = self.branch['MTTF'].values

        return(self.nl, self.fb, self.tb, self.cap_trans, self.MTTF_trans, self.MTTR_trans)

    def bus(self, data_bus):
        """
        Extracts and returns all system bus data.

        Parameters:
            data_bus (str): Path to the CSV file containing bus data.

        Returns:
            tuple: A tuple containing bus names, bus numbers, and the number of buses.
        """

        self.bus = pd.read_csv(data_bus)
        self.bus_name = self.bus['Bus Name']
        self.bus_no = self.bus['Bus No.'].values
        self.nz = len(self.bus_no)

        return(self.bus_name, self.bus_no, self.nz)

    def gen(self, data_gen):
        """
        Extracts and returns all system conventional generator data.

        Parameters:
            data_gen (str): Path to the CSV file containing generator data.

        Returns:
            tuple: A tuple containing generator buses, number of generators, maximum and minimum capacities,
            forced outage rates, MTTF, MTTR, and generation costs.
        """

        self.gen = pd.read_csv(data_gen) # all coventional generator data
        self.genbus = self.gen['Bus No.'].values # bus at which generator is located
        self.ng = len(self.genbus) # no. of generators  
        self.pmax = self.gen['Max Cap'].values # maximum gen. capacity 
        self.pmin = self.gen['Min Cap'].values # minimum gen. capacity
        self.FOR_gen = self.gen['FOR'].values # forced outage rate
        self.MTTF_gen = self.gen['MTTF'].values # mean time to failure in hours
        self.MTTR_gen = self.gen['MTTR'].values # mean time to repair in hours
        self.gencost = self.gen['Cost'].values # cost of generation 

        return(self.genbus, self.ng, self.pmax, self.pmin, self.FOR_gen, self.MTTF_gen, self.MTTR_gen, self.gencost)

    def storage(self, data_storage):
        """
        Extracts and returns all system energy storage data.

        Parameters:
            data_storage (str): Path to the CSV file containing storage data.

        Returns:
            tuple: A tuple containing ESS names, ESS buses, number of ESS, maximum and minimum power output,
            duration, maximum and minimum SOC, efficiency, discharge and charge costs, MTTF, MTTR, and units.
        """

        self.storage = pd.read_csv(data_storage)
        self.essname = self.storage['Name']
        self.essbus = self.storage['Bus'].values # bus at which storage is located
        self.ness = len(self.essbus) # no. of ESS
        self.ess_pmax = self.storage['Pmax'].values # maximum ESS power output
        self.ess_pmin = self.storage['Pmin'].values # minimum ESS power output
        self.ess_duration = self.storage['Duration'].values # duration of storage
        self.ess_socmax = self.storage['max_SOC'].values # maximum ESS SOC as fraction
        self.ess_socmin = self.storage['min_SOC'].values # minimum ESS SOC as fraction
        self.ess_eff = self.storage['Efficiency'].values # round-trip efficiency
        self.disch_cost = self.storage['Discharge Cost'].values # cost of discharging from storage
        self.ch_cost = self.storage['Charge Cost'].values
        self.MTTF_ess = self.storage['MTTF'].values
        self.MTTR_ess = self.storage['MTTR'].values
        self.ess_units = self.storage['Units'].values
        self.ess_chemistry = self.storage['Chemistry'].values # cell chemistry of BESS
        return(self.essname, self.essbus, self.ness, self.ess_pmax, self.ess_pmin, self.ess_duration, self.ess_socmax, self.ess_socmin, \
               self.ess_eff, self.disch_cost, self.ch_cost, self.MTTF_ess, self.MTTR_ess, self.ess_units, self.ess_chemistry)

    def load(self, bus_name, data_load):
        """
        Extracts and returns all system load data.

        Parameters:
            bus_name (str): Name of the bus.
            data_load (str): Path to the CSV file containing load data.

        Returns:
            numpy.ndarray: Array containing load data for all regions.
        """
        self.load = pd.read_csv(data_load)
        self.load_all_regions = self.load[bus_name].values

        return(self.load_all_regions)