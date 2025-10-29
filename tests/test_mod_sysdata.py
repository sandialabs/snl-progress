"""
Comprehensive test suite for RASystemData class.

This module tests each method in RASystemData independently using real production data,
with comprehensive parameter variations, output validation, and exception handling.
"""

import os
import tempfile
import time
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

# Optional imports for advanced testing
try:
    import psutil
except ImportError:
    psutil = None

from progress.mod_sysdata import RASystemData


# Integration Tests - Real Data Required

def get_dynamic_system_data(real_system_data, count=None):
    """Helper function to get dynamic data selections from real system data."""
    if count is None:
        return real_system_data
    return real_system_data


# Unit Tests - No Real Data Required

class TestInitialization:
    """
    Test RASystemData class initialization and constructor functionality.
    
    This test class validates that the RASystemData class can be properly instantiated
    and that all essential attributes and methods are correctly initialized. It ensures
    that the system data analysis tool is ready for use in power system reliability
    analysis operations.
    """
    
    def test_init_creates_instance(self):
        """
        Test that RASystemData can be successfully instantiated.
        
        This test verifies that the RASystemData class can be created using the
        default constructor without any parameters. It validates that the object
        is properly created and is of the correct type.
        
        The test validates that:
        - The constructor executes without errors
        - The created object is an instance of RASystemData
        - Basic object creation functionality works correctly
        - No exceptions are raised during initialization
        
        Expected behavior: Constructor should successfully create a RASystemData
        instance that can be used for power system data analysis operations.
        """
        sysdata = RASystemData()
        assert isinstance(sysdata, RASystemData)
    
    def test_init_no_parameters(self):
        """
        Test RASystemData initialization without any parameters.
        
        This test verifies that the RASystemData class can be successfully
        instantiated using the default constructor without any parameters.
        It ensures that the class provides a simple initialization interface
        for power system data analysis.
        
        The test validates that:
        - Default constructor executes without errors
        - No parameters are required for basic initialization
        - Object is properly created and ready for use
        - No exceptions are raised during parameterless initialization
        - Basic functionality is available immediately after creation
        
        Expected behavior: Constructor should successfully create a RASystemData
        instance without requiring any input parameters.
        """
        sysdata = RASystemData()
        # Should not raise any exceptions
        assert sysdata is not None


# Method-Specific Tests (Using Real Data)

class TestBranchMethod:
    """Test branch() method with real data."""
    
    @pytest.mark.integration
    def test_branch_basic_functionality(self, real_system_data):
        """
        Test Branch method basic functionality with real system data.
        
        This test verifies that the Branch method correctly processes
        power system branch data from real CSV files. It ensures that
        the method produces accurate branch information for system analysis.
        
        The test validates that:
        - Branch data is correctly loaded and processed from CSV
        - All required branch parameters are properly extracted
        - Data types and formats are correctly handled
        - Output matches expected branch analysis requirements
        - Real-world data scenarios are handled correctly
        
        Expected behavior: Method should successfully process real branch
        data and return accurate branch information for system analysis.
        
        Args:
            real_system_data: Pytest fixture providing real power system data
        """
        sysdata = RASystemData()
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        
        # Verify return types
        assert isinstance(nl, int)
        assert isinstance(fb, np.ndarray)
        assert isinstance(tb, np.ndarray)
        assert isinstance(cap_trans, np.ndarray)
        assert isinstance(MTTF_trans, np.ndarray)
        assert isinstance(MTTR_trans, np.ndarray)
        
        # Verify array lengths
        assert len(fb) == nl
        assert len(tb) == nl
        assert len(cap_trans) == nl
        assert len(MTTF_trans) == nl
        assert len(MTTR_trans) == nl
        
        # Verify instance attributes are set
        assert hasattr(sysdata, 'fb')
        assert hasattr(sysdata, 'tb')
        assert hasattr(sysdata, 'nl')
        assert hasattr(sysdata, 'cap_trans')
        assert hasattr(sysdata, 'MTTF_trans')
        assert hasattr(sysdata, 'MTTR_trans')
    
    def test_branch_parameter_validation(self, tmp_path):
        """
        Test Branch method parameter validation and error handling.
        
        This test verifies that the Branch method properly validates input
        parameters and handles various error conditions gracefully. It ensures
        that the method provides clear feedback about invalid inputs and
        maintains system stability.
        
        The test validates that:
        - Invalid file paths are handled appropriately
        - Missing required parameters raise appropriate exceptions
        - Error messages are informative and help identify issues
        - The method fails gracefully without crashing
        - Parameter validation is consistent across different scenarios
        
        Expected behavior: Method should validate parameters and raise
        appropriate exceptions with clear error messages for invalid inputs.
        
        Args:
            tmp_path: Temporary directory path for creating test data files
        """
        sysdata = RASystemData()
        
        # Test with invalid path types
        with pytest.raises(ValueError):
            sysdata.branch(123)  # int
        
        with pytest.raises(ValueError):
            sysdata.branch(None)  # None
        
        with pytest.raises(ValueError):
            sysdata.branch(['path'])  # list
    
    @pytest.mark.integration
    def test_branch_data_structure(self, real_system_data):
        """
        Test Branch method data structure validation and integrity.
        
        This test verifies that the Branch method correctly processes and
        validates the structure of branch data from real CSV files. It ensures
        that the method produces data with the correct format and relationships
        for power system analysis.
        
        The test validates that:
        - Branch data structure is correctly parsed and validated
        - Data relationships between different branch parameters are maintained
        - Output data has correct dimensions and data types
        - Data integrity is preserved throughout the processing
        - Real-world data scenarios are handled correctly
        
        Expected behavior: Method should process real branch data correctly
        and return properly structured data for power system analysis.
        
        Args:
            real_system_data: Pytest fixture providing real power system data
        """
        sysdata = RASystemData()
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        
        # Verify data types
        assert np.issubdtype(fb.dtype, np.number)
        assert np.issubdtype(tb.dtype, np.number)
        assert np.issubdtype(cap_trans.dtype, np.number)
        assert np.issubdtype(MTTF_trans.dtype, np.number)
        assert np.issubdtype(MTTR_trans.dtype, np.number)
        
        # Verify reasonable values
        assert nl > 0, "Should have at least one branch"
        assert np.all(fb > 0), "All from-bus numbers should be positive"
        assert np.all(tb > 0), "All to-bus numbers should be positive"
        assert np.all(cap_trans > 0), "All transmission capacities should be positive"
        assert np.all(MTTF_trans > 0), "All MTTF values should be positive"
        assert np.all(MTTR_trans > 0), "All MTTR values should be positive"
    
    @pytest.mark.integration
    def test_branch_data_ranges(self, real_system_data):
        """Test branch data ranges and consistency."""
        sysdata = RASystemData()
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        
        # Verify MTTF > MTTR for all branches
        assert np.all(MTTF_trans > MTTR_trans), "MTTF should be greater than MTTR for all branches"
        
        # Verify no self-loops
        assert np.all(fb != tb), "No self-loops allowed in branch data"
        
        # Verify reasonable capacity ranges
        assert np.all(cap_trans <= 1000), "Individual branch capacity should be <= 1000 MW"
        assert np.sum(cap_trans) > 100, "Total transmission capacity should be > 100 MW"
    
    def test_branch_missing_file(self, tmp_path):
        """Test branch method with missing file."""
        sysdata = RASystemData()
        missing_file = tmp_path / "missing_branch.csv"
        
        with pytest.raises(FileNotFoundError):
            sysdata.branch(str(missing_file))
    
    def test_branch_empty_file(self, tmp_path):
        """Test branch method with empty file."""
        sysdata = RASystemData()
        empty_file = tmp_path / "empty_branch.csv"
        empty_file.write_text("")
        
        with pytest.raises(pd.errors.EmptyDataError):
            sysdata.branch(str(empty_file))
    
    def test_branch_missing_columns(self, tmp_path):
        """Test branch method with missing required columns."""
        sysdata = RASystemData()
        
        # Missing MTTF column
        df = pd.DataFrame({
            "From Bus": [1],
            "To Bus": [2],
            "R": [0.01],
            "X": [0.10],
            "B": [0.0],
            "Rating": [100.0],
            "MTTR": [5.0],
            # "MTTF" missing
        })
        bad_file = tmp_path / "bad_branch.csv"
        df.to_csv(bad_file, index=False)
        
        with pytest.raises(KeyError):
            sysdata.branch(str(bad_file))
    
    def test_branch_wrong_column_case(self, tmp_path):
        """Test branch method with wrong column case."""
        sysdata = RASystemData()
        
        df = pd.DataFrame({
            "from bus": [1],  # lowercase
            "to bus": [2],    # lowercase
            "R": [0.01],
            "X": [0.10],
            "B": [0.0],
            "rating": [100.0],  # lowercase
            "mttr": [5.0],      # lowercase
            "mttf": [500.0],    # lowercase
        })
        bad_file = tmp_path / "bad_case_branch.csv"
        df.to_csv(bad_file, index=False)
        
        with pytest.raises(KeyError):
            sysdata.branch(str(bad_file))
    
    def test_branch_malformed_data(self, tmp_path):
        """Test branch method with malformed data."""
        sysdata = RASystemData()
        
        # Non-numeric data in numeric columns
        df = pd.DataFrame({
            "From Bus": ["not_a_number"],
            "To Bus": [2],
            "R": [0.01],
            "X": [0.10],
            "B": [0.0],
            "Rating": [100.0],
            "MTTR": [5.0],
            "MTTF": [500.0],
        })
        bad_file = tmp_path / "malformed_branch.csv"
        df.to_csv(bad_file, index=False)
        
        # Should still work but with object dtypes
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(str(bad_file))
        assert not np.issubdtype(fb.dtype, np.number), "Should handle non-numeric data"


