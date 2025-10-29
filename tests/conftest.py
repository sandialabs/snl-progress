"""
Shared fixtures for production data integration tests.

This module provides access to real production data from the Data/ directory
for comprehensive integration testing that mirrors actual usage patterns.
"""

import os
from pathlib import Path
import pytest
import pandas as pd


@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def data_directory(project_root):
    """Get the Data directory path."""
    return project_root / "progress" / "Data"


@pytest.fixture(scope="session")
def real_system_data(data_directory):
    """
    Production system data fixtures.
    
    Returns:
        dict: Paths to real system CSV files with 93 generators, 3 buses, 8760-hour load
    """
    system_dir = data_directory / "System"
    
    if not system_dir.exists():
        pytest.skip("Production system data not available")
    
    return {
        "gen_csv": str(system_dir / "gen.csv"),
        "bus_csv": str(system_dir / "bus.csv"), 
        "branch_csv": str(system_dir / "branch.csv"),
        "load_csv": str(system_dir / "load.csv"),
        "storage_csv": str(system_dir / "storage.csv"),
        "system_dir": str(system_dir)
    }


@pytest.fixture(scope="session")
def real_solar_sites(data_directory):
    """
    Production solar sites data.
    
    Returns:
        str: Path to solar_sites.csv with 27 sites across 3 zones
    """
    solar_sites_path = data_directory / "Solar" / "solar_sites.csv"
    
    if not solar_sites_path.exists():
        pytest.skip("Production solar sites data not available")
    
    return str(solar_sites_path)


@pytest.fixture(scope="session")
def real_wind_sites(data_directory):
    """
    Production wind sites data.
    
    Returns:
        str: Path to wind_sites.csv with 4 farms, zones 1 and 3
    """
    wind_sites_path = data_directory / "Wind" / "wind_sites.csv"
    
    if not wind_sites_path.exists():
        pytest.skip("Production wind sites data not available")
    
    return str(wind_sites_path)


@pytest.fixture(scope="session")
def real_solar_data(data_directory):
    """
    Production solar generation data.
    
    Returns:
        str: Path to solar_data.xlsx if available
    """
    solar_data_path = data_directory / "Solar" / "solar_data.xlsx"
    
    if not solar_data_path.exists():
        pytest.skip("Production solar generation data not available")
    
    return str(solar_data_path)


@pytest.fixture(scope="session")
def real_wind_data(data_directory):
    """
    Production wind data.
    
    Returns:
        dict: Paths to wind data files
    """
    wind_dir = data_directory / "Wind"
    
    if not wind_dir.exists():
        pytest.skip("Production wind data not available")
    
    return {
        "wind_sites_csv": str(wind_dir / "wind_sites.csv"),
        "power_curves_csv": str(wind_dir / "w_power_curves.csv"),
        "windspeed_data_csv": str(wind_dir / "windspeed_data.csv"),
        "wind_dir": str(wind_dir)
    }


@pytest.fixture(scope="session")
def production_system_summary(real_system_data):
    """
    Summary statistics of production system data for validation.
    
    Returns:
        dict: Expected counts and dimensions from production data
    """
    # Load and analyze production data
    gen_df = pd.read_csv(real_system_data["gen_csv"])
    bus_df = pd.read_csv(real_system_data["bus_csv"])
    load_df = pd.read_csv(real_system_data["load_csv"])
    storage_df = pd.read_csv(real_system_data["storage_csv"])
    
    return {
        "n_generators": len(gen_df),
        "n_buses": len(bus_df),
        "n_hours": len(load_df),
        "n_ess": len(storage_df),
        "bus_names": bus_df["Bus Name"].tolist(),
        "zones": sorted(gen_df["Bus No."].unique().tolist()),
        "gen_technologies": gen_df["Tech"].unique().tolist()
    }


@pytest.fixture
def kmeans_test_helper(real_solar_data, real_solar_sites):
    """Helper fixture for creating pipelines with common configurations."""
    def _create_pipeline(selected_sites=None, n_clusters=5):
        from progress.mod_kmeans import KMeans_Pipeline
        solar_dir = Path(real_solar_data).parent
        pipeline = KMeans_Pipeline(
            directory=str(solar_dir),
            site_data=real_solar_sites,
            selected_sites=selected_sites
        )
        return pipeline
    return _create_pipeline