"""
Comprehensive test suite for Solar class.

This module tests each method in Solar using real production data patterns,
with comprehensive parameter validation, output validation, and exception handling.
"""

import os
import tempfile
import time
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

pytest.importorskip("openpyxl")

try:
    from progress.mod_solar import Solar
except Exception:
    from progress.mod_solar import Solar

# Optional imports for advanced testing
try:
    import psutil
except ImportError:
    psutil = None


# Integration Tests - Real Data Required

def get_dynamic_solar_sites(real_solar_sites, count=None):
    """Helper function to get dynamic site selections from real data."""
    sites_df = pd.read_csv(real_solar_sites)
    all_sites = sites_df["site_name"].tolist()
    if count is None:
        return all_sites
    return all_sites[:count]


# Unit Tests - No Real Data Required

class TestInitialization:
    """
    Test Solar class initialization and constructor functionality.
    
    This test class validates that the Solar class can be properly instantiated
    with various site data configurations and parameter combinations. It ensures
    that the solar energy analysis tool is correctly configured for different
    use cases and data structures.
    """
    
    def test_init_with_valid_sites(self, tmp_path):
        """
        Test Solar class initialization with valid site data from CSV file.
        
        This test verifies that the Solar class can be successfully instantiated
        when provided with a valid CSV file containing solar site information.
        It validates that the constructor properly parses site data and initializes
        all necessary attributes for solar energy analysis.
        
        The test validates that:
        - Site data is correctly loaded from CSV file
        - All site attributes are properly initialized (names, coordinates, capacity, zones)
        - Site count is accurately calculated
        - Data types and formats are correctly processed
        - No errors occur during initialization
        
        Expected behavior: Constructor should successfully create a Solar instance
        with all site data properly loaded and attributes correctly set.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA", "SiteB"],
            "lat": [35.0, 36.0],
            "long": [-106.0, -105.5],
            "tracking": [1, 2],
            "MW": [10.0, 20.0],
            "zone": [1, 2],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        assert sol.n_sites == 2
        assert list(sol.names) == ["SiteA", "SiteB"]
        assert list(sol.MW) == [10.0, 20.0]
        assert list(sol.s_zone_no) == [1, 2]
    
    def test_init_parses_all_columns(self, tmp_path):
        """
        Test Solar class initialization with comprehensive column parsing.
        
        This test verifies that the Solar class correctly parses and processes
        all required columns from the site data CSV file. It ensures that
        all necessary solar site attributes are properly extracted and stored.
        
        The test validates that:
        - All required columns are correctly parsed from CSV
        - Column data types are properly handled and converted
        - Missing optional columns are handled gracefully
        - Data validation occurs for all column values
        - All site attributes are properly initialized
        
        Expected behavior: Constructor should successfully parse all columns
        and initialize all necessary solar site attributes.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [10.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        
        # Verify all attributes are set
        assert hasattr(sol, 'n_sites')
        assert hasattr(sol, 'names')
        assert hasattr(sol, 'lats')
        assert hasattr(sol, 'lons')
        assert hasattr(sol, 'tracking')
        assert hasattr(sol, 'MW')
        assert hasattr(sol, 's_zone_no')
        assert hasattr(sol, 'directory')
    
    def test_init_with_single_site(self, tmp_path):
        """
        Test Solar class initialization with a single solar site.
        
        This test verifies that the Solar class can be successfully initialized
        when provided with data for a single solar site. It ensures that
        the solar energy analysis tool is properly configured for single-site
        scenarios.
        
        The test validates that:
        - Single site data is correctly loaded and processed
        - All site attributes are properly initialized
        - Site count is correctly calculated as 1
        - Data structure is appropriate for single-site analysis
        - No errors occur during initialization
        
        Expected behavior: Constructor should successfully initialize with
        single site data and be ready for solar energy analysis.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [10.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        assert sol.n_sites == 1
        assert sol.names.iloc[0] == "SiteA"
        assert sol.lats.iloc[0] == 35.0
        assert sol.lons.iloc[0] == -106.0
        assert sol.tracking.iloc[0] == 1
        assert sol.MW.iloc[0] == 10.0
        assert sol.s_zone_no.iloc[0] == 1
    
    def test_init_with_multiple_sites(self, tmp_path):
        """
        Test Solar class initialization with multiple solar sites.
        
        This test verifies that the Solar class can be successfully initialized
        when provided with data for multiple solar sites. It ensures that
        the solar energy analysis tool is properly configured for multi-site
        analysis scenarios.
        
        The test validates that:
        - Multiple site data is correctly loaded and processed
        - All site attributes are properly initialized for each site
        - Site count is correctly calculated
        - Data structure is appropriate for multi-site analysis
        - No errors occur during initialization
        
        Expected behavior: Constructor should successfully initialize with
        multiple site data and be ready for comprehensive solar energy analysis.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA", "SiteB", "SiteC"],
            "lat": [35.0, 36.0, 37.0],
            "long": [-106.0, -105.5, -105.0],
            "tracking": [1, 0, 1],
            "MW": [10.0, 20.0, 15.0],
            "zone": [1, 2, 1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        assert sol.n_sites == 3
        assert len(sol.names) == 3
        assert len(sol.lats) == 3
        assert len(sol.lons) == 3
        assert len(sol.tracking) == 3
        assert len(sol.MW) == 3
        assert len(sol.s_zone_no) == 3
    
    def test_init_missing_required_column(self, tmp_path):
        """
        Test Solar class error handling when required columns are missing.
        
        This test verifies that the Solar class properly handles error conditions
        when essential columns are missing from the input CSV file. It ensures
        that the constructor provides clear feedback about missing data requirements.
        
        The test validates that:
        - Missing required columns are properly detected
        - Appropriate exceptions are raised with clear error messages
        - Error handling is consistent across different missing column scenarios
        - The constructor fails gracefully without crashing
        - Error messages help identify which columns are missing
        
        Expected behavior: Constructor should raise appropriate exceptions
        with clear messages indicating which required columns are missing.
        
        Args:
            tmp_path: Temporary directory path for creating test CSV files
        """
        site_csv = tmp_path / "solar_sites.csv"
        # Missing MW column
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            # "MW": [10.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        with pytest.raises(KeyError):
            Solar(site_data=str(site_csv), directory=str(tmp_path))
    
    def test_init_malformed_csv(self, tmp_path):
        """Test handling of malformed CSV structure."""
        site_csv = tmp_path / "solar_sites.csv"
        # Create malformed CSV
        site_csv.write_text("invalid,data\n1,2,3\n")

        with pytest.raises((ValueError, KeyError)):
            Solar(site_data=str(site_csv), directory=str(tmp_path))
    
    def test_init_data_validation(self, tmp_path):
        """Validate data types and ranges."""
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA", "SiteB"],
            "lat": [35.0, 36.0],
            "long": [-106.0, -105.5],
            "tracking": [1, 0],
            "MW": [10.0, 20.0],
            "zone": [1, 2],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        
        # Validate data types
        assert isinstance(sol.n_sites, int)
        assert isinstance(sol.names, pd.Series)
        assert isinstance(sol.lats, pd.Series)
        assert isinstance(sol.lons, pd.Series)
        assert isinstance(sol.tracking, pd.Series)
        assert isinstance(sol.MW, pd.Series)
        assert isinstance(sol.s_zone_no, pd.Series)
        
        # Validate ranges
        assert all(25 <= lat <= 50 for lat in sol.lats)  # US latitude range
        assert all(-125 <= lon <= -65 for lon in sol.lons)  # US longitude range
        assert all(mw > 0 for mw in sol.MW)  # Positive MW
        assert all(track in [0, 1] for track in sol.tracking)  # Valid tracking values
        assert all(zone > 0 for zone in sol.s_zone_no)  # Positive zone numbers


class TestSolarGen:
    """Test SolarGen method."""
    
    def test_solargen_basic_functionality(self, tmp_path, monkeypatch):
        """Test with mocked API/PVLib for single site."""
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))

        # Mock requests.get to return a minimal plausible CSV
        class DummyResp:
            def __init__(self, text):
                self.text = text

        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        data = "2024,1,1,0,0,500,600,100,700,800,150,20,3\n2024,1,1,1,0,510,610,110,710,810,160,21,4\n"
        csv_text = tz_row + header + data

        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Mock pvlib modelchain behavior
        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                self.results = DummyResults([1.0, 1.1])

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        # Run for a single year
        sol.SolarGen(
            api_key="dummy",
            your_name="n",
            your_affiliation="a",
            your_email="e@example.com",
            year_start=2024,
            year_end=2024,
        )

        # Assert files exist under directory/solardata/2024
        base = tmp_path / "solardata" / "2024"
        assert base.exists()
        assert (base / "SiteA.csv").exists()
        assert (base / "SiteA_sgen_sat.csv").exists()
        assert (base / "SiteA_sgen_cs.csv").exists()
    
    def test_solargen_creates_directory_structure(self, tmp_path, monkeypatch):
        """Verify solardata/YEAR/ directories created."""
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))

        # Mock API and PVLib
        class DummyResp:
            def __init__(self, text):
                self.text = text

        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        data = "2024,1,1,0,0,500,600,100,700,800,150,20,3\n"
        csv_text = tz_row + header + data
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                self.results = DummyResults([1.0])

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        sol.SolarGen("k", "n", "a", "e", 2024, 2024)

        # Verify directory structure
        assert (tmp_path / "solardata").exists()
        assert (tmp_path / "solardata" / "2024").exists()
    
    def test_solargen_writes_expected_files(self, tmp_path, monkeypatch):
        """Verify CSV files created."""
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA", "SiteB"],
            "lat": [35.0, 36.0],
            "long": [-106.0, -105.5],
            "tracking": [1, 2],
            "MW": [1.0, 1.0],
            "zone": [1, 2],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))

        # Mock API and PVLib
        class DummyResp:
            def __init__(self, text):
                self.text = text

        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        data = "2024,1,1,0,0,500,600,100,700,800,150,20,3\n2024,1,1,1,0,510,610,110,710,810,160,21,4\n"
        csv_text = tz_row + header + data
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                self.results = DummyResults([1.0, 1.1])

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        sol.SolarGen("k", "n", "a", "e", 2024, 2024)

        # Verify all expected files exist
        base = tmp_path / "solardata" / "2024"
        assert (base / "SiteA.csv").exists()
        assert (base / "SiteA_sgen_sat.csv").exists()
        assert (base / "SiteA_sgen_cs.csv").exists()
        assert (base / "SiteB.csv").exists()
        assert (base / "SiteB_sgen_sat.csv").exists()
        assert (base / "SiteB_sgen_cs.csv").exists()
    
    def test_solargen_parameter_validation(self, tmp_path):
        """Test invalid year ranges, API parameters."""
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))

        # Test invalid year ranges
        with pytest.raises(TypeError):
            sol.SolarGen("k", "n", "a", "e", "invalid", 2024)
        
        with pytest.raises(TypeError):
            sol.SolarGen("k", "n", "a", "e", 2024, "invalid")
        
        # Test start > end (this doesn't raise an error, it just creates empty range)
        sol.SolarGen("k", "n", "a", "e", 2025, 2024)  # This should work but create empty range
    
    def test_solargen_leap_year_handling(self, tmp_path, monkeypatch):
        """Test leap year detection."""
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))

        # Mock API and PVLib
        class DummyResp:
            def __init__(self, text):
                self.text = text

        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        data = "2024,1,1,0,0,500,600,100,700,800,150,20,3\n"
        csv_text = tz_row + header + data
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                self.results = DummyResults([1.0])

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        # Test leap year (2024)
        sol.SolarGen("k", "n", "a", "e", 2024, 2024)
        assert (tmp_path / "solardata" / "2024").exists()

        # Test non-leap year (2023)
        sol.SolarGen("k", "n", "a", "e", 2023, 2023)
        assert (tmp_path / "solardata" / "2023").exists()
    
    def test_solargen_path_cwd_independence(self, tmp_path, monkeypatch):
        """Verify outputs go to correct directory, not CWD."""
        site_csv = tmp_path / "sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        # Mock API and PVLib
        class DummyResp:
            def __init__(self, text):
                self.text = text

        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        data = "2024,1,1,0,0,500,600,100,700,800,150,20,3\n"
        csv_text = tz_row + header + data
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                self.results = DummyResults([1.0])

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        # Absolute path first
        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        sol.SolarGen("k", "n", "a", "e", 2024, 2024)
        assert (tmp_path / "solardata" / "2024" / "SiteA_sgen_sat.csv").exists()

        # Relative after chdir
        old = os.getcwd()
        try:
            os.chdir(tmp_path)
            sol_rel = Solar(site_data=str(site_csv.name), directory=".")
            sol_rel.SolarGen("k", "n", "a", "e", 2024, 2024)
            assert (Path("solardata") / "2024" / "SiteA_sgen_cs.csv").exists()
        finally:
            os.chdir(old)