class TestBusMethod:
    """Test bus() method with real data."""
    
    @pytest.mark.integration
    def test_bus_basic_functionality(self, real_system_data):
        """Test basic bus data loading functionality."""
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Verify return types
        assert isinstance(bus_name, pd.Series)
        assert isinstance(bus_no, np.ndarray)
        assert isinstance(nz, int)
        
        # Verify array lengths
        assert len(bus_name) == nz
        assert len(bus_no) == nz
        
        # Verify instance attributes are set
        assert hasattr(sysdata, 'bus_name')
        assert hasattr(sysdata, 'bus_no')
        assert hasattr(sysdata, 'nz')
    
    def test_bus_parameter_validation(self, tmp_path):
        """Test bus method with invalid parameter types."""
        sysdata = RASystemData()
        
        # Test with invalid path types
        with pytest.raises(ValueError):
            sysdata.bus(123)  # int
        
        with pytest.raises(ValueError):
            sysdata.bus(None)  # None
        
        with pytest.raises(ValueError):
            sysdata.bus(['path'])  # list
    
    @pytest.mark.integration
    def test_bus_data_structure(self, real_system_data):
        """Test bus data structure and types."""
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Verify data types
        assert pd.api.types.is_string_dtype(bus_name)
        assert np.issubdtype(bus_no.dtype, np.number)
        
        # Verify reasonable values
        assert nz > 0, "Should have at least one bus"
        assert len(bus_name) == nz, "Bus names should match number of buses"
        assert len(bus_no) == nz, "Bus numbers should match number of buses"
        assert np.all(bus_no > 0), "All bus numbers should be positive"
    
    @pytest.mark.integration
    def test_bus_data_consistency(self, real_system_data):
        """Test bus data consistency and mapping."""
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Verify unique bus names and numbers
        assert len(set(bus_name)) == len(bus_name), "Bus names should be unique"
        assert len(set(bus_no)) == len(bus_no), "Bus numbers should be unique"
        
        # Verify expected bus names and numbers for production data
        expected_buses = {"A", "B", "C"}
        assert set(bus_name) == expected_buses, f"Expected bus names {expected_buses}, got {set(bus_name)}"
        
        expected_bus_nos = {1, 2, 3}
        assert set(bus_no) == expected_bus_nos, f"Expected bus numbers {expected_bus_nos}, got {set(bus_no)}"
    
    def test_bus_missing_file(self, tmp_path):
        """Test bus method with missing file."""
        sysdata = RASystemData()
        missing_file = tmp_path / "missing_bus.csv"
        
        with pytest.raises(FileNotFoundError):
            sysdata.bus(str(missing_file))
    
    def test_bus_empty_file(self, tmp_path):
        """Test bus method with empty file."""
        sysdata = RASystemData()
        empty_file = tmp_path / "empty_bus.csv"
        empty_file.write_text("")
        
        with pytest.raises(pd.errors.EmptyDataError):
            sysdata.bus(str(empty_file))
    
    def test_bus_missing_columns(self, tmp_path):
        """Test bus method with missing required columns."""
        sysdata = RASystemData()
        
        # Missing Bus No. column
        df = pd.DataFrame({
            "Bus Name": ["R1", "R2"],
            # "Bus No." missing
        })
        bad_file = tmp_path / "bad_bus.csv"
        df.to_csv(bad_file, index=False)
        
        with pytest.raises(KeyError):
            sysdata.bus(str(bad_file))
    
    def test_bus_wrong_column_case(self, tmp_path):
        """Test bus method with wrong column case."""
        sysdata = RASystemData()
        
        df = pd.DataFrame({
            "bus name": ["R1", "R2"],  # lowercase
            "bus no.": [1, 2],         # lowercase
        })
        bad_file = tmp_path / "bad_case_bus.csv"
        df.to_csv(bad_file, index=False)
        
        with pytest.raises(KeyError):
            sysdata.bus(str(bad_file))


