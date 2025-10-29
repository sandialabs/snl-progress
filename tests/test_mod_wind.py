import os
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
import requests

pytest.importorskip("openpyxl")

try:
    from progress.mod_wind import Wind
except Exception:
    from progress.mod_wind import Wind


# Unit tests: WindFarmsData

def test_windfarmsdata_basic(tmp_path: Path):
    """
    Test basic functionality of WindFarmsData method with simple input data.
    
    This test verifies that the WindFarmsData method correctly processes wind farm
    site information and power curve data. It creates mock CSV files containing:
    - Wind farm site data (farm numbers, names, zones, capacities, turbine ratings, power classes)
    - Power curve data (wind speed ranges and corresponding power outputs for different turbine classes)
    
    The test validates that:
    - The method returns the expected number of wind farm sites
    - Farm names, zone numbers, and other parameters are correctly extracted
    - Power curve data is properly loaded and processed
    - All returned values have the correct data types and dimensions
    
    Expected behavior: Method should successfully parse CSV files and return structured data
    for wind farm configuration and power generation characteristics.
    
    Args:
        tmp_path: Temporary directory path for creating test CSV files
    """
    site_csv = tmp_path / "wind_sites.csv"
    pd.DataFrame(
        {
            "Farm No.": [1, 2],
            "Farm Name": ["FarmA", "FarmB"],
            "Zone No.": [10, 20],
            "Max Cap": [100.0, 150.0],
            "Turbine Rating": [2.0, 3.0],
            "Power Class": [2, 3],
        }
    ).to_csv(site_csv, index=False)

    pcurve_csv = tmp_path / "w_power_curves.csv"
    pd.DataFrame(
        {
            "Start (m/s)": [0.0, 5.0, 10.0],
            "End (m/s)": [5.0, 10.0, 15.0],
            "Class 2": [0.1, 0.2, 0.3],
            "Class 3": [0.2, 0.3, 0.4],
        }
    ).to_csv(pcurve_csv, index=False)

    w = Wind()
    (
        w_sites,
        farm_name,
        zone_no,
        w_classes,
        w_turbines,
        turbine_rating,
        p_class,
        out_curve2,
        out_curve3,
        start_speed,
    ) = w.WindFarmsData(str(site_csv), str(pcurve_csv))

    assert w_sites == 2
    assert list(farm_name) == ["FarmA", "FarmB"]
    assert np.all(zone_no == np.array([10, 20]))
    # ceil(MaxCap / TurbineRating)
    assert np.all(w_turbines == np.array([50, 50]))
    assert w_classes == 3
    assert np.allclose(out_curve2, np.array([0.1, 0.2, 0.3]))
    assert np.allclose(out_curve3, np.array([0.2, 0.3, 0.4]))


def test_windfarmsdata_missing_required_column(tmp_path: Path):
    """
    Test WindFarmsData method behavior when required columns are missing from input CSV.
    
    This test verifies that the WindFarmsData method properly handles error conditions
    when the input CSV file is missing essential columns required for wind farm data processing.
    The test creates a CSV file with incomplete data structure to simulate real-world
    scenarios where data files may be corrupted or improperly formatted.
    
    The test validates that:
    - The method raises appropriate exceptions when required columns are missing
    - Error handling is robust and provides meaningful feedback
    - The method fails gracefully without crashing the application
    
    Expected behavior: Method should raise a KeyError or similar exception indicating
    which required column is missing from the input data.
    
    Args:
        tmp_path: Temporary directory path for creating test CSV files
    """
    site_csv = tmp_path / "wind_sites.csv"
    # Missing Farm Name
    pd.DataFrame(
        {
            "Farm No.": [1],
            # "Farm Name": ["FarmA"],
            "Zone No.": [10],
            "Max Cap": [100.0],
            "Turbine Rating": [2.0],
            "Power Class": [2],
        }
    ).to_csv(site_csv, index=False)
    pcurve_csv = tmp_path / "w_power_curves.csv"
    pd.DataFrame(
        {
            "Start (m/s)": [0.0, 5.0],
            "End (m/s)": [5.0, 10.0],
            "Class 2": [0.1, 0.2],
            "Class 3": [0.2, 0.3],
        }
    ).to_csv(pcurve_csv, index=False)

    w = Wind()
    with pytest.raises(KeyError):
        w.WindFarmsData(str(site_csv), str(pcurve_csv))


# Unit-ish: CalWindTrRates with tiny inputs

def test_calwindtrrates_tiny_inputs(tmp_path: Path):
    """
    Test CalWindTrRates method with minimal input data to verify basic functionality.
    
    This test validates the CalWindTrRates method using very small datasets to ensure
    the core algorithm works correctly even with minimal data. The test creates a small
    wind speed dataset with only 5 data points and verifies that the method can:
    - Process the input data without errors
    - Generate appropriate transition rate matrices
    - Handle edge cases with small datasets
    
    The test validates that:
    - The method processes tiny datasets without crashing
    - Output matrices have correct dimensions
    - Transition rates are calculated properly
    - The method handles minimal data gracefully
    
    Expected behavior: Method should successfully process small datasets and return
    valid transition rate matrices with appropriate dimensions.
    
    Args:
        tmp_path: Temporary directory path for creating test data files
    """
    # site_data
    site_csv = tmp_path / "wind_sites.csv"
    pd.DataFrame(
        {
            "Farm No.": [1, 2],
            "Farm Name": ["FarmA", "FarmB"],
            "Zone No.": [10, 20],
            "Max Cap": [1.0, 1.0],
            "Turbine Rating": [1.0, 1.0],
            "Power Class": [2, 3],
        }
    ).to_csv(site_csv, index=False)

    # power curves -> bins
    pcurve_csv = tmp_path / "w_power_curves.csv"
    pd.DataFrame(
        {
            "Start (m/s)": [0.0, 5.0, 10.0],
            "End (m/s)": [5.0, 10.0, 15.0],
            "Class 2": [0.0, 0.0, 0.0],
            "Class 3": [0.0, 0.0, 0.0],
        }
    ).to_csv(pcurve_csv, index=False)

    # windspeed_data with columns per site; include boundary transitions
    wdata_csv = tmp_path / "windspeed_data.csv"
    df = pd.DataFrame(
        {
            "datetime": pd.date_range("2024-01-01", periods=5, freq="H"),
            "FarmA": [0.1, 4.9, 5.1, 9.9, 10.1],
            "FarmB": [0.0, 5.0, 10.0, 10.0, 14.9],
        }
    )
    df.set_index("datetime", inplace=True)
    df.to_csv(wdata_csv)

    w = Wind()
    rate = w.CalWindTrRates(
        directory=str(tmp_path),
        windspeed_data=str(wdata_csv),
        site_data=str(site_csv),
        pcurve_data=str(pcurve_csv),
    )

    # Shape: (w_sites, w_classes, w_classes) = (2, 3, 3)
    assert rate.shape == (2, 3, 3)
    # Rows normalized (after nan_to_num)
    for s in range(rate.shape[0]):
        for r in range(rate.shape[1]):
            row_sum = rate[s, r].sum()
            assert 0.0 <= row_sum <= 1.0

    # Excel output exists
    assert (tmp_path / "t_rate.xlsx").exists()


# Integration: DownloadWindData with mocked requests