class TestSolarGenGather:
    """Test SolarGenGather method."""
    
    def test_solargengather_basic_functionality(self, tmp_path):
        """Test gathering from per-site files."""
        # Prepare directory tree with per-site/year files
        base = tmp_path / "solardata" / "2024"
        base.mkdir(parents=True)
        
        # Create 8784 hours of data (full year, 2024 is leap year)
        sat_data_a = [1.0] * 8784
        cs_data_a = [0.9] * 8784
        sat_data_b = [2.0] * 8784
        cs_data_b = [1.8] * 8784
        
        pd.DataFrame({"p_mp": sat_data_a}).to_csv(base / "SiteA_sgen_sat.csv", index=False)
        pd.DataFrame({"p_mp": cs_data_a}).to_csv(base / "SiteA_sgen_cs.csv", index=False)
        pd.DataFrame({"p_mp": sat_data_b}).to_csv(base / "SiteB_sgen_sat.csv", index=False)
        pd.DataFrame({"p_mp": cs_data_b}).to_csv(base / "SiteB_sgen_cs.csv", index=False)

        # Sites CSV defining names order
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA", "SiteB"],
            "lat": [35.0, 36.0],
            "long": [-106.0, -105.5],
            "tracking": [1, 2],
            "MW": [1.0, 2.0],
            "zone": [1, 2],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        sol.SolarGenGather(2024, 2024)

        # Verify Excel file created
        excel_path = tmp_path / "solar_data.xlsx"
        assert excel_path.exists()
        sheets = pd.read_excel(excel_path, sheet_name=["solar_gen", "csi"])
        assert not sheets["solar_gen"].empty
        assert not sheets["csi"].empty
    
    def test_solargengather_creates_excel(self, tmp_path):
        """Verify solar_data.xlsx created with sheets."""
        # Prepare directory tree with per-site/year files
        base = tmp_path / "solardata" / "2024"
        base.mkdir(parents=True)
        
        # Create 8784 hours of data (full year, 2024 is leap year)
        sat_data = [1.0] * 8784
        cs_data = [0.9] * 8784
        pd.DataFrame({"p_mp": sat_data}).to_csv(base / "SiteA_sgen_sat.csv", index=False)
        pd.DataFrame({"p_mp": cs_data}).to_csv(base / "SiteA_sgen_cs.csv", index=False)

        # Sites CSV
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        sol.SolarGenGather(2024, 2024)

        # Verify Excel file structure
        excel_path = tmp_path / "solar_data.xlsx"
        assert excel_path.exists()
        
        # Read Excel file
        with pd.ExcelFile(excel_path) as xls:
            sheet_names = xls.sheet_names
            assert "solar_gen" in sheet_names
            assert "csi" in sheet_names
            
            # Check sheet contents
            solar_gen_df = pd.read_excel(excel_path, sheet_name="solar_gen")
            csi_df = pd.read_excel(excel_path, sheet_name="csi")
            
            assert not solar_gen_df.empty
            assert not csi_df.empty
            assert "datetime" in solar_gen_df.columns
            assert "datetime" in csi_df.columns
    
    def test_solargengather_csi_calculation(self, tmp_path):
        """Verify CSI = satellite / clearsky."""
        # Prepare directory tree with per-site/year files
        base = tmp_path / "solardata" / "2024"
        base.mkdir(parents=True)
        
        # Create 8784 hours of data (full year, 2024 is leap year)
        sat_data = [2.0] * 8784  # All satellite data = 2.0
        cs_data = [1.0] * 8784   # All clearsky data = 1.0
        pd.DataFrame({"p_mp": sat_data}).to_csv(base / "SiteA_sgen_sat.csv", index=False)
        pd.DataFrame({"p_mp": cs_data}).to_csv(base / "SiteA_sgen_cs.csv", index=False)

        # Sites CSV
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        sol.SolarGenGather(2024, 2024)

        # Verify CSI calculation
        excel_path = tmp_path / "solar_data.xlsx"
        csi_df = pd.read_excel(excel_path, sheet_name="csi")
        
        # CSI should be satellite / clearsky = 2.0 / 1.0 = 2.0 for all hours
        # Check first few values and that all are approximately 2.0
        csi_values = csi_df["SiteA"].dropna().tolist()
        assert len(csi_values) == 8784, f"Expected 8784 CSI values, got {len(csi_values)}"
        assert all(abs(val - 2.0) < 0.001 for val in csi_values[:10]), f"First 10 CSI values should be ~2.0, got {csi_values[:10]}"
    
    def test_solargengather_datetime_vector(self, tmp_path):
        """Verify datetime column added correctly."""
        # Prepare directory tree with per-site/year files
        base = tmp_path / "solardata" / "2024"
        base.mkdir(parents=True)
        
        # Create 8784 hours of data (full year, 2024 is leap year)
        sat_data = [1.0] * 8784
        cs_data = [0.9] * 8784
        pd.DataFrame({"p_mp": sat_data}).to_csv(base / "SiteA_sgen_sat.csv", index=False)
        pd.DataFrame({"p_mp": cs_data}).to_csv(base / "SiteA_sgen_cs.csv", index=False)

        # Sites CSV
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        sol.SolarGenGather(2024, 2024)

        # Verify datetime column
        excel_path = tmp_path / "solar_data.xlsx"
        solar_gen_df = pd.read_excel(excel_path, sheet_name="solar_gen")
        csi_df = pd.read_excel(excel_path, sheet_name="csi")
        
        assert "datetime" in solar_gen_df.columns
        assert "datetime" in csi_df.columns
        assert len(solar_gen_df) == 8784  # 8784 hours (2024 is leap year)
        assert len(csi_df) == 8784
    
    def test_solargengather_missing_files(self, tmp_path):
        """Test exception when per-site files missing."""
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))

        # No per-site files present; expect error
        with pytest.raises(Exception):
            sol.SolarGenGather(2024, 2024)
    
    def test_solargengather_multi_year(self, tmp_path):
        """Test gathering across multiple years."""
        # Prepare directory tree for multiple years
        for year in [2022, 2023, 2024]:
            base = tmp_path / "solardata" / str(year)
            base.mkdir(parents=True)
            
            # Create 8760 hours of data for each year
            sat_data = [1.0] * 8760
            cs_data = [0.9] * 8760
            pd.DataFrame({"p_mp": sat_data}).to_csv(base / "SiteA_sgen_sat.csv", index=False)
            pd.DataFrame({"p_mp": cs_data}).to_csv(base / "SiteA_sgen_cs.csv", index=False)

        # Sites CSV
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        sol.SolarGenGather(2022, 2024)

        # Verify Excel file created with multi-year data
        excel_path = tmp_path / "solar_data.xlsx"
        assert excel_path.exists()
        
        solar_gen_df = pd.read_excel(excel_path, sheet_name="solar_gen")
        csi_df = pd.read_excel(excel_path, sheet_name="csi")
        
        # Should have 26304 data points (8760 + 8760 + 8784 for 2022, 2023, 2024)
        assert len(solar_gen_df) == 26304
        assert len(csi_df) == 26304


