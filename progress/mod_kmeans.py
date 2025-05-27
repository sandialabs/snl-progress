"""
KMeans_Pipeline Package
=======================

This package provides the `KMeans_Pipeline` class to perform KMeans clustering on solar generation data.
The package includes functionality for preprocessing, data transformation, clustering, and evaluation.

Class:
    KMeans_Pipeline: A pipeline class for running KMeans clustering on solar generation data.

Attributes:
    directory (str): Path to the directory containing the solar data files.
    site_data (str): Path to the CSV file containing site information.

Example Usage:
--------------
This example demonstrates how to use the `KMeans_Pipeline` class to perform KMeans clustering on solar generation data.
It performs the following steps:
1. Initializes the pipeline with the `solar_data.xlsx` file and a list of selected sites.
2. Calculates the cluster probabilities using the `calculate_cluster_probability` method.
3. Splits and clusters the data based on the generated labels using the `split_and_cluster_data` method.
4. Outputs metrics of the clustering to a text file using the `test_metrics` method.

Note: Ensure the data file `solar_data.xlsx` exists in the same directory as the script, or provide an absolute path to it.

.. code-block:: python

    if __name__ == "__main__":

        # Define the list of selected sites for analysis
        directory = r'/Users/abera/Documents/My_Projects/QuESt_Reliability/QuESt_Reliability_App/Data/Solar'
        site_data = directory + '/solar_sites.csv'

        # Initialize the KMeans_Pipeline class
        pipeline = KMeans_Pipeline(directory, site_data)

        # Generate and save the clustering metrics to a text file
        pipeline.test_metrics(clust_eval = 4)

        # Uncomment the following lines to run additional steps
        # pipeline.run(n_clusters = 5)
        # pipeline.calculate_cluster_probability()
        # pipeline.split_and_cluster_data()

"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA  #used for dimensionality reduction, not sure if needed or desired for this project
from sklearn.metrics import silhouette_score #used for evaluating the efficacy of the clustering
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from kneed import KneeLocator

class KMeans_Pipeline:
    """
    A pipeline class for running KMeans clustering on solar generation data.
    It performs preprocessing, data transformation, and finally clusters the data.

    Attributes:
        excel_file_path (str): Path to the Excel file containing the Solar Generation, Site Information, and CSI data.
        solar_gen_df (pd.DataFrame): DataFrame containing Solar Generation data.
        site_info_df (pd.DataFrame): DataFrame containing Site Information.
        csi_df (pd.DataFrame): DataFrame containing Clear Sky Index (CSI) data.
        selected_sites (list): List of site names to be included in the analysis.
        first_light (pd.DataFrame): DataFrame containing first light timings.
        last_light (pd.DataFrame): DataFrame containing last light timings.
        sg_mean_am (pd.DataFrame): AM Solar generation mean values.
        sg_mean_pm (pd.DataFrame): PM Solar generation mean values.
        csi_sd_am (pd.DataFrame): AM Cloud Sky Irradiance standard deviation values.
        csi_sd_pm (pd.DataFrame): PM Cloud Sky Irradiance standard deviation values.
        kmeans_df (pd.DataFrame): DataFrame prepared for KMeans clustering.
        predicted_labels (array): Cluster labels for each data point.
        silhouette (float): Silhouette score of the clustering.
    """
    def update_progress(self, process, progress):
            bar_length = 50  # Length of the progress bar
            block = int(round(bar_length * progress))
            text = "\r{}: [{}] {:.0f}% Complete.".format(process, "#" * block + "-" * (bar_length - block), progress * 100)
            print(text, end='', flush=True)


    def __init__(self, directory, site_data, **kwargs):
        """
        Initializes the KMeans_Pipeline with an Excel file containing solar generation data,
        site information, and CSI data. Preprocesses and prepares the data for clustering.

        Parameters:
            directory (str): Path to the directory.
            site_data (str): Path to the CSV file.
            **kwargs (dict): Optional arguments that the function takes.
        """
        self.directory = directory
        self.excel_file_path = f'{self.directory}/solar_data.xlsx'

        # Read the data from different sheets in the Excel file
        self.solar_gen_df = pd.read_excel(self.excel_file_path, sheet_name='solar_gen')
        self.csi_df = pd.read_excel(self.excel_file_path, sheet_name='csi')
        self.site_info_df = pd.read_csv(site_data)

        # Select sites based on optional argument or use all sites
        if 'selected_sites' in kwargs:
            self.selected_sites = kwargs['selected_sites']
        else:
            self.selected_sites = self.site_info_df['site_name'].tolist()


        self.first_light, self.last_light = self.process_flh_and_llh(self.solar_gen_df, self.selected_sites)
        self.sg_mean_am, self.sg_mean_pm = self.process_solar_data(self.solar_gen_df, self.site_info_df, self.selected_sites)
        self.csi_sd_am, self.csi_sd_pm = self.process_csi_data(self.csi_df, self.selected_sites)
        self.kmeans_df = self.create_kmeans_df(self.sg_mean_am, self.sg_mean_pm, self.csi_sd_am, self.csi_sd_pm, self.first_light, self.last_light)

    def process_flh_and_llh(self, solar_gen_df, selected_sites):
        """
        Processes first and last light hours from solar generation data.

        This function performs the following:
        - Identifies the first and last light hours for each day based on solar generation data.
        - Encodes these hours as cyclic features.

        Parameters:
            solar_gen_df (DataFrame): DataFrame containing the solar generation data.
                The DataFrame should have a 'datetime' column and columns for each site's solar generation.
            selected_sites (list): List of site columns to include from solar_gen_df.

        Returns:
            tuple: Two DataFrames representing first and last light hours, respectively,
                   with cyclic features encoded.

        Internal Functions:
            - get_first_non_zero(series): Returns the first non-zero hour in a time series.
            - get_last_non_zero(series): Returns the last non-zero hour in a time series.
            - encode_cyclic_features(df): Encodes specified features as cyclic.
        """
        # Function to get the first non-zero value in a time series
        def get_first_non_zero(series):
            for idx, val in series.items():
                if val != 0:
                    return idx.hour  # Return the hour of the first non-zero value
            return None  # Return None if all values are zero

        # Function to get the last non-zero value in a time series
        def get_last_non_zero(series):
            for idx, val in series[::-1].items():  # Reverse the series
                if val != 0:
                    return idx.hour  # Return the hour of the last non-zero value
            return None  # Return None if all values are zero

        # Function to encode cyclic features like time
        def encode_cyclic_features(df):
            # Select columns that are not 'col_to_exclude'
            cyclic_features = [col for col in df.columns if col != 'col_to_exclude']

            for col in cyclic_features:
                max_val = df[col].max()  # Find the maximum value for the column
                # Create sine and cosine features
                df[col + '_sin'] = np.sin(2 * np.pi * df[col] / max_val)
                df[col + '_cos'] = np.cos(2 * np.pi * df[col] / max_val)
                df = df.drop(columns=[col])  # Drop the original column

            return df  # Return the dataframe with cyclic features

        # Read the solar generation data from a CSV file
        sg_df = solar_gen_df
        self.update_progress("Processing FLH and LLH", 1/7)

        sg_df = sg_df[['datetime'] + selected_sites]  # Keep only the selected columns
        sg_df['datetime'] = pd.to_datetime(sg_df['datetime'])  # Convert 'datetime' to a datetime object
        sg_df.set_index('datetime', inplace=True)  # Set 'datetime' as the index
        self.update_progress("Processing FLH and LLH", 2/7)

        # Resample data in groups of 24
        sg_by_day = sg_df.resample('D')
        self.update_progress("Processing FLH and LLH", 3/7)

        # Apply the functions to find the first and last non-zero value for each day
        first_light = sg_by_day.apply(get_first_non_zero)
        last_light = sg_by_day.apply(get_last_non_zero)
        self.update_progress("Processing FLH and LLH", 4/7)

        # Encode cyclic features for first_light and last_light
        first_light = encode_cyclic_features(first_light)
        last_light = encode_cyclic_features(last_light)
        self.update_progress("Processing FLH and LLH", 5/7)

        # Add a date column and reset the index for first_light
        first_light['date'] = first_light.index.date
        first_light = first_light.reset_index(drop=True)
        first_light = first_light.set_index('date').reset_index()
        self.update_progress("Processing FLH and LLH", 6/7)

        # Add a date column and reset the index for last_light
        last_light['date'] = last_light.index.date
        last_light = last_light.reset_index(drop=True)
        last_light = last_light.set_index('date').reset_index()
        self.update_progress("Processing FLH and LLH", 7/7)
        print("\n")

        # Return the two DataFrames
        return first_light, last_light

    def process_solar_data(self, solar_gen_df, site_info_df, selected_sites):
        """
        Processes solar generation data to obtain mean AM and PM values.

        This function performs several operations:
        - Filters the data for selected sites.
        - Normalizes solar generation data by the wattage limit for each site.
        - Calculates the mean solar generation for AM and PM slots.

        Parameters:
            solar_gen_df (DataFrame): DataFrame containing the solar generation data.
                The DataFrame should have a 'datetime' column and columns for each site's solar generation.
            site_info_df (DataFrame): DataFrame containing information about the sites,
                including 'site_name' and 'MW' (megawatt capacity).
            selected_sites (list): List of site names to include in the processing.

        Returns:
            tuple: Two DataFrames representing mean AM and mean PM values, respectively.

        """
        # Load data
        sg_df = solar_gen_df
        site_df = site_info_df
        self.update_progress("Processing Solar Data", 1/9)

        # Filter columns based on selected sites
        sg_df = sg_df[['datetime'] + selected_sites]
        self.update_progress("Processing Solar Data", 2/9)

        # Filter rows in site_df based on selected sites
        site_df = site_df[site_df['site_name'].isin(selected_sites)].reset_index(drop=True)
        self.update_progress("Processing Solar Data", 3/9)

        # Convert datetime to date
        sg_df['datetime'] = pd.to_datetime(sg_df['datetime'])
        sg_df['date'] = sg_df['datetime'].dt.date
        sg_df = sg_df.set_index('date').reset_index()
        sg_df = sg_df.drop('datetime', axis=1)
        self.update_progress("Processing Solar Data", 4/9)

        # Create group_id for AM/PM grouping
        sg_df['group_id'] = np.arange(len(sg_df)) // 12
        self.update_progress("Processing Solar Data", 5/9)

        # Get the site wattage for the selected sites
        site_wattage = site_df[site_df['site_name'].isin(selected_sites)][['site_name', 'MW']]
        self.update_progress("Processing Solar Data", 6/9)

        # Normalize by wattage limit
        for index, row in site_wattage.iterrows():
            site_name = row['site_name']
            wattage_limit = row['MW']
            sg_df[site_name] = sg_df[site_name] / wattage_limit
            self.update_progress("Processing Solar Data", 7/9)

        # Calculate mean and preserve date
        sg_df_mean = sg_df.drop(columns=['date']).groupby('group_id').mean()
        dates_sg = sg_df.groupby('group_id')['date'].first()
        sg_df_mean['date'] = dates_sg
        sg_df_mean = sg_df_mean.set_index('date').reset_index()
        self.update_progress("Processing Solar Data", 8/9)

        # Split into AM and PM
        sg_mean_am = sg_df_mean[sg_df_mean.index % 2 == 0].reset_index(drop=True)
        sg_mean_pm = sg_df_mean[sg_df_mean.index % 2 != 0].reset_index(drop=True)
        self.update_progress("Processing Solar Data", 9/9)
        print("\n")

        return sg_mean_am, sg_mean_pm

    def process_csi_data(self, csi_info, selected_sites):
        """
        Processes cloud-to-sun irradiance data to get standard deviation for AM and PM periods.

        This function performs several operations:
        - Filters the data for selected sites.
        - Scales the data using standardization.
        - Calculates the standard deviation for AM and PM slots.

        Parameters:
            csi_info (DataFrame): DataFrame containing the cloud-to-sun irradiance data.
                The DataFrame should have a 'datetime' column and columns for each site's irradiance.
            selected_sites (list): List of site names to include in the processing.

        Returns:
            tuple: Two DataFrames representing the standard deviation for AM and PM values, respectively.

        """
        # Load the data into a pandas dataframe
        csi_df = csi_info
        self.update_progress("Processing CSI Data", 1/9)

        # Filter columns based on selected sites
        csi_df = csi_df[['datetime'] + selected_sites]
        self.update_progress("Processing CSI Data", 2/9)

        # Convert the datetime column into just date without time
        csi_df['datetime'] = pd.to_datetime(csi_df['datetime'])
        csi_df['date'] = csi_df['datetime'].dt.date
        csi_df = csi_df.drop('datetime', axis=1).set_index('date').reset_index()
        self.update_progress("Processing CSI Data", 3/9)

        # Create a group id that will be used to group into am/pm for each date
        csi_df['group_id'] = np.arange(len(csi_df)) // 12
        self.update_progress("Processing CSI Data", 4/9)

        # Store the dates that will be reapplied to the new dataframe
        dates_csi = csi_df.groupby('group_id')['date'].first()
        self.update_progress("Processing CSI Data", 5/9)

        # Get the standard deviation of each group of 12 (am/pm)
        csi_df_std = csi_df.drop(columns=['date']).groupby('group_id').std()
        self.update_progress("Processing CSI Data", 6/9)

        # Scale the data to have a variance of 1 and mean of 0
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(csi_df_std)
        csi_sd_df = pd.DataFrame(scaled_data, columns=csi_df_std.columns)
        self.update_progress("Processing CSI Data", 7/9)

        # Add the dates back to the data frame after processing
        csi_sd_df['date'] = dates_csi
        csi_sd_df = csi_sd_df.set_index('date').reset_index()
        self.update_progress("Processing CSI Data", 8/9)

        # Split the data into am and pm
        csi_sd_am = csi_sd_df[csi_sd_df.index % 2 == 0].reset_index(drop=True)
        csi_sd_pm = csi_sd_df[csi_sd_df.index % 2 != 0].reset_index(drop=True)
        self.update_progress("Processing CSI Data", 9/9)
        print("\n")

        return csi_sd_am, csi_sd_pm

    def create_kmeans_df(self, sg_mean_am, sg_mean_pm, csi_sd_am, csi_sd_pm, first_light, last_light):
        """
        Combines various DataFrames to form a DataFrame ready for K-means clustering.

        This function performs several operations:
        - Sets the index to 'date' for all input DataFrames.
        - Adds appropriate suffixes to each DataFrame to maintain data context.
        - Concatenates all DataFrames along the columns.
        - Sorts the resulting DataFrame by the column names.

        Parameters:
            sg_mean_am (DataFrame): DataFrame containing mean AM solar generation data.
            sg_mean_pm (DataFrame): DataFrame containing mean PM solar generation data.
            csi_sd_am (DataFrame): DataFrame containing standard deviation of AM cloud-to-sun irradiance data.
            csi_sd_pm (DataFrame): DataFrame containing standard deviation of PM cloud-to-sun irradiance data.
            first_light (DataFrame): DataFrame containing the first light hours for each day.
            last_light (DataFrame): DataFrame containing the last light hours for each day.

        Returns:
            DataFrame: A DataFrame that combines all input DataFrames, ready for K-means clustering.

        """
        # Set the index for each dataframe
        sg_mean_am.set_index('date', inplace=True)
        sg_mean_pm.set_index('date', inplace=True)
        csi_sd_am.set_index('date', inplace=True)
        csi_sd_pm.set_index('date', inplace=True)
        first_light.set_index('date', inplace=True)
        last_light.set_index('date', inplace=True)
        self.update_progress("Creating Tables", 1/4)

        # Add suffixes to each set
        sg_mean_am = sg_mean_am.add_suffix('_sg_mean_am')
        sg_mean_pm = sg_mean_pm.add_suffix('_sg_mean_pm')
        csi_sd_am = csi_sd_am.add_suffix('_csi_sd_am')
        csi_sd_pm = csi_sd_pm.add_suffix('_csi_sd_pm')
        first_light = first_light.add_suffix('_first_light')
        last_light = last_light.add_suffix('_last_light')
        self.update_progress("Creating Tables", 2/4)

        # Concatenate the dataframes along columns
        kmeans_df = pd.concat([sg_mean_am, sg_mean_pm, csi_sd_am, csi_sd_pm, first_light, last_light], axis=1)
        self.update_progress("Creating Tables", 3/4)

        # Sort the columns
        kmeans_df = kmeans_df.sort_index(axis=1)
        self.update_progress("Creating Tables", 4/4)
        print("\n")

        return kmeans_df

    def run(self, **kwargs):
       self.predicted_labels = self.run_kmeans_pipeline(self.kmeans_df, **kwargs)

    def run_kmeans_pipeline(self, kmeans_df, **kwargs):
        """
        Executes the K-means clustering pipeline on the input DataFrame.

        The function performs the following steps:
        1. Resets the DataFrame index.
        2. Converts 'date' to 'month' and creates cyclical features for it.
        3. Scales features and applies PCA via a preprocessing pipeline.
        4. Executes K-means clustering.
        5. Combines preprocessing and clustering into one pipeline.
        6. Fits the pipeline to the data.
        7. Computes the silhouette score to evaluate clustering quality.

        Parameters:
            kmeans_df (DataFrame): The DataFrame to cluster.
            **kwargs: Additional keyword arguments to configure K-means clustering,
                      such as 'n_clusters' to specify the number of clusters (default is 11).

        Returns:
            tuple: Contains the following elements:
                - Clustered DataFrame with a new 'cluster' column.
                - Predicted cluster labels.
                - The fitted pipeline object.
                - Silhouette score for the clustering.

        """
        n_clusters = kwargs.get('n_clusters', 11)  # Default value is 11

        #reset index
        kmeans_df.reset_index(inplace=True)
        self.update_progress("Running Pipeline", 1/13)

        #removes the date and leaves the month. Kmeans doesnt handle dates because it is distance based.
        kmeans_df['date'] = pd.to_datetime(kmeans_df['date'])
        kmeans_df['month'] = kmeans_df['date'].dt.month
        kmeans_df = kmeans_df.drop('date',axis=1)
        self.update_progress("Running Pipeline", 2/13)

        #scale month by turning it into a two dimensional cyclical attribute that is unitary
        kmeans_df['month_sin'] = np.sin(2* np.pi * kmeans_df['month']/12)
        kmeans_df['month_cos'] = np.cos(2* np.pi * kmeans_df['month']/12)
        self.update_progress("Running Pipeline", 3/13)

        #drop month and keep the 2d feature
        kmeans_df = kmeans_df.drop('month', axis=1)
        self.update_progress("Running Pipeline", 4/13)
        kmeans_df.fillna(0, inplace=True)
        self.update_progress("Running Pipeline", 5/13)


        # Create the preprocessor pipeline
        preprocessor = Pipeline(
            [
                ("scaler", MinMaxScaler()),
                ("pca", PCA(n_components=2)),
            ]
        )
        self.update_progress("Running Pipeline", 6/13)

        # Create the K-means clustering pipeline
        cluster = Pipeline(
            [
                ("kmeans", KMeans(n_clusters=n_clusters,
                                    init='k-means++',
                                    n_init=100,
                                    max_iter=1500,
                                    random_state=42
                                    )
                    ),
            ]
        )
        self.update_progress("Running Pipeline", 7/13)

        # Combine both pipelines
        pipe = Pipeline(
            [
                ("preprocessor", preprocessor),
                ("cluster", cluster),
            ]
        )
        self.update_progress("Running Pipeline", 8/13)

        # Fit the pipeline on the data
        pipe.fit(kmeans_df)
        self.update_progress("Running Pipeline", 9/13)

        # Transform the data
        preprocessed_data = pipe["preprocessor"].transform(kmeans_df)
        self.update_progress("Running Pipeline", 10/13)

        # Get the predicted labels
        predicted_labels = pipe["cluster"]["kmeans"].labels_
        self.update_progress("Running Pipeline", 11/13)

        # Add the cluster labels to the original DataFrame
        kmeans_df['cluster'] = predicted_labels
        self.update_progress("Running Pipeline", 12/13)

        # Compute the silhouette score
        silhouette = silhouette_score(preprocessed_data, predicted_labels)
        self.update_progress("Running Pipeline", 13/13)
        print("\n")

        return predicted_labels

    def find_elbow(self, kmeans_df, clust_eval):
        """
        Finds the optimal number of clusters for KMeans clustering using the elbow method.

        This method goes through the following steps:
        1. Resets the DataFrame index.
        2. Converts 'date' to 'month' and creates cyclical features for it.
        3. Scales features and applies PCA via a preprocessing pipeline.
        4. Loops through a predefined number of clusters (1 to 11).
        5. Performs KMeans clustering with the specified number of clusters.
        6. Calculates the sum of squared errors (SSE) for each KMeans run.
        7. Uses the KneeLocator to identify the "elbow point" in the SSE curve, which indicates the optimal number of clusters.

        Parameters:
            kmeans_df (DataFrame): The DataFrame to cluster.

        Returns:
            tuple: Contains the following elements:
                - The optimal number of clusters, as determined by the elbow method.
                - The sum of squared errors (SSE) for each number of clusters from 1 to 11.
                - Silhouette scores for each number of clusters from 2 to 11.
        """
        # Preprocessing steps
        kmeans_df.reset_index(inplace=True)

        kmeans_df['date'] = pd.to_datetime(kmeans_df['date'])
        kmeans_df['month'] = kmeans_df['date'].dt.month
        kmeans_df = kmeans_df.drop('date', axis=1)

        kmeans_df['month_sin'] = np.sin(2 * np.pi * kmeans_df['month'] / 12)
        kmeans_df['month_cos'] = np.cos(2 * np.pi * kmeans_df['month'] / 12)

        kmeans_df = kmeans_df.drop('month', axis=1)
        kmeans_df.fillna(0, inplace=True)

        sse = []
        silhouette_scores = []
        self.update_progress("Evaluating Clusters", 0/clust_eval)

        for k in range(1, clust_eval + 1):
            # Create the preprocessor pipeline
            preprocessor = Pipeline(
                [
                    ("scaler", MinMaxScaler()),
                    ("pca", PCA(n_components=2)),
                ]
            )

            # Create the K-means clustering pipeline
            cluster = Pipeline(
                [
                    ("kmeans", KMeans(n_clusters=k,
                                    init='k-means++',
                                    n_init=100,
                                    max_iter=1500,
                                    random_state=42
                                    )
                    ),
                ]
            )

            # Combine both pipelines
            pipe = Pipeline(
                [
                    ("preprocessor", preprocessor),
                    ("cluster", cluster),
                ]
            )

            # Fit the pipeline on the data
            pipe.fit(kmeans_df)
            sse.append(pipe['cluster']['kmeans'].inertia_)

            # Calculate the silhouette score only for k > 1
            if k > 1:
                preprocessed_data = pipe["preprocessor"].transform(kmeans_df)
                silhouette_score_t = silhouette_score(preprocessed_data, pipe["cluster"]["kmeans"].labels_)
                silhouette_scores.append(silhouette_score_t)
            else:
                silhouette_scores.append(None)

            self.update_progress("Evaluating Clusters", k/clust_eval)

        print("\n")

        kl = KneeLocator(
            range(1, clust_eval+1), sse, curve="convex", direction="decreasing"
        )

        # # plot SSE vs clusters
        # fig = go.Figure(data=[go.Scatter(x = list(range(1, clust_eval+1)), y = sse, mode = 'lines' )])
        # fig.update_layout(
        #     xaxis_title="No. of Clusters", 
        #     yaxis_title="Sum of Squared Errors",
        # )
        # sseplot_name = "SSE_Curve.png"
        # fig.write_image(f"{self.directory}/{sseplot_name}")

        return kl.elbow, sse, silhouette_scores

    def calculate_cluster_probability(self):
        """
        Calculates the monthly probabilities for each cluster label.

        This method generates a pivot DataFrame that shows the monthly probabilities for each cluster.
        It operates on the class attributes `predicted_labels` and `kmeans_df`.

        The function goes through the following steps:
        1. Resets the index of `kmeans_df`.
        2. Extracts the month from the date column in `kmeans_df`.
        3. Groups the data by cluster and month, calculating the count of data points in each group.
        4. Calculates the total count for each month.
        5. Merges both counts to calculate probabilities.
        6. Saves the calculated probabilities in a pivot DataFrame.

        The resulting DataFrame is saved to a CSV file named 'percentage_probability.csv'.

        Returns:
            None: The function saves the output to a CSV file and modifies class attributes.
        """
        cluster_labels = self.predicted_labels
        kmeans_df = self.kmeans_df

        kmeans_df.reset_index(inplace=True)

        # Extract the month from the date column in the kmeans_df
        date = pd.to_datetime(kmeans_df['date'])
        month = date.dt.month

        # Create a DataFrame with month and cluster labels
        prob_df = pd.DataFrame({'month': month, 'cluster': cluster_labels})
        self.update_progress("Calculating Probabilities", 1/6)

        # Count the number of each cluster per month
        cluster_month_counts = prob_df.groupby(['cluster', 'month']).size().reset_index(name='counts')
        self.update_progress("Calculating Probabilities", 2/6)

        # Calculate the total counts for each month
        month_total_counts = prob_df.groupby('month').size().reset_index(name='total_counts')
        self.update_progress("Calculating Probabilities", 3/6)

        # Merge both dataframes on 'month'
        merged_df = pd.merge(cluster_month_counts, month_total_counts, on='month')
        self.update_progress("Calculating Probabilities", 4/6)

        # Calculate the probabilities
        merged_df['probability'] = merged_df['counts'] / merged_df['total_counts']

        # Convert the 'cluster' column to integers if they are not already
        merged_df['cluster'] = merged_df['cluster'].astype(int)
        self.update_progress("Calculating Probabilities", 5/6)

        # Create a DataFrame with probabilities as string percentages
        merged_df['probability'] = merged_df['probability'].apply(lambda x: str(round(x, 6)))
        pivot_df_str_percentage = merged_df.pivot(index='cluster', columns='month', values='probability')
        pivot_df_str_percentage.fillna('0', inplace=True)
        pivot_df_str_percentage.to_csv(f'{self.directory}/solar_probs.csv', index=False)
        self.update_progress("Calculating Probabilities", 6/6)
        print("\n")

    def split_and_cluster_data(self):
        """
        Splits the solar generation data into clusters and saves each cluster's data into separate CSV files.

        This method first normalizes the solar generation data by site wattage and then transposes the data
        into 24-hour segments. Each segment is labeled with a cluster identifier based on previously determined
        labels. The data for each cluster is then saved into a dedicated directory and CSV file.

        The method organizes the output by creating a directory for each cluster under a main 'Clusters' directory,
        where each directory contains CSV files for each data column, segmented by day.

        Side Effects:
            - Creates a directory structure under 'Clusters' in the specified directory.
            - Writes multiple CSV files containing the clustered data.

        Returns:
            None: This method performs file I/O operations and does not return any values.

        Example Directory Structure:
            Clusters/
                cluster_1/
                    site1.csv
                    site2.csv
                cluster_2/
                    site1.csv
                    site2.csv
        """
        # # Create overarching directory for all clusters if it does not exist
        # os.makedirs('clusters', exist_ok=True)

        # Step 1: Import the .csv file into a pandas DataFrame
        df = self.solar_gen_df
        site_df = self.site_info_df

        # Remove un-needed values
        df = df[['datetime'] + self.selected_sites]

        # Gets the site wattage for normalization
        site_wattage = site_df[['site_name','MW']]

        # Normalize values
        for index, row in site_wattage.iterrows():
            site_name = row['site_name']
            wattage_limit = row['MW']

            if site_name in df.columns:
                df[site_name] = df[site_name] / wattage_limit

        labels = self.predicted_labels

        # Step 2: In each split DataFrame column, transpose every 24 rows into a single row in a new DataFrame
        col = 1
        for column in df.columns:
            self.update_progress("Clustering Original Data", col/df.columns.size)
            col = col+1

            if column == 'datetime':
                continue

            temp_df = df[[column]]

            reshaped_data = []

            for i in range(0, len(temp_df), 24):
                row = temp_df.iloc[i:i+24].values.flatten()
                reshaped_data.append(row)

            reshaped_df = pd.DataFrame(reshaped_data)
            repeated_labels = np.repeat(labels, len(reshaped_df) // len(labels))

            reshaped_df['labels'] = repeated_labels

            # Step 3: Split each reshaped DataFrame into more DataFrames based on the corresponding cluster
            for label in reshaped_df['labels'].unique():
                df_cluster = reshaped_df[reshaped_df['labels'] == label]

                # Create a directory for the cluster under "Clusters" if it does not exist
                os.makedirs(f'{self.directory}/Clusters/{label + 1}', exist_ok=True)

                # Remove the labels column
                df_cluster = df_cluster.drop(columns=['labels'])

                # Save the DataFrame to the cluster directory under "clusters"
                df_cluster.to_csv(f'{self.directory}/Clusters/{label + 1}/{column}.csv', index=False)
                # df_cluster.to_csv(f'clusters/cluster_{label}/{column}.csv', index=False)
        print("\n")
 
    def test_metrics(self, clust_eval):
        """
        Calculates and writes K-means clustering metrics to a text file.

        Parameters:
            clust_eval (int): The max number of clusters to evaluate.

        Returns:
            tuple: (elbow, sse) — used for plotting in the main thread.
        """
        elbow, sse, silhouette_scores = self.find_elbow(self.kmeans_df, clust_eval)

        results_text = (
            "The optimal number of clusters in a dataset is the number that\n"
            "best captures the underlying structure of the data.\n\n"
            "Elbow Method: This method involves plotting the explained variation\n"
            "(e.g., within-cluster sum of squares) against the number of clusters\n"
            "and looking for an 'elbow' point where the rate of decrease sharply changes.\n"
            "This point is considered to be the optimal number of clusters.\n\n"
            "Silhouette score:\n\n"
            "Near +1: A silhouette score near +1 indicates that the sample is far away\n"
            "from the neighboring clusters. This means that the sample is very well clustered\n"
            "and clearly distinguishable from other clusters.\n\n"
            "Near 0: A silhouette score near 0 indicates that the sample is on or very close\n"
            "to the decision boundary between two neighboring clusters. This means that the\n"
            "sample could potentially be assigned to either cluster.\n\n"
            "Below 0: A silhouette score below 0 indicates that the sample might have been\n"
            "assigned to the wrong cluster. Samples with a score below 0 are closer to the\n"
            "neighboring clusters than to their own cluster.\n\n"
            "A higher silhouette score indicates better clustering quality, with well-separated\n"
            "clusters that are dense internally.\n\n"
            f"Optimal Number of Clusters: {elbow}\n\n"
        )

        for i, (sse_value, sil_score) in enumerate(zip(sse, silhouette_scores), start=1):
            results_text += f"SSE for {i} Clusters: {sse_value}\n"
            results_text += f"Silhouette Score for {i} Clusters: {sil_score}\n"

        # Write to file
        with open(f"{self.directory}/clustering_results.txt", "w") as f:
            f.write(results_text)

        return elbow, sse






    # def test_metrics(self, clust_eval):
    #     """
    #     Calculates and writes K-means clustering metrics to a text file.

    #     This method evaluates the clustering performance using the elbow method and silhouette scores,
    #     and writes the detailed results to a file named 'clustering_results.txt'.

    #     The method outputs a detailed explanation of the elbow method and silhouette scores, and
    #     it identifies the optimal number of clusters based on the provided dataset. It also captures
    #     the sum of squared errors (SSE) for different numbers of clusters, along with their respective
    #     silhouette scores.

    #     Parameters:
    #         clust_eval (int): The maximum number of clusters to evaluate, which determines the range
    #                         of clusters to consider for finding the elbow point.

    #     Side Effects:
    #         - Writes to a file 'clustering_results.txt' in the specified directory.
    #         - Temporarily redirects stdout to this file to capture print statements.

    #     Returns:
    #         None: This method does not return a value but writes output to a file.

    #     Example of File Output:
    #         The optimal number of clusters in a dataset is the number that...
    #         Optimal Number of Clusters: X
    #         SSE for Y Clusters: Z
    #         Silhouette Score for Y Clusters: W
    #     """

    #     text = (
    #         "The optimal number of clusters in a dataset is the number that\n"
    #         "best captures the underlying structure of the data.\n\n"
    #         "Elbow Method: This method involves plotting the explained variation\n"
    #         "(e.g., within-cluster sum of squares) against the number of clusters\n"
    #         "and looking for an 'elbow' point where the rate of decrease sharply changes.\n"
    #         "This point is considered to be the optimal number of clusters.\n\n"
    #         "Silhouette score:\n\n"
    #         "Near +1: A silhouette score near +1 indicates that the sample is far away\n"
    #         "from the neighboring clusters. This means that the sample is very well clustered\n"
    #         "and clearly distinguishable from other clusters.\n\n"
    #         "Near 0: A silhouette score near 0 indicates that the sample is on or very close\n"
    #         "to the decision boundary between two neighboring clusters. This means that the\n"
    #         "sample could potentially be assigned to either cluster.\n\n"
    #         "Below 0: A silhouette score below 0 indicates that the sample might have been\n"
    #         "assigned to the wrong cluster. Samples with a score below 0 are closer to the\n"
    #         "neighboring clusters than to their own cluster.\n\n"
    #         "A higher silhouette score indicates better clustering quality, with well-separated\n"
    #         "clusters that are dense internally.\n"
    #     )
    #     # Call the find_elbow method to get the elbow point and SSE
    #     elbow, sse, silhouette_scores = self.find_elbow(self.kmeans_df, clust_eval)

    #     # Open 'results.txt' for writing
    #     with open(f"{self.directory}/clustering_results.txt", "w") as f:

    #         # Save the current stdout so that it can be restored later
    #         original_stdout = sys.stdout

    #         # Redirect stdout to the file, so print statements write to the file
    #         sys.stdout = f

    #         # Write the best number of clusters to the file
    #         print(f"{text}Optimal Number of Clusters: {elbow}")
    #         print(f"{text}")

    #         # Write the SSE for different numbers of clusters to the file.
    #         # Start the numbering from 2 as specified.
    #         for i, (sse_value, silhouette_score) in enumerate(zip(sse, silhouette_scores), start=2):
    #             print(f"SSE for {i-1} Clusters: {sse_value}")
    #             print(f"Silhouette Score for {i-1} Clusters: {silhouette_score}")

    #         # Restore the original stdout
    #         sys.stdout = original_stdout

# if __name__ == "__main__":

#     # Define the list of selected sites for analysis
#     directory = r'path/to/Data//solar'
#     site_data = directory + '/solar_sites.csv'


#     # Initialize the KMeans_Pipeline class
#     pipeline = KMeans_Pipeline(directory, site_data)

#     # Generate and save the clustering metrics to a text file
#     pipeline.test_metrics(clust_eval = 4)

#     # # Run the pipeline before performing any other actions
#     # pipeline.run(n_clusters = 8)

#     # # Calculate the cluster probabilities and save them to a CSV file
#     # pipeline.calculate_cluster_probability()

#     # # Split the data and cluster them based on the generated labels
#     # pipeline.split_and_cluster_data()