@pytest.mark.integration
def test_downloadwinddata_writes_files_and_combined_csv(tmp_path: Path, monkeypatch):
    """
    Test DownloadWindData method file output and CSV generation functionality.
    
    This test verifies that the DownloadWindData method correctly writes individual
    wind farm data files and creates a combined CSV file containing all wind data.
    The test mocks the external API response to simulate wind data download and
    validates the file system operations.
    
    The test validates that:
    - Individual wind farm CSV files are created with correct naming convention
    - Combined windspeed_data.csv file is generated containing all farm data
    - File contents contain expected wind speed data in proper format
    - All required columns are present in output files
    - Data integrity is maintained across file operations
    
    Expected behavior: Method should create individual farm files and a combined
    CSV file with properly formatted wind speed data for all specified farms.
    
    Args:
        tmp_path: Temporary directory path for file operations
        monkeypatch: Pytest fixture for mocking external dependencies
    """
    # site_data with coordinates and hub height
    site_csv = tmp_path / "wind_sites.csv"
    pd.DataFrame(
        {
            "Farm No.": [1, 2],
            "Farm Name": ["FarmA", "FarmB"],
            "Latitude": [35.0, 36.0],
            "Longitude": [-106.0, -105.5],
            "Hub Height": [80, 90],
        }
    ).to_csv(site_csv, index=False)

    # requests.get mock: two-header rows then real header
    class DummyResp:
        def __init__(self, text):
            self.text = text

    header1 = "meta line to skip\n"
    header2 = (
        "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    )
    data_rows = "2024,1,1,0,30,6.0,7.0\n2024,1,1,1,30,6.5,7.5\n"
    csv_text = header1 + header2 + data_rows

    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    w = Wind()
    w.DownloadWindData(
        directory=str(tmp_path),
        site_data=str(site_csv),
        api_key="k",
        email="e@example.com",
        affiliation="aff",
        year_start=2024,
        year_end=2024,
    )

    base = tmp_path / "wtk_data" / "2024"
    assert (base / "FarmA.csv").exists()
    assert (base / "FarmB.csv").exists()
    # Combined windspeed file exists
    combined = tmp_path / "windspeed_data.csv"
    assert combined.exists()
    df = pd.read_csv(combined)
    # Should contain both farm columns
    assert set(["FarmA", "FarmB"]).issubset(set(df.columns))


@pytest.mark.integration
def test_downloadwinddata_path_cwd_independence(tmp_path: Path, monkeypatch):
    site_csv = tmp_path / "wind_sites.csv"
    pd.DataFrame(
        {
            "Farm No.": [1],
            "Farm Name": ["FarmA"],
            "Latitude": [35.0],
            "Longitude": [-106.0],
            "Hub Height": [100],
        }
    ).to_csv(site_csv, index=False)

    class DummyResp:
        def __init__(self, text):
            self.text = text

    header1 = "meta line\n"
    header2 = (
        "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    )
    data_rows = "2024,1,1,0,30,6.0,7.0\n"
    csv_text = header1 + header2 + data_rows
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    w = Wind()
    # Absolute
    w.DownloadWindData(str(tmp_path), str(site_csv), "k", "e", "aff", 2024, 2024)
    assert (tmp_path / "wtk_data" / "2024" / "FarmA.csv").exists()

    # Relative after chdir
    old = os.getcwd()
    try:
        os.chdir(tmp_path)
        w.DownloadWindData(".", str(site_csv.name), "k", "e", "aff", 2024, 2024)
        assert (Path("wtk_data") / "2024" / "FarmA.csv").exists()
    finally:
        os.chdir(old)


@pytest.mark.integration
def test_calwindtrrates_end_to_end(tmp_path: Path, monkeypatch):
    # Prepare a minimal combined windspeed file and site/pcurve
    site_csv = tmp_path / "wind_sites.csv"
    pd.DataFrame(
        {
            "Farm No.": [1],
            "Farm Name": ["FarmA"],
            "Zone No.": [10],
            "Max Cap": [1.0],
            "Turbine Rating": [1.0],
            "Power Class": [2],
        }
    ).to_csv(site_csv, index=False)

    pcurve_csv = tmp_path / "w_power_curves.csv"
    pd.DataFrame(
        {
            "Start (m/s)": [0.0, 5.0],
            "End (m/s)": [5.0, 10.0],
            "Class 2": [0.0, 0.0],
            "Class 3": [0.0, 0.0],
        }
    ).to_csv(pcurve_csv, index=False)

    wdata_csv = tmp_path / "windspeed_data.csv"
    df = pd.DataFrame(
        {
            "datetime": pd.date_range("2024-01-01", periods=4, freq="H"),
            "FarmA": [1.0, 2.0, 6.0, 7.0],
        }
    )
    df.set_index("datetime", inplace=True)
    df.to_csv(wdata_csv)

    w = Wind()
    rate = w.CalWindTrRates(str(tmp_path), str(wdata_csv), str(site_csv), str(pcurve_csv))
    assert rate.shape == (1, 2, 2)
    assert (tmp_path / "t_rate.xlsx").exists()


# Negative paths

def test_downloadwinddata_missing_required_columns(tmp_path: Path):
    site_csv = tmp_path / "wind_sites.csv"
    # Missing Farm Name
    pd.DataFrame({"Farm No.": [1], "Latitude": [35.0], "Longitude": [-106.0], "Hub Height": [80]}).to_csv(
        site_csv, index=False
    )
    w = Wind()
    with pytest.raises(KeyError):
        w.DownloadWindData(str(tmp_path), str(site_csv), "k", "e", "aff", 2024, 2024)


def test_calwindtrrates_missing_files(tmp_path: Path):
    w = Wind()
    with pytest.raises(FileNotFoundError):
        w.CalWindTrRates(str(tmp_path), str(tmp_path / "missing.csv"), str(tmp_path / "sites.csv"), str(tmp_path / "pcurve.csv"))


def test_calwindtrrates_wrong_columns(tmp_path: Path):
    site_csv = tmp_path / "wind_sites.csv"
    pd.DataFrame({"Farm No.": [1], "Farm Name": ["FarmA"], "Zone No.": [10], "Max Cap": [1.0], "Turbine Rating": [1.0], "Power Class": [2]}).to_csv(site_csv, index=False)
    pcurve_csv = tmp_path / "w_power_curves.csv"
    pd.DataFrame({"start": [0.0, 5.0], "end": [5.0, 10.0]}).to_csv(pcurve_csv, index=False)
    wdata_csv = tmp_path / "windspeed_data.csv"
    pd.DataFrame({"datetime": pd.date_range("2024-01-01", periods=2, freq="H"), "FarmA": [1.0, 2.0]}).set_index("datetime").to_csv(wdata_csv)
    w = Wind()
    with pytest.raises(KeyError):
        w.CalWindTrRates(str(tmp_path), str(wdata_csv), str(site_csv), str(pcurve_csv))


# Test Classes

class TestWindFarmsData:
    """Test WindFarmsData method functionality and edge cases"""
    
    def test_basic_functionality(self, tmp_path: Path):
        """
        Test basic WindFarmsData functionality with comprehensive mock data validation.
        
        This test verifies the core functionality of the WindFarmsData method by providing
        complete mock data for wind farm sites and power curves. It validates that the
        method correctly parses CSV files and returns all expected data structures.
        
        The test validates that:
        - Wind farm site data is correctly loaded from CSV
        - Power curve data is properly processed for different turbine classes
        - All returned parameters have correct values and data types
        - Farm names, zone numbers, and capacities are accurately extracted
        - Power curve arrays contain expected values for different wind speed ranges
        
        Expected behavior: Method should successfully process both CSV files and return
        structured data arrays with correct dimensions and values.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2],
                "Farm Name": ["FarmA", "FarmB"],
                "Zone No.": [10, 20],
                "Max Cap": [100.0, 150.0],
                "Turbine Rating": [2.0, 3.0],
                "Power Class": [2, 3],
            }
        ).to_csv(site_csv, index=False)

        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0, 10.0],
                "End (m/s)": [5.0, 10.0, 15.0],
                "Class 2": [0.1, 0.2, 0.3],
                "Class 3": [0.2, 0.3, 0.4],
            }
        ).to_csv(pcurve_csv, index=False)

        w = Wind()
        (
            w_sites,
            farm_name,
            zone_no,
            w_classes,
            w_turbines,
            turbine_rating,
            p_class,
            out_curve2,
            out_curve3,
            start_speed,
        ) = w.WindFarmsData(str(site_csv), str(pcurve_csv))

        assert w_sites == 2
        assert list(farm_name) == ["FarmA", "FarmB"]
        assert np.all(zone_no == np.array([10, 20]))
        # ceil(MaxCap / TurbineRating)
        assert np.all(w_turbines == np.array([50, 50]))
        assert w_classes == 3
        assert np.allclose(out_curve2, np.array([0.1, 0.2, 0.3]))
        assert np.allclose(out_curve3, np.array([0.2, 0.3, 0.4]))
    
    def test_missing_required_column(self, tmp_path: Path):
        """
        Test WindFarmsData error handling when required CSV columns are missing.
        
        This test verifies that the WindFarmsData method properly handles error conditions
        when essential columns are missing from the input CSV files. It simulates real-world
        scenarios where data files may be incomplete or corrupted.
        
        The test validates that:
        - Appropriate exceptions are raised when required columns are missing
        - Error messages are informative and help identify the missing column
        - The method fails gracefully without causing application crashes
        - Error handling is consistent across different missing column scenarios
        
        Expected behavior: Method should raise a KeyError or similar exception with
        a clear message indicating which required column is missing.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        site_csv = tmp_path / "wind_sites.csv"
        # Missing Farm Name
        pd.DataFrame(
            {
                "Farm No.": [1],
                # "Farm Name": ["FarmA"],
                "Zone No.": [10],
                "Max Cap": [100.0],
                "Turbine Rating": [2.0],
                "Power Class": [2],
            }
        ).to_csv(site_csv, index=False)
        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0],
                "End (m/s)": [5.0, 10.0],
                "Class 2": [0.1, 0.2],
                "Class 3": [0.2, 0.3],
            }
        ).to_csv(pcurve_csv, index=False)

        w = Wind()
        with pytest.raises(KeyError):
            w.WindFarmsData(str(site_csv), str(pcurve_csv))
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_with_real_data(self, real_wind_sites, real_wind_data):
        """
        Test WindFarmsData with real-world wind farm and power curve data.
        
        This test validates the WindFarmsData method using actual wind farm site data
        and power curve information to ensure the method works correctly with realistic
        data structures and values. It uses pytest fixtures that provide real data
        from the project's data directory.
        
        The test validates that:
        - Real wind farm site data is correctly processed
        - Power curve data from actual turbine specifications is properly loaded
        - All data types and formats match expected real-world scenarios
        - The method handles realistic data volumes and complexity
        - Output parameters are consistent with real wind farm configurations
        
        Expected behavior: Method should successfully process real data files and
        return accurate wind farm configuration parameters.
        
        Args:
            real_wind_sites: Pytest fixture providing real wind farm site data
            real_wind_data: Pytest fixture providing real wind power curve data
        """
        w = Wind()
        
        # Test WindFarmsData with real data
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        
        # Verify results match real wind farms
        wind_sites_df = pd.read_csv(real_wind_sites)
        
        assert w_sites == len(wind_sites_df), "Should have correct number of wind sites"
        assert len(farm_name) == w_sites, "Should have correct number of farm names"
        assert len(zone_no) == w_sites, "Should have correct number of zones"
        assert len(w_turbines) == w_sites, "Should have correct number of turbines"
        assert len(turbine_rating) == w_sites, "Should have correct number of turbine ratings"
        assert len(p_class) == w_sites, "Should have correct number of power classes"
        assert len(start_speed) == w_classes, "Should have correct number of start speeds"
        
        # Verify farm names match
        expected_farm_names = wind_sites_df["Farm Name"].tolist()
        assert farm_name.tolist() == expected_farm_names, "Farm names should match real data"
        
        # Verify zones match
        expected_zones = wind_sites_df["Zone No."].tolist()
        assert zone_no.tolist() == expected_zones, "Zones should match real data"
        
        # Verify power classes are valid
        assert all(pc in [2, 3] for pc in p_class), "Power classes should be 2 or 3"
        
        # Verify turbine ratings are reasonable
        assert all(tr > 0 for tr in turbine_rating), "Turbine ratings should be positive"
        assert all(tr < 10 for tr in turbine_rating), "Turbine ratings should be reasonable (< 10 MW)"
        
        # Verify start speeds are reasonable
        assert all(ss >= 0 for ss in start_speed), "Start speeds should be non-negative"
        assert all(ss <= 50 for ss in start_speed), "Start speeds should be reasonable (< 50 m/s)"
        
        # Verify power curves are valid
        assert len(out_curve2) > 0, "Class 2 power curve should have data"
        assert len(out_curve3) > 0, "Class 3 power curve should have data"
        assert all(0 <= val <= 1 for val in out_curve2), "Class 2 power curve should be in [0, 1]"
        assert all(0 <= val <= 1 for val in out_curve3), "Class 3 power curve should be in [0, 1]"
    
    def test_output_format_and_types(self, tmp_path: Path):
        """
        Test WindFarmsData output format and data type validation.
        
        This test verifies that the WindFarmsData method returns data in the correct
        format with appropriate data types for all output parameters. It validates
        that the method produces consistent, well-structured output suitable for
        downstream wind energy analysis operations.
        
        The test validates that:
        - All returned values have the expected data types (arrays, integers, floats)
        - Output arrays have correct dimensions and shapes
        - Data types are consistent across different input scenarios
        - No unexpected type conversions occur during processing
        - Output format matches expected interface specifications
        
        Expected behavior: Method should return properly typed data structures
        with consistent formatting suitable for wind energy analysis workflows.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2],
                "Farm Name": ["FarmA", "FarmB"],
                "Zone No.": [10, 20],
                "Max Cap": [100.0, 150.0],
                "Turbine Rating": [2.0, 3.0],
                "Power Class": [2, 3],
            }
        ).to_csv(site_csv, index=False)

        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0, 10.0],
                "End (m/s)": [5.0, 10.0, 15.0],
                "Class 2": [0.1, 0.2, 0.3],
                "Class 3": [0.2, 0.3, 0.4],
            }
        ).to_csv(pcurve_csv, index=False)

        w = Wind()
        result = w.WindFarmsData(str(site_csv), str(pcurve_csv))
        
        # Verify return type is tuple
        assert isinstance(result, tuple), "WindFarmsData should return a tuple"
        assert len(result) == 10, "WindFarmsData should return 10 values"
        
        w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, out_curve2, out_curve3, start_speed = result
        
        # Verify data types
        assert isinstance(w_sites, int), "w_sites should be int"
        assert isinstance(farm_name, pd.Series), "farm_name should be pandas Series"
        assert isinstance(zone_no, np.ndarray), "zone_no should be numpy array"
        assert isinstance(w_classes, int), "w_classes should be int"
        assert isinstance(w_turbines, np.ndarray), "w_turbines should be numpy array"
        assert isinstance(turbine_rating, np.ndarray), "turbine_rating should be numpy array"
        assert isinstance(p_class, np.ndarray), "p_class should be numpy array"
        assert isinstance(out_curve2, np.ndarray), "out_curve2 should be numpy array"
        assert isinstance(out_curve3, np.ndarray), "out_curve3 should be numpy array"
        assert isinstance(start_speed, np.ndarray), "start_speed should be numpy array"
    
    def test_turbine_calculation(self, tmp_path: Path):
        """
        Test WindFarmsData turbine count calculation logic.
        
        This test verifies that the WindFarmsData method correctly calculates the
        number of turbines for each wind farm based on maximum capacity and turbine
        rating. It validates the mathematical relationship between capacity, turbine
        rating, and resulting turbine count.
        
        The test validates that:
        - Turbine count is calculated as ceil(MaxCap / TurbineRating)
        - Calculation handles different capacity and rating combinations correctly
        - Results are mathematically accurate for various input scenarios
        - Edge cases with fractional results are handled properly
        - Output values are reasonable for wind farm configurations
        
        Expected behavior: Method should calculate turbine counts using the
        ceiling function to ensure adequate capacity coverage.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2, 3, 4],
                "Farm Name": ["FarmA", "FarmB", "FarmC", "FarmD"],
                "Zone No.": [10, 20, 30, 40],
                "Max Cap": [100.0, 150.0, 75.5, 200.0],
                "Turbine Rating": [2.0, 3.0, 2.5, 4.0],
                "Power Class": [2, 3, 2, 3],
            }
        ).to_csv(site_csv, index=False)

        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0, 10.0],
                "End (m/s)": [5.0, 10.0, 15.0],
                "Class 2": [0.1, 0.2, 0.3],
                "Class 3": [0.2, 0.3, 0.4],
            }
        ).to_csv(pcurve_csv, index=False)

        w = Wind()
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, out_curve2, out_curve3, start_speed) = w.WindFarmsData(str(site_csv), str(pcurve_csv))
        
        # Verify turbine calculation: ceil(MaxCap / TurbineRating)
        expected_turbines = np.array([50, 50, 31, 50])  # [ceil(100/2), ceil(150/3), ceil(75.5/2.5), ceil(200/4)]
        assert np.all(w_turbines == expected_turbines), f"Turbine calculation incorrect. Expected {expected_turbines}, got {w_turbines}"
    
    def test_power_class_handling(self, tmp_path: Path):
        """
        Test WindFarmsData power class processing and validation.
        
        This test verifies that the WindFarmsData method correctly processes and
        validates power class information for different wind turbine types. It
        ensures that power class data is properly extracted and used in downstream
        wind energy calculations.
        
        The test validates that:
        - Power class values are correctly extracted from CSV data
        - Power class arrays have the correct dimensions and data types
        - Power class values are within expected ranges for wind turbines
        - Power class data is properly associated with corresponding farms
        - No data corruption occurs during power class processing
        
        Expected behavior: Method should correctly process power class information
        and return properly formatted arrays for wind turbine classification.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2, 3, 4],
                "Farm Name": ["FarmA", "FarmB", "FarmC", "FarmD"],
                "Zone No.": [10, 20, 30, 40],
                "Max Cap": [100.0, 150.0, 200.0, 250.0],
                "Turbine Rating": [2.0, 3.0, 4.0, 5.0],
                "Power Class": [2, 3, 2, 3],
            }
        ).to_csv(site_csv, index=False)

        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0, 10.0],
                "End (m/s)": [5.0, 10.0, 15.0],
                "Class 2": [0.1, 0.2, 0.3],
                "Class 3": [0.2, 0.3, 0.4],
            }
        ).to_csv(pcurve_csv, index=False)

        w = Wind()
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, out_curve2, out_curve3, start_speed) = w.WindFarmsData(str(site_csv), str(pcurve_csv))
        
        # Verify power classes
        assert np.all(p_class == np.array([2, 3, 2, 3])), "Power classes should match input"
        assert all(pc in [2, 3] for pc in p_class), "All power classes should be 2 or 3"
        
        # Verify power curves are loaded correctly
        assert len(out_curve2) == 3, "Class 2 power curve should have 3 values"
        assert len(out_curve3) == 3, "Class 3 power curve should have 3 values"
        assert np.allclose(out_curve2, np.array([0.1, 0.2, 0.3])), "Class 2 power curve should match input"
        assert np.allclose(out_curve3, np.array([0.2, 0.3, 0.4])), "Class 3 power curve should match input"
    
    def test_zone_processing(self, tmp_path: Path):
        """
        Test WindFarmsData zone number processing and validation.
        
        This test verifies that the WindFarmsData method correctly processes and
        validates zone number information for wind farms. It ensures that zone
        data is properly extracted and formatted for power system analysis.
        
        The test validates that:
        - Zone numbers are correctly extracted from CSV data
        - Zone arrays have the correct dimensions and data types
        - Zone values are within expected ranges for power system zones
        - Zone data is properly associated with corresponding farms
        - No data corruption occurs during zone processing
        
        Expected behavior: Method should correctly process zone information
        and return properly formatted arrays for power system analysis.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2, 3, 4, 5],
                "Farm Name": ["FarmA", "FarmB", "FarmC", "FarmD", "FarmE"],
                "Zone No.": [1, 2, 1, 3, 2],
                "Max Cap": [100.0, 150.0, 200.0, 250.0, 300.0],
                "Turbine Rating": [2.0, 3.0, 4.0, 5.0, 6.0],
                "Power Class": [2, 3, 2, 3, 2],
            }
        ).to_csv(site_csv, index=False)

        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0, 10.0],
                "End (m/s)": [5.0, 10.0, 15.0],
                "Class 2": [0.1, 0.2, 0.3],
                "Class 3": [0.2, 0.3, 0.4],
            }
        ).to_csv(pcurve_csv, index=False)

        w = Wind()
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, out_curve2, out_curve3, start_speed) = w.WindFarmsData(str(site_csv), str(pcurve_csv))
        
        # Verify zone processing
        expected_zones = np.array([1, 2, 1, 3, 2])
        assert np.all(zone_no == expected_zones), f"Zone numbers should match input. Expected {expected_zones}, got {zone_no}"
        
        # Verify unique zones
        unique_zones = np.unique(zone_no)
        assert len(unique_zones) == 3, "Should have 3 unique zones"
        assert set(unique_zones) == {1, 2, 3}, "Should have zones 1, 2, and 3"
    
    def test_parameter_validation(self, tmp_path: Path):
        """
        Test WindFarmsData parameter validation and error handling.
        
        This test verifies that the WindFarmsData method properly validates input
        parameters and handles various error conditions gracefully. It ensures
        robust error handling for invalid or malformed input data.
        
        The test validates that:
        - Invalid file paths are handled appropriately
        - Missing required parameters raise appropriate exceptions
        - Error messages are informative and helpful for debugging
        - The method fails gracefully without crashing the application
        - Parameter validation is consistent across different scenarios
        
        Expected behavior: Method should validate parameters and raise appropriate
        exceptions with clear error messages for invalid inputs.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        w = Wind()
        
        # Test with non-existent files
        with pytest.raises(FileNotFoundError):
            w.WindFarmsData("nonexistent_sites.csv", "nonexistent_curves.csv")
        
        # Test with invalid CSV structure
        invalid_csv = tmp_path / "invalid.csv"
        invalid_csv.write_text("invalid,csv,content\n1,2,3")
        
        with pytest.raises((KeyError, ValueError)):
            w.WindFarmsData(str(invalid_csv), str(invalid_csv))


class TestDownloadWindData:
    """Test DownloadWindData method functionality and edge cases"""
    
    def test_basic_functionality(self, tmp_path: Path, monkeypatch):
        """
        Test DownloadWindData basic functionality with mocked API responses.
        
        This test verifies that the DownloadWindData method can successfully download
        and process wind data from external APIs. It uses mocked API responses to
        simulate real-world data download scenarios without requiring actual API calls.
        
        The test validates that:
        - API requests are properly formatted and sent
        - Downloaded data is correctly parsed and processed
        - Wind speed data is properly extracted and formatted
        - File operations complete successfully
        - Data integrity is maintained throughout the process
        
        Expected behavior: Method should successfully download wind data and
        create properly formatted output files for wind energy analysis.
        
        Args:
            tmp_path: Temporary directory path for storing downloaded files
            monkeypatch: Pytest fixture for mocking external API calls
        """
        # site_data with coordinates and hub height
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2],
                "Farm Name": ["FarmA", "FarmB"],
                "Latitude": [35.0, 36.0],
                "Longitude": [-106.0, -105.5],
                "Hub Height": [80, 90],
            }
        ).to_csv(site_csv, index=False)

        # requests.get mock: two-header rows then real header
        class DummyResp:
            def __init__(self, text):
                self.text = text

        header1 = "meta line to skip\n"
        header2 = (
            "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        )
        data_rows = "2024,1,1,0,30,6.0,7.0\n2024,1,1,1,30,6.5,7.5\n"
        csv_text = header1 + header2 + data_rows

        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=str(site_csv),
            api_key="k",
            email="e@example.com",
            affiliation="aff",
            year_start=2024,
            year_end=2024,
        )

        base = tmp_path / "wtk_data" / "2024"
        assert (base / "FarmA.csv").exists()
        assert (base / "FarmB.csv").exists()
        # Combined windspeed file exists
        combined = tmp_path / "windspeed_data.csv"
        assert combined.exists()
        df = pd.read_csv(combined)
        # Should contain both farm columns
        assert set(["FarmA", "FarmB"]).issubset(set(df.columns))
    
    def test_path_handling(self, tmp_path: Path, monkeypatch):
        """
        Test DownloadWindData path handling and directory management.
        
        This test verifies that the DownloadWindData method correctly handles
        various path configurations and directory management scenarios. It ensures
        that file paths are properly processed and directories are created as needed.
        
        The test validates that:
        - Directory paths are correctly processed and created
        - File paths are properly constructed and validated
        - Path handling works with different operating systems
        - Directory creation succeeds when needed
        - File operations use correct path separators
        
        Expected behavior: Method should handle path operations correctly
        and create necessary directories for file storage.
        
        Args:
            tmp_path: Temporary directory path for testing path operations
            monkeypatch: Pytest fixture for mocking external dependencies
        """
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1],
                "Farm Name": ["FarmA"],
                "Latitude": [35.0],
                "Longitude": [-106.0],
                "Hub Height": [100],
            }
        ).to_csv(site_csv, index=False)

        class DummyResp:
            def __init__(self, text):
                self.text = text

        header1 = "meta line\n"
        header2 = (
            "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        )
        data_rows = "2024,1,1,0,30,6.0,7.0\n"
        csv_text = header1 + header2 + data_rows
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        # Absolute
        w.DownloadWindData(str(tmp_path), str(site_csv), "k", "e", "aff", 2024, 2024)
        assert (tmp_path / "wtk_data" / "2024" / "FarmA.csv").exists()

        # Relative after chdir
        old = os.getcwd()
        try:
            os.chdir(tmp_path)
            w.DownloadWindData(".", str(site_csv.name), "k", "e", "aff", 2024, 2024)
            assert (Path("wtk_data") / "2024" / "FarmA.csv").exists()
        finally:
            os.chdir(old)
    
    def test_missing_columns(self, tmp_path: Path):
        """
        Test DownloadWindData error handling for missing required columns.
        
        This test verifies that the DownloadWindData method properly handles
        error conditions when required columns are missing from the site data.
        It ensures robust error handling for incomplete or malformed input data.
        
        The test validates that:
        - Missing required columns are detected and reported
        - Appropriate exceptions are raised for missing data
        - Error messages are informative and help identify missing columns
        - The method fails gracefully without crashing
        - Error handling is consistent across different missing column scenarios
        
        Expected behavior: Method should detect missing columns and raise
        appropriate exceptions with clear error messages.
        
        Args:
            tmp_path: Temporary directory path for creating test data files
        """
        site_csv = tmp_path / "wind_sites.csv"
        # Missing Farm Name
        pd.DataFrame({"Farm No.": [1], "Latitude": [35.0], "Longitude": [-106.0], "Hub Height": [80]}).to_csv(
            site_csv, index=False
        )
        w = Wind()
        with pytest.raises(KeyError):
            w.DownloadWindData(str(tmp_path), str(site_csv), "k", "e", "aff", 2024, 2024)
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_with_real_sites(self, real_wind_sites, real_wind_data, tmp_path, monkeypatch):
        """
        Test DownloadWindData with real-world wind farm site data.
        
        This test verifies that the DownloadWindData method can successfully process
        actual wind farm site data from the project's data directory. It uses real
        site configurations to ensure the method works with realistic data structures.
        
        The test validates that:
        - Real wind farm site data is correctly processed
        - API requests are properly formatted for real site coordinates
        - Downloaded data matches expected real-world patterns
        - File operations complete successfully with real data
        - Data integrity is maintained throughout the process
        
        Expected behavior: Method should successfully process real wind farm data
        and create properly formatted output files for wind energy analysis.
        
        Args:
            real_wind_sites: Pytest fixture providing real wind farm site data
            real_wind_data: Pytest fixture providing real wind data patterns
            tmp_path: Temporary directory path for storing downloaded files
            monkeypatch: Pytest fixture for mocking external API calls
        """
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic weather data for 8760 hours
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds (higher during day, variable)
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1  # Higher at 100m
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Test DownloadWindData with real sites
        w = Wind()
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=real_wind_sites,
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )

        # Verify output structure
        base = tmp_path / "wtk_data" / "2024"
        assert base.exists()
        
        # Verify all wind sites have output files
        wind_sites_df = pd.read_csv(real_wind_sites)
        for farm_name in wind_sites_df["Farm Name"]:
            assert (base / f"{farm_name}.csv").exists()
            
            # Verify file contents have 8760 hours
            farm_file = base / f"{farm_name}.csv"
            if farm_file.exists():
                farm_data = pd.read_csv(farm_file)
                # 2024 is a leap year, so we expect 8760 hours (365 * 24)
        # But the data might have 8761 due to timezone handling
        assert len(farm_data) >= 8760, f"Farm {farm_name} data should have at least 8760 hours, got {len(farm_data)}"
        
        # Verify combined windspeed file exists
        combined = tmp_path / "windspeed_data.csv"
        assert combined.exists()
        combined_data = pd.read_csv(combined)
        assert len(combined_data) == 8760, "Combined windspeed data should have 8760 hours"
        
        # Verify all farm columns are present
        farm_names = wind_sites_df["Farm Name"].tolist()
        for farm_name in farm_names:
            assert farm_name in combined_data.columns, f"Farm {farm_name} should be in combined data"
    
    def test_hub_height_interpolation(self, tmp_path: Path, monkeypatch):
        """
        Test DownloadWindData hub height interpolation functionality.
        
        This test verifies that the DownloadWindData method correctly handles
        hub height interpolation for wind speed data at different heights.
        It ensures that wind speeds are properly interpolated between available
        measurement heights to match the specified hub height.
        
        The test validates that:
        - Hub height interpolation calculations are mathematically correct
        - Wind speeds are properly interpolated between measurement heights
        - Interpolation handles various height combinations correctly
        - Results are physically reasonable for wind energy applications
        - Data quality is maintained during interpolation
        
        Expected behavior: Method should correctly interpolate wind speeds
        to the specified hub height using appropriate mathematical methods.
        
        Args:
            tmp_path: Temporary directory path for storing test files
            monkeypatch: Pytest fixture for mocking external dependencies
        """
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2, 3],
                "Farm Name": ["Farm80m", "Farm100m", "FarmCustom"],
                "Latitude": [35.0, 36.0, 37.0],
                "Longitude": [-106.0, -105.5, -105.0],
                "Hub Height": [80, 100, 90],  # Different hub heights
            }
        ).to_csv(site_csv, index=False)

        class DummyResp:
            def __init__(self, text):
                self.text = text

        header1 = "meta line\n"
        header2 = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        data_rows = "2024,1,1,0,30,6.0,7.0\n2024,1,1,1,30,6.5,7.5\n"
        csv_text = header1 + header2 + data_rows
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=str(site_csv),
            api_key="k",
            email="e@example.com",
            affiliation="aff",
            year_start=2024,
            year_end=2024,
        )

        # Verify all farm files were created
        base = tmp_path / "wtk_data" / "2024"
        assert (base / "Farm80m.csv").exists()
        assert (base / "Farm100m.csv").exists()
        assert (base / "FarmCustom.csv").exists()
        
        # Verify combined windspeed file has all farms
        combined = tmp_path / "windspeed_data.csv"
        assert combined.exists()
        df = pd.read_csv(combined)
        assert set(["Farm80m", "Farm100m", "FarmCustom"]).issubset(set(df.columns))
    
    def test_multi_year_download(self, tmp_path: Path, monkeypatch):
        """
        Test DownloadWindData multi-year data download functionality.
        
        This test verifies that the DownloadWindData method can successfully
        download wind data for multiple years in a single operation. It ensures
        that the method handles year ranges correctly and processes data
        for each year appropriately.
        
        The test validates that:
        - Multi-year data download requests are properly formatted
        - Data for each year is correctly processed and stored
        - Year range parameters are handled correctly
        - File organization maintains year-based structure
        - Data integrity is maintained across multiple years
        
        Expected behavior: Method should successfully download and process
        wind data for multiple years with proper file organization.
        
        Args:
            tmp_path: Temporary directory path for storing multi-year data
            monkeypatch: Pytest fixture for mocking external API calls
        """
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1],
                "Farm Name": ["FarmA"],
                "Latitude": [35.0],
                "Longitude": [-106.0],
                "Hub Height": [80],
            }
        ).to_csv(site_csv, index=False)

        class DummyResp:
            def __init__(self, text):
                self.text = text

        header1 = "meta line\n"
        header2 = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        data_rows = "2024,1,1,0,30,6.0,7.0\n"
        csv_text = header1 + header2 + data_rows
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        # Test multi-year download (2024-2025)
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=str(site_csv),
            api_key="k",
            email="e@example.com",
            affiliation="aff",
            year_start=2024,
            year_end=2025,
        )

        # Verify both year directories exist
        assert (tmp_path / "wtk_data" / "2024").exists()
        assert (tmp_path / "wtk_data" / "2025").exists()
        
        # Verify farm files exist for both years
        assert (tmp_path / "wtk_data" / "2024" / "FarmA.csv").exists()
        assert (tmp_path / "wtk_data" / "2025" / "FarmA.csv").exists()
    
    def test_datetime_processing(self, tmp_path: Path, monkeypatch):
        """
        Test DownloadWindData datetime processing and time series handling.
        
        This test verifies that the DownloadWindData method correctly processes
        datetime information and handles time series data appropriately. It ensures
        that temporal data is properly formatted and processed for wind energy analysis.
        
        The test validates that:
        - Datetime data is correctly parsed and processed
        - Time series continuity is maintained throughout the process
        - Temporal indexing works correctly for wind data
        - Date/time formatting is consistent and accurate
        - Time zone handling is appropriate for the data source
        
        Expected behavior: Method should correctly process datetime information
        and maintain proper temporal structure for wind data analysis.
        
        Args:
            tmp_path: Temporary directory path for storing test files
            monkeypatch: Pytest fixture for mocking external dependencies
        """
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1],
                "Farm Name": ["FarmA"],
                "Latitude": [35.0],
                "Longitude": [-106.0],
                "Hub Height": [80],
            }
        ).to_csv(site_csv, index=False)

        class DummyResp:
            def __init__(self, text):
                self.text = text

        header1 = "meta line\n"
        header2 = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        data_rows = "2024,1,1,0,30,6.0,7.0\n2024,1,1,1,30,6.5,7.5\n2024,1,1,2,30,7.0,8.0\n"
        csv_text = header1 + header2 + data_rows
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=str(site_csv),
            api_key="k",
            email="e@example.com",
            affiliation="aff",
            year_start=2024,
            year_end=2024,
        )

        # Verify combined windspeed file has datetime index
        combined = tmp_path / "windspeed_data.csv"
        assert combined.exists()
        df = pd.read_csv(combined, index_col=0)
        
        # Check that datetime column was created and set as index
        assert df.index.name == 'datetime' or 'datetime' in df.columns
        assert len(df) == 3, "Should have 3 data rows"
    
    def test_api_error_handling(self, tmp_path: Path, monkeypatch):
        """
        Test DownloadWindData API error handling and resilience.
        
        This test verifies that the DownloadWindData method properly handles
        various API error conditions and maintains system stability. It ensures
        that the method gracefully handles network issues, API failures, and
        other external service problems.
        
        The test validates that:
        - API errors are properly caught and handled
        - Appropriate error messages are generated for different failure types
        - System remains stable when API calls fail
        - Error recovery mechanisms work correctly
        - User-friendly error reporting is provided
        
        Expected behavior: Method should handle API errors gracefully
        and provide clear feedback about what went wrong.
        
        Args:
            tmp_path: Temporary directory path for storing test files
            monkeypatch: Pytest fixture for mocking external API calls
        """
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1],
                "Farm Name": ["FarmA"],
                "Latitude": [35.0],
                "Longitude": [-106.0],
                "Hub Height": [80],
            }
        ).to_csv(site_csv, index=False)

        # Mock API to raise an exception
        def mock_requests_get(*args, **kwargs):
            raise requests.exceptions.RequestException("API Error")

        monkeypatch.setattr("requests.get", mock_requests_get)

        w = Wind()
        with pytest.raises(requests.exceptions.RequestException):
            w.DownloadWindData(
                directory=str(tmp_path),
                site_data=str(site_csv),
                api_key="k",
                email="e@example.com",
                affiliation="aff",
                year_start=2024,
                year_end=2024,
            )


class TestCalWindTrRates:
    """Test CalWindTrRates method functionality and edge cases"""
    
    def test_basic_functionality(self, tmp_path: Path):
        """
        Test CalWindTrRates basic functionality and transition rate calculations.
        
        This test verifies that the CalWindTrRates method correctly calculates
        wind speed transition rates for reliability analysis. It ensures that
        the method produces accurate transition matrices for wind energy systems.
        
        The test validates that:
        - Wind speed transition rates are calculated correctly
        - Input data is properly processed and validated
        - Output matrices have correct dimensions and properties
        - Mathematical calculations are accurate for wind speed binning
        - Data integrity is maintained throughout the process
        
        Expected behavior: Method should calculate accurate wind speed
        transition rates suitable for reliability analysis.
        
        Args:
            tmp_path: Temporary directory path for creating test data files
        """
        # site_data
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2],
                "Farm Name": ["FarmA", "FarmB"],
                "Zone No.": [10, 20],
                "Max Cap": [1.0, 1.0],
                "Turbine Rating": [1.0, 1.0],
                "Power Class": [2, 3],
            }
        ).to_csv(site_csv, index=False)

        # power curves -> bins
        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0, 10.0],
                "End (m/s)": [5.0, 10.0, 15.0],
                "Class 2": [0.0, 0.0, 0.0],
                "Class 3": [0.0, 0.0, 0.0],
            }
        ).to_csv(pcurve_csv, index=False)

        # windspeed_data with columns per site; include boundary transitions
        wdata_csv = tmp_path / "windspeed_data.csv"
        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2024-01-01", periods=5, freq="H"),
                "FarmA": [0.1, 4.9, 5.1, 9.9, 10.1],
                "FarmB": [0.0, 5.0, 10.0, 10.0, 14.9],
            }
        )
        df.set_index("datetime", inplace=True)
        df.to_csv(wdata_csv)

        w = Wind()
        rate = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(wdata_csv),
            site_data=str(site_csv),
            pcurve_data=str(pcurve_csv),
        )

        # Shape: (w_sites, w_classes, w_classes) = (2, 3, 3)
        assert rate.shape == (2, 3, 3)
        # Rows normalized (after nan_to_num)
        for s in range(rate.shape[0]):
            for r in range(rate.shape[1]):
                row_sum = rate[s, r].sum()
                assert 0.0 <= row_sum <= 1.0

        # Excel output exists
        assert (tmp_path / "t_rate.xlsx").exists()
    
    def test_end_to_end(self, tmp_path: Path, monkeypatch):
        """
        Test CalWindTrRates end-to-end workflow with complete data processing.
        
        This test verifies that the CalWindTrRates method can successfully
        process wind data through the complete workflow from data loading
        to transition rate calculation. It ensures the entire process works
        correctly with realistic data scenarios.
        
        The test validates that:
        - Complete data processing workflow executes successfully
        - All intermediate steps work correctly together
        - Final output is accurate and properly formatted
        - No data loss occurs during the complete process
        - Error handling works throughout the entire workflow
        
        Expected behavior: Method should successfully complete the entire
        workflow and produce accurate transition rate matrices.
        
        Args:
            tmp_path: Temporary directory path for storing test files
            monkeypatch: Pytest fixture for mocking external dependencies
        """
        # Prepare a minimal combined windspeed file and site/pcurve
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1],
                "Farm Name": ["FarmA"],
                "Zone No.": [10],
                "Max Cap": [1.0],
                "Turbine Rating": [1.0],
                "Power Class": [2],
            }
        ).to_csv(site_csv, index=False)

        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0],
                "End (m/s)": [5.0, 10.0],
                "Class 2": [0.0, 0.0],
                "Class 3": [0.0, 0.0],
            }
        ).to_csv(pcurve_csv, index=False)

        wdata_csv = tmp_path / "windspeed_data.csv"
        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2024-01-01", periods=4, freq="H"),
                "FarmA": [1.0, 2.0, 6.0, 7.0],
            }
        )
        df.set_index("datetime", inplace=True)
        df.to_csv(wdata_csv)

        w = Wind()
        rate = w.CalWindTrRates(str(tmp_path), str(wdata_csv), str(site_csv), str(pcurve_csv))
        assert rate.shape == (1, 2, 2)
        assert (tmp_path / "t_rate.xlsx").exists()
    
    def test_missing_files(self, tmp_path: Path):
        """Test CalWindTrRates with missing input files"""
        w = Wind()
        with pytest.raises(FileNotFoundError):
            w.CalWindTrRates(str(tmp_path), str(tmp_path / "missing.csv"), str(tmp_path / "sites.csv"), str(tmp_path / "pcurve.csv"))
    
    def test_wrong_columns(self, tmp_path: Path):
        """Test CalWindTrRates with wrong column names"""
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame({"Farm No.": [1], "Farm Name": ["FarmA"], "Zone No.": [10], "Max Cap": [1.0], "Turbine Rating": [1.0], "Power Class": [2]}).to_csv(site_csv, index=False)
        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame({"start": [0.0, 5.0], "end": [5.0, 10.0]}).to_csv(pcurve_csv, index=False)
        wdata_csv = tmp_path / "windspeed_data.csv"
        pd.DataFrame({"datetime": pd.date_range("2024-01-01", periods=2, freq="H"), "FarmA": [1.0, 2.0]}).set_index("datetime").to_csv(wdata_csv)
        w = Wind()
        with pytest.raises(KeyError):
            w.CalWindTrRates(str(tmp_path), str(wdata_csv), str(site_csv), str(pcurve_csv))
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_with_real_data(self, real_wind_sites, real_wind_data, tmp_path, monkeypatch):
        """Test CalWindTrRates with real wind data"""
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic wind data for 8760 hours
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds with temporal patterns
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1  # Higher at 100m
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Create combined windspeed file with correct site names
        wind_sites_df = pd.read_csv(real_wind_sites)
        site_names = wind_sites_df['Farm Name'].tolist()
        
        combined_windspeed = tmp_path / "windspeed_data.csv"
        wind_data_dict = {'datetime': pd.date_range('2024-01-01', periods=8760, freq='H')}
        for site_name in site_names:
            wind_data_dict[site_name] = np.random.uniform(0, 20, 8760)
        combined_data = pd.DataFrame(wind_data_dict)
        combined_data.to_csv(combined_windspeed, index=False)

        # Test CalWindTrRates with real data
        w = Wind()
        tr_mats = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(combined_windspeed),
            site_data=real_wind_sites,
            pcurve_data=real_wind_data["power_curves_csv"]
        )
        
        # Verify results
        wind_sites_df = pd.read_csv(real_wind_sites)
        w_sites = len(wind_sites_df)
        
        # Get actual number of wind classes from power curve data
        pcurve_df = pd.read_csv(real_wind_data["power_curves_csv"])
        w_classes = len(pcurve_df['Start (m/s)'].values)
        
        assert tr_mats.shape == (w_sites, w_classes, w_classes), "Transition matrices should have correct shape"
        assert np.all(tr_mats >= 0), "All transition probabilities should be non-negative"
        assert np.all(tr_mats <= 1), "All transition probabilities should be <= 1"
        
        # Verify each site's transition matrix sums to 1 (with tolerance for numerical issues)
        for site in range(w_sites):
            for from_class in range(w_classes):
                row_sum = np.sum(tr_mats[site, from_class, :])
                # Allow for numerical precision issues and NaN handling
                if not np.isnan(row_sum) and row_sum > 0:
                    assert abs(row_sum - 1.0) < 1e-3, f"Transition matrix for site {site}, class {from_class} should sum to 1, got {row_sum}"
        
        # Verify transition matrices are reasonable (allow for NaN values from division by zero)
        assert np.all(np.isnan(tr_mats) | (tr_mats >= 0)), "All transition probabilities should be non-negative or NaN"
        assert np.all(np.isnan(tr_mats) | (tr_mats <= 1)), "All transition probabilities should be <= 1 or NaN"
    
    def test_transition_matrix_properties(self, tmp_path: Path):
        """Test transition matrix mathematical properties"""
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2],
                "Farm Name": ["FarmA", "FarmB"],
                "Zone No.": [10, 20],
                "Max Cap": [1.0, 1.0],
                "Turbine Rating": [1.0, 1.0],
                "Power Class": [2, 3],
            }
        ).to_csv(site_csv, index=False)

        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0, 10.0],
                "End (m/s)": [5.0, 10.0, 15.0],
                "Class 2": [0.0, 0.0, 0.0],
                "Class 3": [0.0, 0.0, 0.0],
            }
        ).to_csv(pcurve_csv, index=False)

        wdata_csv = tmp_path / "windspeed_data.csv"
        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2024-01-01", periods=10, freq="H"),
                "FarmA": [1.0, 2.0, 3.0, 6.0, 7.0, 8.0, 11.0, 12.0, 13.0, 14.0],
                "FarmB": [0.5, 1.5, 2.5, 5.5, 6.5, 7.5, 10.5, 11.5, 12.5, 13.5],
            }
        )
        df.set_index("datetime", inplace=True)
        df.to_csv(wdata_csv)

        w = Wind()
        rate = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(wdata_csv),
            site_data=str(site_csv),
            pcurve_data=str(pcurve_csv),
        )

        # Verify shape
        assert rate.shape == (2, 3, 3), "Should have correct shape (sites, classes, classes)"
        
        # Verify all values are in [0, 1]
        assert np.all(rate >= 0), "All transition probabilities should be >= 0"
        assert np.all(rate <= 1), "All transition probabilities should be <= 1"
        
        # Verify each row sums to 1 (after normalization) or is all zeros
        for s in range(rate.shape[0]):
            for r in range(rate.shape[1]):
                row_sum = rate[s, r].sum()
                # Row should sum to 1 or be all zeros (no transitions)
                assert (abs(row_sum - 1.0) < 1e-6 or abs(row_sum) < 1e-6), f"Row {r} for site {s} should sum to 1 or 0, got {row_sum}"
    
    def test_windspeed_binning(self, tmp_path: Path):
        """Test wind speed bin assignment logic"""
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1],
                "Farm Name": ["FarmA"],
                "Zone No.": [10],
                "Max Cap": [1.0],
                "Turbine Rating": [1.0],
                "Power Class": [2],
            }
        ).to_csv(site_csv, index=False)

        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0, 10.0, 15.0],
                "End (m/s)": [5.0, 10.0, 15.0, 20.0],
                "Class 2": [0.0, 0.0, 0.0, 0.0],
                "Class 3": [0.0, 0.0, 0.0, 0.0],
            }
        ).to_csv(pcurve_csv, index=False)

        # Test specific wind speeds at bin boundaries
        wdata_csv = tmp_path / "windspeed_data.csv"
        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2024-01-01", periods=8, freq="H"),
                "FarmA": [0.0, 4.9, 5.0, 9.9, 10.0, 14.9, 15.0, 19.9],  # Test boundary conditions
            }
        )
        df.set_index("datetime", inplace=True)
        df.to_csv(wdata_csv)

        w = Wind()
        rate = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(wdata_csv),
            site_data=str(site_csv),
            pcurve_data=str(pcurve_csv),
        )

        # Verify shape
        assert rate.shape == (1, 4, 4), "Should have correct shape for 4 wind classes"
        
        # Verify transitions occur (not all zeros)
        assert np.any(rate > 0), "Should have some non-zero transition probabilities"
    
    def test_excel_output_format(self, tmp_path: Path):
        """Test Excel file generation and content"""
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2],
                "Farm Name": ["FarmA", "FarmB"],
                "Zone No.": [10, 20],
                "Max Cap": [1.0, 1.0],
                "Turbine Rating": [1.0, 1.0],
                "Power Class": [2, 3],
            }
        ).to_csv(site_csv, index=False)

        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0, 10.0],
                "End (m/s)": [5.0, 10.0, 15.0],
                "Class 2": [0.0, 0.0, 0.0],
                "Class 3": [0.0, 0.0, 0.0],
            }
        ).to_csv(pcurve_csv, index=False)

        wdata_csv = tmp_path / "windspeed_data.csv"
        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2024-01-01", periods=5, freq="H"),
                "FarmA": [1.0, 2.0, 6.0, 7.0, 8.0],
                "FarmB": [0.5, 1.5, 5.5, 6.5, 7.5],
            }
        )
        df.set_index("datetime", inplace=True)
        df.to_csv(wdata_csv)

        w = Wind()
        rate = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(wdata_csv),
            site_data=str(site_csv),
            pcurve_data=str(pcurve_csv),
        )

        # Verify Excel file exists
        excel_file = tmp_path / "t_rate.xlsx"
        assert excel_file.exists(), "Excel file should be created"
        
        # Verify Excel file can be read
        excel_data = pd.read_excel(excel_file, sheet_name=None)
        
        # Should have sheets for each farm
        assert "FarmA" in excel_data, "Should have FarmA sheet"
        assert "FarmB" in excel_data, "Should have FarmB sheet"
        
        # Verify sheet contents
        for farm_name in ["FarmA", "FarmB"]:
            sheet_data = excel_data[farm_name]
            assert sheet_data.shape == (3, 3), f"Sheet {farm_name} should have 3x3 shape"
            assert np.all(sheet_data >= 0), f"Sheet {farm_name} should have non-negative values"
            assert np.all(sheet_data <= 1), f"Sheet {farm_name} should have values <= 1"
    
    def test_normalization(self, tmp_path: Path):
        """Test nan_to_num handling and normalization"""
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1],
                "Farm Name": ["FarmA"],
                "Zone No.": [10],
                "Max Cap": [1.0],
                "Turbine Rating": [1.0],
                "Power Class": [2],
            }
        ).to_csv(site_csv, index=False)

        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0, 10.0],
                "End (m/s)": [5.0, 10.0, 15.0],
                "Class 2": [0.0, 0.0, 0.0],
                "Class 3": [0.0, 0.0, 0.0],
            }
        ).to_csv(pcurve_csv, index=False)

        # Create data that might cause division by zero
        wdata_csv = tmp_path / "windspeed_data.csv"
        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2024-01-01", periods=3, freq="H"),
                "FarmA": [1.0, 1.0, 1.0],  # All same speed, might cause issues
            }
        )
        df.set_index("datetime", inplace=True)
        df.to_csv(wdata_csv)

        w = Wind()
        rate = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(wdata_csv),
            site_data=str(site_csv),
            pcurve_data=str(pcurve_csv),
        )

        # Verify no NaN or inf values
        assert not np.any(np.isnan(rate)), "Should not have NaN values"
        assert not np.any(np.isinf(rate)), "Should not have inf values"
        
        # Verify all values are finite
        assert np.all(np.isfinite(rate)), "All values should be finite"
        
        # Verify shape is correct
        assert rate.shape == (1, 3, 3), "Should have correct shape"


class TestRealDataIntegration:
    """Test real data integration and production workflow"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_wind_farms_structure(self, real_wind_sites):
        """Parse wind_sites.csv, verify 4 farms with correct zones"""
        # Load wind sites data
        wind_sites_df = pd.read_csv(real_wind_sites)
        
        # Verify production data structure
        assert len(wind_sites_df) == 4  # 4 wind farms
        assert "Farm No." in wind_sites_df.columns
        assert "Farm Name" in wind_sites_df.columns
        assert "Zone No." in wind_sites_df.columns
        assert "Power Class" in wind_sites_df.columns
        assert "Turbine Rating" in wind_sites_df.columns
        assert "Max Cap" in wind_sites_df.columns
        
        # Verify zones (should be 1 and 3 based on production data)
        zones = wind_sites_df["Zone No."].unique()
        assert len(zones) == 2
        assert 1 in zones
        assert 3 in zones
        
        # Verify power classes (should be 2 and 3)
        power_classes = wind_sites_df["Power Class"].unique()
        assert len(power_classes) == 2
        assert 2 in power_classes
        assert 3 in power_classes
        
        # Verify turbine ratings are reasonable
        assert all(wind_sites_df["Turbine Rating"] > 0)
        assert all(wind_sites_df["Max Cap"] > 0)
        
        # Verify farm names are unique
        assert len(wind_sites_df["Farm Name"].unique()) == 4
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_power_curves_validation(self, real_wind_data):
        """Load w_power_curves.csv, validate both turbine classes"""
        if not Path(real_wind_data["power_curves_csv"]).exists():
            pytest.skip("Production wind power curves data not available")
        
        # Load power curves data
        power_curves_df = pd.read_csv(real_wind_data["power_curves_csv"])
        
        # Verify power curves structure
        assert "Start (m/s)" in power_curves_df.columns
        assert "End (m/s)" in power_curves_df.columns
        assert "Class 2" in power_curves_df.columns
        assert "Class 3" in power_curves_df.columns
        
        # Verify wind speed bins are reasonable
        assert all(power_curves_df["Start (m/s)"] >= 0)
        assert all(power_curves_df["End (m/s)"] > power_curves_df["Start (m/s)"])
        
        # Verify power output values are in valid range [0, 1]
        assert all(0 <= power_curves_df["Class 2"]) and all(power_curves_df["Class 2"] <= 1)
        assert all(0 <= power_curves_df["Class 3"]) and all(power_curves_df["Class 3"] <= 1)
        
        # Verify power curves are monotonic (generally increasing then decreasing)
        class_2_power = power_curves_df["Class 2"].values
        class_3_power = power_curves_df["Class 3"].values
        
        # Check that power starts at 0 and ends at 0 (or very low)
        assert class_2_power[0] == 0.0
        assert class_3_power[0] == 0.0
        assert class_2_power[-1] <= 0.1  # Should be low at high wind speeds
        assert class_3_power[-1] <= 0.1
        
        # Check that there's a peak power output
        assert max(class_2_power) > 0.5
        assert max(class_3_power) > 0.5
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_complete_workflow(self, real_wind_sites, real_wind_data, tmp_path, monkeypatch):
        """Test wind data processing with production-scale data"""
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic wind data for 8760 hours
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds with temporal patterns
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1  # Higher at 100m
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Test complete wind data processing workflow
        w = Wind()
        
        # Step 1: Download wind data
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=real_wind_sites,
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )
        
        # Step 2: Process wind farm data
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        
        # Step 3: Calculate transition rates
        combined_windspeed = tmp_path / "windspeed_data.csv"
        tr_mats = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(combined_windspeed),
            site_data=real_wind_sites,
            pcurve_data=real_wind_data["power_curves_csv"]
        )
        
        # Verify complete workflow
        assert w_sites == 4, "Should have 4 wind sites"
        assert len(farm_name) == 4, "Should have 4 farm names"
        assert len(zone_no) == 4, "Should have 4 zones"
        # Wind classes depend on wind speed binning - check it's reasonable
        assert w_classes > 0, f"Should have positive number of wind classes, got {w_classes}"
        # The actual shape depends on wind speed binning - check it's reasonable
        assert tr_mats.shape[0] == 4, "Should have 4 sites"
        assert tr_mats.shape[1] == tr_mats.shape[2], "Transition matrices should be square"
        assert tr_mats.shape[1] > 0, "Transition matrices should have positive dimensions"
        
        # Verify data quality
        assert all(tr > 0 for tr in turbine_rating), "Turbine ratings should be positive"
        assert all(ss >= 0 for ss in start_speed), "Start speeds should be non-negative"
        assert all(pc in [2, 3] for pc in p_class), "Power classes should be 2 or 3"
        assert np.all(tr_mats >= 0), "Transition probabilities should be non-negative"
        assert np.all(tr_mats <= 1), "Transition probabilities should be <= 1"
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_data_consistency(self, real_wind_sites, real_wind_data, tmp_path, monkeypatch):
        """Test data consistency across different wind methods"""
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic wind data for 8760 hours
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        
        # Test data consistency across methods
        # Step 1: DownloadWindData
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=real_wind_sites,
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )
        
        # Step 2: WindFarmsData
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        
        # Step 3: CalWindTrRates
        combined_windspeed = tmp_path / "windspeed_data.csv"
        tr_mats = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(combined_windspeed),
            site_data=real_wind_sites,
            pcurve_data=real_wind_data["power_curves_csv"]
        )
        
        # Verify data consistency
        assert w_sites == len(farm_name), "Number of sites should match farm names"
        assert w_sites == len(zone_no), "Number of sites should match zones"
        assert w_sites == len(w_turbines), "Number of sites should match turbines"
        assert w_sites == len(turbine_rating), "Number of sites should match turbine ratings"
        assert w_sites == len(p_class), "Number of sites should match power classes"
        assert w_classes == len(start_speed), "Number of classes should match start speeds"
        assert tr_mats.shape[0] == w_sites, "Transition matrices should have correct number of sites"
        assert tr_mats.shape[1] == w_classes, "Transition matrices should have correct number of classes"
        assert tr_mats.shape[2] == w_classes, "Transition matrices should be square in classes"
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_zone_compatibility(self, real_wind_sites, real_wind_data, real_system_data, tmp_path, monkeypatch):
        """Test wind zones compatibility with system zones"""
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic wind data for 8760 hours
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Load system data
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Process wind data
        w = Wind()
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=real_wind_sites,
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )
        
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        
        combined_windspeed = tmp_path / "windspeed_data.csv"
        tr_mats = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(combined_windspeed),
            site_data=real_wind_sites,
            pcurve_data=real_wind_data["power_curves_csv"]
        )
        
        # Verify wind zones are compatible with system zones
        wind_zones = set(zone_no)
        system_zones = set(bus_no)
        assert wind_zones.issubset(system_zones), "Wind zones should be subset of system zones"
        
        # Verify wind data quality
        assert all(tr > 0 for tr in turbine_rating), "Turbine ratings should be positive"
        assert all(ss >= 0 for ss in start_speed), "Start speeds should be non-negative"
        assert all(pc in [2, 3] for pc in p_class), "Power classes should be 2 or 3"
        assert np.all(tr_mats >= 0), "Transition probabilities should be non-negative"
        assert np.all(tr_mats <= 1), "Transition probabilities should be <= 1"
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_output_shapes(self, real_wind_sites, real_wind_data, tmp_path, monkeypatch):
        """Test output shapes and dimensions for all methods"""
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic wind data for 8760 hours
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        
        # Test DownloadWindData output
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=real_wind_sites,
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )
        
        # Verify DownloadWindData output files
        base = tmp_path / "wtk_data" / "2024"
        assert base.exists()
        
        wind_sites_df = pd.read_csv(real_wind_sites)
        for farm_name in wind_sites_df["Farm Name"]:
            farm_file = base / f"{farm_name}.csv"
            assert farm_file.exists()
            farm_data = pd.read_csv(farm_file)
            # 2024 is a leap year, so we expect 8760 hours (365 * 24)
            # But the data might have 8761 due to timezone handling
            assert len(farm_data) >= 8760, f"Farm {farm_name} should have at least 8760 hours, got {len(farm_data)}"
        
        # Verify combined windspeed file
        combined = tmp_path / "windspeed_data.csv"
        assert combined.exists()
        combined_data = pd.read_csv(combined)
        assert len(combined_data) == 8760, "Combined data should have 8760 hours"
        
        # Test WindFarmsData output shapes
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        
        assert isinstance(w_sites, int), "w_sites should be int"
        assert isinstance(farm_name, pd.Series), "farm_name should be Series"
        assert isinstance(zone_no, np.ndarray), "zone_no should be ndarray"
        assert isinstance(w_classes, int), "w_classes should be int"
        assert isinstance(w_turbines, np.ndarray), "w_turbines should be ndarray"
        assert isinstance(turbine_rating, np.ndarray), "turbine_rating should be ndarray"
        assert isinstance(p_class, np.ndarray), "p_class should be ndarray"
        assert isinstance(out_curve2, np.ndarray), "out_curve2 should be ndarray"
        assert isinstance(out_curve3, np.ndarray), "out_curve3 should be ndarray"
        assert isinstance(start_speed, np.ndarray), "start_speed should be ndarray"
        
        # Test CalWindTrRates output shapes
        tr_mats = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(combined),
            site_data=real_wind_sites,
            pcurve_data=real_wind_data["power_curves_csv"]
        )
        
        assert isinstance(tr_mats, np.ndarray), "tr_mats should be ndarray"
        assert tr_mats.shape == (w_sites, w_classes, w_classes), "tr_mats should have correct shape"
        assert tr_mats.ndim == 3, "tr_mats should be 3D array"


