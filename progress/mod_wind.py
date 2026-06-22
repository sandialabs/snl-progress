import numpy as np
import pandas as pd
import requests
import os
from rex import WindResource as WR
import yaml
from pathlib import Path
import cdsapi
import zipfile
import logging

logger = logging.getLogger(__name__)

class Wind:

    '''This class contains the methods required for downloading and processing wind data.'''

    def __init__(self, wind_directory):

        self.wind_directory = wind_directory
        
        # directory for storing downloaded weather data
        self.weather_data_directory = Path(wind_directory + "/wind_weather_data")
        self.weather_data_directory.mkdir(exist_ok=True)

        # get wind sites data
        self.wind_site_data = wind_directory + "/wind_sites.csv"
        self.sites_df = pd.read_csv(self.wind_site_data)

    def DownloadWindData(self, start_year, end_year):

        if not {"Latitude", "Longitude"}.issubset(self.sites_df.columns):
            raise ValueError("CSV must contain 'Latitude and 'Longitude' columns")

        # --- DATA DESCRIPTION FOR ERA5 ---
        dataset = "reanalysis-era5-single-levels-timeseries"
        base_request = {
            "variable": [
                "100m_u_component_of_wind",
                "100m_v_component_of_wind",
            ],
            "date": [f"{start_year}-01-01/{end_year}-12-31"],
            "data_format": "csv"
        }

        client = cdsapi.Client(
            timeout=60,
            retry_max=2,
            sleep_max=10
        )

        # --- DOWNLOAD LOOP ---
        for idx, row in self.sites_df.iterrows():

            lat = float(row["Latitude"])
            lon = float(row["Longitude"])
            name = row["Site Name"]

            request = base_request.copy()
            request["location"] = {"longitude": lon, "latitude": lat}

            logger.info(f"Downloading {name} (lat={lat}, lon={lon})...")

            result = client.retrieve(dataset, request)
            zip_path = Path(result.download())

            final_csv_path = self.weather_data_directory / f"{name}.csv"

            # --- EXTRACT FROM DOWNLOADED ZIP ---
            with zipfile.ZipFile(zip_path, 'r') as z:
                csv_files = [f for f in z.namelist() if f.endswith(".csv")]

                if not csv_files:
                    raise RuntimeError(f"No CSV found in ZIP for {name}")

                extracted_name = csv_files[0]
                z.extract(extracted_name, self.weather_data_directory)

                extracted_path = self.weather_data_directory / extracted_name

                os.replace(extracted_path, final_csv_path) # rename csv file for convenience

            # --- CLEANUP ---
            zip_path.unlink()

        
        # ======================================================
        # consolidate all wind speed data into a single csv file
        # ======================================================
        site_dfs = []

        for file in sorted(self.weather_data_directory.glob("*.csv")):

            logger.info(f"Processing {file.name}")

            df = pd.read_csv(file)

            required_cols = ["valid_time", "u100", "v100"]

            missing = [c for c in required_cols if c not in df.columns]
            if missing:
                raise ValueError(
                    f"{file.name} is missing columns: {missing}"
                )

            windspeed = np.sqrt(
                df["u100"].astype(float) ** 2 +
                df["v100"].astype(float) ** 2
            )

            site_name = file.stem

            site_df = pd.DataFrame({
                "datetime": pd.to_datetime(df["valid_time"]),
                site_name: windspeed
            })

            site_dfs.append(site_df)

        # Merge all sites
        windspeed_df = site_dfs[0]

        for site_df in site_dfs[1:]:
            windspeed_df = windspeed_df.merge(
                site_df,
                on="datetime",
                how="outer"
            )

        windspeed_df = windspeed_df.sort_values("datetime")

        # Remove duplicate timestamps if any exist
        windspeed_df = windspeed_df.drop_duplicates(
            subset="datetime",
            keep="first"
        )

        windspeed_df.to_csv(f"{self.wind_directory}/windspeed_data.csv", index=False)
        logger.info("FINISHED DOWNLOADING WIND DATA")


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

    def CalWindTrRates(self, directory, windspeed_data, pcurve_data):
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
        wind = pd.read_csv(self.wind_site_data) # read file for wind farm data
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
        
        logger.info("Completed processing wind data and returning transition rate matrices")
        return(rate_matrix)

# if __name__ == "__main__":

#     # --- CONFIG ---
#     input_file = 'input.yaml'
#     with open(input_file, 'r') as f:
#         config = yaml.safe_load(f)

#     # --- INPUTS ---
#     wind_directory = config['data']+"/Wind"
#     start_year = config['year_start_w']
#     end_year = config['year_end_w']

#     wind = Wind(wind_directory)

#     wind.DownloadWindData(start_year, end_year)