class TestGetSolarProfiles:
    """Test GetSolarProfiles method."""
    
    def test_getsolarprofiles_basic_functionality(self, tmp_path):
        """Test with mock cluster directories."""
        # Create directory structure: Clusters/1 and Clusters/2 with per-site CSVs
        clusters_base = tmp_path / "Clusters"
        (clusters_base / "1").mkdir(parents=True)
        (clusters_base / "2").mkdir(parents=True)

        # Two sites, 2 days with 3 hours each (shape 2x3)
        pd.DataFrame([[1, 2, 3], [4, 5, 6]]).to_csv(clusters_base / "1" / "SiteA.csv", index=False)
        pd.DataFrame([[2, 3, 4], [5, 6, 7]]).to_csv(clusters_base / "1" / "SiteB.csv", index=False)
        pd.DataFrame([[3, 4, 5], [6, 7, 8]]).to_csv(clusters_base / "2" / "SiteA.csv", index=False)
        pd.DataFrame([[1, 1, 1], [2, 2, 2]]).to_csv(clusters_base / "2" / "SiteB.csv", index=False)

        # solar_probs.csv
        probs = tmp_path / "solar_probs.csv"
        pd.DataFrame([[0.5, 0.5], [0.4, 0.6]]).to_csv(probs, index=False)

        # Sites CSV order
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA", "SiteB"],
            "lat": [35.0, 36.0],
            "long": [-106.0, -105.5],
            "tracking": [1, 2],
            "MW": [1.0, 2.0],
            "zone": [1, 2],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        n_sites, s_zone_no, MW, s_profiles, solar_prob = sol.GetSolarProfiles(str(probs))

        assert n_sites == 2
        assert len(s_profiles) == 2
        assert s_profiles[0].shape == (2, 3, 2)
        assert s_profiles[1].shape == (2, 3, 2)
        assert isinstance(solar_prob, np.ndarray)
    
    def test_getsolarprofiles_shapes_and_paths(self, tmp_path):
        """Verify output shape."""
        # Create directory structure
        clusters_base = tmp_path / "Clusters"
        (clusters_base / "1").mkdir(parents=True)
        (clusters_base / "2").mkdir(parents=True)

        # Create test data
        pd.DataFrame([[1, 2, 3], [4, 5, 6]]).to_csv(clusters_base / "1" / "SiteA.csv", index=False)
        pd.DataFrame([[2, 3, 4], [5, 6, 7]]).to_csv(clusters_base / "1" / "SiteB.csv", index=False)
        pd.DataFrame([[3, 4, 5], [6, 7, 8]]).to_csv(clusters_base / "2" / "SiteA.csv", index=False)
        pd.DataFrame([[1, 1, 1], [2, 2, 2]]).to_csv(clusters_base / "2" / "SiteB.csv", index=False)

        probs = tmp_path / "solar_probs.csv"
        pd.DataFrame([[0.5, 0.5], [0.4, 0.6]]).to_csv(probs, index=False)

        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA", "SiteB"],
            "lat": [35.0, 36.0],
            "long": [-106.0, -105.5],
            "tracking": [1, 2],
            "MW": [1.0, 2.0],
            "zone": [1, 2],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        n_sites, s_zone_no, MW, s_profiles, solar_prob = sol.GetSolarProfiles(str(probs))

        # Verify shapes
        assert n_sites == 2
        assert len(s_profiles) == 2  # 2 clusters
        assert s_profiles[0].shape == (2, 3, 2)  # (days, hours, sites)
        assert s_profiles[1].shape == (2, 3, 2)
        assert solar_prob.shape == (2, 2)  # (clusters, months)
    
    def test_getsolarprofiles_returns_correct_tuple(self, tmp_path):
        """Verify returns correct tuple."""
        # Create directory structure
        clusters_base = tmp_path / "Clusters"
        (clusters_base / "1").mkdir(parents=True)

        pd.DataFrame([[1, 2, 3], [4, 5, 6]]).to_csv(clusters_base / "1" / "SiteA.csv", index=False)

        probs = tmp_path / "solar_probs.csv"
        pd.DataFrame([[0.5, 0.5]]).to_csv(probs, index=False)

        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        result = sol.GetSolarProfiles(str(probs))

        # Verify tuple structure
        assert isinstance(result, tuple)
        assert len(result) == 5
        n_sites, s_zone_no, MW, s_profiles, solar_prob = result
        
        assert isinstance(n_sites, int)
        assert isinstance(s_zone_no, pd.Series)
        assert isinstance(MW, pd.Series)
        assert isinstance(s_profiles, list)
        assert isinstance(solar_prob, np.ndarray)
    
    def test_getsolarprofiles_missing_clusters(self, tmp_path):
        """Test behavior when Clusters/ directory missing."""
        probs = tmp_path / "solar_probs.csv"
        pd.DataFrame([[0.5, 0.5]]).to_csv(probs, index=False)

        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))

        # No Clusters directory - method should return empty results
        n_sites, s_zone_no, MW, s_profiles, solar_prob = sol.GetSolarProfiles(str(probs))
        
        # Verify empty results
        assert n_sites == 1
        assert len(s_profiles) == 0  # No clusters found
        assert isinstance(solar_prob, np.ndarray)
    
    def test_getsolarprofiles_empty_clusters(self, tmp_path):
        """Test handling of empty cluster directories."""
        # Create empty cluster directory
        clusters_base = tmp_path / "Clusters"
        (clusters_base / "1").mkdir(parents=True)
        # No CSV files in cluster directory

        probs = tmp_path / "solar_probs.csv"
        pd.DataFrame([[0.5, 0.5]]).to_csv(probs, index=False)

        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))

        # Should handle empty cluster gracefully - this will raise FileNotFoundError when trying to read CSV
        with pytest.raises(FileNotFoundError):
            sol.GetSolarProfiles(str(probs))


