import pandas as pd
import requests
import os
import glob
import numpy as np
from datetime import datetime, timedelta

import pvlib.pvsystem as pv
import pvlib.location as loc
import pvlib.modelchain as mc
import pvlib

class Solar:
    """
    A class to handle solar generation data, downloading weather data, calculating solar generation using PVLib,
    and processing the data for Monte Carlo Simulation (MCS).
    """

    def __init__(self, site_data, directory):
        """
        Initializes the Solar class with site data and directory.

        Parameters:
            site_data (str): Path to the CSV file containing site data.
            directory (str): Directory to save the data.
        """

        self.sites_df = pd.read_csv(site_data)
        self.n_sites = len(self.sites_df)
        self.s_zone_no = self.sites_df['zone']
        self.names = self.sites_df["site_name"]
        self.lats = self.sites_df["lat"]
        self.lons = self.sites_df["long"]
        self.tracking = self.sites_df["tracking"]
        self.MW = self.sites_df["MW"]
        self.directory = directory
        pass

    def SolarGen(self, api_key, your_name, your_affiliation, your_email, year_start, year_end):
        """
        Downloads weather data from NREL NSRDB and calculates solar generation using PVLib.

        Parameters:
            api_key (str): API key for NREL NSRDB.
            your_name (str): Your full name.
            your_affiliation (str): Your affiliation.
            your_email (str): Your email address.
            year_start (int): Start year for data download.
            year_end (int): End year for data download.
        """
        interval = '60'; utc = 'false'; reason = 'beta+testing'; mailing_list = 'false'

        self.year_range = range(year_start, year_end + 1)
        self.years = [str(num) for num in self.year_range]

        for year in self.years:

            # check if leap year
            if int(year)%4==0:
                leap_year = 'true'
            else:
                leap_year = 'false'

            for i in range(len(self.sites_df)):

                name = self.names[i]
                lat = self.lats[i]
                lon = self.lons[i]

                # download data for satellite
                url = 'https://developer.nrel.gov/api/nsrdb/v2/solar/nsrdb-GOES-tmy-v4-0-0-download.csv?wkt=POINT({lon}%20{lat})&names=tmy-{year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}'\
                    .format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, \
                    email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason, \
                    api=api_key)
                response = requests.get(url, verify=False)

                # store data in csv file
                csv_data = response.text
                if not os.path.exists(f"{self.directory}/solardata/{year}"):
                    os.makedirs(f"{self.directory}/solardata/{year}")
                with open(f"{self.directory}/solardata/{year}/{name}.csv", "w") as csv_file:
                    csv_file.write(csv_data)
                timezone = pd.read_csv(f'{self.directory}/solardata/{year}/{name}.csv', nrows=1)['Time Zone'][0]
                dataF = pd.read_csv(f'{self.directory}/solardata/{year}/{name}.csv', skiprows=[0, 1])

                print('NSRDB weather data for', name, 'for the year', year, 'obtained and saved to csv file.')

                # calculate weather data to solar generation data using pvlib
                ac = 1.04+1/600; dc = ac * 1.3 # Set AC to 1, DC to 1.3 for all projects. Scale up so that once 4% losses applied, get AC=1MW, DC=1.3MW.
                tilt = round((lat*0.76+3.1), 0)

                system = pv.PVSystem(surface_tilt=tilt, surface_azimuth=180,
                                module_parameters={'pdc0': dc, 'gamma_pdc': -0.004},
                                inverter_parameters={'pdc0': ac},
                                temperature_model_parameters=pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS[
                                    'sapm']
                                ['open_rack_glass_glass'])

                location = pvlib.location.Location(lat, lon)
                mchain = mc.ModelChain.with_pvwatts(system, location)

                # prep weather data for mchain
                dataF.index = pd.to_datetime(dataF[['Year','Month','Day','Hour','Minute']])
                dataF.index = dataF.index.tz_localize(int(timezone)*3600)
                weather_sat = dataF[['DNI','GHI','DHI','Temperature','Wind Speed']].copy()
                weather_sat.columns = ['dni','ghi','dhi','temp_air','wind_speed']
                weather_cs = dataF[['Clearsky DNI','Clearsky GHI','Clearsky DHI','Temperature','Wind Speed']].copy()
                weather_cs.columns = ['dni','ghi','dhi','temp_air','wind_speed']

                # run mchain model for satellite data
                mchain.run_model(weather_sat)
                ac_power_sat = pd.DataFrame(mchain.results.ac)*self.MW[i]
                ac_power_sat.to_csv(f'{self.directory}/solardata/{year}/{name}_sgen_sat.csv')

                # run mchain model for clearsky data
                mchain.run_model(weather_cs)
                ac_power_cs = pd.DataFrame(mchain.results.ac)*self.MW[i]
                ac_power_cs.to_csv(f'{self.directory}/solardata/{year}/{name}_sgen_cs.csv')

    def SolarGenGather(self, year_start, year_end):
        """
        Gathers solar generation data from all sites and years, processes it, and saves it to CSV files.

        Parameters:
            year_start (int): Start year for data gathering.
            year_end (int): End year for data gathering.
        """

        solar_directory = f'{self.directory}/solardata/'
        self.year_range = range(year_start, year_end + 1)
        self.years = [str(num) for num in self.year_range]

        for year in self.years:

            year_directory = f'{solar_directory}/{year}/'

            file_pattern_sat = '*_sgen_sat.csv'
            file_pattern_cs = '*_sgen_cs.csv'

            common_to_remove_sat = '_sgen_sat'
            common_to_remove_cs = '_sgen_cs'

            file_paths_sat = glob.glob(year_directory + file_pattern_sat)
            file_paths_cs = glob.glob(year_directory + file_pattern_cs)

            columns_to_extract = ['p_mp']
            allsites_year_sat = pd.DataFrame()
            allsites_year_cs = pd.DataFrame()

            for file_path in file_paths_sat:

                file_name = os.path.splitext(os.path.basename(file_path))[0]
                cleaned_name = file_name.replace(common_to_remove_sat, '')

                df = pd.read_csv(file_path)
                selected_columns = df[columns_to_extract]
                allsites_year_sat[cleaned_name] = selected_columns

            for file_path in file_paths_cs:

                file_name = os.path.splitext(os.path.basename(file_path))[0]
                cleaned_name = file_name.replace(common_to_remove_cs, '')

                df = pd.read_csv(file_path)
                selected_columns = df[columns_to_extract]
                allsites_year_cs[cleaned_name] = selected_columns


            allsites_year_sat.to_csv(f'{self.directory}/solardata/allsites_sat_{year}.csv', index = False)
            allsites_year_cs.to_csv(f'{self.directory}/solardata/allsites_cs_{year}.csv', index = False)

        file_pattern_sat_all = 'allsites_sat_*.csv'
        file_pattern_cs_all = 'allsites_cs_*.csv'

        file_paths_sat_all = glob.glob(solar_directory + file_pattern_sat_all)
        file_paths_cs_all = glob.glob(solar_directory + file_pattern_cs_all)

        gendata_sat = pd.DataFrame()
        gendata_cs = pd.DataFrame()

        for file_path in file_paths_sat_all:

            df_sat = pd.read_csv(file_path)
            selected_columns_all = df_sat[self.names]
            gendata_sat = pd.concat([gendata_sat, pd.DataFrame(selected_columns_all)], ignore_index=True)
            os.remove(file_path)

        for file_path_cs in file_paths_cs_all:

            df_cs = pd.read_csv(file_path_cs)
            selected_columns_all = df_cs[self.names]
            gendata_cs = pd.concat([gendata_cs, pd.DataFrame(selected_columns_all)], ignore_index=True)
            os.remove(file_path_cs)

        csi = pd.DataFrame(gendata_sat.values/gendata_cs.values) # calculate clear-sky index
        csi.columns = self.names
        csi.fillna(0, inplace=True)

        # Set the start date
        start_date = datetime(year_start, 1, 1, 0, 0, 0)

        # Set the end date to '2012-12-31'
        end_date = datetime(year_end, 12, 31, 23, 0, 0)
        time_step = '1H'
        datetime_vector = pd.date_range(start=start_date, end=end_date, freq=time_step)
        datetime_df = pd.DataFrame({'datetime':datetime_vector.strftime('%m/%d/%y %H:%M')})
        gendata_sat = pd.concat([datetime_df, gendata_sat], axis = 1)
        csi = pd.concat([datetime_df, csi], axis = 1)

        excel_file_path = f'{self.directory}/solar_data.xlsx'

        with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
            gendata_sat.to_excel(writer, sheet_name= 'solar_gen', index = False)
            csi.to_excel(writer, sheet_name = 'csi', index = False)

        print("Solar data download and processing complete! Let's evaluate performance of clusters now ...")


    def GetSolarProfiles(self, solar_prob_data):
        '''
        This function extracts the solar data from clusters and modifies it for the MCS. The solar data is stored in a 4D ndarray where the dimensions are: [cluster, day, hour, site]. The clusters are created using the K-means clustering algorithm. Similar days of solar generation are put in the same cluster.

        Parameters:
            solar_prob_data (str): Path to the CSV file containing solar probability data.

        Returns:
            tuple: Number of sites, zone numbers, MW capacity, solar profiles, and solar probability.

        '''
        clusters = glob.glob(os.path.join(self.directory + "/Clusters/", '*/'))
        n_clust = len(clusters) # no. of clusters created (depends on user and data)

        self.s_profiles = [] # this array will contain solar data for all clusters, sites, and days
        for i in range(1, n_clust + 1):
            self.cluster_list = []
            for site in self.names:
                matrix=pd.read_csv(self.directory + "/Clusters/" + str(i) + "/"+site+".csv")
                self.cluster_list.append(matrix)
            self.s_profiles.append(np.stack(self.cluster_list,-1))

        self.solar_prob = pd.read_csv(solar_prob_data).values

        return(self.n_sites, self.s_zone_no, self.MW, self.s_profiles, self.solar_prob)

    #-------------------------------------OTHER RENEWABLES (Optional)-------------------------------------------------
    #-----------------------------(CSP, RTPV, Geothermal, etc.)--------------------------------------------

    # def CSP(self, nh, data_CSP):
    #     '''This function extracts and returns all system Concentrated Solar Power data'''
    #     self.CSP = pd.read_csv(data_CSP).values
    #     self.CSP_all_buses = np.zeros((nh, 3))
    #     self.CSP_all_buses[:, 1] = self.CSP[:, 4]

    #     return(self.CSP_all_buses)

    # def RTPV(self, nh, data_RTPV):
    #     '''This function extracts and returns all system Rooftop Solar PV data'''
    #     self.RTPV = pd.read_csv(data_RTPV).values
    #     self.RTPV_all_buses = np.zeros((nh, 3))
    #     self.RTPV_all_buses[:, 0] = np.sum(self.RTPV[:, 24:34], axis = 1)
    #     self.RTPV_all_buses[:, 1] = self.RTPV[:, 34]
    #     self.RTPV_all_buses[:, 2] = np.sum(self.RTPV[:, 4:24], axis = 1)

    #     return(self.RTPV_all_buses)