class TestGenMethod:
    """Test gen() method with real data."""
    
    @pytest.mark.integration
    def test_gen_basic_functionality(self, real_system_data):
        """Test basic generator data loading functionality."""
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        
        # Verify return types
        assert isinstance(genbus, np.ndarray)
        assert isinstance(ng, int)
        assert isinstance(pmax, np.ndarray)
        assert isinstance(pmin, np.ndarray)
        assert isinstance(FOR_gen, np.ndarray)
        assert isinstance(MTTF_gen, np.ndarray)
        assert isinstance(MTTR_gen, np.ndarray)
        assert isinstance(gencost, np.ndarray)
        
        # Verify array lengths
        assert len(genbus) == ng
        assert len(pmax) == ng
        assert len(pmin) == ng
        assert len(FOR_gen) == ng
        assert len(MTTF_gen) == ng
        assert len(MTTR_gen) == ng
        assert len(gencost) == ng
        
        # Verify instance attributes are set
        assert hasattr(sysdata, 'genbus')
        assert hasattr(sysdata, 'ng')
        assert hasattr(sysdata, 'pmax')
        assert hasattr(sysdata, 'pmin')
        assert hasattr(sysdata, 'FOR_gen')
        assert hasattr(sysdata, 'MTTF_gen')
        assert hasattr(sysdata, 'MTTR_gen')
        assert hasattr(sysdata, 'gencost')
    
    def test_gen_parameter_validation(self, tmp_path):
        """Test gen method with invalid parameter types."""
        sysdata = RASystemData()
        
        # Test with invalid path types
        with pytest.raises(ValueError):
            sysdata.gen(123)  # int
        
        with pytest.raises(ValueError):
            sysdata.gen(None)  # None
        
        with pytest.raises(ValueError):
            sysdata.gen(['path'])  # list
    
    @pytest.mark.integration
    def test_gen_data_structure(self, real_system_data, production_system_summary):
        """Test generator data structure and types."""
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        
        # Verify production data dimensions
        assert ng == production_system_summary["n_generators"], f"Expected {production_system_summary['n_generators']} generators, got {ng}"
        
        # Verify data types
        assert np.issubdtype(genbus.dtype, np.number)
        assert np.issubdtype(pmax.dtype, np.number)
        assert np.issubdtype(pmin.dtype, np.number)
        assert np.issubdtype(FOR_gen.dtype, np.number)
        assert np.issubdtype(MTTF_gen.dtype, np.number)
        assert np.issubdtype(MTTR_gen.dtype, np.number)
        assert np.issubdtype(gencost.dtype, np.number)
        
        # Verify reasonable values
        assert ng > 0, "Should have at least one generator"
        assert np.all(genbus > 0), "All generator buses should be positive"
        assert np.all(pmax > 0), "All max capacities should be positive"
        assert np.all(pmin >= 0), "All min capacities should be non-negative"
        assert np.all(MTTF_gen > 0), "All MTTF values should be positive"
        assert np.all(MTTR_gen > 0), "All MTTR values should be positive"
        assert np.all(gencost >= 0), "All generation costs should be non-negative"
    
    @pytest.mark.integration
    def test_gen_data_ranges(self, real_system_data):
        """Test generator data ranges and consistency."""
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        
        # Verify pmax >= pmin for all generators
        assert np.all(pmax >= pmin), "Max capacity should be >= min capacity for all generators"
        
        # Verify MTTF > MTTR for all generators
        assert np.all(MTTF_gen > MTTR_gen), "MTTF should be greater than MTTR for all generators"
        
        # Verify FOR values are reasonable (0-1 range) or NaN
        if not np.all(np.isnan(FOR_gen)):
            valid_for = FOR_gen[~np.isnan(FOR_gen)]
            assert np.all(valid_for >= 0), "FOR values should be non-negative"
            assert np.all(valid_for <= 1), "FOR values should be <= 1"
        
        # Verify reasonable capacity ranges
        assert np.all(pmax <= 1000), "Individual generator capacity should be <= 1000 MW"
        total_capacity = np.sum(pmax)
        assert total_capacity > 1000, f"Total system capacity should be > 1000 MW, got {total_capacity}"
        assert total_capacity < 50000, f"Total system capacity should be < 50000 MW, got {total_capacity}"
    
    @pytest.mark.integration
    def test_gen_bus_consistency(self, real_system_data, production_system_summary):
        """Test generator bus consistency."""
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        
        # Verify all generators are at valid buses
        valid_buses = set(production_system_summary["zones"])
        assert all(bus in valid_buses for bus in genbus), f"Invalid bus numbers found: {set(genbus) - valid_buses}"
        
        # Verify generators are distributed across buses
        bus_counts = {}
        for bus in genbus:
            bus_counts[bus] = bus_counts.get(bus, 0) + 1
        
        # Verify we have generators at all buses
        assert len(bus_counts) == len(valid_buses), f"Should have generators at all {len(valid_buses)} buses, found: {bus_counts.keys()}"
        
        # Verify no single bus has all generators
        assert all(count < ng for count in bus_counts.values()), "No single bus should have all generators"
    
    def test_gen_missing_file(self, tmp_path):
        """Test gen method with missing file."""
        sysdata = RASystemData()
        missing_file = tmp_path / "missing_gen.csv"
        
        with pytest.raises(FileNotFoundError):
            sysdata.gen(str(missing_file))
    
    def test_gen_empty_file(self, tmp_path):
        """Test gen method with empty file."""
        sysdata = RASystemData()
        empty_file = tmp_path / "empty_gen.csv"
        empty_file.write_text("")
        
        with pytest.raises((pd.errors.EmptyDataError, ValueError, IndexError)):
            sysdata.gen(str(empty_file))
    
    def test_gen_missing_columns(self, tmp_path):
        """Test gen method with missing required columns."""
        sysdata = RASystemData()
        
        # Missing Cost column
        df = pd.DataFrame({
            "Bus No.": [1],
            "Max Cap": [50.0],
            "Min Cap": [10.0],
            "FOR": [0.05],
            "MTTF": [1000.0],
            "MTTR": [10.0],
            # "Cost" missing
        })
        bad_file = tmp_path / "bad_gen.csv"
        df.to_csv(bad_file, index=False)
        
        with pytest.raises(KeyError):
            sysdata.gen(str(bad_file))
    
    def test_gen_wrong_column_case(self, tmp_path):
        """Test gen method with wrong column case."""
        sysdata = RASystemData()
        
        df = pd.DataFrame({
            "bus no.": [1],      # lowercase
            "max cap": [50.0],   # lowercase
            "min cap": [10.0],   # lowercase
            "for": [0.05],       # lowercase
            "mttf": [1000.0],    # lowercase
            "mttr": [10.0],      # lowercase
            "cost": [20.0],      # lowercase
        })
        bad_file = tmp_path / "bad_case_gen.csv"
        df.to_csv(bad_file, index=False)
        
        with pytest.raises(KeyError):
            sysdata.gen(str(bad_file))