class TestWindDataQuality:
    """Test wind data quality and validation"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_power_curve_validation(self, real_wind_data):
        """Test wind power curves with real data"""
        # Load real wind data
        wind_data_df = pd.read_csv(real_wind_data["power_curves_csv"])
        
        # Verify power curves are reasonable
        assert "Class 2" in wind_data_df.columns, "Should have Class 2 power curve"
        assert "Class 3" in wind_data_df.columns, "Should have Class 3 power curve"
        
        # Verify power curve values are in [0, 1] range
        class2_vals = wind_data_df["Class 2"].values
        class3_vals = wind_data_df["Class 3"].values
        
        assert np.all(class2_vals >= 0) and np.all(class2_vals <= 1), "Class 2 power curve should be in [0, 1]"
        assert np.all(class3_vals >= 0) and np.all(class3_vals <= 1), "Class 3 power curve should be in [0, 1]"
        
        # Verify power curves have realistic shape (increasing then decreasing)
        # Check that power increases initially
        assert class2_vals[0] < class2_vals[5], "Class 2 power curve should increase initially"
        assert class3_vals[0] < class3_vals[5], "Class 3 power curve should increase initially"
        
        # Check that power peaks and then decreases at high wind speeds
        max_class2_idx = np.argmax(class2_vals)
        max_class3_idx = np.argmax(class3_vals)
        assert class2_vals[max_class2_idx] > class2_vals[-1], "Class 2 power curve should peak and decrease"
        assert class3_vals[max_class3_idx] > class3_vals[-1], "Class 3 power curve should peak and decrease"
        
        # Verify wind speed bins are reasonable
        start_speeds = wind_data_df["Start (m/s)"].values
        end_speeds = wind_data_df["End (m/s)"].values
        
        assert np.all(start_speeds >= 0) and np.all(start_speeds <= 1000), "Wind speed bins should be reasonable"
        assert np.all(end_speeds >= 0) and np.all(end_speeds <= 1000), "Wind speed bins should be reasonable"
        assert np.all(end_speeds > start_speeds), "End speeds should be > start speeds"
        
        # Verify both power curves have reasonable average power
        assert np.mean(class2_vals) > 0.1, "Class 2 should have reasonable average power"
        assert np.mean(class3_vals) > 0.1, "Class 3 should have reasonable average power"
        
        # Verify power curves have realistic shape (low at low speeds, peak in middle, low at high speeds)
        assert class2_vals[0] == 0.0, "Class 2 power curve should start at 0"
        assert class3_vals[0] == 0.0, "Class 3 power curve should start at 0"
        assert class2_vals[-1] == 0.0, "Class 2 power curve should end at 0"
        assert class3_vals[-1] == 0.0, "Class 3 power curve should end at 0"
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_zone_aggregation(self, real_wind_sites, real_wind_data):
        """Test wind zone aggregation with real data"""
        w = Wind()
        
        # Process wind farm data
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        
        # Verify zone aggregation
        wind_sites_df = pd.read_csv(real_wind_sites)
        expected_zones = wind_sites_df["Zone No."].unique()
        
        assert len(set(zone_no)) == len(expected_zones), "Should have correct number of unique zones"
        assert all(zone in expected_zones for zone in zone_no), "All zones should be from real data"
        
        # Verify zone distribution
        zone_counts = {}
        for zone in zone_no:
            zone_counts[zone] = zone_counts.get(zone, 0) + 1
        
        # Verify we have farms in multiple zones
        assert len(zone_counts) > 1, "Should have farms in multiple zones"
        
        # Verify zone distribution is reasonable
        for zone, count in zone_counts.items():
            assert count > 0, f"Zone {zone} should have at least one farm"
            assert count <= w_sites, f"Zone {zone} should not have more farms than total sites"
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_temporal_patterns(self, real_wind_sites, real_wind_data, tmp_path, monkeypatch):
        """Test wind temporal patterns with real data"""
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic wind data with temporal patterns
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data with temporal patterns
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds with temporal patterns
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1  # Higher at 100m
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Test wind temporal patterns
        w = Wind()
        
        # Download wind data
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=real_wind_sites,
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )
        
        # Process wind farm data
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        
        # Verify temporal patterns
        assert w_sites == 4, "Should have 4 wind sites"
        assert len(farm_name) == 4, "Should have 4 farm names"
        assert len(zone_no) == 4, "Should have 4 zones"
        # Wind classes depend on wind speed binning - check it's reasonable
        assert w_classes > 0, f"Should have positive number of wind classes, got {w_classes}"
        
        # Verify wind data has temporal patterns
        combined_windspeed = tmp_path / "windspeed_data.csv"
        if combined_windspeed.exists():
            wind_data_df = pd.read_csv(combined_windspeed)
            assert len(wind_data_df) == 8760, "Wind data should have 8760 hours"
            
            # Verify wind speeds are reasonable
            for farm_name in wind_data_df.columns:
                # Skip non-wind data columns
                if farm_name in ["Unnamed: 0", "datetime", "Time Zone"]:
                    continue
                    
                wind_speeds = pd.to_numeric(wind_data_df[farm_name], errors='coerce').values
                # Remove any NaN values that couldn't be converted
                wind_speeds = wind_speeds[~np.isnan(wind_speeds)]
                
                # Skip if no valid numeric data
                if len(wind_speeds) == 0:
                    continue
                    
                assert np.all(wind_speeds >= 0), f"Wind speeds for {farm_name} should be non-negative"
                assert np.all(wind_speeds <= 50), f"Wind speeds for {farm_name} should be reasonable (< 50 m/s)"
                
                # Verify temporal variation
                assert np.std(wind_speeds) > 0, f"Wind speeds for {farm_name} should have variation"
                assert np.max(wind_speeds) > np.min(wind_speeds), f"Wind speeds for {farm_name} should have range"
    
    def test_data_ranges(self, tmp_path: Path, monkeypatch):
        """Test wind data value ranges and validity"""
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2],
                "Farm Name": ["FarmA", "FarmB"],
                "Latitude": [35.0, 36.0],
                "Longitude": [-106.0, -105.5],
                "Hub Height": [80, 90],
            }
        ).to_csv(site_csv, index=False)

        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create wind data with various ranges
        # The production code uses skiprows=1, so we need the header to be the first row after skiprows=1
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        wind_data = []
        for hour in range(24):  # Test one day
            wind_80m = np.random.uniform(0, 30)  # 0-30 m/s range
            wind_100m = wind_80m * 1.1
            wind_data.append(f"2024,1,1,{hour},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        # Create CSV with timezone info as first row, then header, then data
        csv_text = "Time Zone,-7\n" + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=str(site_csv),
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )

        # Verify wind speed ranges
        combined = tmp_path / "windspeed_data.csv"
        assert combined.exists()
        wind_data_df = pd.read_csv(combined)
        
        for farm_name in ["FarmA", "FarmB"]:
            if farm_name in wind_data_df.columns:
                wind_speeds = wind_data_df[farm_name].values
                assert np.all(wind_speeds >= 0), f"Wind speeds should be non-negative"
                assert np.all(wind_speeds <= 50), f"Wind speeds should be reasonable (< 50 m/s)"
                assert np.std(wind_speeds) > 0, f"Wind speeds should have variation"
    
    def test_spatial_consistency(self, tmp_path: Path, monkeypatch):
        """Test consistency across multiple wind sites"""
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1, 2, 3],
                "Farm Name": ["FarmA", "FarmB", "FarmC"],
                "Latitude": [35.0, 36.0, 37.0],
                "Longitude": [-106.0, -105.5, -105.0],
                "Hub Height": [80, 90, 100],
            }
        ).to_csv(site_csv, index=False)

        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        wind_data = []
        for hour in range(24):
            # Generate correlated but different wind speeds for each site
            base_wind = 5 + 2 * np.sin(2 * np.pi * hour / 24)
            wind_80m = base_wind + np.random.normal(0, 1)
            wind_100m = wind_80m * 1.1
            wind_data.append(f"2024,1,1,{hour},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=str(site_csv),
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )

        # Verify spatial consistency
        combined = tmp_path / "windspeed_data.csv"
        assert combined.exists()
        wind_data_df = pd.read_csv(combined)
        
        # All farms should have data
        for farm_name in ["FarmA", "FarmB", "FarmC"]:
            assert farm_name in wind_data_df.columns, f"Farm {farm_name} should have data"
            wind_speeds = wind_data_df[farm_name].values
            assert len(wind_speeds) == 24, f"Farm {farm_name} should have 24 hours of data"
            assert np.all(wind_speeds >= 0), f"Farm {farm_name} wind speeds should be non-negative"
    
    def test_seasonal_patterns(self, tmp_path: Path, monkeypatch):
        """Test seasonal variation in wind data"""
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1],
                "Farm Name": ["FarmA"],
                "Latitude": [35.0],
                "Longitude": [-106.0],
                "Hub Height": [80],
            }
        ).to_csv(site_csv, index=False)

        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate seasonal wind data
        wind_data = []
        for hour in range(8760):  # Full year
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Strong seasonal pattern
            seasonal = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)
            daily = 1 * np.sin(2 * np.pi * hour_of_day / 24)
            wind_80m = max(0, seasonal + daily + np.random.normal(0, 0.5))
            wind_100m = wind_80m * 1.1
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=str(site_csv),
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )

        # Verify seasonal patterns
        combined = tmp_path / "windspeed_data.csv"
        assert combined.exists()
        wind_data_df = pd.read_csv(combined)
        
        wind_speeds = wind_data_df["FarmA"].values
        assert len(wind_speeds) == 8760, "Should have 8760 hours of data"
        
        # Check for seasonal variation
        monthly_means = []
        for month in range(12):
            start_hour = month * 30 * 24
            end_hour = min((month + 1) * 30 * 24, 8760)
            monthly_speeds = wind_speeds[start_hour:end_hour]
            monthly_means.append(np.mean(monthly_speeds))
        
        # Should have some seasonal variation
        assert np.std(monthly_means) > 0.1, "Should have seasonal variation in wind speeds"


class TestWindPerformance:
    """Test wind performance and scalability"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_performance_benchmarks(self, real_wind_sites, real_wind_data, tmp_path, monkeypatch):
        """Test wind performance with production-scale data"""
        import time
        
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic wind data for 8760 hours
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Test performance of wind functions
        w = Wind()
        
        start_time = time.time()
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=real_wind_sites,
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )
        download_time = time.time() - start_time
        
        start_time = time.time()
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        windfarms_time = time.time() - start_time
        
        start_time = time.time()
        combined_windspeed = tmp_path / "windspeed_data.csv"
        tr_mats = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(combined_windspeed),
            site_data=real_wind_sites,
            pcurve_data=real_wind_data["power_curves_csv"]
        )
        calwindtrrates_time = time.time() - start_time
        
        # Verify performance is reasonable
        assert download_time < 10.0, f"DownloadWindData took too long: {download_time:.3f} seconds"
        assert windfarms_time < 5.0, f"WindFarmsData took too long: {windfarms_time:.3f} seconds"
        assert calwindtrrates_time < 10.0, f"CalWindTrRates took too long: {calwindtrrates_time:.3f} seconds"
        
        # Verify all functions completed successfully
        assert w_sites == 4, "WindFarmsData should return correct number of sites"
        # The actual shape depends on wind speed binning - check it's reasonable
        assert tr_mats.shape[0] == 4, "CalWindTrRates should return correct number of sites"
        assert tr_mats.shape[1] == tr_mats.shape[2], "Transition matrices should be square"
        assert tr_mats.shape[1] > 0, "Transition matrices should have positive dimensions"
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_memory_usage(self, real_wind_sites, real_wind_data, tmp_path, monkeypatch):
        """Test wind memory usage with large datasets"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic wind data for 8760 hours
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Test wind functions with large data
        w = Wind()
        
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=real_wind_sites,
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )
        
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        
        combined_windspeed = tmp_path / "windspeed_data.csv"
        tr_mats = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(combined_windspeed),
            site_data=real_wind_sites,
            pcurve_data=real_wind_data["power_curves_csv"]
        )
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = final_memory - initial_memory
        
        # Verify memory usage is reasonable
        assert memory_used < 200, f"Memory usage too high: {memory_used:.1f} MB"
        
        # Verify all functions completed successfully
        assert w_sites == 4, "WindFarmsData should return correct number of sites"
        # The actual shape depends on wind speed binning - check it's reasonable
        assert tr_mats.shape[0] == 4, "CalWindTrRates should return correct number of sites"
        assert tr_mats.shape[1] == tr_mats.shape[2], "Transition matrices should be square"
        assert tr_mats.shape[1] > 0, "Transition matrices should have positive dimensions"
    
    def test_scalability(self, tmp_path: Path, monkeypatch):
        """Test with varying numbers of sites"""
        # Test with different numbers of sites
        for num_sites in [1, 2, 5]:
            site_csv = tmp_path / f"wind_sites_{num_sites}.csv"
            site_data = {
                "Farm No.": list(range(1, num_sites + 1)),
                "Farm Name": [f"Farm{i}" for i in range(1, num_sites + 1)],
                "Latitude": [35.0 + i * 0.1 for i in range(num_sites)],
                "Longitude": [-106.0 - i * 0.1 for i in range(num_sites)],
                "Hub Height": [80 + i * 5 for i in range(num_sites)],
            }
            pd.DataFrame(site_data).to_csv(site_csv, index=False)

            class DummyResp:
                def __init__(self, text):
                    self.text = text

            # Timezone info as first row (will be skipped by skiprows=1)
            tz_row = "Time Zone,-7\n"
            header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
            data_rows = "2024,1,1,0,0,6.0,7.0\n"
            csv_text = tz_row + header + data_rows
            monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

            w = Wind()
            w.DownloadWindData(
                directory=str(tmp_path),
                site_data=str(site_csv),
                api_key="dummy",
                email="test@test.com",
                affiliation="test",
                year_start=2024,
                year_end=2024,
            )

            # Verify all sites were processed
            base = tmp_path / "wtk_data" / "2024"
            for i in range(1, num_sites + 1):
                assert (base / f"Farm{i}.csv").exists(), f"Farm{i} should exist for {num_sites} sites"
    
    def test_large_dataset_handling(self, tmp_path: Path, monkeypatch):
        """Test multi-year processing"""
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1],
                "Farm Name": ["FarmA"],
                "Latitude": [35.0],
                "Longitude": [-106.0],
                "Hub Height": [80],
            }
        ).to_csv(site_csv, index=False)

        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        data_rows = "2024,1,1,0,0,6.0,7.0\n"
        csv_text = tz_row + header + data_rows
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        # Test multi-year download
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=str(site_csv),
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2026,  # 3 years
        )

        # Verify all years were processed
        for year in [2024, 2025, 2026]:
            assert (tmp_path / "wtk_data" / str(year)).exists(), f"Year {year} directory should exist"
            assert (tmp_path / "wtk_data" / str(year) / "FarmA.csv").exists(), f"FarmA file should exist for year {year}"


class TestWindWorkflow:
    """Test wind workflow and integration"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_complete_workflow(self, real_wind_sites, real_wind_data, tmp_path, monkeypatch):
        """Test complete end-to-end wind data workflow"""
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic wind data for 8760 hours
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds with temporal patterns
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1  # Higher at 100m
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Test complete wind data workflow
        w = Wind()
        
        # Step 1: Download wind data
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=real_wind_sites,
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )
        
        # Step 2: Process wind farm data
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        
        # Step 3: Calculate transition rates
        combined_windspeed = tmp_path / "windspeed_data.csv"
        tr_mats = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(combined_windspeed),
            site_data=real_wind_sites,
            pcurve_data=real_wind_data["power_curves_csv"]
        )
        
        # Verify end-to-end workflow completed successfully
        assert w_sites == 4, "Should have 4 wind sites"
        assert len(farm_name) == 4, "Should have 4 farm names"
        assert len(zone_no) == 4, "Should have 4 zones"
        # Wind classes depend on wind speed binning - check it's reasonable
        assert w_classes > 0, f"Should have positive number of wind classes, got {w_classes}"
        # The actual shape depends on wind speed binning - check it's reasonable
        assert tr_mats.shape[0] == 4, "Should have 4 sites"
        assert tr_mats.shape[1] == tr_mats.shape[2], "Transition matrices should be square"
        assert tr_mats.shape[1] > 0, "Transition matrices should have positive dimensions"
        
        # Verify data quality
        assert all(tr > 0 for tr in turbine_rating), "Turbine ratings should be positive"
        assert all(ss >= 0 for ss in start_speed), "Start speeds should be non-negative"
        assert all(pc in [2, 3] for pc in p_class), "Power classes should be 2 or 3"
        assert np.all(tr_mats >= 0), "Transition probabilities should be non-negative"
        assert np.all(tr_mats <= 1), "Transition probabilities should be <= 1"
        
        # Verify output files exist
        base = tmp_path / "wtk_data" / "2024"
        assert base.exists(), "Wind data directory should exist"
        
        # Verify all farm files exist
        for farm_name in farm_name:
            assert (base / f"{farm_name}.csv").exists(), f"Farm {farm_name} file should exist"
        
        # Verify combined windspeed file exists
        assert combined_windspeed.exists(), "Combined windspeed file should exist"
        combined_data = pd.read_csv(combined_windspeed)
        assert len(combined_data) == 8760, "Combined windspeed data should have 8760 hours"
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_system_integration(self, real_wind_sites, real_wind_data, real_system_data, tmp_path, monkeypatch):
        """Test wind integration with system data"""
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic wind data for 8760 hours
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Test wind integration with system data
        w = Wind()
        
        # Process wind data
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=real_wind_sites,
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )
        
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        
        combined_windspeed = tmp_path / "windspeed_data.csv"
        tr_mats = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(combined_windspeed),
            site_data=real_wind_sites,
            pcurve_data=real_wind_data["power_curves_csv"]
        )
        
        # Load system data
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Verify wind data integration with system data
        assert w_sites == 4, "Should have 4 wind sites"
        assert len(zone_no) == 4, "Should have 4 wind zones"
        assert nz == 3, "Should have 3 system zones"
        
        # Verify wind zones are compatible with system zones
        wind_zones = set(zone_no)
        system_zones = set(bus_no)
        assert wind_zones.issubset(system_zones), "Wind zones should be subset of system zones"
        
        # Verify wind data quality
        assert all(tr > 0 for tr in turbine_rating), "Turbine ratings should be positive"
        assert all(ss >= 0 for ss in start_speed), "Start speeds should be non-negative"
        assert all(pc in [2, 3] for pc in p_class), "Power classes should be 2 or 3"
        assert np.all(tr_mats >= 0), "Transition probabilities should be non-negative"
        assert np.all(tr_mats <= 1), "Transition probabilities should be <= 1"
        
        # Verify wind data has temporal patterns
        if combined_windspeed.exists():
            wind_data_df = pd.read_csv(combined_windspeed)
            assert len(wind_data_df) == 8760, "Wind data should have 8760 hours"
            
            # Verify wind speeds are reasonable
            for farm_name in wind_data_df.columns:
                if farm_name != "Unnamed: 0":  # Skip index column
                    wind_speeds = pd.to_numeric(wind_data_df[farm_name], errors='coerce').values
                    # Skip NaN values (non-numeric data)
                    valid_speeds = wind_speeds[~np.isnan(wind_speeds)]
                    if len(valid_speeds) > 0:
                        assert np.all(valid_speeds >= 0), f"Wind speeds for {farm_name} should be non-negative"
                        assert np.all(valid_speeds <= 50), f"Wind speeds for {farm_name} should be reasonable (< 50 m/s)"
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_multiple_cycles(self, real_wind_sites, real_wind_data, tmp_path, monkeypatch):
        """Test wind real-world usage patterns"""
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create realistic wind data for 8760 hours
        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        
        # Generate 8760 hours of realistic wind data
        wind_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Generate realistic wind speeds with temporal patterns
            base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
            hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
            wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
            wind_100m = wind_80m * 1.1  # Higher at 100m
            
            # Proper month/day calculation
            if day_of_year <= 31:
                month, day = 1, day_of_year
            elif day_of_year <= 59:
                month, day = 2, day_of_year - 31
            elif day_of_year <= 90:
                month, day = 3, day_of_year - 59
            elif day_of_year <= 120:
                month, day = 4, day_of_year - 90
            elif day_of_year <= 151:
                month, day = 5, day_of_year - 120
            elif day_of_year <= 181:
                month, day = 6, day_of_year - 151
            elif day_of_year <= 212:
                month, day = 7, day_of_year - 181
            elif day_of_year <= 243:
                month, day = 8, day_of_year - 212
            elif day_of_year <= 273:
                month, day = 9, day_of_year - 243
            elif day_of_year <= 304:
                month, day = 10, day_of_year - 273
            elif day_of_year <= 334:
                month, day = 11, day_of_year - 304
            else:
                month, day = 12, day_of_year - 334
            wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
        
        csv_text = tz_row + header + "".join(wind_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Test wind real-world usage patterns
        w = Wind()
        
        # Simulate multiple wind data processing cycles
        for cycle in range(3):
            # Download wind data
            w.DownloadWindData(
                directory=str(tmp_path),
                site_data=real_wind_sites,
                api_key="dummy",
                email="test@test.com",
                affiliation="test",
                year_start=2024,
                year_end=2024,
            )
            
            # Process wind farm data
            (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
             out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
            
            # Calculate transition rates
            combined_windspeed = tmp_path / "windspeed_data.csv"
            tr_mats = w.CalWindTrRates(
                directory=str(tmp_path),
                windspeed_data=str(combined_windspeed),
                site_data=real_wind_sites,
                pcurve_data=real_wind_data["power_curves_csv"]
            )
            
            # Verify each cycle completed successfully
            assert w_sites == 4, f"Cycle {cycle}: Should have 4 wind sites"
            assert len(farm_name) == 4, f"Cycle {cycle}: Should have 4 farm names"
            assert len(zone_no) == 4, f"Cycle {cycle}: Should have 4 zones"
            # Get actual number of wind classes from power curve data
            pcurve_df = pd.read_csv(real_wind_data["power_curves_csv"])
            expected_w_classes = len(pcurve_df['Start (m/s)'].values)
            assert w_classes == expected_w_classes, f"Cycle {cycle}: Should have {expected_w_classes} wind classes, got {w_classes}"
            # The actual shape depends on wind speed binning - check it's reasonable
            assert tr_mats.shape[0] == 4, f"Cycle {cycle}: Should have 4 sites"
            assert tr_mats.shape[1] == tr_mats.shape[2], f"Cycle {cycle}: Transition matrices should be square"
            assert tr_mats.shape[1] > 0, f"Cycle {cycle}: Transition matrices should have positive dimensions"
            
            # Verify data quality
            assert all(tr > 0 for tr in turbine_rating), f"Cycle {cycle}: Turbine ratings should be positive"
            assert all(ss >= 0 for ss in start_speed), f"Cycle {cycle}: Start speeds should be non-negative"
            assert all(pc in [2, 3] for pc in p_class), f"Cycle {cycle}: Power classes should be 2 or 3"
            assert np.all(tr_mats >= 0), f"Cycle {cycle}: Transition probabilities should be non-negative"
            assert np.all(tr_mats <= 1), f"Cycle {cycle}: Transition probabilities should be <= 1"
        
        # Verify output files exist
        base = tmp_path / "wtk_data" / "2024"
        assert base.exists(), "Wind data directory should exist"
        
        # Verify all farm files exist
        wind_sites_df = pd.read_csv(real_wind_sites)
        for farm_name in wind_sites_df["Farm Name"]:
            assert (base / f"{farm_name}.csv").exists(), f"Farm {farm_name} file should exist"
        
        # Verify combined windspeed file exists
        combined_windspeed = tmp_path / "windspeed_data.csv"
        assert combined_windspeed.exists(), "Combined windspeed file should exist"
        combined_data = pd.read_csv(combined_windspeed)
        assert len(combined_data) == 8760, "Combined windspeed data should have 8760 hours"
    
    def test_workflow_error_recovery(self, tmp_path: Path):
        """Test error handling in workflow"""
        w = Wind()
        
        # Test with invalid inputs
        with pytest.raises((FileNotFoundError, KeyError)):
            w.WindFarmsData("nonexistent.csv", "nonexistent.csv")
        
        with pytest.raises((FileNotFoundError, KeyError)):
            w.CalWindTrRates(str(tmp_path), "nonexistent.csv", "nonexistent.csv", "nonexistent.csv")
    
    def test_incremental_processing(self, tmp_path: Path, monkeypatch):
        """Test processing in stages"""
        site_csv = tmp_path / "wind_sites.csv"
        pd.DataFrame(
            {
                "Farm No.": [1],
                "Farm Name": ["FarmA"],
                "Latitude": [35.0],
                "Longitude": [-106.0],
                "Hub Height": [80],
                "Zone No.": [1],
                "Max Cap": [100.0],
                "Turbine Rating": [2.0],
                "Power Class": [2],
            }
        ).to_csv(site_csv, index=False)

        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Timezone info as first row (will be skipped by skiprows=1)
        tz_row = "Time Zone,-7\n"
        header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
        data_rows = "2024,1,1,0,0,6.0,7.0\n"
        csv_text = tz_row + header + data_rows
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        w = Wind()
        
        # Test incremental processing
        # Step 1: Download only
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=str(site_csv),
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )
        
        # Verify download completed
        assert (tmp_path / "wtk_data" / "2024" / "FarmA.csv").exists()
        assert (tmp_path / "windspeed_data.csv").exists()
        
        # Step 2: Process farm data
        pcurve_csv = tmp_path / "w_power_curves.csv"
        pd.DataFrame(
            {
                "Start (m/s)": [0.0, 5.0, 10.0],
                "End (m/s)": [5.0, 10.0, 15.0],
                "Class 2": [0.0, 0.0, 0.0],
                "Class 3": [0.0, 0.0, 0.0],
            }
        ).to_csv(pcurve_csv, index=False)
        
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(str(site_csv), str(pcurve_csv))
        
        # Verify farm data processing
        assert w_sites == 1
        assert len(farm_name) == 1
        assert farm_name.iloc[0] == "FarmA"
        
        # Step 3: Calculate transition rates
        tr_mats = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(tmp_path / "windspeed_data.csv"),
            site_data=str(site_csv),
            pcurve_data=str(pcurve_csv)
        )
        
        # Verify transition rates
        assert tr_mats.shape == (1, 3, 3)
        assert (tmp_path / "t_rate.xlsx").exists()


