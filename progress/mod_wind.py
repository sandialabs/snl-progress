import numpy as np
import pandas as pd
import requests
import os
from rex import WindResource as WR

class Wind:

    '''This class contains the methods required for downloading and processing wind data.'''

    def DownloadWindData(self, directory, site_data, api_key, email, affiliation, year_start, year_end):
        """
        Downloads wind speed data from the NREL wind toolkit.

        Parameters:
            directory (str): Directory to save the data.
            site_data (str): Path to the CSV file containing site data.
            api_key (str): API key for NREL.
            email (str): Your email address.
            affiliation (str): Your affiliation.
            year_start (int): Start year for data download.
            year_end (int): End year for data download.
        """

        year_list = range(year_start, year_end + 1)
        wind_site_df = pd.read_csv(site_data)
        site_count = len(wind_site_df)
        name_list = wind_site_df["Site Name"].tolist()
        wind_site_df["LON_LAT"] = wind_site_df["Longitude"].map(str) + " " + wind_site_df["Latitude"].map(str)
        coord_list = wind_site_df["LON_LAT"].tolist()
        interval = '60'

        for year in year_list:
            print("Collecting Data For ", year)
            for i in range(site_count):
                name = name_list[i]
                coords = coord_list[i]
                print(name, " at ", coords)
                response = requests.get("https://developer.nrel.gov/api/wind-toolkit/v2/wind/wtk-download.csv", params={
                    "api_key": api_key,
                    "wkt": f"POINT({coords})",
                    "attributes": "windspeed_80m,windspeed_100m",
                    "interval": interval,
                    "names": year,
                    "utc": "true",
                    "leap_day": "true",
                    "email": email,
                    "reason": "R&D",
                    "affiliation": affiliation,
                }, verify= False)
                csv_data = response.text
                if not os.path.exists(f"{directory}/wtk_data/{year}"):
                    os.makedirs(f"{directory}/wtk_data/{year}")
                with open(f"{directory}/wtk_data/{year}/{name}.csv", "w") as csv_file:
                    csv_file.write(csv_data)

        HH_list = wind_site_df["Hub Height"].tolist()
        append_years = list()
        for year in year_list:
            print("Processing Data For ", year)
            current_year_DF = pd.read_csv(directory+f"/wtk_data/{year}/{name_list[0]}.csv", skiprows=1)
            current_year_DF.drop(columns=["wind speed at 80m (m/s)","wind speed at 100m (m/s)"],inplace=True)
            for i in range(site_count):
                name = name_list[i]
                HH = HH_list[i]
                current_site_DF = pd.read_csv(directory+f"/wtk_data/{year}/{name}.csv", skiprows=1)
                if HH == 80:
                    current_site_DF[name_list[i]] = current_site_DF["wind speed at 80m (m/s)"]
                elif HH == 100:
                    current_site_DF[name_list[i]] = current_site_DF["wind speed at 100m (m/s)"]
                else:
                    current_site_DF[name_list[i]]=WR.power_law_interp(current_site_DF["wind speed at 80m (m/s)"],80,current_site_DF["wind speed at 100m (m/s)"],100,HH,mean=False)
                current_year_DF[name_list[i]] = current_site_DF[name_list[i]]
            append_years.append(current_year_DF)
        wind_speeds_DF = pd.concat(append_years, axis=0,ignore_index=True)

        wind_speeds_DF["Minute"] = wind_speeds_DF["Minute"] - 30
        wind_speeds_DF['datetime'] = pd.to_datetime(wind_speeds_DF[['Year', 'Month', 'Day', 'Hour', 'Minute']])
        wind_speeds_DF.set_index('datetime', inplace=True)
        wind_speeds_DF.drop(columns=['Year', 'Month', 'Day', 'Hour', 'Minute'], inplace=True)

        print('Done downloading and processing wind data!')

        wind_speeds_DF.to_csv(directory+f"/windspeed_data.csv")

    def WindFarmsData(self, site_data, pcurve_data, model):
        """
        Collects wind farm data from user input.

        Parameters:
            site_data (str): Path to the CSV file containing site data.
            pcurve_data (str): Path to the CSV file containing power curve data.

        Returns:
            tuple: Wind farm data including number of sites, farm names, zone numbers, wind classes, turbines, turbine ratings, power classes, output curves, and start speeds.
        """
        self.wind = pd.read_csv(site_data) # read file for wind farm data
        # self.farm_no = self.wind['Farm No.'].values # wind farm numbers
        self.farm_name = self.wind['Site Name'] # wind farm names
        self.w_sites = len(self.farm_name) # number of wind sites
        if model in ['Nodal', 'Copper Sheet']:
            self.zone_no = self.wind['Bus No.'].values # zone number for wind farms
        else:
            self.zone_no = self.wind['Zone'].values
        self.wcap = self.wind['MW_Capacity'].values # MW capacity of wind farms
        self.turbine_rating = self.wind['Turbine Rating'].values
        self.w_turbines = np.ceil(self.wcap/self.turbine_rating).astype(int) # no. of wind turbines
        self.p_class = self.wind['Power Class'].values
        
        self.pcurve = pd.read_csv(pcurve_data) # read file for wind power curve data
        self.start_speed = self.pcurve['Start (m/s)'].values # start speeds for each wind class
        self.end_speed = self.pcurve['End (m/s)'].values # end speed for each wind class
        self.w_classes = len(self.start_speed) # no. of wind classes
        self.out_curve2 = self.pcurve['Class 2'].values # output curve for power class 2 sites 
        self.out_curve3 = self.pcurve['Class 3'].values # output curve for power class 3 sites        

        return(self.w_sites, self.farm_name, self.zone_no, self.w_classes, self.w_turbines, \
               self.turbine_rating, self.p_class, self.out_curve2, self.out_curve3, self.start_speed)

    def CalWindTrRates(self, directory, windspeed_data, site_data, pcurve_data):
        """
        Calculates transition rate matrices for the wind farms using wind speed data downloaded from the wind toolkit.

        Parameters:
            directory (str): Directory to save the transition rates.
            windspeed_data (str): Path to the CSV file containing wind speed data.
            site_data (str): Path to the CSV file containing site data.
            pcurve_data (str): Path to the CSV file containing power curve data.

        Returns:
            numpy.ndarray: Transition rate matrices.
        """
        wind = pd.read_csv(site_data) # read file for wind farm data
        bus_no = wind['Bus No.'].values # wind farm numbers
        w_sites = len(bus_no) # number of wind sites

        pcurve = pd.read_csv(pcurve_data) # read file for wind power curve data
        start_speed = pcurve['Start (m/s)'].values # start speeds for each wind class
        w_classes = len(start_speed) # no. of wind classes

        speed_bins = start_speed
        wdata_df = pd.read_csv(windspeed_data, index_col=0)

        wdata = {col: wdata_df[col].to_numpy() for col in wdata_df.columns}
        keys = list(wdata.keys())
        data_len = len(next(iter(wdata.values())))

        speedbin_values = {key: np.zeros(data_len).astype(int) for key in keys}

        for key in wdata:
            for i in range(data_len):
                for j in range(len(speed_bins) - 1):
                    if speed_bins[j] <= wdata[key][i] < speed_bins[j + 1]:
                        speedbin_values[key][i] = j
                        break

        rate_matrix = np.zeros((w_sites, w_classes, w_classes))
        s_temp = 0
        for key in wdata:
            for i in range(data_len - 1):
                j = speedbin_values[key][i]
                k = speedbin_values[key][i + 1]
                rate_matrix[s_temp, j, k] += 1
            s_temp += 1

        for s in range(w_sites):
            for r in range(w_classes):
                rate_matrix[s, r] = rate_matrix[s, r]/sum(rate_matrix[s, r])

        rate_matrix = np.nan_to_num(rate_matrix)

        #-------------for storing transition rates in an excel file----------------
        k_temp = 0
        with pd.ExcelWriter(f'{directory}/t_rate.xlsx') as writer:
            for idx, array in enumerate(rate_matrix, start=1):
                sheet_name = keys[k_temp]
                df = pd.DataFrame(array)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                k_temp += 1    
        
        return(rate_matrix)