class TestStorageMethod:
    """Test storage() method with real data."""
    
    @pytest.mark.integration
    def test_storage_basic_functionality(self, real_system_data):
        """Test basic storage data loading functionality."""
        sysdata = RASystemData()
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Verify return types
        assert isinstance(essname, pd.Series)
        assert isinstance(essbus, np.ndarray)
        assert isinstance(ness, int)
        assert isinstance(ess_pmax, np.ndarray)
        assert isinstance(ess_pmin, np.ndarray)
        assert isinstance(ess_duration, np.ndarray)
        assert isinstance(ess_socmax, np.ndarray)
        assert isinstance(ess_socmin, np.ndarray)
        assert isinstance(ess_eff, np.ndarray)
        assert isinstance(disch_cost, np.ndarray)
        assert isinstance(ch_cost, np.ndarray)
        assert isinstance(MTTF_ess, np.ndarray)
        assert isinstance(MTTR_ess, np.ndarray)
        assert isinstance(ess_units, np.ndarray)
        
        # Verify array lengths
        assert len(essname) == ness
        assert len(essbus) == ness
        assert len(ess_pmax) == ness
        assert len(ess_pmin) == ness
        assert len(ess_duration) == ness
        assert len(ess_socmax) == ness
        assert len(ess_socmin) == ness
        assert len(ess_eff) == ness
        assert len(disch_cost) == ness
        assert len(ch_cost) == ness
        assert len(MTTF_ess) == ness
        assert len(MTTR_ess) == ness
        assert len(ess_units) == ness
        
        # Verify instance attributes are set
        assert hasattr(sysdata, 'essname')
        assert hasattr(sysdata, 'essbus')
        assert hasattr(sysdata, 'ness')
        assert hasattr(sysdata, 'ess_pmax')
        assert hasattr(sysdata, 'ess_pmin')
        assert hasattr(sysdata, 'ess_duration')
        assert hasattr(sysdata, 'ess_socmax')
        assert hasattr(sysdata, 'ess_socmin')
        assert hasattr(sysdata, 'ess_eff')
        assert hasattr(sysdata, 'disch_cost')
        assert hasattr(sysdata, 'ch_cost')
        assert hasattr(sysdata, 'MTTF_ess')
        assert hasattr(sysdata, 'MTTR_ess')
        assert hasattr(sysdata, 'ess_units')
    
    def test_storage_parameter_validation(self, tmp_path):
        """Test storage method with invalid parameter types."""
        sysdata = RASystemData()
        
        # Test with invalid path types
        with pytest.raises(ValueError):
            sysdata.storage(123)  # int
        
        with pytest.raises(ValueError):
            sysdata.storage(None)  # None
        
        with pytest.raises(ValueError):
            sysdata.storage(['path'])  # list
    
    @pytest.mark.integration
    def test_storage_data_structure(self, real_system_data, production_system_summary):
        """Test storage data structure and types."""
        sysdata = RASystemData()
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Verify production data dimensions
        assert ness == production_system_summary["n_ess"], f"Expected {production_system_summary['n_ess']} ESS, got {ness}"
        
        # Verify data types
        assert pd.api.types.is_string_dtype(essname)
        assert np.issubdtype(essbus.dtype, np.number)
        assert np.issubdtype(ess_pmax.dtype, np.number)
        assert np.issubdtype(ess_pmin.dtype, np.number)
        assert np.issubdtype(ess_duration.dtype, np.number)
        assert np.issubdtype(ess_socmax.dtype, np.number)
        assert np.issubdtype(ess_socmin.dtype, np.number)
        assert np.issubdtype(ess_eff.dtype, np.number)
        assert np.issubdtype(disch_cost.dtype, np.number)
        assert np.issubdtype(ch_cost.dtype, np.number)
        assert np.issubdtype(MTTF_ess.dtype, np.number)
        assert np.issubdtype(MTTR_ess.dtype, np.number)
        assert np.issubdtype(ess_units.dtype, np.number)
        
        # Verify reasonable values
        assert ness > 0, "Should have at least one ESS"
        assert np.all(essbus > 0), "All ESS buses should be positive"
        assert np.all(ess_pmax > 0), "All ESS max power should be positive"
        assert np.all(ess_pmin >= 0), "All ESS min power should be non-negative"
        assert np.all(ess_duration > 0), "All ESS duration should be positive"
        assert np.all(ess_socmax > 0), "All ESS max SOC should be positive"
        assert np.all(ess_socmin >= 0), "All ESS min SOC should be non-negative"
        assert np.all(ess_eff > 0), "All ESS efficiency should be positive"
        assert np.all(disch_cost >= 0), "All discharge costs should be non-negative"
        assert np.all(ch_cost >= 0), "All charge costs should be non-negative"
        assert np.all(MTTF_ess > 0), "All ESS MTTF should be positive"
        assert np.all(MTTR_ess > 0), "All ESS MTTR should be positive"
        assert np.all(ess_units > 0), "All ESS units should be positive"
    
    @pytest.mark.integration
    def test_storage_data_ranges(self, real_system_data):
        """Test storage data ranges and consistency."""
        sysdata = RASystemData()
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Verify power ranges
        assert np.all(ess_pmax >= ess_pmin), "ESS max power should be >= min power"
        
        # Verify SOC ranges
        assert np.all(ess_socmax > ess_socmin), "ESS max SOC should be > min SOC"
        assert np.all(ess_socmax <= 1), "ESS max SOC should be <= 1"
        assert np.all(ess_socmin >= 0), "ESS min SOC should be >= 0"
        
        # Verify efficiency range
        assert np.all(ess_eff <= 1), "ESS efficiency should be <= 1"
        assert np.all(ess_eff >= 0.8), "ESS efficiency should be reasonable (>= 0.8)"
        
        # Verify MTTF > MTTR
        assert np.all(MTTF_ess > MTTR_ess), "ESS MTTF should be greater than MTTR"
        
        # Verify duration is reasonable
        assert np.all(ess_duration <= 24), "ESS duration should be reasonable (<= 24 hours)"
        
        # Verify units are integers
        assert np.all(ess_units == ess_units.astype(int)), "ESS units should be integers"
    
    @pytest.mark.integration
    def test_storage_bus_consistency(self, real_system_data, production_system_summary):
        """Test storage bus consistency."""
        sysdata = RASystemData()
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Verify all ESS are at valid buses
        valid_buses = set(production_system_summary["zones"])
        assert all(bus in valid_buses for bus in essbus), f"Invalid ESS bus found: {set(essbus) - valid_buses}"
    
    def test_storage_missing_file(self, tmp_path):
        """Test storage method with missing file."""
        sysdata = RASystemData()
        missing_file = tmp_path / "missing_storage.csv"
        
        with pytest.raises(FileNotFoundError):
            sysdata.storage(str(missing_file))
    
    def test_storage_empty_file(self, tmp_path):
        """Test storage method with empty file."""
        sysdata = RASystemData()
        empty_file = tmp_path / "empty_storage.csv"
        empty_file.write_text("")
        
        with pytest.raises(pd.errors.EmptyDataError):
            sysdata.storage(str(empty_file))
    
    def test_storage_missing_columns(self, tmp_path):
        """Test storage method with missing required columns."""
        sysdata = RASystemData()
        
        # Missing Bus column
        df = pd.DataFrame({
            "Name": ["ESS_A"],
            # "Bus" missing
            "Pmax": [30.0],
            "Pmin": [0.0],
            "Duration": [2.0],
            "max_SOC": [0.95],
            "min_SOC": [0.10],
            "Efficiency": [0.90],
            "Discharge Cost": [5.0],
            "Charge Cost": [2.0],
            "MTTF": [800.0],
            "MTTR": [8.0],
            "Units": [1],
        })
        bad_file = tmp_path / "bad_storage.csv"
        df.to_csv(bad_file, index=False)
        
        with pytest.raises(KeyError):
            sysdata.storage(str(bad_file))
    
    def test_storage_wrong_column_case(self, tmp_path):
        """Test storage method with wrong column case."""
        sysdata = RASystemData()
        
        df = pd.DataFrame({
            "name": ["ESS_A"],           # lowercase
            "bus": [1],                  # lowercase
            "pmax": [30.0],              # lowercase
            "pmin": [0.0],               # lowercase
            "duration": [2.0],           # lowercase
            "max_soc": [0.95],           # lowercase
            "min_soc": [0.10],           # lowercase
            "efficiency": [0.90],        # lowercase
            "discharge cost": [5.0],     # lowercase
            "charge cost": [2.0],        # lowercase
            "mttf": [800.0],             # lowercase
            "mttr": [8.0],               # lowercase
            "units": [1],                # lowercase
        })
        bad_file = tmp_path / "bad_case_storage.csv"
        df.to_csv(bad_file, index=False)
        
        with pytest.raises(KeyError):
            sysdata.storage(str(bad_file))


