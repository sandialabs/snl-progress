import pandas as pd
import numpy as np

class RASystemData:
    """
    Manages and processes the core system data needed for resource adequacy (RA) assessments.

    This class provides methods to read and extract power system information from CSV files:
      - **Branch data** (e.g., line capacities, MTTF/MTTR)
      - **Bus data** (bus names, bus numbers)
      - **Generator data** (pmax, pmin, forced outage rates, maintenance times, costs)
      - **Storage data** (ESS ratings, SOC constraints, costs, reliability parameters)
      - **Load data** (regional load profiles)

    These methods facilitate easy import and organization of data so that reliability 
    or adequacy simulations can be conducted downstream (e.g., Monte Carlo simulations).
    """
    # def __init__(self, nh):
    #     '''Hours of data available'''
    #     self.nh = nh

    def branch(self, data_branch):
        """
        Loads branch (transmission line) data and extracts key attributes for RA analysis.

        :param data_branch: Path to the CSV file containing branch data, typically including 
                            columns like "From Bus", "To Bus", "Rating", "MTTF", "MTTR", etc.
        :type data_branch: str

        :return:
            A tuple containing:

            * **nl** (*int*): Number of transmission lines (rows in the CSV).
            * **fb** (*np.ndarray*): 1D array of "From Bus" indices for each line.
            * **tb** (*np.ndarray*): 1D array of "To Bus" indices for each line.
            * **cap_trans** (*np.ndarray*): 1D array of transmission line ratings (MW).
            * **MTTF_trans** (*np.ndarray*): Mean time to failure for each line (hours).
            * **MTTR_trans** (*np.ndarray*): Mean time to repair for each line (hours).

        :rtype: tuple

        :raises FileNotFoundError: If ``data_branch`` does not point to a valid file.
        :raises pd.errors.EmptyDataError: If the CSV file is empty or badly formatted.
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
        Loads bus data and extracts bus names and numbers.

        :param data_bus: Path to the CSV file containing bus data, often with columns 
                         "Bus Name" and "Bus No.".
        :type data_bus: str

        :return:
            A tuple containing:

            * **bus_name** (*pd.Series*): Series of bus names.
            * **bus_no** (*np.ndarray*): 1D array of bus indices.
            * **nz** (*int*): Number of buses (length of ``bus_no``).

        :rtype: tuple

        :raises FileNotFoundError: If ``data_bus`` is not found.
        :raises pd.errors.EmptyDataError: If the CSV is empty or invalid.
        """

        self.bus = pd.read_csv(data_bus)
        self.bus_name = self.bus['Bus Name']
        self.bus_no = self.bus['Bus No.'].values
        self.nz = len(self.bus_no)

        return(self.bus_name, self.bus_no, self.nz)

    def gen(self, data_gen):
        """
        Loads conventional generator data, including capacities and reliability parameters.

        :param data_gen: Path to the CSV file containing generator info (e.g., "Bus No.", 
                         "Max Cap", "Min Cap", "FOR", "MTTF", "MTTR", "Cost").
        :type data_gen: str

        :return:
            A tuple containing:

            * **genbus** (*np.ndarray*): Bus indices (1D) for each generator.
            * **ng** (*int*): Number of generators in the system.
            * **pmax** (*np.ndarray*): Max capacity (MW) of each generator.
            * **pmin** (*np.ndarray*): Min capacity (MW) of each generator.
            * **FOR_gen** (*np.ndarray*): Forced outage rate of each generator.
            * **MTTF_gen** (*np.ndarray*): Mean time to failure (hours).
            * **MTTR_gen** (*np.ndarray*): Mean time to repair (hours).
            * **gencost** (*np.ndarray*): Generation cost for each generator.

        :rtype: tuple

        :raises FileNotFoundError: If ``data_gen`` file is not found.
        :raises pd.errors.EmptyDataError: If the CSV is empty or malformed.
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
        Loads and returns data on energy storage systems (ESS), including power ratings and SOC limits.

        :param data_storage: Path to the CSV file containing ESS data (e.g., "Pmax", "Pmin", 
                             "Duration", "max_SOC", "min_SOC", "MTTF", "MTTR", etc.).
        :type data_storage: str

        :return:
            A tuple containing:

            * **essname** (*pd.Series*): Names/IDs for each ESS unit.
            * **essbus** (*np.ndarray*): Bus indices corresponding to each ESS.
            * **ness** (*int*): Number of ESS units.
            * **ess_pmax** (*np.ndarray*): Maximum power output (MW) for each ESS.
            * **ess_pmin** (*np.ndarray*): Minimum power output (MW) for each ESS.
            * **ess_duration** (*np.ndarray*): Duration (hours) of each ESS at rated power.
            * **ess_socmax** (*np.ndarray*): Max SOC fraction for each ESS (0-1).
            * **ess_socmin** (*np.ndarray*): Min SOC fraction for each ESS (0-1).
            * **ess_eff** (*np.ndarray*): Round-trip efficiency of each ESS.
            * **disch_cost** (*np.ndarray*): Discharge cost for each ESS.
            * **ch_cost** (*np.ndarray*): Charge cost for each ESS.
            * **MTTF_ess** (*np.ndarray*): Mean time to failure (hours) for each ESS.
            * **MTTR_ess** (*np.ndarray*): Mean time to repair (hours) for each ESS.
            * **ess_units** (*np.ndarray*): Multiplicities or number of identical ESS units.

        :rtype: tuple

        :raises FileNotFoundError: If ``data_storage`` file does not exist.
        :raises pd.errors.EmptyDataError: If the CSV is empty or malformed.
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

        return(self.essname, self.essbus, self.ness, self.ess_pmax, self.ess_pmin, self.ess_duration, self.ess_socmax, self.ess_socmin, \
               self.ess_eff, self.disch_cost, self.ch_cost, self.MTTF_ess, self.MTTR_ess, self.ess_units)

    def load(self, bus_name, data_load):
        """
        Loads and returns time-series load data (demand) for specified bus(es).

        :param bus_name: Column label(s) in the load CSV corresponding to each region's load. 
                         Can be a string for a single bus or a list of strings for multiple buses.
        :type bus_name: str or list[str]
        :param data_load: Path to the CSV file containing hourly or sub-hourly load data.
        :type data_load: str

        :return:
            A NumPy array containing load values. Its shape depends on whether ``bus_name`` 
            references one or multiple columns.

        :rtype: np.ndarray

        :raises FileNotFoundError: If ``data_load`` is not found.
        :raises pd.errors.EmptyDataError: If the CSV is empty or invalid.
        """
        self.load = pd.read_csv(data_load)
        self.load_all_regions = self.load[bus_name].values

        return(self.load_all_regions)