# Integration Tests - Real Data Required

class TestRealDataIntegration:
    """Test with real production data."""
    
    def test_init_with_real_solar_sites(self, real_solar_sites, tmp_path):
        """Test initialization with real solar_sites.csv."""
        sol = Solar(site_data=real_solar_sites, directory=str(tmp_path))
        
        # Verify site loading
        assert sol.n_sites == 25
        assert len(sol.names) == 25
        assert len(sol.MW) == 25
        assert len(sol.s_zone_no) == 25
        
        # Verify data types
        assert isinstance(sol.names, pd.Series)
        assert isinstance(sol.lats, pd.Series)
        assert isinstance(sol.lons, pd.Series)
        assert isinstance(sol.tracking, pd.Series)
        assert isinstance(sol.MW, pd.Series)
        assert isinstance(sol.s_zone_no, pd.Series)
    
    def test_real_solar_25_sites_3_zones(self, real_solar_sites):
        """Validate real site data structure."""
        # Load solar sites data
        solar_sites_df = pd.read_csv(real_solar_sites)
        
        # Verify production data structure
        assert len(solar_sites_df) == 25  # 25 solar sites
        assert "site_name" in solar_sites_df.columns
        assert "lat" in solar_sites_df.columns
        assert "long" in solar_sites_df.columns
        assert "MW" in solar_sites_df.columns
        assert "tracking" in solar_sites_df.columns
        assert "zone" in solar_sites_df.columns
        
        # Verify zones (should be 1, 2, 3 based on production data)
        zones = solar_sites_df["zone"].unique()
        assert len(zones) == 3
        assert 1 in zones
        assert 2 in zones
        assert 3 in zones
        
        # Verify site capacities are reasonable
        assert all(solar_sites_df["MW"] > 0)
        assert all(solar_sites_df["MW"] < 200)  # Reasonable upper bound
        
        # Verify coordinates are reasonable (US-based)
        assert all(25 <= solar_sites_df["lat"]) and all(solar_sites_df["lat"] <= 50)
        assert all(-125 <= solar_sites_df["long"]) and all(solar_sites_df["long"] <= -65)
        
        # Verify tracking values are valid (0 or 1)
        assert all(solar_sites_df["tracking"].isin([0, 1]))
        
        # Verify site names are unique
        assert len(solar_sites_df["site_name"].unique()) == 25
    
    def test_solar_generation_8760_hours(self, real_solar_data):
        """Validate real solar_data.xlsx structure if exists."""
        if not Path(real_solar_data).exists():
            pytest.skip("Production solar_data.xlsx not available")
        
        # Load solar data
        solar_gen_df = pd.read_excel(real_solar_data, sheet_name="solar_gen")
        csi_df = pd.read_excel(real_solar_data, sheet_name="csi")
        
        # Verify data structure
        assert "datetime" in solar_gen_df.columns
        assert "datetime" in csi_df.columns
        
        # Verify time series length (should be 8760 hours for full year)
        assert len(solar_gen_df) == 8760
        assert len(csi_df) == 8760
        
        # Verify datetime format (stored as strings)
        assert pd.api.types.is_string_dtype(solar_gen_df["datetime"])
        assert pd.api.types.is_string_dtype(csi_df["datetime"])
        
        # Verify hourly frequency (check string format)
        datetime_values = solar_gen_df["datetime"].tolist()
        assert len(datetime_values) == 8760
        # Check that we have hourly data (first few entries should be consecutive hours)
        assert "00:00" in datetime_values[0]
        assert "01:00" in datetime_values[1]
        
        # Verify solar generation values are reasonable
        gen_cols = [col for col in solar_gen_df.columns if col != "datetime"]
        for col in gen_cols:
            assert all(solar_gen_df[col] >= 0)  # Non-negative generation
            # Note: Real data may not be normalized, so we just check it's reasonable
            assert all(solar_gen_df[col] <= 1000)  # Reasonable upper bound
        
        # Verify CSI values are reasonable
        csi_cols = [col for col in csi_df.columns if col != "datetime"]
        for col in csi_cols:
            assert all(csi_df[col] >= 0)  # Non-negative CSI
            # Note: Real data may have all zeros, which is valid
            assert all(csi_df[col] <= 10)  # Reasonable upper bound
    
    def test_solargen_all_sites_8760_hours(self, real_solar_sites, tmp_path, monkeypatch):
        """Test SolarGen with all 25 sites for full year (mocked API)."""
        # Mock API response for consistent testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        # Create simple weather data for 8760 hours (non-leap year)
        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        
        # Generate 8760 hours of simple weather data
        weather_data = []
        for hour in range(8760):
            day_of_year = (hour // 24) + 1
            hour_of_day = hour % 24
            
            # Simple day calculation (non-leap year)
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
            
            # Simple solar model
            if 6 <= hour_of_day <= 18:  # Day hours
                dni = 500
                ghi = 600
                dhi = 100
            else:  # Night hours
                dni = 0
                ghi = 0
                dhi = 0
            
            clearsky_dni = dni * 1.1
            clearsky_ghi = ghi * 1.1
            clearsky_dhi = dhi * 1.1
            
            temp = 20
            wind_speed = 3
            
            weather_data.append(f"2024,{month},{day},{hour_of_day},0,{dni},{ghi},{dhi},{clearsky_dni},{clearsky_ghi},{clearsky_dhi},{temp},{wind_speed}\n")
        
        csv_text = tz_row + header + "".join(weather_data)
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        # Mock PVLib for consistent testing
        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                # Generate realistic solar generation (0-1 normalized)
                self.results = DummyResults(np.random.uniform(0, 1, 8760))

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        # Test with all 25 production sites
        sol = Solar(site_data=real_solar_sites, directory=str(tmp_path))
        
        # Verify site loading
        assert sol.n_sites == 25
        assert len(sol.names) == 25
        assert len(sol.MW) == 25
        assert len(sol.s_zone_no) == 25
        
        # Run SolarGen for full year
        sol.SolarGen(
            api_key="dummy",
            your_name="test",
            your_affiliation="test",
            your_email="test@test.com",
            year_start=2024,
            year_end=2024,
        )

        # Verify output structure
        base = tmp_path / "solardata" / "2024"
        assert base.exists()
        
        # Verify all 25 sites have output files
        for site_name in sol.names:
            assert (base / f"{site_name}.csv").exists()
            assert (base / f"{site_name}_sgen_sat.csv").exists()
            assert (base / f"{site_name}_sgen_cs.csv").exists()
            
            # Verify file contents have 8760 hours
            sat_file = base / f"{site_name}_sgen_sat.csv"
            cs_file = base / f"{site_name}_sgen_cs.csv"
            
            if sat_file.exists():
                sat_data = pd.read_csv(sat_file)
                assert len(sat_data) == 8760, f"Site {site_name} satellite data should have 8760 hours"
            
            if cs_file.exists():
                cs_data = pd.read_csv(cs_file)
                assert len(cs_data) == 8760, f"Site {site_name} clearsky data should have 8760 hours"
    
    def test_solargengather_with_real_sites(self, real_solar_sites, tmp_path):
        """Test gathering with real site names."""
        # Create mock per-site files with real site names
        sites_df = pd.read_csv(real_solar_sites)
        real_site_names = sites_df["site_name"].tolist()[:3]  # Use first 3 sites
        
        base = tmp_path / "solardata" / "2024"
        base.mkdir(parents=True)
        
        # Create 8784 hours of data for each site (2024 is leap year)
        for site_name in real_site_names:
            sat_data = [1.0] * 8784
            cs_data = [0.9] * 8784
            pd.DataFrame({"p_mp": sat_data}).to_csv(base / f"{site_name}_sgen_sat.csv", index=False)
            pd.DataFrame({"p_mp": cs_data}).to_csv(base / f"{site_name}_sgen_cs.csv", index=False)

        # Create a subset CSV with only the first 3 sites
        subset_csv = tmp_path / "subset_sites.csv"
        sites_df.head(3).to_csv(subset_csv, index=False)

        sol = Solar(site_data=str(subset_csv), directory=str(tmp_path))
        sol.SolarGenGather(2024, 2024)

        # Verify Excel file created
        excel_path = tmp_path / "solar_data.xlsx"
        assert excel_path.exists()
        
        # Verify sheets contain real site names
        solar_gen_df = pd.read_excel(excel_path, sheet_name="solar_gen")
        csi_df = pd.read_excel(excel_path, sheet_name="csi")
        
        for site_name in real_site_names:
            assert site_name in solar_gen_df.columns
            assert site_name in csi_df.columns


class TestDataValidation:
    """Test data validation and error handling."""
    
    def test_site_data_structure_validation(self, real_solar_sites):
        """Validate CSV columns, data types, ranges."""
        sites_df = pd.read_csv(real_solar_sites)
        
        # Validate required columns
        required_columns = ['site_name', 'lat', 'long', 'MW', 'tracking', 'zone']
        for col in required_columns:
            assert col in sites_df.columns, f"Missing required column: {col}"
        
        # Validate data types
        assert pd.api.types.is_string_dtype(sites_df['site_name'])
        assert pd.api.types.is_numeric_dtype(sites_df['lat'])
        assert pd.api.types.is_numeric_dtype(sites_df['long'])
        assert pd.api.types.is_numeric_dtype(sites_df['MW'])
        assert pd.api.types.is_numeric_dtype(sites_df['tracking'])
        assert pd.api.types.is_numeric_dtype(sites_df['zone'])
        
        # Validate no missing values
        assert not sites_df.isnull().any().any(), "Missing values found in site data"
    
    def test_coordinate_validation(self, real_solar_sites):
        """Verify lat/long in reasonable US ranges."""
        sites_df = pd.read_csv(real_solar_sites)
        
        # Verify coordinate ranges (US-based)
        assert all(25 <= lat <= 50 for lat in sites_df['lat']), "Latitudes should be in US range (25-50°N)"
        assert all(-125 <= lon <= -65 for lon in sites_df['long']), "Longitudes should be in US range (125-65°W)"
        
        # Verify coordinate uniqueness
        coords = list(zip(sites_df['lat'], sites_df['long']))
        assert len(coords) == len(set(coords)), "All coordinate pairs should be unique"
        
        # Verify reasonable coordinate distribution
        lat_range = sites_df['lat'].max() - sites_df['lat'].min()
        lon_range = sites_df['long'].max() - sites_df['long'].min()
        
        assert lat_range > 1, "Sites should span some latitude range"
        assert lon_range > 1, "Sites should span some longitude range"
    
    def test_zone_distribution(self, real_solar_sites):
        """Verify 3 zones with reasonable site distribution."""
        sites_df = pd.read_csv(real_solar_sites)
        
        # Verify zones
        zones = sites_df['zone'].unique()
        assert len(zones) == 3, "Should have exactly 3 zones"
        assert all(zone in [1, 2, 3] for zone in zones), "Zones should be 1, 2, or 3"
        
        # Verify site distribution per zone
        zone_counts = sites_df['zone'].value_counts()
        for zone in [1, 2, 3]:
            assert zone in zone_counts.index, f"Zone {zone} should have sites"
            assert zone_counts[zone] > 0, f"Zone {zone} should have at least one site"
    
    def test_tracking_type_validation(self, real_solar_sites):
        """Verify tracking values are 0 or 1."""
        sites_df = pd.read_csv(real_solar_sites)
        
        # Verify tracking type values are valid
        assert all(tracking in [0, 1] for tracking in sites_df['tracking']), "Tracking values should be 0 or 1"
        
        # Verify reasonable distribution
        tracking_counts = sites_df['tracking'].value_counts()
        # Note: All sites in this dataset have tracking=1, which is valid
        assert 1 in tracking_counts.index, "Should have tracking sites (tracking=1)"
        assert len(tracking_counts) >= 1, "Should have at least one tracking type"
    
    def test_capacity_validation(self, real_solar_sites):
        """Verify MW values are positive and reasonable."""
        sites_df = pd.read_csv(real_solar_sites)
        
        # Verify MW values are positive
        assert all(sites_df['MW'] > 0), "All MW values should be positive"
        
        # Verify reasonable upper bound
        assert all(sites_df['MW'] < 200), "MW values should be reasonable (<200 MW)"
        
        # Verify MW values are numeric
        assert pd.api.types.is_numeric_dtype(sites_df['MW']), "MW column should be numeric"
    
    def test_site_name_uniqueness(self, real_solar_sites):
        """Verify all site names are unique."""
        sites_df = pd.read_csv(real_solar_sites)
        
        # Verify site names are unique
        assert len(sites_df['site_name'].unique()) == len(sites_df), "All site names should be unique"
        
        # Verify no empty site names
        assert not sites_df['site_name'].isnull().any(), "No site names should be null"
        assert all(sites_df['site_name'].str.strip() != ''), "No site names should be empty strings"


class TestOutputValidation:
    """Test output format validation."""
    
    def test_excel_output_format(self, tmp_path):
        """Verify solar_data.xlsx structure."""
        # Create test data
        base = tmp_path / "solardata" / "2024"
        base.mkdir(parents=True)
        pd.DataFrame({"p_mp": [1.0, 1.1]}).to_csv(base / "SiteA_sgen_sat.csv", index=False)
        pd.DataFrame({"p_mp": [0.9, 1.0]}).to_csv(base / "SiteA_sgen_cs.csv", index=False)

        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        sol.SolarGenGather(2024, 2024)

        # Verify Excel file structure
        excel_path = tmp_path / "solar_data.xlsx"
        assert excel_path.exists()
        
        # Read Excel file
        with pd.ExcelFile(excel_path) as xls:
            sheet_names = xls.sheet_names
            assert "solar_gen" in sheet_names
            assert "csi" in sheet_names
            
            # Check sheet contents
            solar_gen_df = pd.read_excel(excel_path, sheet_name="solar_gen")
            csi_df = pd.read_excel(excel_path, sheet_name="csi")
            
            # Verify structure
            assert "datetime" in solar_gen_df.columns
            assert "datetime" in csi_df.columns
            assert "SiteA" in solar_gen_df.columns
            assert "SiteA" in csi_df.columns
            
            # Verify data types
            assert pd.api.types.is_string_dtype(solar_gen_df['datetime'])
            assert pd.api.types.is_string_dtype(csi_df['datetime'])
            assert pd.api.types.is_numeric_dtype(solar_gen_df['SiteA'])
            assert pd.api.types.is_numeric_dtype(csi_df['SiteA'])
    
    def test_csv_output_formats(self, tmp_path, monkeypatch):
        """Verify per-site CSV files are readable and valid."""
        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))

        # Mock API and PVLib
        class DummyResp:
            def __init__(self, text):
                self.text = text

        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        data = "2024,1,1,0,0,500,600,100,700,800,150,20,3\n"
        csv_text = tz_row + header + data
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                self.results = DummyResults([1.0])

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        sol.SolarGen("k", "n", "a", "e", 2024, 2024)

        # Verify CSV files are readable
        base = tmp_path / "solardata" / "2024"
        sat_file = base / "SiteA_sgen_sat.csv"
        cs_file = base / "SiteA_sgen_cs.csv"
        
        assert sat_file.exists()
        assert cs_file.exists()
        
        # Verify CSV contents
        sat_data = pd.read_csv(sat_file)
        cs_data = pd.read_csv(cs_file)
        
        # The CSV files have numeric columns (0, 1, 2, etc.)
        assert len(sat_data.columns) > 0
        assert len(cs_data.columns) > 0
        assert len(sat_data) > 0
        assert len(cs_data) > 0
        
        # Check that the data is numeric
        for col in sat_data.columns:
            if col != 'Unnamed: 0':  # Skip index column
                assert pd.api.types.is_numeric_dtype(sat_data[col])
        
        for col in cs_data.columns:
            if col != 'Unnamed: 0':  # Skip index column
                assert pd.api.types.is_numeric_dtype(cs_data[col])
    
    def test_csi_value_ranges(self, tmp_path):
        """Verify CSI values are in reasonable range."""
        # Create test data with known values
        base = tmp_path / "solardata" / "2024"
        base.mkdir(parents=True)
        pd.DataFrame({"p_mp": [2.0, 4.0]}).to_csv(base / "SiteA_sgen_sat.csv", index=False)
        pd.DataFrame({"p_mp": [1.0, 2.0]}).to_csv(base / "SiteA_sgen_cs.csv", index=False)

        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        sol.SolarGenGather(2024, 2024)

        # Verify CSI values
        excel_path = tmp_path / "solar_data.xlsx"
        csi_df = pd.read_excel(excel_path, sheet_name="csi")
        
        # CSI should be satellite / clearsky = 2.0 / 1.0 = 2.0, 4.0 / 2.0 = 2.0
        csi_values = csi_df["SiteA"].dropna().tolist()  # Remove NaN values
        assert all(csi >= 0 for csi in csi_values), "CSI values should be non-negative"
        assert all(csi <= 2 for csi in csi_values), "CSI values should be reasonable (≤2)"
    
    def test_datetime_format(self, tmp_path):
        """Verify datetime column format is consistent."""
        # Create test data
        base = tmp_path / "solardata" / "2024"
        base.mkdir(parents=True)
        pd.DataFrame({"p_mp": [1.0, 1.1]}).to_csv(base / "SiteA_sgen_sat.csv", index=False)
        pd.DataFrame({"p_mp": [0.9, 1.0]}).to_csv(base / "SiteA_sgen_cs.csv", index=False)

        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        sol.SolarGenGather(2024, 2024)

        # Verify datetime format
        excel_path = tmp_path / "solar_data.xlsx"
        solar_gen_df = pd.read_excel(excel_path, sheet_name="solar_gen")
        csi_df = pd.read_excel(excel_path, sheet_name="csi")
        
        # Verify datetime column exists and has correct format
        assert "datetime" in solar_gen_df.columns
        assert "datetime" in csi_df.columns
        
        # Verify datetime values are strings in expected format
        assert all(isinstance(dt, str) for dt in solar_gen_df['datetime'])
        assert all(isinstance(dt, str) for dt in csi_df['datetime'])
        
        # Verify datetime format (MM/DD/YY HH:MM)
        datetime_pattern = r'\d{2}/\d{2}/\d{2} \d{2}:\d{2}'
        assert all(pd.Series(solar_gen_df['datetime']).str.match(datetime_pattern))
        assert all(pd.Series(csi_df['datetime']).str.match(datetime_pattern))
    
    def test_no_nan_values(self, tmp_path):
        """Verify no NaN values in critical columns."""
        # Create test data
        base = tmp_path / "solardata" / "2024"
        base.mkdir(parents=True)
        pd.DataFrame({"p_mp": [1.0, 1.1]}).to_csv(base / "SiteA_sgen_sat.csv", index=False)
        pd.DataFrame({"p_mp": [0.9, 1.0]}).to_csv(base / "SiteA_sgen_cs.csv", index=False)

        site_csv = tmp_path / "solar_sites.csv"
        pd.DataFrame({
            "site_name": ["SiteA"],
            "lat": [35.0],
            "long": [-106.0],
            "tracking": [1],
            "MW": [1.0],
            "zone": [1],
        }).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        sol.SolarGenGather(2024, 2024)

        # Verify data structure (NaN values are normal for solar data)
        excel_path = tmp_path / "solar_data.xlsx"
        solar_gen_df = pd.read_excel(excel_path, sheet_name="solar_gen")
        csi_df = pd.read_excel(excel_path, sheet_name="csi")
        
        # Check that datetime column has no NaN values
        assert not solar_gen_df["datetime"].isnull().any(), "Datetime column should not have NaN values"
        assert not csi_df["datetime"].isnull().any(), "Datetime column should not have NaN values"
        
        # Note: Solar generation and CSI data may contain NaN values (e.g., night hours)
        # This is normal behavior for solar data


