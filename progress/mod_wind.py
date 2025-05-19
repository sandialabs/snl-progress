import numpy as np
import pandas as pd
import requests
import os
from rex import WindResource as WR

class Wind:

    """
    Handles downloading, assembling, and analyzing wind data from the NREL Wind Toolkit for 
    resource adequacy or other power system studies.

    This class provides methods to:

    1. **DownloadWindData**: Fetch and parse wind speed data (at specified heights) 
       from NREL's Wind Toolkit for each wind site/year.
    2. **WindFarmsData**: Read and organize farm-level metadata (capacity, turbine rating, etc.) 
       along with power curve information.
    3. **CalWindTrRates**: Compute transition rate matrices for wind speed classes based on 
       time series data, useful in Markov chain-based reliability or adequacy models.
    """
    def DownloadWindData(self, directory, site_data, api_key, email, affiliation, year_start, year_end):
        """
        Downloads wind speed data from the NREL Wind Toolkit for the given sites and years, 
        then consolidates it into a single CSV file.

        **Process Summary**:
          1. Reads site metadata (longitude, latitude, hub height) from the specified CSV.
          2. Iterates through each site and year to request wind speed data at 80m and 100m heights 
             from the NREL API.
          3. Applies power-law interpolation if a site's hub height differs from 80m and 100m.
          4. Merges all sites (for each year) into a single DataFrame, adjusting timestamps, and 
             finally writes a combined CSV of wind speeds at each site.

        :param directory: Directory where downloaded data and final merged CSV will be saved.
        :type directory: str
        :param site_data: Path to the CSV file containing site metadata (Farm Name, Longitude, Latitude, Hub Height, etc.).
        :type site_data: str
        :param api_key: Your personal API key for accessing the NREL Wind Toolkit.
        :type api_key: str
        :param email: Your email address (required by the NREL API).
        :type email: str
        :param affiliation: Your organization or affiliation (required by the NREL API).
        :type affiliation: str
        :param year_start: The first (earliest) year of data to download.
        :type year_start: int
        :param year_end: The last (latest) year of data to download.
        :type year_end: int

        :return:
            None

        :rtype: None

        :raises FileNotFoundError: If the site CSV file is missing or unreachable.
        :raises requests.exceptions.RequestException: For network or API-related failures during data download.
        """

        year_list = range(year_start, year_end + 1)
        wind_site_df = pd.read_csv(site_data)
        site_count = len(wind_site_df)
        name_list = wind_site_df["Farm Name"].tolist()
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

    def WindFarmsData(self, site_data, pcurve_data):
        """
        Reads and organizes wind farm metadata and power curve data to facilitate 
        wind power output calculations in subsequent modeling.

        **Process Summary**:
          1. Reads the wind farm CSV to extract site/farm identifiers, zone numbers, 
             and capacities (MW).
          2. Computes the number of turbines per farm based on rated capacity and turbine rating.
          3. Reads the power curve CSV to identify wind speed class thresholds 
             and power output curves for Classes 2 and 3.

        :param site_data: Path to the CSV containing wind farm data (Farm No., Farm Name, Zone No., Max Cap, Turbine Rating, etc.).
        :type site_data: str
        :param pcurve_data: Path to the CSV containing power curve data (Start/End speeds, Class 2 curve, Class 3 curve, etc.).
        :type pcurve_data: str

        :return:
            A 10-element tuple containing:

            * **w_sites** (*int*): Number of wind farm sites.
            * **farm_name** (*pd.Series*): Names of each wind farm.
            * **zone_no** (*np.ndarray*): Zone indices corresponding to each wind farm.
            * **w_classes** (*int*): Number of discrete wind speed classes.
            * **w_turbines** (*np.ndarray*): Number of turbines at each site.
            * **turbine_rating** (*np.ndarray*): Rated power (MW) of each turbine.
            * **p_class** (*np.ndarray*): Array indicating which power curve class (2 or 3) each site uses.
            * **out_curve2** (*np.ndarray*): Power output curve for Class 2 turbines (indexed by wind speed class).
            * **out_curve3** (*np.ndarray*): Power output curve for Class 3 turbines (indexed by wind speed class).
            * **start_speed** (*np.ndarray*): Lower bounds of wind speed classes (m/s).

        :rtype: tuple

        :raises FileNotFoundError: If either CSV (site_data or pcurve_data) is not found.
        :raises pd.errors.EmptyDataError: If either CSV file is empty or cannot be parsed.
        """
        self.wind = pd.read_csv(site_data) # read file for wind farm data
        self.farm_no = self.wind['Farm No.'].values # wind farm numbers
        self.farm_name = self.wind['Farm Name'] # wind farm names
        self.w_sites = len(self.farm_no) # number of wind sites
        self.zone_no = self.wind['Zone No.'].values # zone number for wind farms
        self.wcap = self.wind['Max Cap'].values # MW capacity of wind farms
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
        Computes and stores transition rate matrices for wind speed classes 
        using Markov chain assumptions. Each site's wind speed time series 
        is discretized into classes, and a transition probability matrix 
        is computed.

        **Process Summary**:
          1. Reads wind speed data from the merged CSV created by :meth:`DownloadWindData`.
          2. Bins wind speed observations into classes based on the start speeds 
             defined in the power curve CSV.
          3. Increments counts for transitions between consecutive hours 
             (e.g., from class j to class k).
          4. Converts transition counts to probabilities and writes each site's 
             transition matrix to an Excel file.

        :param directory: Directory to save the resulting transition rate Excel file.
        :type directory: str
        :param windspeed_data: Path to the CSV file containing wind speed time series 
                               for all sites (output of :meth:`DownloadWindData`).
        :type windspeed_data: str
        :param site_data: Path to the CSV containing wind farm data 
                          (Farm No., Farm Name, etc.).
        :type site_data: str
        :param pcurve_data: Path to the CSV containing power curve data (defining wind speed classes).
        :type pcurve_data: str

        :return:
            A 3D NumPy array of shape ``(sites, classes, classes)`` representing 
            transition probability matrices for each site. Each [i, j, k] 
            entry is the probability of moving from class j to class k at site i.

        :rtype: np.ndarray

        :raises FileNotFoundError: If any of the CSV files (windspeed_data, site_data, pcurve_data) are missing.
        :raises pd.errors.EmptyDataError: If any CSV is empty or cannot be parsed.
        """
        wind = pd.read_csv(site_data) # read file for wind farm data
        farm_no = wind['Farm No.'].values # wind farm numbers
        w_sites = len(farm_no) # number of wind sites

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
