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
    A class to handle solar generation data by downloading weather data from the NSRDB, 
    calculating solar generation using PVLib, and preparing data for Monte Carlo Simulation (MCS).

    :param site_data: Path to the CSV file containing site data (site name, latitude, longitude, etc.).
    :type site_data: str
    :param directory: Directory for saving and reading solar-related data files.
    :type directory: str
    """

    def __init__(self, site_data, directory):
        """
        Initializes the Solar class with site data and working directory.

        :param site_data: Path to the CSV file containing site data. This file should have columns 
                          such as 'site_name', 'lat', 'long', 'zone', 'tracking', and 'MW'.
        :type site_data: str
        :param directory: Path to the directory where data will be downloaded and stored.
        :type directory: str

        :raises FileNotFoundError: If the provided ``site_data`` file does not exist.
        :raises pd.errors.EmptyDataError: If the CSV file is empty or improperly formatted.
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
        Downloads weather data from NREL NSRDB and calculates solar generation using PVLib for each site.

        This method:
          1. Iterates through each site and year in the specified range.
          2. Downloads weather data (DNI, GHI, DHI, etc.) from the NSRDB using HTTP requests.
          3. Uses PVLib's ModelChain with a simple PVWatts-based system to convert the weather data 
             into AC power output.
          4. Writes both the satellite-based and clearsky-based generation profiles to CSV files.

        :param api_key: Your personal API key for the NREL NSRDB.
        :type api_key: str
        :param your_name: Your full name (required by the NSRDB API).
        :type your_name: str
        :param your_affiliation: Your organizational affiliation (required by the NSRDB API).
        :type your_affiliation: str
        :param your_email: Your email address (required by the NSRDB API).
        :type your_email: str
        :param year_start: Start year for data downloads.
        :type year_start: int
        :param year_end: End year (inclusive) for data downloads.
        :type year_end: int

        :return: None
        :rtype: None

        :raises requests.exceptions.RequestException: If there is a network-related error during the download.
        :raises OSError: If writing to the local file system fails for any reason.
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
                url = 'https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}'\
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
        Gathers and processes solar generation data from all sites and years, concatenating 
        each site's satellite-based and clearsky-based generation files into single CSVs. 
        It then computes a clearsky index (CSI) and stores the final data in an Excel file.

        :param year_start: Start year (inclusive) for gathering solar generation data.
        :type year_start: int
        :param year_end: End year (inclusive) for gathering solar generation data.
        :type year_end: int

        :return: None
        :rtype: None

        :raises FileNotFoundError: If expected CSV files do not exist in the specified directory.
        :raises OSError: If any file operation (read/write/remove) fails.
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
        """
        Extracts and organizes solar data from clustered CSVs for use in Monte Carlo Simulation (MCS). 
        Each cluster directory contains daily solar generation profiles for all sites; these are stacked 
        into a 4D array of shape (cluster, day, hour, site). Probability data for each cluster is also read 
        from the given CSV.

        :param solar_prob_data: Path to the CSV file containing solar probability data (cluster probabilities).
        :type solar_prob_data: str

        :return:
            A 5-element tuple containing:

            * **n_sites** (*int*): Number of solar sites.
            * **s_zone_no** (*pd.Series*): Zone numbers corresponding to each site.
            * **MW** (*pd.Series*): Rated capacity (in MW) for each site.
            * **s_profiles** (*list[np.ndarray]*): A list of 3D NumPy arrays, one per cluster, 
              with shape (days, hours, sites).
            * **solar_prob** (*np.ndarray*): Probability values for each cluster.

        :rtype: tuple

        :raises FileNotFoundError: If cluster directories or CSV files are missing.
        """
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