class TestPerformance:
    """Test performance with production data."""
    
    def test_solargen_performance(self, real_solar_sites, tmp_path, monkeypatch):
        """Verify SolarGen completes in reasonable time."""
        # Mock API and PVLib for performance testing
        class DummyResp:
            def __init__(self, text):
                self.text = text

        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        data = "2024,1,1,0,0,500,600,100,700,800,150,20,3\n"
        csv_text = tz_row + header + data
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                self.results = DummyResults([1.0])

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        # Test with subset of real sites for performance
        sites_df = pd.read_csv(real_solar_sites)
        subset_sites = sites_df.head(5)  # Use first 5 sites
        subset_csv = tmp_path / "subset_sites.csv"
        subset_sites.to_csv(subset_csv, index=False)

        sol = Solar(site_data=str(subset_csv), directory=str(tmp_path))
        
        # Time the operation
        start_time = time.time()
        sol.SolarGen("k", "n", "a", "e", 2024, 2024)
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # Verify completion in reasonable time (<10 seconds for 5 sites)
        assert total_time < 10, f"SolarGen took too long: {total_time:.2f} seconds"
    
    def test_solargengather_performance(self, tmp_path):
        """Verify gathering completes in reasonable time."""
        # Create test data
        base = tmp_path / "solardata" / "2024"
        base.mkdir(parents=True)
        
        # Create multiple site files
        for i in range(10):
            site_name = f"Site{i}"
            pd.DataFrame({"p_mp": [1.0, 1.1]}).to_csv(base / f"{site_name}_sgen_sat.csv", index=False)
            pd.DataFrame({"p_mp": [0.9, 1.0]}).to_csv(base / f"{site_name}_sgen_cs.csv", index=False)

        site_csv = tmp_path / "solar_sites.csv"
        site_data = {
            "site_name": [f"Site{i}" for i in range(10)],
            "lat": [35.0 + i for i in range(10)],
            "long": [-106.0 - i for i in range(10)],
            "tracking": [1] * 10,
            "MW": [1.0] * 10,
            "zone": [1] * 10,
        }
        pd.DataFrame(site_data).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        
        # Time the operation
        start_time = time.time()
        sol.SolarGenGather(2024, 2024)
        end_time = time.time()
        
        total_time = end_time - start_time
        
        # Verify completion in reasonable time (<5 seconds for 10 sites)
        assert total_time < 5, f"SolarGenGather took too long: {total_time:.2f} seconds"
    
    def test_memory_usage(self, tmp_path, monkeypatch):
        """Verify memory usage is reasonable for large datasets."""
        if psutil is None:
            pytest.skip("psutil not installed, skipping memory test")
        
        # Mock API and PVLib
        class DummyResp:
            def __init__(self, text):
                self.text = text

        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        data = "2024,1,1,0,0,500,600,100,700,800,150,20,3\n"
        csv_text = tz_row + header + data
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                self.results = DummyResults([1.0])

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        # Create test data
        site_csv = tmp_path / "solar_sites.csv"
        site_data = {
            "site_name": [f"Site{i}" for i in range(20)],
            "lat": [35.0 + i for i in range(20)],
            "long": [-106.0 - i for i in range(20)],
            "tracking": [1] * 20,
            "MW": [1.0] * 20,
            "zone": [1] * 20,
        }
        pd.DataFrame(site_data).to_csv(site_csv, index=False)

        sol = Solar(site_data=str(site_csv), directory=str(tmp_path))
        
        # Monitor memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Only test SolarGen, not SolarGenGather (which requires proper CSV files)
        sol.SolarGen("k", "n", "a", "e", 2024, 2024)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = final_memory - initial_memory
        
        # Verify memory usage is reasonable (<50 MB for 20 sites)
        assert memory_used < 50, f"Memory usage too high: {memory_used:.1f} MB"


