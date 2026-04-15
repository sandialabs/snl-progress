import numpy as np
import pandas as pd
import yaml

from mod_wind import Wind
from mod_solar import Solar
from mod_kmeans import KMeans_Pipeline


class DataProcess:

    def __init__(self, input_file):
        # open configuration file
        with open(input_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def ProcessWindData(self):

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

        solar_directory = self.config['data'] + '/Solar'
        n_clusters = self.config['n_clusters']

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
            pipeline.run(n_clusters = n_clusters)

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