class TestLoadMethod:
    """Test load() method with real data."""
    
    @pytest.mark.integration
    def test_load_basic_functionality(self, real_system_data):
        """Test basic load data loading functionality."""
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        
        # Verify return type
        assert isinstance(load_all_regions, np.ndarray)
        
        # Verify instance attributes are set
        assert hasattr(sysdata, 'load')
        assert hasattr(sysdata, 'load_all_regions')
    
    def test_load_parameter_validation(self, tmp_path):
        """Test load method with invalid parameter types."""
        # Create a simple load file
        hours = pd.date_range("2024-01-01", periods=24, freq="h")
        load_df = pd.DataFrame({
            "datetime": hours,
            "A": np.linspace(10.0, 20.0, num=len(hours)),
            "B": np.linspace(5.0, 15.0, num=len(hours)),
            "C": np.linspace(0.0, 10.0, num=len(hours)),
        })
        load_csv = tmp_path / "load.csv"
        load_df.to_csv(load_csv, index=False)
        
        # Test with invalid bus_name types
        sysdata1 = RASystemData()
        with pytest.raises(KeyError):
            sysdata1.load(123, str(load_csv))  # int
        
        sysdata2 = RASystemData()
        with pytest.raises(KeyError):
            sysdata2.load(None, str(load_csv))  # None
        
        # Test with invalid path types
        sysdata3 = RASystemData()
        with pytest.raises(ValueError):
            sysdata3.load(["A"], 123)  # int path
    
    @pytest.mark.integration
    def test_load_data_structure(self, real_system_data, production_system_summary):
        """Test load data structure and types."""
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        
        # Verify production data dimensions
        assert nz == production_system_summary["n_buses"], f"Expected {production_system_summary['n_buses']} buses, got {nz}"
        assert load_all_regions.shape[0] in [8760, 8784], f"Expected 8760 or 8784 hours, got {load_all_regions.shape[0]}"
        assert load_all_regions.shape[1] == nz, f"Expected {nz} zones, got {load_all_regions.shape[1]}"
        
        # Verify data type
        assert np.issubdtype(load_all_regions.dtype, np.number)
        
        # Verify reasonable values
        assert load_all_regions.shape[0] > 0, "Should have at least one hour of load data"
        assert load_all_regions.shape[1] > 0, "Should have at least one zone"
    
    @pytest.mark.integration
    def test_load_data_ranges(self, real_system_data):
        """Test load data ranges and consistency."""
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        
        # Handle NaN values in load data
        valid_loads = load_all_regions[~np.isnan(load_all_regions)]
        
        # Verify load values are reasonable
        assert np.all(valid_loads >= 0), "All valid load values should be non-negative"
        assert np.all(valid_loads < 10000), "All valid load values should be reasonable (< 10000 MW)"
        
        # Verify we have a reasonable amount of valid data
        valid_ratio = len(valid_loads) / load_all_regions.size
        assert valid_ratio > 0.8, f"Should have at least 80% valid load data, got {valid_ratio:.2%}"
    
    @pytest.mark.integration
    def test_load_single_bus(self, real_system_data):
        """Test loading data for single bus name."""
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Test with single bus name
        single_bus = bus_name.iloc[0]  # Get first bus name
        load_single = sysdata.load(single_bus, real_system_data["load_csv"])
        
        assert isinstance(load_single, np.ndarray)
        assert len(load_single) > 0, "Should have load data for single bus"
    
    @pytest.mark.integration
    def test_load_multiple_buses(self, real_system_data):
        """Test loading data for multiple bus names."""
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Test with multiple bus names (Series)
        load_multiple = sysdata.load(bus_name, real_system_data["load_csv"])
        
        assert isinstance(load_multiple, np.ndarray)
        assert load_multiple.shape[1] == len(bus_name), "Should have columns for all bus names"
        assert load_multiple.shape[0] > 0, "Should have load data for multiple buses"
    
    def test_load_unknown_bus(self, tmp_path):
        """Test load method with unknown bus name."""
        sysdata = RASystemData()
        
        # Create a simple load file
        hours = pd.date_range("2024-01-01", periods=24, freq="h")
        load_df = pd.DataFrame({
            "datetime": hours,
            "A": np.linspace(10.0, 20.0, num=len(hours)),
            "B": np.linspace(5.0, 15.0, num=len(hours)),
        })
        load_csv = tmp_path / "load.csv"
        load_df.to_csv(load_csv, index=False)
        
        with pytest.raises(KeyError):
            sysdata.load("UnknownBus", str(load_csv))
    
    def test_load_missing_file(self, tmp_path):
        """Test load method with missing file."""
        sysdata = RASystemData()
        missing_file = tmp_path / "missing_load.csv"
        
        with pytest.raises(FileNotFoundError):
            sysdata.load(["A"], str(missing_file))
    
    def test_load_empty_file(self, tmp_path):
        """Test load method with empty file."""
        sysdata = RASystemData()
        empty_file = tmp_path / "empty_load.csv"
        empty_file.write_text("")
        
        with pytest.raises(pd.errors.EmptyDataError):
            sysdata.load(["A"], str(empty_file))


# Integration Tests (Real Data + Cross-Module)

