import numpy as np
import pandas as pd
import yaml

from progress.mod_wind import Wind
from progress.mod_solar import Solar
from progress.mod_kmeans import KMeans_Pipeline


class DataProcess:
    """
    A class used to process wind and solar data from configuration and create 
    relevant input files for further modeling.

    This class reads a configuration file, and uses it to download, prepare, and 
    organize wind and solar data. It delegates certain tasks (e.g., data download, 
    transformation, K-means clustering) to specialized modules:
      - ``Wind`` for wind data processing
      - ``Solar`` for solar data processing
      - ``KMeans_Pipeline`` for clustering the resultant data

    :param input_file: Path to the YAML configuration file containing 
                      user settings and file/directory paths.
    :type input_file: str
    """
    def __init__(self, input_file):
        """
        Initializes the DataProcess instance by loading the configuration from a YAML file.

        This method opens and parses a YAML file specified by ``input_file``, 
        storing its contents in the ``self.config`` attribute for subsequent use.

        :param input_file: Absolute or relative path to the YAML configuration file.
        :type input_file: str

        :raises FileNotFoundError: If the YAML file is not found at the given path.
        :raises yaml.YAMLError: If the YAML file contains syntax errors or is invalid.
        """

        # open configuration file
        with open(input_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def ProcessWindData(self):
        """
        Downloads, processes, and prepares wind data for modeling.

        This method performs the following steps:

        1. **Set Up Paths**: Derives file paths for wind sites, power curves, 
           windspeed data, and transition rate Excel sheets from the loaded configuration.

        2. **Download Wind Data**: Invokes ``wind.DownloadWindData()`` to fetch 
           raw wind speed data using the user’s API credentials and configuration parameters.

        3. **Prepare Wind Farms Data**: Calls ``wind.WindFarmsData()`` to aggregate 
           site information, farm names, zone numbers, wind classes, and power curves.

        4. **Calculate Transition Rates**: Uses ``wind.CalWindTrRates()`` to compute 
           wind transition rates (wind speed state transitions) from the downloaded datasets.

        5. **Read Transition Matrices**: Loads transition matrices from an Excel file 
           and organizes them into a NumPy array.

        This step ultimately collects and prepares wind-related data so that it can 
        be integrated into larger studies (e.g., generating time-series or capacity 
        factor profiles for wind generation).

        :return: None
        :rtype: None

        :raises FileNotFoundError: If expected CSV/Excel files for wind data are missing.
        :raises ValueError: If wind data files contain invalid values or structures.
        """


        wind_directory = self.config['data'] + '/Wind'
        
        # download and process wind data
        if wind_directory:

            print("Downloading and processing wind data ...")

            wind_sites = wind_directory + '/wind_sites.csv'
            wind_power_curves = wind_directory + '/w_power_curves.csv'
            windspeed_data = wind_directory + '/windspeed_data.csv'
            wind_tr_rate = wind_directory + '/t_rate.xlsx'
            
            wind = Wind()

            # download wind data
            wind.DownloadWindData(wind_directory, wind_sites, self.config['api_key'], self.config['email'], self.config['affiliation'], \
                                self.config['year_start_w'], self.config['year_end_w'])
                
            w_sites, farm_name, zone_no, w_classes, w_turbines, r_cap, p_class, out_curve2, out_curve3,\
                start_speed = wind.WindFarmsData(wind_sites, wind_power_curves)

            # calculate transition rates 
            wind.CalWindTrRates(wind_directory, windspeed_data, wind_sites, wind_power_curves)

            tr_mats = pd.read_excel(wind_tr_rate, sheet_name=None)
            tr_mats = np.array([tr_mats[sheet_name].to_numpy() for sheet_name in tr_mats])

            return

    def ProcessSolarData(self):
        """
        Downloads, processes, and prepares solar data for modeling.

        This method performs the following sequence of operations:

        1. **Initialize Solar Module**: Creates a ``Solar`` instance with user-specified 
           site data paths and directory locations.

        2. **Download & Compute Solar Generation**: Invokes ``solar.SolarGen()`` to fetch 
           weather data from the user’s API and compute solar generation profiles 
           across the specified date range.

        3. **Gather Computed Profiles**: Executes ``solar.SolarGenGather()`` to combine 
           yearly generation results into a single dataset, suitable for clustering 
           or probability analysis.

        4. **Perform K-Means Clustering**: Creates and runs a ``KMeans_Pipeline`` instance. 
           It clusters the processed solar generation data into a specified number of 
           clusters, calculates probabilities, and saves the results to file.

        5. **Obtain Solar Profiles & Probabilities**: Uses ``solar.GetSolarProfiles()`` 
           to retrieve final site-level data, maximum possible generation, and the 
           probability distribution for solar capacity factors.

        In the end, this prepares solar data for further simulation or scenario analysis.

        :return: None
        :rtype: None

        :raises FileNotFoundError: If required CSV files for solar sites or probabilities 
                                  are not present.
        :raises ValueError: If solar data files contain invalid values or structures.
        """

        solar_directory = self.config['data'] + '/Solar'

        # download and process solar data
        if solar_directory:

            print("Downloading and processing solar data ...")

            solar_site_data = solar_directory+"/solar_sites.csv"
            solar_prob_data = solar_directory+"/solar_probs.csv"

            solar = Solar(solar_site_data, solar_directory)

            # download weather data and calculate solar generation
            solar.SolarGen(self.config['api_key'], self.config['name'], self.config['affiliation'], \
                       self.config['email'], self.config['year_start_s'], self.config['year_end_s'])
            
            # process data for input into k-means code
            solar.SolarGenGather(self.config['year_start_s'], self.config['year_end_s'])
            
            # Initialize the KMeans_Pipeline class
            pipeline = KMeans_Pipeline(solar_directory, solar_site_data)

            # Run the pipeline before performing any other actions
            pipeline.run(n_clusters = 10)

            # Calculate the cluster probabilities and save them to a CSV file
            pipeline.calculate_cluster_probability()

            # Split the data and cluster them based on the generated labels
            pipeline.split_and_cluster_data()

            s_sites, s_zone_no, s_max, s_profiles, solar_prob = solar.GetSolarProfiles(solar_prob_data)

            print("Solar data processing complete!")

            return
        
if __name__ == "__main__":

    data = DataProcess('input.yaml')
    data.ProcessWindData()
    data.ProcessSolarData()