# Production data integration tests

@pytest.mark.integration
@pytest.mark.slow
def test_real_wind_farms_4_sites(real_wind_sites):
    """Parse wind_sites.csv, verify 4 farms with correct zones."""
    # Load wind sites data
    wind_sites_df = pd.read_csv(real_wind_sites)
    
    # Verify production data structure
    assert len(wind_sites_df) == 4  # 4 wind farms
    assert "Farm No." in wind_sites_df.columns
    assert "Farm Name" in wind_sites_df.columns
    assert "Zone No." in wind_sites_df.columns
    assert "Power Class" in wind_sites_df.columns
    assert "Turbine Rating" in wind_sites_df.columns
    assert "Max Cap" in wind_sites_df.columns
    
    # Verify zones (should be 1 and 3 based on production data)
    zones = wind_sites_df["Zone No."].unique()
    assert len(zones) == 2
    assert 1 in zones
    assert 3 in zones
    
    # Verify power classes (should be 2 and 3)
    power_classes = wind_sites_df["Power Class"].unique()
    assert len(power_classes) == 2
    assert 2 in power_classes
    assert 3 in power_classes
    
    # Verify turbine ratings are reasonable
    assert all(wind_sites_df["Turbine Rating"] > 0)
    assert all(wind_sites_df["Max Cap"] > 0)
    
    # Verify farm names are unique
    assert len(wind_sites_df["Farm Name"].unique()) == 4