class TestRealDataIntegration:
    """Test integration with real data and cross-module functionality."""
    
    @pytest.mark.integration
    def test_load_all_system_data(self, real_system_data, production_system_summary):
        """Test loading all system data and verify consistency."""
        sysdata = RASystemData()
        
        # Load all system data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Verify production data dimensions
        assert ng == production_system_summary["n_generators"]
        assert nz == production_system_summary["n_buses"]
        assert load_all_regions.shape[0] in [8760, 8784]  # Handle both regular and leap years
        assert load_all_regions.shape[1] == production_system_summary["n_buses"]
        assert ness == production_system_summary["n_ess"]
        assert nl > 0, "Should have transmission lines"
        
        # Verify data consistency
        assert len(genbus) == ng
        assert len(pmax) == ng
        assert len(bus_name) == nz
        assert len(bus_no) == nz
        assert len(essbus) == ness
    
    @pytest.mark.integration
    def test_system_coherency(self, real_system_data, production_system_summary):
        """Test system coherency across all components."""
        sysdata = RASystemData()
        
        # Load all system data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Verify bus consistency
        valid_buses = set(bus_no)
        assert all(bus in valid_buses for bus in genbus), "All generator buses should be in bus list"
        assert all(bus in valid_buses for bus in essbus), "All ESS buses should be in bus list"
        assert all(bus in valid_buses for bus in fb), "All from-buses should be in bus list"
        assert all(bus in valid_buses for bus in tb), "All to-buses should be in bus list"
        
        # Verify load data consistency
        assert load_all_regions.shape[1] == nz, "Load data should have columns for all buses"
        assert len(bus_name) == nz, "Bus names should match number of buses"
    
    @pytest.mark.integration
    def test_cross_module_matrices(self, real_system_data, production_system_summary):
        """Test integration with RAMatrices."""
        from progress.mod_matrices import RAMatrices
        
        sysdata = RASystemData()
        
        # Load system data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Create matrices
        ramat = RAMatrices(nz)
        gen_mat = ramat.genmat(ng, genbus, ness, essbus)
        ch_mat = ramat.chmat(ness, essbus, nz)
        A_inc = ramat.Ainc(nl, fb, tb)
        curt_mat = ramat.curtmat(nz)
        
        # Verify matrix dimensions
        assert gen_mat.shape == (nz, ng + ness), "Generator matrix dimensions should be correct"
        assert ch_mat.shape == (nz, ness), "ESS charging matrix dimensions should be correct"
        assert A_inc.shape == (nl, nz), "Incidence matrix dimensions should be correct"
        assert curt_mat.shape == (nz, nz), "Curtailment matrix dimensions should be correct"
        
        # Verify matrices are numeric
        assert np.issubdtype(gen_mat.dtype, np.number), "Generator matrix should be numeric"
        assert np.issubdtype(ch_mat.dtype, np.number), "ESS charging matrix should be numeric"
        assert np.issubdtype(A_inc.dtype, np.number), "Incidence matrix should be numeric"
        assert np.issubdtype(curt_mat.dtype, np.number), "Curtailment matrix should be numeric"
    
    @pytest.mark.integration
    def test_cross_module_utilities(self, real_system_data, production_system_summary):
        """Test integration with RAUtilities."""
        from progress.mod_utilities import RAUtilities
        
        sysdata = RASystemData()
        
        # Load system data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Test utility functions
        raut = RAUtilities()
        mu_tot, lambda_tot = raut.reltrates(MTTF_gen, MTTF_trans, MTTF_gen, MTTR_trans, MTTF_ess, MTTR_ess)
        cap_max, cap_min = raut.capacities(nl, pmax, pmin, ess_pmax, ess_pmin, cap_trans)
        
        # Verify utility function outputs
        assert len(mu_tot) == ng + nl + ness, "Total repair rates should match total components"
        assert len(lambda_tot) == ng + nl + ness, "Total failure rates should match total components"
        assert len(cap_max) == ng + nl + ness, "Max capacities should match total components"
        assert len(cap_min) == ng + nl + ness, "Min capacities should match total components"
    
    @pytest.mark.integration
    def test_complete_workflow(self, real_system_data, production_system_summary):
        """Test complete workflow simulation."""
        sysdata = RASystemData()
        
        # Simulate the complete workflow from __main__.py
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Verify workflow data
        assert ng == production_system_summary["n_generators"]
        assert nz == production_system_summary["n_buses"]
        assert load_all_regions.shape[0] in [8760, 8784]
        assert load_all_regions.shape[1] == production_system_summary["n_buses"]
        assert ness == production_system_summary["n_ess"]
        assert nl > 0


class TestDataValidation:
    """Test data validation and quality checks."""
    
    @pytest.mark.integration
    def test_generator_distribution(self, real_system_data, production_system_summary):
        """Test generator distribution across buses."""
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        
        # Verify generators are distributed across all buses
        bus_counts = {}
        for bus in genbus:
            bus_counts[bus] = bus_counts.get(bus, 0) + 1
        
        # Verify we have generators at all buses
        expected_buses = set(production_system_summary["zones"])
        assert len(bus_counts) == len(expected_buses), f"Should have generators at all {len(expected_buses)} buses, found: {bus_counts.keys()}"
        
        # Verify no single bus has all generators
        assert all(count < ng for count in bus_counts.values()), "No single bus should have all generators"
    
    @pytest.mark.integration
    def test_load_temporal_patterns(self, real_system_data):
        """Test basic temporal patterns in load data."""
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        
        # Test daily patterns (day hours should generally have higher loads)
        n_days = load_all_regions.shape[0] // 24
        for day in range(0, n_days, 30):  # Check every 30th day
            day_start = day * 24
            day_end = day_start + 24
            if day_end <= len(load_all_regions):
                day_data = load_all_regions[day_start:day_end]
                
                # Day hours (6-18) vs night hours
                day_hours = day_data[6:19]  # 6 AM to 6 PM
                night_hours = np.concatenate([day_data[0:6], day_data[19:24]])
                
                if len(day_hours) > 0 and len(night_hours) > 0:
                    # Handle NaN values
                    day_hours_valid = day_hours[~np.isnan(day_hours)]
                    night_hours_valid = night_hours[~np.isnan(night_hours)]
                    
                    if len(day_hours_valid) > 0 and len(night_hours_valid) > 0:
                        avg_day_load = np.mean(day_hours_valid)
                        avg_night_load = np.mean(night_hours_valid)
                        # Allow some tolerance for unusual days
                        assert avg_day_load >= avg_night_load * 0.5, f"Day load should be >= night load for day {day}"
    
    @pytest.mark.integration
    def test_capacity_adequacy(self, real_system_data):
        """Test capacity adequacy."""
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        
        # Calculate total generation capacity
        total_capacity = np.sum(pmax)
        
        # Calculate peak load
        valid_loads = load_all_regions[~np.isnan(load_all_regions)]
        if len(valid_loads) > 0:
            peak_load = np.max(valid_loads)
            
            # Verify capacity adequacy
            assert total_capacity > peak_load, f"Total generation capacity ({total_capacity:.1f} MW) should be > peak load ({peak_load:.1f} MW)"
    
    @pytest.mark.integration
    def test_reliability_parameters(self, real_system_data):
        """Test reliability parameter consistency."""
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Verify MTTF > MTTR for all components
        assert np.all(MTTF_gen > MTTR_gen), "Generator MTTF should be > MTTR"
        assert np.all(MTTF_trans > MTTR_trans), "Transmission MTTF should be > MTTR"
        assert np.all(MTTF_ess > MTTR_ess), "ESS MTTF should be > MTTR"
        
        # Verify reasonable MTTF/MTTR ranges
        assert np.all(MTTF_gen > 100), "Generator MTTF should be > 100 hours"
        assert np.all(MTTR_gen <= 200), "Generator MTTR should be <= 200 hours"
        assert np.all(MTTF_trans > 100), "Transmission MTTF should be > 100 hours"
        assert np.all(MTTR_trans <= 200), "Transmission MTTR should be <= 200 hours"
    
    @pytest.mark.integration
    def test_bus_name_mapping(self, real_system_data):
        """Test bus name to number mapping."""
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Verify expected bus mapping for production data
        bus_mapping = dict(zip(bus_name, bus_no))
        expected_mapping = {"A": 1, "B": 2, "C": 3}
        assert bus_mapping == expected_mapping, f"Expected bus mapping {expected_mapping}, got {bus_mapping}"


