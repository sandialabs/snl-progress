import cdsapi
import pandas as pd
import numpy as np
from pathlib import Path
import yaml
import zipfile
import os
import glob
import pvlib
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
import pvlib.modelchain as mc
from timezonefinder import TimezoneFinder
import logging

logger = logging.getLogger(__name__)

class Solar:
    """
    A class to handle solar data: download weather data from ERA5 database, calculate solar generation using PVLib,
    and processing the data for Monte Carlo Simulation (MCS).
    """

    def __init__(self, solar_directory, model):
        """
        Initializes the Solar class with directory.

        Parameters:
            directory (str): Directory to save the data.
        """
        self.solar_directory = solar_directory
        self.solar_site_data = solar_directory + "/solar_sites.csv"
        self.sites_df = pd.read_csv(self.solar_site_data)
        self.model = model

        self.names = self.sites_df["Site Name"]
        self.n_sites = len(self.sites_df)
        if model in ['Nodal', 'Copper Sheet']:
            self.s_zone_no = self.sites_df['Bus No.']
        else:
            self.s_zone_no = self.sites_df['Zone']
        self.MW = self.sites_df["MW_Capacity"]

        # directory for storing downloaded data
        self.weather_data_directory = Path(solar_directory + "/solar_weather_data")
        self.weather_data_directory.mkdir(exist_ok=True)

        # directory for storing solar power generation data
        self.gen_data_directory = Path(solar_directory + "/solar_gen_data")
        self.gen_data_directory.mkdir(exist_ok=True)

        pass

    def download_solar_data(self, start_year, end_year, progress_callback=None):

        if not {"Latitude", "Longitude"}.issubset(self.sites_df.columns):
            raise ValueError("CSV must contain 'Latitude and 'Longitude' columns")

        # --- DATA DESCRIPTION FOR ERA5 ---
        dataset = "reanalysis-era5-single-levels-timeseries"
        base_request = {
            "variable": [
                "surface_solar_radiation_downwards",
                "2m_temperature",
                "10m_u_component_of_wind",
                "10m_v_component_of_wind",
            ],
            "date": [f"{start_year}-01-01/{end_year}-12-31"],
            "data_format": "csv"
        }

        client = cdsapi.Client()

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

            if progress_callback:
                progress_callback()

    def process_solar_data(self, file_path, site):
        df_weather = pd.read_csv(file_path)

        # change time zone
        tf = TimezoneFinder()
        tz = tf.timezone_at(lat=site.Latitude, lng=site.Longitude)

        # parse time
        df_weather['valid_time'] = pd.to_datetime(df_weather['valid_time'], utc=True)
        df_weather['valid_time'] = df_weather['valid_time'].dt.tz_convert(tz)
        df_weather = df_weather.set_index('valid_time').rename_axis('time')

        # convert variables
        df_weather['temp_air'] = df_weather['t2m'] - 273.15
        df_weather['wind_speed'] = np.sqrt(df_weather['u10']**2 + df_weather['v10']**2)
        df_weather['ghi'] = df_weather['ssrd'] / 3600.0
        df_weather = df_weather[['temp_air', 'wind_speed', 'ghi']]

        return df_weather, tz

    def add_irradiance_components(self, df_weather, lat, lon):
        # --- solar position ---
        solpos = pvlib.solarposition.get_solarposition(
            time=df_weather.index,
            latitude=lat,
            longitude=lon
        )

        # --- calculate DNI and DHI ---
        dni_dhi = pvlib.irradiance.erbs(
            ghi=df_weather['ghi'],
            zenith=solpos['zenith'],
            datetime_or_doy=df_weather.index,
        )

        # add indices to weather dataframe
        df_weather['dni'] = dni_dhi['dni']
        df_weather['dhi'] = dni_dhi['dhi']

        return df_weather
    
    def run_pv_model(self, df_weather, site, site_id, tz):
    
        ac = 1; dc = ac*1.3; tilt = site.Latitude

        location = Location(site.Latitude, site.Longitude, tz = tz)
        system = PVSystem(
        surface_tilt=tilt,
        surface_azimuth=180,
        module_parameters={'pdc0': dc, 'gamma_pdc': -0.004},
        inverter_parameters={'pdc0': ac},
        temperature_model_parameters=pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']
        ['open_rack_glass_glass'])

        mchain = mc.ModelChain.with_pvwatts(system, location)

        # prep weather data for mchain
        weather_sat = df_weather[['dni','ghi','dhi','temp_air','wind_speed']].copy()
        weather_sat.columns = ['dni','ghi','dhi','temp_air','wind_speed']

        # run mchain model for satellite data
        mchain.run_model(weather_sat)
        ac_power_sat = pd.DataFrame(mchain.results.ac)*site.MW_Capacity
        ac_power_sat.to_csv(f'{self.gen_data_directory}/{site_id}_gen.csv')

    def combine_site_generation(self, file_pattern):
        """
        Combine multiple solar generation CSVs into one wide CSV.

        Parameters
        ----------
        input_folder : str or Path
            Folder containing site generation files.
        output_file : str
            Output CSV filename.
        file_pattern : str
            Pattern for matching generation files.

        Returns
        -------
        pd.DataFrame
            Combined dataframe.
        """

        input_folder = Path(self.gen_data_directory)

        all_site_series = []

        for file_path in sorted(input_folder.glob(file_pattern)):

            # Example: 101_PV_1_gen.csv -> 101_PV_1
            site_id = file_path.stem.replace("_gen", "")

            # Read file
            df = pd.read_csv(file_path)

            # Basic validation
            required_cols = {"time", "p_mp"}
            if not required_cols.issubset(df.columns):
                raise ValueError(
                    f"{file_path.name} missing required columns: {required_cols}"
                )

            # Parse time
            df["time"] = pd.to_datetime(df["time"])

            # Create series named by site_id
            site_series = (
                df.set_index("time")["p_mp"]
                .rename(site_id)
            )

            all_site_series.append(site_series)

        if not all_site_series:
            raise ValueError(f"No files found in {input_folder}")

        # Combine all sites on timestamp index
        combined_df = pd.concat(all_site_series, axis=1)

        # Optional: sort by time
        combined_df = combined_df.sort_index()

        # Save
        output_file = self.solar_directory + "/gen_all_sites.csv"
        combined_df.to_csv(output_file)

        logger.info(f"Saved combined data to: {output_file}")
        logger.info(f"Shape: {combined_df.shape}")

        return combined_df
    
    def GetSolarProfiles(self, solar_prob_data):
        '''
        This function extracts the solar data from clusters and modifies it for the MCS. The solar data is stored in a 4D ndarray where the dimensions are: [cluster, day, hour, site]. The clusters are created using the K-means clustering algorithm. Similar days of solar generation are put in the same cluster.

        Parameters:
            solar_prob_data (str): Path to the CSV file containing solar probability data.

        Returns:
            tuple: Number of sites, zone numbers, MW capacity, solar profiles, and solar probability.

        '''
        clusters = glob.glob(os.path.join(self.solar_directory + "/Clusters/", '*/'))
        n_clust = len(clusters) # no. of clusters created (depends on user and data)

        self.s_profiles = [] # this array will contain solar data for all clusters, sites, and days
        for i in range(1, n_clust + 1):
            self.cluster_list = []
            for site in self.names:
                matrix=pd.read_csv(self.solar_directory + "/Clusters/" + str(i) + "/"+site+".csv")
                self.cluster_list.append(matrix)
            self.s_profiles.append(np.stack(self.cluster_list,-1))

        self.solar_prob = pd.read_csv(solar_prob_data).values

        return(self.n_sites, self.s_zone_no, self.MW, self.s_profiles, self.solar_prob)

    def run_pipeline(self, start_year, end_year):

        # download solar data
        self.download_solar_data(start_year, end_year)

        all_files = sorted(Path(self.weather_data_directory).glob('*.csv'))

        for file in all_files:

            logger.info(f"Processing {file.name}")
            
            # Extract site_id from filename
            site_id = file.stem
            site_row = self.sites_df[self.sites_df['Site Name'] == site_id]
            site = site_row.iloc[0]

            # convert observations into required indices
            df, tz = self.process_solar_data(file, site)

            # add irradiance components 
            df = self.add_irradiance_components(df, site.Latitude, site.Longitude)

            # run PV model
            self.run_pv_model(df, site, site_id, tz)

        # combine all generation data
        self.combine_site_generation(file_pattern="*_gen.csv")

if __name__ == "__main__":

    # --- CONFIG ---
    input_file = 'input.yaml'
    with open(input_file, 'r') as f:
        config = yaml.safe_load(f)

    # --- INPUTS ---
    solar_directory = config['data']+"/Solar"
    start_year = config['year_start_s']
    end_year = config['year_end_s']
    model = config['model']

    # create instance and run
    solar = Solar(solar_directory, model)
    solar.run_pipeline(start_year, end_year)