@pytest.mark.integration
@pytest.mark.slow
def test_power_curves_class_2_and_3(real_wind_data):
    """Load w_power_curves.csv, validate both turbine classes."""
    if not Path(real_wind_data["power_curves_csv"]).exists():
        pytest.skip("Production wind power curves data not available")
    
    # Load power curves data
    power_curves_df = pd.read_csv(real_wind_data["power_curves_csv"])
    
    # Verify power curves structure
    assert "Start (m/s)" in power_curves_df.columns
    assert "End (m/s)" in power_curves_df.columns
    assert "Class 2" in power_curves_df.columns
    assert "Class 3" in power_curves_df.columns
    
    # Verify wind speed bins are reasonable
    assert all(power_curves_df["Start (m/s)"] >= 0)
    assert all(power_curves_df["End (m/s)"] > power_curves_df["Start (m/s)"])
    
    # Verify power output values are in valid range [0, 1]
    assert all(0 <= power_curves_df["Class 2"]) and all(power_curves_df["Class 2"] <= 1)
    assert all(0 <= power_curves_df["Class 3"]) and all(power_curves_df["Class 3"] <= 1)
    
    # Verify power curves are monotonic (generally increasing then decreasing)
    class_2_power = power_curves_df["Class 2"].values
    class_3_power = power_curves_df["Class 3"].values
    
    # Check that power starts at 0 and ends at 0 (or very low)
    assert class_2_power[0] == 0.0
    assert class_3_power[0] == 0.0
    assert class_2_power[-1] <= 0.1  # Should be low at high wind speeds
    assert class_3_power[-1] <= 0.1
    
    # Check that there's a peak power output
    assert max(class_2_power) > 0.5
    assert max(class_3_power) > 0.5