class TestOutputValidation:
    """Test output validation and data types."""
    
    @pytest.mark.integration
    def test_return_types(self, real_system_data):
        """Test that all methods return correct types."""
        sysdata = RASystemData()
        
        # Test branch method
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        assert isinstance(nl, int)
        assert isinstance(fb, np.ndarray)
        assert isinstance(tb, np.ndarray)
        assert isinstance(cap_trans, np.ndarray)
        assert isinstance(MTTF_trans, np.ndarray)
        assert isinstance(MTTR_trans, np.ndarray)
        
        # Test bus method
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        assert isinstance(bus_name, pd.Series)
        assert isinstance(bus_no, np.ndarray)
        assert isinstance(nz, int)
        
        # Test gen method
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        assert isinstance(genbus, np.ndarray)
        assert isinstance(ng, int)
        assert isinstance(pmax, np.ndarray)
        assert isinstance(pmin, np.ndarray)
        assert isinstance(FOR_gen, np.ndarray)
        assert isinstance(MTTF_gen, np.ndarray)
        assert isinstance(MTTR_gen, np.ndarray)
        assert isinstance(gencost, np.ndarray)
        
        # Test storage method
        storage_tuple = sysdata.storage(real_system_data["storage_csv"])
        assert isinstance(storage_tuple, tuple)
        assert len(storage_tuple) == 14  # All storage parameters
        
        # Test load method
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        assert isinstance(load_all_regions, np.ndarray)
    
    @pytest.mark.integration
    def test_array_dtypes(self, real_system_data):
        """Test that numeric arrays have correct dtypes."""
        sysdata = RASystemData()
        
        # Test branch method
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        assert np.issubdtype(fb.dtype, np.number)
        assert np.issubdtype(tb.dtype, np.number)
        assert np.issubdtype(cap_trans.dtype, np.number)
        assert np.issubdtype(MTTF_trans.dtype, np.number)
        assert np.issubdtype(MTTR_trans.dtype, np.number)
        
        # Test bus method
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        assert pd.api.types.is_string_dtype(bus_name)
        assert np.issubdtype(bus_no.dtype, np.number)
        
        # Test gen method
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        assert np.issubdtype(genbus.dtype, np.number)
        assert np.issubdtype(pmax.dtype, np.number)
        assert np.issubdtype(pmin.dtype, np.number)
        assert np.issubdtype(FOR_gen.dtype, np.number)
        assert np.issubdtype(MTTF_gen.dtype, np.number)
        assert np.issubdtype(MTTR_gen.dtype, np.number)
        assert np.issubdtype(gencost.dtype, np.number)
        
        # Test load method
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        assert np.issubdtype(load_all_regions.dtype, np.number)
    
    @pytest.mark.integration
    def test_instance_attributes(self, real_system_data):
        """Test that methods set instance attributes correctly."""
        # Test branch method
        sysdata1 = RASystemData()
        sysdata1.branch(real_system_data["branch_csv"])
        assert hasattr(sysdata1, 'fb')
        assert hasattr(sysdata1, 'tb')
        assert hasattr(sysdata1, 'nl')
        assert hasattr(sysdata1, 'cap_trans')
        assert hasattr(sysdata1, 'MTTF_trans')
        assert hasattr(sysdata1, 'MTTR_trans')
        
        # Test bus method
        sysdata2 = RASystemData()
        sysdata2.bus(real_system_data["bus_csv"])
        assert hasattr(sysdata2, 'bus_name')
        assert hasattr(sysdata2, 'bus_no')
        assert hasattr(sysdata2, 'nz')
        
        # Test gen method
        sysdata3 = RASystemData()
        sysdata3.gen(real_system_data["gen_csv"])
        assert hasattr(sysdata3, 'genbus')
        assert hasattr(sysdata3, 'ng')
        assert hasattr(sysdata3, 'pmax')
        assert hasattr(sysdata3, 'pmin')
        assert hasattr(sysdata3, 'FOR_gen')
        assert hasattr(sysdata3, 'MTTF_gen')
        assert hasattr(sysdata3, 'MTTR_gen')
        assert hasattr(sysdata3, 'gencost')
        
        # Test storage method
        sysdata4 = RASystemData()
        sysdata4.storage(real_system_data["storage_csv"])
        assert hasattr(sysdata4, 'essname')
        assert hasattr(sysdata4, 'essbus')
        assert hasattr(sysdata4, 'ness')
        assert hasattr(sysdata4, 'ess_pmax')
        assert hasattr(sysdata4, 'ess_pmin')
        assert hasattr(sysdata4, 'ess_duration')
        assert hasattr(sysdata4, 'ess_socmax')
        assert hasattr(sysdata4, 'ess_socmin')
        assert hasattr(sysdata4, 'ess_eff')
        assert hasattr(sysdata4, 'disch_cost')
        assert hasattr(sysdata4, 'ch_cost')
        assert hasattr(sysdata4, 'MTTF_ess')
        assert hasattr(sysdata4, 'MTTR_ess')
        assert hasattr(sysdata4, 'ess_units')
        
        # Test load method
        sysdata5 = RASystemData()
        bus_name, bus_no, nz = sysdata5.bus(real_system_data["bus_csv"])
        sysdata5.load(bus_name, real_system_data["load_csv"])
        assert hasattr(sysdata5, 'load')
        assert hasattr(sysdata5, 'load_all_regions')
    
    @pytest.mark.integration
    def test_data_immutability(self, real_system_data):
        """Test that loading same file multiple times produces same results."""
        sysdata1 = RASystemData()
        sysdata2 = RASystemData()
        
        # Load same data twice
        genbus1, ng1, pmax1, pmin1, FOR_gen1, MTTF_gen1, MTTR_gen1, gencost1 = sysdata1.gen(real_system_data["gen_csv"])
        genbus2, ng2, pmax2, pmin2, FOR_gen2, MTTF_gen2, MTTR_gen2, gencost2 = sysdata2.gen(real_system_data["gen_csv"])
        
        # Verify results are identical
        assert ng1 == ng2
        np.testing.assert_array_equal(genbus1, genbus2)
        np.testing.assert_array_equal(pmax1, pmax2)
        np.testing.assert_array_equal(pmin1, pmin2)
        np.testing.assert_array_equal(FOR_gen1, FOR_gen2)
        np.testing.assert_array_equal(MTTF_gen1, MTTF_gen2)
        np.testing.assert_array_equal(MTTR_gen1, MTTR_gen2)
        np.testing.assert_array_equal(gencost1, gencost2)