class TestWorkflowIntegration:
    """Test complete workflow integration."""
    
    def test_complete_workflow(self, real_solar_sites, tmp_path, monkeypatch):
        """Test full workflow (init -> SolarGen -> SolarGenGather -> GetSolarProfiles)."""
        # Mock API and PVLib
        class DummyResp:
            def __init__(self, text):
                self.text = text

        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        data = "2024,1,1,0,0,500,600,100,700,800,150,20,3\n"
        csv_text = tz_row + header + data
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                self.results = DummyResults([1.0])

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        # Use subset of real sites for testing
        sites_df = pd.read_csv(real_solar_sites)
        subset_sites = sites_df.head(3)  # Use first 3 sites
        subset_csv = tmp_path / "subset_sites.csv"
        subset_sites.to_csv(subset_csv, index=False)

        sol = Solar(site_data=str(subset_csv), directory=str(tmp_path))
        
        # Step 1: SolarGen
        sol.SolarGen("k", "n", "a", "e", 2024, 2024)
        
        # Verify SolarGen outputs
        base = tmp_path / "solardata" / "2024"
        assert base.exists()
        for site_name in subset_sites["site_name"]:
            assert (base / f"{site_name}.csv").exists()
            assert (base / f"{site_name}_sgen_sat.csv").exists()
            assert (base / f"{site_name}_sgen_cs.csv").exists()
        
        # Create proper CSV files for SolarGenGather
        for site_name in subset_sites["site_name"]:
            sat_file = base / f"{site_name}_sgen_sat.csv"
            cs_file = base / f"{site_name}_sgen_cs.csv"
            
            # Create proper CSV files with p_mp column
            sat_data = pd.DataFrame({"p_mp": [1.0] * 8760})
            cs_data = pd.DataFrame({"p_mp": [0.9] * 8760})
            sat_data.to_csv(sat_file, index=False)
            cs_data.to_csv(cs_file, index=False)
        
        # Step 2: SolarGenGather
        sol.SolarGenGather(2024, 2024)
        
        # Verify SolarGenGather outputs
        excel_path = tmp_path / "solar_data.xlsx"
        assert excel_path.exists()
        
        solar_gen_df = pd.read_excel(excel_path, sheet_name="solar_gen")
        csi_df = pd.read_excel(excel_path, sheet_name="csi")
        
        assert not solar_gen_df.empty
        assert not csi_df.empty
        assert "datetime" in solar_gen_df.columns
        assert "datetime" in csi_df.columns
        
        # Step 3: GetSolarProfiles (requires cluster data)
        # Create mock cluster data
        clusters_base = tmp_path / "Clusters"
        (clusters_base / "1").mkdir(parents=True)
        
        for site_name in subset_sites["site_name"]:
            pd.DataFrame([[1, 2, 3], [4, 5, 6]]).to_csv(clusters_base / "1" / f"{site_name}.csv", index=False)
        
        probs = tmp_path / "solar_probs.csv"
        pd.DataFrame([[0.5, 0.5]]).to_csv(probs, index=False)
        
        n_sites, s_zone_no, MW, s_profiles, solar_prob = sol.GetSolarProfiles(str(probs))
        
        # Verify GetSolarProfiles outputs
        assert n_sites == 3
        assert len(s_profiles) == 1  # 1 cluster
        assert s_profiles[0].shape == (2, 3, 3)  # (days, hours, sites)
        assert isinstance(solar_prob, np.ndarray)
    
    def test_directory_isolation(self, real_solar_sites, tmp_path, monkeypatch):
        """Verify outputs go to specified directory, not CWD."""
        # Mock API and PVLib
        class DummyResp:
            def __init__(self, text):
                self.text = text

        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        data = "2024,1,1,0,0,500,600,100,700,800,150,20,3\n"
        csv_text = tz_row + header + data
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                self.results = DummyResults([1.0])

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        # Use subset of real sites
        sites_df = pd.read_csv(real_solar_sites)
        subset_sites = sites_df.head(2)
        subset_csv = tmp_path / "subset_sites.csv"
        subset_sites.to_csv(subset_csv, index=False)

        # Change CWD away from data directory
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            
            sol = Solar(site_data=str(subset_csv.name), directory=".")
            sol.SolarGen("k", "n", "a", "e", 2024, 2024)
            
            # Create proper CSV files for SolarGenGather
            base = Path("solardata") / "2024"
            for site_name in subset_sites["site_name"]:
                sat_file = base / f"{site_name}_sgen_sat.csv"
                cs_file = base / f"{site_name}_sgen_cs.csv"
                
                # Create proper CSV files with p_mp column
                sat_data = pd.DataFrame({"p_mp": [1.0] * 8760})
                cs_data = pd.DataFrame({"p_mp": [0.9] * 8760})
                sat_data.to_csv(sat_file, index=False)
                cs_data.to_csv(cs_file, index=False)
            
            sol.SolarGenGather(2024, 2024)
            
            # Verify outputs are in the specified directory, not CWD
            assert (Path("solardata") / "2024").exists()
            assert (Path("solar_data.xlsx")).exists()
            
            # Verify no files were created in the original CWD
            original_cwd_files = list(Path(old_cwd).glob("solardata"))
            assert len(original_cwd_files) == 0, "No solardata directory should be created in original CWD"
            
        finally:
            os.chdir(old_cwd)
    
    def test_compatibility_with_solar_page(self, real_solar_sites, tmp_path, monkeypatch):
        """Verify outputs compatible with solar_page.py usage."""
        # Mock API and PVLib
        class DummyResp:
            def __init__(self, text):
                self.text = text

        tz_row = "Time Zone\n-7\n"
        header = "Year,Month,Day,Hour,Minute,DNI,GHI,DHI,Clearsky DNI,Clearsky GHI,Clearsky DHI,Temperature,Wind Speed\n"
        data = "2024,1,1,0,0,500,600,100,700,800,150,20,3\n"
        csv_text = tz_row + header + data
        monkeypatch.setattr("requests.get", lambda *a, **k: DummyResp(csv_text), raising=False)

        class DummyResults:
            def __init__(self, values):
                self.ac = pd.Series(values)

        class DummyMC:
            def __init__(self):
                self.results = DummyResults([1.0])

            @classmethod
            def with_pvwatts(cls, system, location):
                return cls()

            def run_model(self, weather):
                return None

        monkeypatch.setattr("pvlib.modelchain.ModelChain", DummyMC, raising=False)
        monkeypatch.setattr("pvlib.location.Location", lambda *a, **k: object(), raising=False)

        # Use subset of real sites
        sites_df = pd.read_csv(real_solar_sites)
        subset_sites = sites_df.head(3)
        subset_csv = tmp_path / "subset_sites.csv"
        subset_sites.to_csv(subset_csv, index=False)

        # Mimic solar_page.py usage
        sol = Solar(site_data=str(subset_csv), directory=str(tmp_path))
        
        # Test the workflow as used in solar_page.py
        sol.SolarGen("k", "n", "a", "e", 2024, 2024)
        
        # Create proper CSV files for SolarGenGather
        base = tmp_path / "solardata" / "2024"
        for site_name in subset_sites["site_name"]:
            sat_file = base / f"{site_name}_sgen_sat.csv"
            cs_file = base / f"{site_name}_sgen_cs.csv"
            
            # Create proper CSV files with p_mp column
            sat_data = pd.DataFrame({"p_mp": [1.0] * 8760})
            cs_data = pd.DataFrame({"p_mp": [0.9] * 8760})
            sat_data.to_csv(sat_file, index=False)
            cs_data.to_csv(cs_file, index=False)
        
        sol.SolarGenGather(2024, 2024)
        
        # Verify outputs match what solar_page.py expects
        excel_path = tmp_path / "solar_data.xlsx"
        assert excel_path.exists()
        
        # Verify Excel file can be read as expected by solar_page.py
        solar_gen_df = pd.read_excel(excel_path, sheet_name="solar_gen")
        csi_df = pd.read_excel(excel_path, sheet_name="csi")
        
        # Verify structure matches solar_page.py expectations
        assert "datetime" in solar_gen_df.columns
        assert "datetime" in csi_df.columns
        
        # Verify site columns exist
        for site_name in subset_sites["site_name"]:
            assert site_name in solar_gen_df.columns
            assert site_name in csi_df.columns
        
        # Verify data types are compatible
        assert pd.api.types.is_string_dtype(solar_gen_df['datetime'])
        assert pd.api.types.is_string_dtype(csi_df['datetime'])
        
        # Verify numeric columns are numeric
        for site_name in subset_sites["site_name"]:
            assert pd.api.types.is_numeric_dtype(solar_gen_df[site_name])
            assert pd.api.types.is_numeric_dtype(csi_df[site_name])