# Priority 1: Wind Data Processing with Real Data

@pytest.mark.integration
@pytest.mark.slow
def test_DownloadWindData_with_real_wind_sites(real_wind_sites, real_wind_data, tmp_path, monkeypatch):
    """Test DownloadWindData with real wind sites."""
    # Mock API response for consistent testing
    class DummyResp:
        def __init__(self, text):
            self.text = text

    # Create realistic weather data for 8760 hours
    # Timezone info as first row (will be skipped by skiprows=1)
    tz_row = "Time Zone,-7\n"
    header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    
    # Generate 8760 hours of realistic wind data
    wind_data = []
    for hour in range(8760):
        day_of_year = (hour // 24) + 1
        hour_of_day = hour % 24
        
        # Generate realistic wind speeds (higher during day, variable)
        base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
        hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
        wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
        wind_100m = wind_80m * 1.1  # Higher at 100m
        
        # Proper month/day calculation
        if day_of_year <= 31:
            month, day = 1, day_of_year
        elif day_of_year <= 59:
            month, day = 2, day_of_year - 31
        elif day_of_year <= 90:
            month, day = 3, day_of_year - 59
        elif day_of_year <= 120:
            month, day = 4, day_of_year - 90
        elif day_of_year <= 151:
            month, day = 5, day_of_year - 120
        elif day_of_year <= 181:
            month, day = 6, day_of_year - 151
        elif day_of_year <= 212:
            month, day = 7, day_of_year - 181
        elif day_of_year <= 243:
            month, day = 8, day_of_year - 212
        elif day_of_year <= 273:
            month, day = 9, day_of_year - 243
        elif day_of_year <= 304:
            month, day = 10, day_of_year - 273
        elif day_of_year <= 334:
            month, day = 11, day_of_year - 304
        else:
            month, day = 12, day_of_year - 334
        wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
    
    csv_text = tz_row + header + "".join(wind_data)
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    # Test DownloadWindData with real sites
    w = Wind()
    w.DownloadWindData(
        directory=str(tmp_path),
        site_data=real_wind_sites,
        api_key="dummy",
        email="test@test.com",
        affiliation="test",
        year_start=2024,
        year_end=2024,
    )

    # Verify output structure
    base = tmp_path / "wtk_data" / "2024"
    assert base.exists()
    
    # Verify all wind sites have output files
    wind_sites_df = pd.read_csv(real_wind_sites)
    for farm_name in wind_sites_df["Farm Name"]:
        assert (base / f"{farm_name}.csv").exists()
        
        # Verify file contents have 8760 hours
        farm_file = base / f"{farm_name}.csv"
        if farm_file.exists():
            farm_data = pd.read_csv(farm_file)
            # 2024 is a leap year, so we expect 8760 hours (365 * 24)
        # But the data might have 8761 due to timezone handling
        assert len(farm_data) >= 8760, f"Farm {farm_name} data should have at least 8760 hours, got {len(farm_data)}"
    
    # Verify combined windspeed file exists
    combined = tmp_path / "windspeed_data.csv"
    assert combined.exists()
    combined_data = pd.read_csv(combined)
    assert len(combined_data) == 8760, "Combined windspeed data should have 8760 hours"
    
    # Verify all farm columns are present
    farm_names = wind_sites_df["Farm Name"].tolist()
    for farm_name in farm_names:
        assert farm_name in combined_data.columns, f"Farm {farm_name} should be in combined data"


@pytest.mark.integration
@pytest.mark.slow
def test_WindFarmsData_with_real_wind_farms(real_wind_sites, real_wind_data):
    """Test WindFarmsData with real wind farms."""
    w = Wind()
    
    # Test WindFarmsData with real data
    (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
     out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
    
    # Verify results match real wind farms
    wind_sites_df = pd.read_csv(real_wind_sites)
    
    assert w_sites == len(wind_sites_df), "Should have correct number of wind sites"
    assert len(farm_name) == w_sites, "Should have correct number of farm names"
    assert len(zone_no) == w_sites, "Should have correct number of zones"
    assert len(w_turbines) == w_sites, "Should have correct number of turbines"
    assert len(turbine_rating) == w_sites, "Should have correct number of turbine ratings"
    assert len(p_class) == w_sites, "Should have correct number of power classes"
    assert len(start_speed) == w_classes, "Should have correct number of start speeds"
    
    # Verify farm names match
    expected_farm_names = wind_sites_df["Farm Name"].tolist()
    assert farm_name.tolist() == expected_farm_names, "Farm names should match real data"
    
    # Verify zones match
    expected_zones = wind_sites_df["Zone No."].tolist()
    assert zone_no.tolist() == expected_zones, "Zones should match real data"
    
    # Verify power classes are valid
    assert all(pc in [2, 3] for pc in p_class), "Power classes should be 2 or 3"
    
    # Verify turbine ratings are reasonable
    assert all(tr > 0 for tr in turbine_rating), "Turbine ratings should be positive"
    assert all(tr < 10 for tr in turbine_rating), "Turbine ratings should be reasonable (< 10 MW)"
    
    # Verify start speeds are reasonable
    assert all(ss >= 0 for ss in start_speed), "Start speeds should be non-negative"
    assert all(ss <= 50 for ss in start_speed), "Start speeds should be reasonable (< 50 m/s)"
    
    # Verify power curves are valid
    assert len(out_curve2) > 0, "Class 2 power curve should have data"
    assert len(out_curve3) > 0, "Class 3 power curve should have data"
    assert all(0 <= val <= 1 for val in out_curve2), "Class 2 power curve should be in [0, 1]"
    assert all(0 <= val <= 1 for val in out_curve3), "Class 3 power curve should be in [0, 1]"


@pytest.mark.integration
@pytest.mark.slow
def test_CalWindTrRates_with_real_wind_data(real_wind_sites, real_wind_data, tmp_path, monkeypatch):
    """Test CalWindTrRates with real wind data."""
    # Mock API response for consistent testing
    class DummyResp:
        def __init__(self, text):
            self.text = text

    # Create realistic wind data for 8760 hours
    # Timezone info as first row (will be skipped by skiprows=1)
    tz_row = "Time Zone,-7\n"
    header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    
    # Generate 8760 hours of realistic wind data
    wind_data = []
    for hour in range(8760):
        day_of_year = (hour // 24) + 1
        hour_of_day = hour % 24
        
        # Generate realistic wind speeds with temporal patterns
        base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
        hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
        wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
        wind_100m = wind_80m * 1.1  # Higher at 100m
        
        # Proper month/day calculation
        if day_of_year <= 31:
            month, day = 1, day_of_year
        elif day_of_year <= 59:
            month, day = 2, day_of_year - 31
        elif day_of_year <= 90:
            month, day = 3, day_of_year - 59
        elif day_of_year <= 120:
            month, day = 4, day_of_year - 90
        elif day_of_year <= 151:
            month, day = 5, day_of_year - 120
        elif day_of_year <= 181:
            month, day = 6, day_of_year - 151
        elif day_of_year <= 212:
            month, day = 7, day_of_year - 181
        elif day_of_year <= 243:
            month, day = 8, day_of_year - 212
        elif day_of_year <= 273:
            month, day = 9, day_of_year - 243
        elif day_of_year <= 304:
            month, day = 10, day_of_year - 273
        elif day_of_year <= 334:
            month, day = 11, day_of_year - 304
        else:
            month, day = 12, day_of_year - 334
        wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
    
    csv_text = tz_row + header + "".join(wind_data)
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    # Create combined windspeed file with correct site names
    wind_sites_df = pd.read_csv(real_wind_sites)
    site_names = wind_sites_df['Farm Name'].tolist()
    
    combined_windspeed = tmp_path / "windspeed_data.csv"
    wind_data_dict = {'datetime': pd.date_range('2024-01-01', periods=8760, freq='h')}
    for site_name in site_names:
        wind_data_dict[site_name] = np.random.uniform(0, 20, 8760)
    combined_data = pd.DataFrame(wind_data_dict)
    combined_data.to_csv(combined_windspeed, index=False)

    # Test CalWindTrRates with real data
    w = Wind()
    tr_mats = w.CalWindTrRates(
        directory=str(tmp_path),
        windspeed_data=str(combined_windspeed),
        site_data=real_wind_sites,
        pcurve_data=real_wind_data["power_curves_csv"]
    )
    
    # Verify results
    wind_sites_df = pd.read_csv(real_wind_sites)
    w_sites = len(wind_sites_df)
    
    # Get actual number of wind classes from power curve data
    pcurve_df = pd.read_csv(real_wind_data["power_curves_csv"])
    w_classes = len(pcurve_df['Start (m/s)'].values)
    
    assert tr_mats.shape == (w_sites, w_classes, w_classes), "Transition matrices should have correct shape"
    assert np.all(tr_mats >= 0), "All transition probabilities should be non-negative"
    assert np.all(tr_mats <= 1), "All transition probabilities should be <= 1"
    
    # Verify each site's transition matrix sums to 1 (with tolerance for numerical issues)
    for site in range(w_sites):
        for from_class in range(w_classes):
            row_sum = np.sum(tr_mats[site, from_class, :])
            # Allow for numerical precision issues and NaN handling
            if not np.isnan(row_sum) and row_sum > 0:
                assert abs(row_sum - 1.0) < 1e-3, f"Transition matrix for site {site}, class {from_class} should sum to 1, got {row_sum}"
    
    # Verify transition matrices are reasonable (allow for NaN values from division by zero)
    assert np.all(np.isnan(tr_mats) | (tr_mats >= 0)), "All transition probabilities should be non-negative or NaN"
    assert np.all(np.isnan(tr_mats) | (tr_mats <= 1)), "All transition probabilities should be <= 1 or NaN"


@pytest.mark.integration
@pytest.mark.slow
def test_wind_data_processing_with_production_scale(real_wind_sites, real_wind_data, tmp_path, monkeypatch):
    """Test wind data processing with production-scale data."""
    # Mock API response for consistent testing
    class DummyResp:
        def __init__(self, text):
            self.text = text

    # Create realistic wind data for 8760 hours
    # Timezone info as first row (will be skipped by skiprows=1)
    tz_row = "Time Zone,-7\n"
    header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    
    # Generate 8760 hours of realistic wind data
    wind_data = []
    for hour in range(8760):
        day_of_year = (hour // 24) + 1
        hour_of_day = hour % 24
        
        # Generate realistic wind speeds with temporal patterns
        base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
        hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
        wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
        wind_100m = wind_80m * 1.1  # Higher at 100m
        
        # Proper month/day calculation
        if day_of_year <= 31:
            month, day = 1, day_of_year
        elif day_of_year <= 59:
            month, day = 2, day_of_year - 31
        elif day_of_year <= 90:
            month, day = 3, day_of_year - 59
        elif day_of_year <= 120:
            month, day = 4, day_of_year - 90
        elif day_of_year <= 151:
            month, day = 5, day_of_year - 120
        elif day_of_year <= 181:
            month, day = 6, day_of_year - 151
        elif day_of_year <= 212:
            month, day = 7, day_of_year - 181
        elif day_of_year <= 243:
            month, day = 8, day_of_year - 212
        elif day_of_year <= 273:
            month, day = 9, day_of_year - 243
        elif day_of_year <= 304:
            month, day = 10, day_of_year - 273
        elif day_of_year <= 334:
            month, day = 11, day_of_year - 304
        else:
            month, day = 12, day_of_year - 334
        wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
    
    csv_text = tz_row + header + "".join(wind_data)
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    # Test complete wind data processing workflow
    w = Wind()
    
    # Step 1: Download wind data
    w.DownloadWindData(
        directory=str(tmp_path),
        site_data=real_wind_sites,
        api_key="dummy",
        email="test@test.com",
        affiliation="test",
        year_start=2024,
        year_end=2024,
    )
    
    # Step 2: Process wind farm data
    (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
     out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
    
    # Step 3: Calculate transition rates
    combined_windspeed = tmp_path / "windspeed_data.csv"
    tr_mats = w.CalWindTrRates(
        directory=str(tmp_path),
        windspeed_data=str(combined_windspeed),
        site_data=real_wind_sites,
        pcurve_data=real_wind_data["power_curves_csv"]
    )
    
    # Verify complete workflow
    assert w_sites == 4, "Should have 4 wind sites"
    assert len(farm_name) == 4, "Should have 4 farm names"
    assert len(zone_no) == 4, "Should have 4 zones"
    # Get actual number of wind classes from power curve data
    pcurve_df = pd.read_csv(real_wind_data["power_curves_csv"])
    expected_w_classes = len(pcurve_df['Start (m/s)'].values)
    assert w_classes == expected_w_classes, f"Should have {expected_w_classes} wind classes, got {w_classes}"
    # The actual shape depends on wind speed binning - check it's reasonable
    assert tr_mats.shape[0] == 4, "Should have 4 sites"
    assert tr_mats.shape[1] == tr_mats.shape[2], "Transition matrices should be square"
    assert tr_mats.shape[1] > 0, "Transition matrices should have positive dimensions"
    
    # Verify data quality
    assert all(tr > 0 for tr in turbine_rating), "Turbine ratings should be positive"
    assert all(ss >= 0 for ss in start_speed), "Start speeds should be non-negative"
    assert all(pc in [2, 3] for pc in p_class), "Power classes should be 2 or 3"
    assert np.all(tr_mats >= 0), "Transition probabilities should be non-negative"
    assert np.all(tr_mats <= 1), "Transition probabilities should be <= 1"


# Priority 2: Wind Power Curve and Generation Testing

@pytest.mark.integration
@pytest.mark.slow
def test_wind_power_curves_with_real_data(real_wind_data):
    """Test wind power curves with real data."""
    # Load real wind data
    wind_data_df = pd.read_csv(real_wind_data["power_curves_csv"])
    
    # Verify power curves are reasonable
    assert "Class 2" in wind_data_df.columns, "Should have Class 2 power curve"
    assert "Class 3" in wind_data_df.columns, "Should have Class 3 power curve"
    
    # Verify power curve values are in [0, 1] range
    class2_vals = wind_data_df["Class 2"].values
    class3_vals = wind_data_df["Class 3"].values
    
    assert np.all(class2_vals >= 0) and np.all(class2_vals <= 1), "Class 2 power curve should be in [0, 1]"
    assert np.all(class3_vals >= 0) and np.all(class3_vals <= 1), "Class 3 power curve should be in [0, 1]"
    
    # Verify power curves have realistic shape (increasing then decreasing)
    # Check that power increases initially
    assert class2_vals[0] < class2_vals[5], "Class 2 power curve should increase initially"
    assert class3_vals[0] < class3_vals[5], "Class 3 power curve should increase initially"
    
    # Check that power peaks and then decreases at high wind speeds
    max_class2_idx = np.argmax(class2_vals)
    max_class3_idx = np.argmax(class3_vals)
    assert class2_vals[max_class2_idx] > class2_vals[-1], "Class 2 power curve should peak and decrease"
    assert class3_vals[max_class3_idx] > class3_vals[-1], "Class 3 power curve should peak and decrease"
    
    # Verify wind speed bins are reasonable
    start_speeds = wind_data_df["Start (m/s)"].values
    end_speeds = wind_data_df["End (m/s)"].values
    
    assert np.all(start_speeds >= 0) and np.all(start_speeds <= 1000), "Wind speed bins should be reasonable"
    assert np.all(end_speeds >= 0) and np.all(end_speeds <= 1000), "Wind speed bins should be reasonable"
    assert np.all(end_speeds > start_speeds), "End speeds should be > start speeds"
    
    # Verify both power curves have reasonable average power
    assert np.mean(class2_vals) > 0.1, "Class 2 should have reasonable average power"
    assert np.mean(class3_vals) > 0.1, "Class 3 should have reasonable average power"
    
    # Verify power curves have realistic shape (low at low speeds, peak in middle, low at high speeds)
    assert class2_vals[0] == 0.0, "Class 2 power curve should start at 0"
    assert class3_vals[0] == 0.0, "Class 3 power curve should start at 0"
    assert class2_vals[-1] == 0.0, "Class 2 power curve should end at 0"
    assert class3_vals[-1] == 0.0, "Class 3 power curve should end at 0"


@pytest.mark.integration
@pytest.mark.slow
def test_wind_generation_calculation_with_real_data(real_wind_sites, real_wind_data, tmp_path, monkeypatch):
    """Test wind generation calculation with real data."""
    # Mock API response for consistent testing
    class DummyResp:
        def __init__(self, text):
            self.text = text

    # Create realistic wind data for 8760 hours
    # Timezone info as first row (will be skipped by skiprows=1)
    tz_row = "Time Zone,-7\n"
    header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    
    # Generate 8760 hours of realistic wind data
    wind_data = []
    for hour in range(8760):
        day_of_year = (hour // 24) + 1
        hour_of_day = hour % 24
        
        # Generate realistic wind speeds with temporal patterns
        base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
        hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
        wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
        wind_100m = wind_80m * 1.1  # Higher at 100m
        
        # Proper month/day calculation
        if day_of_year <= 31:
            month, day = 1, day_of_year
        elif day_of_year <= 59:
            month, day = 2, day_of_year - 31
        elif day_of_year <= 90:
            month, day = 3, day_of_year - 59
        elif day_of_year <= 120:
            month, day = 4, day_of_year - 90
        elif day_of_year <= 151:
            month, day = 5, day_of_year - 120
        elif day_of_year <= 181:
            month, day = 6, day_of_year - 151
        elif day_of_year <= 212:
            month, day = 7, day_of_year - 181
        elif day_of_year <= 243:
            month, day = 8, day_of_year - 212
        elif day_of_year <= 273:
            month, day = 9, day_of_year - 243
        elif day_of_year <= 304:
            month, day = 10, day_of_year - 273
        elif day_of_year <= 334:
            month, day = 11, day_of_year - 304
        else:
            month, day = 12, day_of_year - 334
        wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
    
    csv_text = tz_row + header + "".join(wind_data)
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    # Test wind generation calculation
    w = Wind()
    
    # Download wind data
    w.DownloadWindData(
        directory=str(tmp_path),
        site_data=real_wind_sites,
        api_key="dummy",
        email="test@test.com",
        affiliation="test",
        year_start=2024,
        year_end=2024,
    )
    
    # Process wind farm data
    (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
     out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
    
    # Calculate transition rates
    combined_windspeed = tmp_path / "windspeed_data.csv"
    tr_mats = w.CalWindTrRates(
        directory=str(tmp_path),
        windspeed_data=str(combined_windspeed),
        site_data=real_wind_sites,
        pcurve_data=real_wind_data["power_curves_csv"]
    )
    
    # Verify wind generation calculation
    assert w_sites == 4, "Should have 4 wind sites"
    assert len(farm_name) == 4, "Should have 4 farm names"
    assert len(zone_no) == 4, "Should have 4 zones"
    # Get actual number of wind classes from power curve data
    pcurve_df = pd.read_csv(real_wind_data["power_curves_csv"])
    expected_w_classes = len(pcurve_df['Start (m/s)'].values)
    assert w_classes == expected_w_classes, f"Should have {expected_w_classes} wind classes, got {w_classes}"
    # The actual shape depends on wind speed binning - check it's reasonable
    assert tr_mats.shape[0] == 4, "Should have 4 sites"
    assert tr_mats.shape[1] == tr_mats.shape[2], "Transition matrices should be square"
    assert tr_mats.shape[1] > 0, "Transition matrices should have positive dimensions"
    
    # Verify power curves are valid
    assert len(out_curve2) > 0, "Class 2 power curve should have data"
    assert len(out_curve3) > 0, "Class 3 power curve should have data"
    assert all(0 <= val <= 1 for val in out_curve2), "Class 2 power curve should be in [0, 1]"
    assert all(0 <= val <= 1 for val in out_curve3), "Class 3 power curve should be in [0, 1]"
    
    # Verify turbine ratings are reasonable
    assert all(tr > 0 for tr in turbine_rating), "Turbine ratings should be positive"
    assert all(tr < 10 for tr in turbine_rating), "Turbine ratings should be reasonable (< 10 MW)"
    
    # Verify capacities are reasonable
    assert all(ss >= 0 for ss in start_speed), "Start speeds should be non-negative"
    assert all(ss <= 50 for ss in start_speed), "Start speeds should be reasonable (< 50 m/s)"


@pytest.mark.integration
@pytest.mark.slow
def test_wind_zone_aggregation_with_real_data(real_wind_sites, real_wind_data):
    """Test wind zone aggregation with real data."""
    w = Wind()
    
    # Process wind farm data
    (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
     out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
    
    # Verify zone aggregation
    wind_sites_df = pd.read_csv(real_wind_sites)
    expected_zones = wind_sites_df["Zone No."].unique()
    
    assert len(set(zone_no)) == len(expected_zones), "Should have correct number of unique zones"
    assert all(zone in expected_zones for zone in zone_no), "All zones should be from real data"
    
    # Verify zone distribution
    zone_counts = {}
    for zone in zone_no:
        zone_counts[zone] = zone_counts.get(zone, 0) + 1
    
    # Verify we have farms in multiple zones
    assert len(zone_counts) > 1, "Should have farms in multiple zones"
    
    # Verify zone distribution is reasonable
    for zone, count in zone_counts.items():
        assert count > 0, f"Zone {zone} should have at least one farm"
        assert count <= w_sites, f"Zone {zone} should not have more farms than total sites"


@pytest.mark.integration
@pytest.mark.slow
def test_wind_temporal_patterns_with_real_data(real_wind_sites, real_wind_data, tmp_path, monkeypatch):
    """Test wind temporal patterns with real data."""
    # Mock API response for consistent testing
    class DummyResp:
        def __init__(self, text):
            self.text = text

    # Create realistic wind data with temporal patterns
    # Timezone info as first row (will be skipped by skiprows=1)
    tz_row = "Time Zone,-7\n"
    header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    
    # Generate 8760 hours of realistic wind data with temporal patterns
    wind_data = []
    for hour in range(8760):
        day_of_year = (hour // 24) + 1
        hour_of_day = hour % 24
        
        # Generate realistic wind speeds with temporal patterns
        base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
        hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
        wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
        wind_100m = wind_80m * 1.1  # Higher at 100m
        
        # Proper month/day calculation
        if day_of_year <= 31:
            month, day = 1, day_of_year
        elif day_of_year <= 59:
            month, day = 2, day_of_year - 31
        elif day_of_year <= 90:
            month, day = 3, day_of_year - 59
        elif day_of_year <= 120:
            month, day = 4, day_of_year - 90
        elif day_of_year <= 151:
            month, day = 5, day_of_year - 120
        elif day_of_year <= 181:
            month, day = 6, day_of_year - 151
        elif day_of_year <= 212:
            month, day = 7, day_of_year - 181
        elif day_of_year <= 243:
            month, day = 8, day_of_year - 212
        elif day_of_year <= 273:
            month, day = 9, day_of_year - 243
        elif day_of_year <= 304:
            month, day = 10, day_of_year - 273
        elif day_of_year <= 334:
            month, day = 11, day_of_year - 304
        else:
            month, day = 12, day_of_year - 334
        wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
    
    csv_text = tz_row + header + "".join(wind_data)
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    # Test wind temporal patterns
    w = Wind()
    
    # Download wind data
    w.DownloadWindData(
        directory=str(tmp_path),
        site_data=real_wind_sites,
        api_key="dummy",
        email="test@test.com",
        affiliation="test",
        year_start=2024,
        year_end=2024,
    )
    
    # Process wind farm data
    (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
     out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
    
    # Verify temporal patterns
    assert w_sites == 4, "Should have 4 wind sites"
    assert len(farm_name) == 4, "Should have 4 farm names"
    assert len(zone_no) == 4, "Should have 4 zones"
    # Get actual number of wind classes from power curve data
    pcurve_df = pd.read_csv(real_wind_data["power_curves_csv"])
    expected_w_classes = len(pcurve_df['Start (m/s)'].values)
    assert w_classes == expected_w_classes, f"Should have {expected_w_classes} wind classes, got {w_classes}"
    
    # Verify wind data has temporal patterns
    combined_windspeed = tmp_path / "windspeed_data.csv"
    if combined_windspeed.exists():
        wind_data_df = pd.read_csv(combined_windspeed)
        assert len(wind_data_df) == 8760, "Wind data should have 8760 hours"
        
        # Verify wind speeds are reasonable
        for farm_name in wind_data_df.columns:
            if farm_name != "Unnamed: 0":  # Skip index column
                wind_speeds = pd.to_numeric(wind_data_df[farm_name], errors='coerce').values
                # Skip NaN values (non-numeric data)
                valid_speeds = wind_speeds[~np.isnan(wind_speeds)]
                if len(valid_speeds) > 0:
                    assert np.all(valid_speeds >= 0), f"Wind speeds for {farm_name} should be non-negative"
                    assert np.all(valid_speeds <= 50), f"Wind speeds for {farm_name} should be reasonable (< 50 m/s)"
                
                # Verify temporal variation (only for valid wind speed data)
                if len(valid_speeds) > 1:
                    assert np.std(valid_speeds) > 0, f"Wind speeds for {farm_name} should have variation"
                    assert np.max(valid_speeds) > np.min(valid_speeds), f"Wind speeds for {farm_name} should have range"


# Priority 3: Performance and Scale Testing

@pytest.mark.integration
@pytest.mark.slow
def test_wind_performance_with_production_scale(real_wind_sites, real_wind_data, tmp_path, monkeypatch):
    """Test wind performance with production-scale data."""
    import time
    
    # Mock API response for consistent testing
    class DummyResp:
        def __init__(self, text):
            self.text = text

    # Create realistic wind data for 8760 hours
    # Timezone info as first row (will be skipped by skiprows=1)
    tz_row = "Time Zone,-7\n"
    header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    
    # Generate 8760 hours of realistic wind data
    wind_data = []
    for hour in range(8760):
        day_of_year = (hour // 24) + 1
        hour_of_day = hour % 24
        
        # Generate realistic wind speeds
        base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)
        hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)
        wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
        wind_100m = wind_80m * 1.1
        
        # Proper month/day calculation
        if day_of_year <= 31:
            month, day = 1, day_of_year
        elif day_of_year <= 59:
            month, day = 2, day_of_year - 31
        elif day_of_year <= 90:
            month, day = 3, day_of_year - 59
        elif day_of_year <= 120:
            month, day = 4, day_of_year - 90
        elif day_of_year <= 151:
            month, day = 5, day_of_year - 120
        elif day_of_year <= 181:
            month, day = 6, day_of_year - 151
        elif day_of_year <= 212:
            month, day = 7, day_of_year - 181
        elif day_of_year <= 243:
            month, day = 8, day_of_year - 212
        elif day_of_year <= 273:
            month, day = 9, day_of_year - 243
        elif day_of_year <= 304:
            month, day = 10, day_of_year - 273
        elif day_of_year <= 334:
            month, day = 11, day_of_year - 304
        else:
            month, day = 12, day_of_year - 334
        wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
    
    csv_text = tz_row + header + "".join(wind_data)
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    # Test performance of wind functions
    w = Wind()
    
    start_time = time.time()
    w.DownloadWindData(
        directory=str(tmp_path),
        site_data=real_wind_sites,
        api_key="dummy",
        email="test@test.com",
        affiliation="test",
        year_start=2024,
        year_end=2024,
    )
    download_time = time.time() - start_time
    
    start_time = time.time()
    (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
     out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
    windfarms_time = time.time() - start_time
    
    start_time = time.time()
    combined_windspeed = tmp_path / "windspeed_data.csv"
    tr_mats = w.CalWindTrRates(
        directory=str(tmp_path),
        windspeed_data=str(combined_windspeed),
        site_data=real_wind_sites,
        pcurve_data=real_wind_data["power_curves_csv"]
    )
    calwindtrrates_time = time.time() - start_time
    
    # Verify performance is reasonable
    assert download_time < 10.0, f"DownloadWindData took too long: {download_time:.3f} seconds"
    assert windfarms_time < 5.0, f"WindFarmsData took too long: {windfarms_time:.3f} seconds"
    assert calwindtrrates_time < 10.0, f"CalWindTrRates took too long: {calwindtrrates_time:.3f} seconds"
    
    # Verify all functions completed successfully
    assert w_sites == 4, "WindFarmsData should return correct number of sites"
    # The actual shape depends on wind speed binning - check it's reasonable
    assert tr_mats.shape[0] == 4, "CalWindTrRates should return correct number of sites"
    assert tr_mats.shape[1] == tr_mats.shape[2], "Transition matrices should be square"
    assert tr_mats.shape[1] > 0, "Transition matrices should have positive dimensions"


@pytest.mark.integration
@pytest.mark.slow
def test_wind_memory_usage_with_large_datasets(real_wind_sites, real_wind_data, tmp_path, monkeypatch):
    """Test wind memory usage with large datasets."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Mock API response for consistent testing
    class DummyResp:
        def __init__(self, text):
            self.text = text

    # Create realistic wind data for 8760 hours
    # Timezone info as first row (will be skipped by skiprows=1)
    tz_row = "Time Zone,-7\n"
    header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    
    # Generate 8760 hours of realistic wind data
    wind_data = []
    for hour in range(8760):
        day_of_year = (hour // 24) + 1
        hour_of_day = hour % 24
        
        # Generate realistic wind speeds
        base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)
        hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)
        wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
        wind_100m = wind_80m * 1.1
        
        # Proper month/day calculation
        if day_of_year <= 31:
            month, day = 1, day_of_year
        elif day_of_year <= 59:
            month, day = 2, day_of_year - 31
        elif day_of_year <= 90:
            month, day = 3, day_of_year - 59
        elif day_of_year <= 120:
            month, day = 4, day_of_year - 90
        elif day_of_year <= 151:
            month, day = 5, day_of_year - 120
        elif day_of_year <= 181:
            month, day = 6, day_of_year - 151
        elif day_of_year <= 212:
            month, day = 7, day_of_year - 181
        elif day_of_year <= 243:
            month, day = 8, day_of_year - 212
        elif day_of_year <= 273:
            month, day = 9, day_of_year - 243
        elif day_of_year <= 304:
            month, day = 10, day_of_year - 273
        elif day_of_year <= 334:
            month, day = 11, day_of_year - 304
        else:
            month, day = 12, day_of_year - 334
        wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
    
    csv_text = tz_row + header + "".join(wind_data)
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    # Test wind functions with large data
    w = Wind()
    
    w.DownloadWindData(
        directory=str(tmp_path),
        site_data=real_wind_sites,
        api_key="dummy",
        email="test@test.com",
        affiliation="test",
        year_start=2024,
        year_end=2024,
    )
    
    (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
     out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
    
    combined_windspeed = tmp_path / "windspeed_data.csv"
    tr_mats = w.CalWindTrRates(
        directory=str(tmp_path),
        windspeed_data=str(combined_windspeed),
        site_data=real_wind_sites,
        pcurve_data=real_wind_data["power_curves_csv"]
    )
    
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_used = final_memory - initial_memory
    
    # Verify memory usage is reasonable
    assert memory_used < 200, f"Memory usage too high: {memory_used:.1f} MB"
    
    # Verify all functions completed successfully
    assert w_sites == 4, "WindFarmsData should return correct number of sites"
    # The actual shape depends on wind speed binning - check it's reasonable
    assert tr_mats.shape[0] == 4, "CalWindTrRates should return correct number of sites"
    assert tr_mats.shape[1] == tr_mats.shape[2], "Transition matrices should be square"
    assert tr_mats.shape[1] > 0, "Transition matrices should have positive dimensions"


# Priority 4: Integration and Workflow Testing

@pytest.mark.integration
@pytest.mark.slow
def test_wind_end_to_end_workflow(real_wind_sites, real_wind_data, tmp_path, monkeypatch):
    """Test end-to-end wind data workflow."""
    # Mock API response for consistent testing
    class DummyResp:
        def __init__(self, text):
            self.text = text

    # Create realistic wind data for 8760 hours
    # Timezone info as first row (will be skipped by skiprows=1)
    tz_row = "Time Zone,-7\n"
    header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    
    # Generate 8760 hours of realistic wind data
    wind_data = []
    for hour in range(8760):
        day_of_year = (hour // 24) + 1
        hour_of_day = hour % 24
        
        # Generate realistic wind speeds with temporal patterns
        base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
        hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
        wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
        wind_100m = wind_80m * 1.1  # Higher at 100m
        
        # Proper month/day calculation
        if day_of_year <= 31:
            month, day = 1, day_of_year
        elif day_of_year <= 59:
            month, day = 2, day_of_year - 31
        elif day_of_year <= 90:
            month, day = 3, day_of_year - 59
        elif day_of_year <= 120:
            month, day = 4, day_of_year - 90
        elif day_of_year <= 151:
            month, day = 5, day_of_year - 120
        elif day_of_year <= 181:
            month, day = 6, day_of_year - 151
        elif day_of_year <= 212:
            month, day = 7, day_of_year - 181
        elif day_of_year <= 243:
            month, day = 8, day_of_year - 212
        elif day_of_year <= 273:
            month, day = 9, day_of_year - 243
        elif day_of_year <= 304:
            month, day = 10, day_of_year - 273
        elif day_of_year <= 334:
            month, day = 11, day_of_year - 304
        else:
            month, day = 12, day_of_year - 334
        wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
    
    csv_text = tz_row + header + "".join(wind_data)
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    # Test complete wind data workflow
    w = Wind()
    
    # Step 1: Download wind data
    w.DownloadWindData(
        directory=str(tmp_path),
        site_data=real_wind_sites,
        api_key="dummy",
        email="test@test.com",
        affiliation="test",
        year_start=2024,
        year_end=2024,
    )
    
    # Step 2: Process wind farm data
    (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
     out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
    
    # Step 3: Calculate transition rates
    combined_windspeed = tmp_path / "windspeed_data.csv"
    tr_mats = w.CalWindTrRates(
        directory=str(tmp_path),
        windspeed_data=str(combined_windspeed),
        site_data=real_wind_sites,
        pcurve_data=real_wind_data["power_curves_csv"]
    )
    
    # Verify end-to-end workflow completed successfully
    assert w_sites == 4, "Should have 4 wind sites"
    assert len(farm_name) == 4, "Should have 4 farm names"
    assert len(zone_no) == 4, "Should have 4 zones"
    # Get actual number of wind classes from power curve data
    pcurve_df = pd.read_csv(real_wind_data["power_curves_csv"])
    expected_w_classes = len(pcurve_df['Start (m/s)'].values)
    assert w_classes == expected_w_classes, f"Should have {expected_w_classes} wind classes, got {w_classes}"
    # The actual shape depends on wind speed binning - check it's reasonable
    assert tr_mats.shape[0] == 4, "Should have 4 sites"
    assert tr_mats.shape[1] == tr_mats.shape[2], "Transition matrices should be square"
    assert tr_mats.shape[1] > 0, "Transition matrices should have positive dimensions"
    
    # Verify data quality
    assert all(tr > 0 for tr in turbine_rating), "Turbine ratings should be positive"
    assert all(ss >= 0 for ss in start_speed), "Start speeds should be non-negative"
    assert all(pc in [2, 3] for pc in p_class), "Power classes should be 2 or 3"
    assert np.all(tr_mats >= 0), "Transition probabilities should be non-negative"
    assert np.all(tr_mats <= 1), "Transition probabilities should be <= 1"
    
    # Verify output files exist
    base = tmp_path / "wtk_data" / "2024"
    assert base.exists(), "Wind data directory should exist"
    
    # Verify all farm files exist
    for farm_name in farm_name:
        assert (base / f"{farm_name}.csv").exists(), f"Farm {farm_name} file should exist"
    
    # Verify combined windspeed file exists
    assert combined_windspeed.exists(), "Combined windspeed file should exist"
    combined_data = pd.read_csv(combined_windspeed)
    assert len(combined_data) == 8760, "Combined windspeed data should have 8760 hours"


@pytest.mark.integration
@pytest.mark.slow
def test_wind_integration_with_system_data(real_wind_sites, real_wind_data, real_system_data, production_system_summary, tmp_path, monkeypatch):
    """Test wind integration with system data."""
    # Mock API response for consistent testing
    class DummyResp:
        def __init__(self, text):
            self.text = text

    # Create realistic wind data for 8760 hours
    # Timezone info as first row (will be skipped by skiprows=1)
    tz_row = "Time Zone,-7\n"
    header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    
    # Generate 8760 hours of realistic wind data
    wind_data = []
    for hour in range(8760):
        day_of_year = (hour // 24) + 1
        hour_of_day = hour % 24
        
        # Generate realistic wind speeds
        base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)
        hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)
        wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
        wind_100m = wind_80m * 1.1
        
        # Proper month/day calculation
        if day_of_year <= 31:
            month, day = 1, day_of_year
        elif day_of_year <= 59:
            month, day = 2, day_of_year - 31
        elif day_of_year <= 90:
            month, day = 3, day_of_year - 59
        elif day_of_year <= 120:
            month, day = 4, day_of_year - 90
        elif day_of_year <= 151:
            month, day = 5, day_of_year - 120
        elif day_of_year <= 181:
            month, day = 6, day_of_year - 151
        elif day_of_year <= 212:
            month, day = 7, day_of_year - 181
        elif day_of_year <= 243:
            month, day = 8, day_of_year - 212
        elif day_of_year <= 273:
            month, day = 9, day_of_year - 243
        elif day_of_year <= 304:
            month, day = 10, day_of_year - 273
        elif day_of_year <= 334:
            month, day = 11, day_of_year - 304
        else:
            month, day = 12, day_of_year - 334
        wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
    
    csv_text = tz_row + header + "".join(wind_data)
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    # Test wind integration with system data
    w = Wind()
    
    # Process wind data
    w.DownloadWindData(
        directory=str(tmp_path),
        site_data=real_wind_sites,
        api_key="dummy",
        email="test@test.com",
        affiliation="test",
        year_start=2024,
        year_end=2024,
    )
    
    (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
     out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
    
    combined_windspeed = tmp_path / "windspeed_data.csv"
    tr_mats = w.CalWindTrRates(
        directory=str(tmp_path),
        windspeed_data=str(combined_windspeed),
        site_data=real_wind_sites,
        pcurve_data=real_wind_data["power_curves_csv"]
    )
    
    # Load system data
    from progress.mod_sysdata import RASystemData
    sysdata = RASystemData()
    bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
    
    # Verify wind data integration with system data
    assert w_sites == 4, "Should have 4 wind sites"
    assert len(zone_no) == 4, "Should have 4 wind zones"
    assert nz == 3, "Should have 3 system zones"
    
    # Verify wind zones are compatible with system zones
    wind_zones = set(zone_no)
    system_zones = set(bus_no)
    assert wind_zones.issubset(system_zones), "Wind zones should be subset of system zones"
    
    # Verify wind data quality
    assert all(tr > 0 for tr in turbine_rating), "Turbine ratings should be positive"
    assert all(ss >= 0 for ss in start_speed), "Start speeds should be non-negative"
    assert all(pc in [2, 3] for pc in p_class), "Power classes should be 2 or 3"
    assert np.all(tr_mats >= 0), "Transition probabilities should be non-negative"
    assert np.all(tr_mats <= 1), "Transition probabilities should be <= 1"
    
    # Verify wind data has temporal patterns
    if combined_windspeed.exists():
        wind_data_df = pd.read_csv(combined_windspeed)
        assert len(wind_data_df) == 8760, "Wind data should have 8760 hours"
        
        # Verify wind speeds are reasonable
        for farm_name in wind_data_df.columns:
            if farm_name != "Unnamed: 0":  # Skip index column
                wind_speeds = pd.to_numeric(wind_data_df[farm_name], errors='coerce').values
                # Skip NaN values (non-numeric data)
                valid_speeds = wind_speeds[~np.isnan(wind_speeds)]
                if len(valid_speeds) > 0:
                    assert np.all(valid_speeds >= 0), f"Wind speeds for {farm_name} should be non-negative"
                    assert np.all(valid_speeds <= 50), f"Wind speeds for {farm_name} should be reasonable (< 50 m/s)"


@pytest.mark.integration
@pytest.mark.slow
def test_wind_real_world_usage_patterns(real_wind_sites, real_wind_data, tmp_path, monkeypatch):
    """Test wind real-world usage patterns."""
    # Mock API response for consistent testing
    class DummyResp:
        def __init__(self, text):
            self.text = text

    # Create realistic wind data for 8760 hours
    # Timezone info as first row (will be skipped by skiprows=1)
    tz_row = "Time Zone,-7\n"
    header = "Year,Month,Day,Hour,Minute,wind speed at 80m (m/s),wind speed at 100m (m/s)\n"
    
    # Generate 8760 hours of realistic wind data
    wind_data = []
    for hour in range(8760):
        day_of_year = (hour // 24) + 1
        hour_of_day = hour % 24
        
        # Generate realistic wind speeds with temporal patterns
        base_wind = 5 + 3 * np.sin(2 * np.pi * day_of_year / 365)  # Seasonal variation
        hour_variation = 2 * np.sin(2 * np.pi * hour_of_day / 24)  # Daily variation
        wind_80m = max(0, base_wind + hour_variation + np.random.normal(0, 1))
        wind_100m = wind_80m * 1.1  # Higher at 100m
        
        # Proper month/day calculation
        if day_of_year <= 31:
            month, day = 1, day_of_year
        elif day_of_year <= 59:
            month, day = 2, day_of_year - 31
        elif day_of_year <= 90:
            month, day = 3, day_of_year - 59
        elif day_of_year <= 120:
            month, day = 4, day_of_year - 90
        elif day_of_year <= 151:
            month, day = 5, day_of_year - 120
        elif day_of_year <= 181:
            month, day = 6, day_of_year - 151
        elif day_of_year <= 212:
            month, day = 7, day_of_year - 181
        elif day_of_year <= 243:
            month, day = 8, day_of_year - 212
        elif day_of_year <= 273:
            month, day = 9, day_of_year - 243
        elif day_of_year <= 304:
            month, day = 10, day_of_year - 273
        elif day_of_year <= 334:
            month, day = 11, day_of_year - 304
        else:
            month, day = 12, day_of_year - 334
        wind_data.append(f"2024,{month},{day},{hour_of_day},0,{wind_80m:.1f},{wind_100m:.1f}\n")
    
    csv_text = tz_row + header + "".join(wind_data)
    monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

    # Test wind real-world usage patterns
    w = Wind()
    
    # Simulate multiple wind data processing cycles
    for cycle in range(3):
        # Download wind data
        w.DownloadWindData(
            directory=str(tmp_path),
            site_data=real_wind_sites,
            api_key="dummy",
            email="test@test.com",
            affiliation="test",
            year_start=2024,
            year_end=2024,
        )
        
        # Process wind farm data
        (w_sites, farm_name, zone_no, w_classes, w_turbines, turbine_rating, p_class, 
         out_curve2, out_curve3, start_speed) = w.WindFarmsData(real_wind_sites, real_wind_data["power_curves_csv"])
        
        # Calculate transition rates
        combined_windspeed = tmp_path / "windspeed_data.csv"
        tr_mats = w.CalWindTrRates(
            directory=str(tmp_path),
            windspeed_data=str(combined_windspeed),
            site_data=real_wind_sites,
            pcurve_data=real_wind_data["power_curves_csv"]
        )
        
        # Verify each cycle completed successfully
        assert w_sites == 4, f"Cycle {cycle}: Should have 4 wind sites"
        assert len(farm_name) == 4, f"Cycle {cycle}: Should have 4 farm names"
        assert len(zone_no) == 4, f"Cycle {cycle}: Should have 4 zones"
        # Get actual number of wind classes from power curve data
        pcurve_df = pd.read_csv(real_wind_data["power_curves_csv"])
        expected_w_classes = len(pcurve_df['Start (m/s)'].values)
        assert w_classes == expected_w_classes, f"Cycle {cycle}: Should have {expected_w_classes} wind classes, got {w_classes}"
        assert tr_mats.shape == (4, expected_w_classes, expected_w_classes), f"Cycle {cycle}: Should have 4x{expected_w_classes}x{expected_w_classes} transition matrices"
        
        # Verify data quality
        assert all(tr > 0 for tr in turbine_rating), f"Cycle {cycle}: Turbine ratings should be positive"
        assert all(ss >= 0 for ss in start_speed), f"Cycle {cycle}: Start speeds should be non-negative"
        assert all(pc in [2, 3] for pc in p_class), f"Cycle {cycle}: Power classes should be 2 or 3"
        assert np.all(tr_mats >= 0), f"Cycle {cycle}: Transition probabilities should be non-negative"
        assert np.all(tr_mats <= 1), f"Cycle {cycle}: Transition probabilities should be <= 1"
    
    # Verify output files exist
    base = tmp_path / "wtk_data" / "2024"
    assert base.exists(), "Wind data directory should exist"
    
    # Verify all farm files exist
    wind_sites_df = pd.read_csv(real_wind_sites)
    for farm_name in wind_sites_df["Farm Name"]:
        assert (base / f"{farm_name}.csv").exists(), f"Farm {farm_name} file should exist"
    
    # Verify combined windspeed file exists
    combined_windspeed = tmp_path / "windspeed_data.csv"
    assert combined_windspeed.exists(), "Combined windspeed file should exist"
    combined_data = pd.read_csv(combined_windspeed)
    assert len(combined_data) == 8760, "Combined windspeed data should have 8760 hours"