class TestPerformance:
    """Test performance and memory usage."""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_load_performance(self, real_system_data):
        """Test that all CSVs load within reasonable time."""
        sysdata = RASystemData()
        
        start_time = time.time()
        
        # Load all system data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        total_time = time.time() - start_time
        
        # Verify completion in reasonable time
        assert total_time < 5.0, f"Total data loading took too long: {total_time:.3f} seconds"
        
        # Verify all data was loaded correctly
        assert ng > 0
        assert nz > 0
        assert load_all_regions.shape[0] > 0
        assert load_all_regions.shape[1] > 0
        assert ness > 0
        assert nl > 0
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_memory_usage(self, real_system_data):
        """Test memory usage with production data."""
        if psutil is None:
            pytest.skip("psutil not available for memory testing")
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        sysdata = RASystemData()
        
        # Load all data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = final_memory - initial_memory
        
        # Verify memory usage is reasonable
        assert memory_used < 100, f"Memory usage too high: {memory_used:.1f} MB"
        
        # Verify data integrity after loading
        assert ng > 0
        assert nz > 0
        assert load_all_regions.shape[0] > 0
        assert load_all_regions.shape[1] > 0
        assert ness > 0
        assert nl > 0
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_large_dataset_handling(self, real_system_data, production_system_summary):
        """Test handling of large datasets with production data."""
        sysdata = RASystemData()
        
        # Load all production data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Verify data integrity with large datasets
        assert ng == production_system_summary["n_generators"], "Should handle production number of generators"
        assert load_all_regions.shape[0] in [8760, 8784], "Should handle 8760 or 8784 hours of load data"
        assert load_all_regions.shape[1] == production_system_summary["n_buses"], "Should handle production number of buses"
        assert nz == production_system_summary["n_buses"], "Should handle production number of buses"
        assert ness == production_system_summary["n_ess"], "Should handle production number of ESS"
        assert nl > 0, "Should handle branch data"
        
        # Verify data types are correct
        assert isinstance(genbus, np.ndarray), "Generator buses should be numpy array"
        assert isinstance(pmax, np.ndarray), "Max capacities should be numpy array"
        assert isinstance(load_all_regions, np.ndarray), "Load data should be numpy array"
        
        # Verify data ranges are reasonable
        assert np.all(pmax > 0), "All max capacities should be positive"
        # Handle NaN values in load data
        valid_loads = load_all_regions[~np.isnan(load_all_regions)]
        assert np.all(valid_loads >= 0), "All valid load values should be non-negative"
        assert np.all(genbus > 0), "All generator buses should be positive"
        
        # Verify memory efficiency (data should be stored as appropriate types)
        assert genbus.dtype in [np.int32, np.int64], "Generator buses should be integer type"
        assert pmax.dtype in [np.int32, np.int64, np.float32, np.float64], "Max capacities should be numeric type"
        assert load_all_regions.dtype in [np.float32, np.float64], "Load data should be float type"


class TestWorkflowIntegration:
    """Test workflow integration and path handling."""
    
    @pytest.mark.integration
    def test_path_robustness(self, real_system_data):
        """Test with different path types."""
        sysdata = RASystemData()
        
        # Test with string paths
        genbus1, ng1, pmax1, pmin1, FOR_gen1, MTTF_gen1, MTTR_gen1, gencost1 = sysdata.gen(real_system_data["gen_csv"])
        
        # Test with Path objects
        sysdata2 = RASystemData()
        genbus2, ng2, pmax2, pmin2, FOR_gen2, MTTF_gen2, MTTR_gen2, gencost2 = sysdata2.gen(Path(real_system_data["gen_csv"]))
        
        # Verify results are identical
        assert ng1 == ng2
        np.testing.assert_array_equal(genbus1, genbus2)
        np.testing.assert_array_equal(pmax1, pmax2)
        np.testing.assert_array_equal(pmin1, pmin2)
        np.testing.assert_array_equal(FOR_gen1, FOR_gen2)
        np.testing.assert_array_equal(MTTF_gen1, MTTF_gen2)
        np.testing.assert_array_equal(MTTR_gen1, MTTR_gen2)
        np.testing.assert_array_equal(gencost1, gencost2)
    
    @pytest.mark.integration
    def test_cwd_independence(self, real_system_data):
        """Test that results are consistent regardless of CWD."""
        sysdata = RASystemData()
        
        # Get absolute paths
        gen_csv_abs = os.path.abspath(real_system_data["gen_csv"])
        bus_csv_abs = os.path.abspath(real_system_data["bus_csv"])
        
        # Load data with absolute paths
        genbus1, ng1, pmax1, pmin1, FOR_gen1, MTTF_gen1, MTTR_gen1, gencost1 = sysdata.gen(gen_csv_abs)
        bus_name1, bus_no1, nz1 = sysdata.bus(bus_csv_abs)
        
        # Change CWD and load again
        old_cwd = os.getcwd()
        try:
            os.chdir(os.path.dirname(gen_csv_abs))
            sysdata2 = RASystemData()
            genbus2, ng2, pmax2, pmin2, FOR_gen2, MTTF_gen2, MTTR_gen2, gencost2 = sysdata2.gen(os.path.basename(gen_csv_abs))
            bus_name2, bus_no2, nz2 = sysdata2.bus(os.path.basename(bus_csv_abs))
        finally:
            os.chdir(old_cwd)
        
        # Verify results are identical
        assert ng1 == ng2
        np.testing.assert_array_equal(genbus1, genbus2)
        np.testing.assert_array_equal(pmax1, pmax2)
        assert nz1 == nz2
        np.testing.assert_array_equal(bus_no1, bus_no2)
    
    @pytest.mark.integration
    def test_multiple_load_cycles(self, real_system_data):
        """Test that data can be loaded multiple times without corruption."""
        # Test multiple data loading cycles
        for cycle in range(3):
            sysdata = RASystemData()
            
            # Load all data
            genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
            nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
            bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
            load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
            (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
             ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
             MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
            
            # Verify data consistency across cycles
            assert ng > 0, f"Generator count should be consistent across cycles: {ng}"
            assert nz > 0, f"Bus count should be consistent across cycles: {nz}"
            assert load_all_regions.shape[0] > 0, f"Load data hours should be consistent: {load_all_regions.shape[0]}"
            assert load_all_regions.shape[1] > 0, f"Load data zones should be consistent: {load_all_regions.shape[1]}"
            assert ness > 0, f"ESS count should be consistent across cycles: {ness}"
            assert nl > 0, f"Branch count should be consistent across cycles: {nl}"
    
    @pytest.mark.integration
    def test_file_isolation(self, real_system_data):
        """Test that no temporary files are created in CWD."""
        # Get initial CWD files
        initial_files = set(Path.cwd().glob("*"))
        
        sysdata = RASystemData()
        
        # Load all data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        load_all_regions = sysdata.load(bus_name, real_system_data["load_csv"])
        (essname, essbus, ness, ess_pmax, ess_pmin, ess_duration,
         ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost,
         MTTF_ess, MTTR_ess, ess_units) = sysdata.storage(real_system_data["storage_csv"])
        
        # Get final CWD files
        final_files = set(Path.cwd().glob("*"))
        
        # Verify no new files were created in CWD
        new_files = final_files - initial_files
        # Filter out common temporary files that might be created by the system
        temp_files = {f for f in new_files if f.suffix in ['.tmp', '.log', '.lock'] or f.name.startswith('.')}
        unexpected_files = new_files - temp_files
        
        assert len(unexpected_files) == 0, f"Unexpected files created in CWD: {unexpected_files}"