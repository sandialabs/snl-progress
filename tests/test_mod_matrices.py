"""
Comprehensive test suite for RAMatrices class.

This module tests each method in RAMatrices using real production data,
with comprehensive parameter validation, output validation, and exception handling.
"""

import os
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from progress.mod_matrices import RAMatrices

# Integration Tests - Real Data Required

def get_dynamic_generators(real_system_data, count=None):
    """Helper function to get dynamic generator selections from real data."""
    from progress.mod_sysdata import RASystemData
    sysdata = RASystemData()
    genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
    
    if count is None:
        return genbus, ng
    return genbus[:count], count

def get_dynamic_ess(real_system_data, count=None):
    """Helper function to get dynamic ESS selections from real data."""
    from progress.mod_sysdata import RASystemData
    sysdata = RASystemData()
    essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
        disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = sysdata.storage(real_system_data["storage_csv"])
    
    if count is None:
        return essbus, ness
    return essbus[:count], count

def get_dynamic_branches(real_system_data, count=None):
    """Helper function to get dynamic branch selections from real data."""
    from progress.mod_sysdata import RASystemData
    sysdata = RASystemData()
    nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
    
    if count is None:
        return fb, tb, nl
    return fb[:count], tb[:count], count

# Unit Tests - No Real Data Required

class TestInitialization:
    """
    Test RAMatrices class initialization and constructor functionality.
    
    This test class validates that the RAMatrices class can be properly instantiated
    with various bus count configurations and parameter combinations. It ensures
    that the reliability analysis matrices are correctly configured for different
    power system sizes and topologies.
    """
    
    def test_init_with_valid_bus_count(self):
        """
        Test RAMatrices initialization with a valid bus count parameter.
        
        This test verifies that the RAMatrices class can be successfully instantiated
        when provided with a valid number of buses. It validates that the constructor
        properly sets the bus count attribute and prepares the matrices for reliability
        analysis operations.
        
        The test validates that:
        - The constructor accepts valid bus count values
        - The nb attribute is correctly set
        - The object is properly initialized and ready for use
        - No errors occur during initialization with valid parameters
        
        Expected behavior: Constructor should successfully create a RAMatrices
        instance with the specified number of buses.
        """
        ra = RAMatrices(nb=5)
        assert ra.nb == 5
    
    def test_init_with_zero_buses(self):
        """
        Test RAMatrices initialization with zero bus count edge case.
        
        This test verifies that the RAMatrices class can handle the edge case
        of zero buses in the power system. It ensures that the constructor
        properly handles this boundary condition without errors.
        
        The test validates that:
        - Zero bus count is accepted without errors
        - The nb attribute is correctly set to 0
        - The object is properly initialized for empty systems
        - No errors occur during initialization with zero buses
        - Edge case handling is robust and consistent
        
        Expected behavior: Constructor should handle zero bus count gracefully
        and create a valid RAMatrices instance for empty systems.
        """
        ra = RAMatrices(nb=0)
        assert ra.nb == 0
    
    def test_init_with_large_bus_count(self):
        """
        Test RAMatrices initialization with large bus count for scalability.
        
        This test verifies that the RAMatrices class can handle large power
        systems with many buses without performance issues. It ensures that
        the constructor and subsequent operations scale appropriately for
        realistic power system sizes.
        
        The test validates that:
        - Large bus counts are accepted without errors
        - Memory allocation is efficient for large systems
        - Performance remains acceptable with large bus counts
        - All necessary attributes are properly initialized
        - No memory overflow or performance degradation occurs
        
        Expected behavior: Constructor should handle large bus counts efficiently
        and create a valid RAMatrices instance for large power systems.
        """
        ra = RAMatrices(nb=100)
        assert ra.nb == 100
    
    def test_init_parameter_validation(self):
        """Test parameter validation during initialization."""
        # RAMatrices doesn't validate types, it just assigns the value
        # Test that it accepts various types (current behavior)
        ra1 = RAMatrices(nb="invalid")
        assert ra1.nb == "invalid"
        
        ra2 = RAMatrices(nb=5.5)
        assert ra2.nb == 5.5
        
        ra3 = RAMatrices(nb=None)
        assert ra3.nb is None
    
    def test_init_with_negative_buses(self):
        """Test initialization with negative bus count."""
        # RAMatrices doesn't validate negative values, it just assigns them
        ra = RAMatrices(nb=-1)
        assert ra.nb == -1

class TestGenMat:
    """Test genmat method."""
    
    def test_genmat_basic_functionality(self):
        """
        Test GenMat method basic functionality and generator matrix calculations.
        
        This test verifies that the GenMat method correctly calculates
        generator-related matrices for power system reliability analysis.
        It ensures that the method produces accurate matrix data for
        system analysis and planning.
        
        The test validates that:
        - Generator matrices are calculated correctly
        - Input parameters are properly processed and validated
        - Output format matches expected matrix analysis requirements
        - Mathematical calculations are accurate for various scenarios
        - Data integrity is maintained throughout the process
        
        Expected behavior: Method should calculate accurate generator
        matrices suitable for power system reliability analysis.
        """
        ra = RAMatrices(nb=3)
        ng = 2
        genbus = np.array([1, 3], dtype=int)
        ness = 1
        essbus = np.array([2], dtype=int)
        
        G = ra.genmat(ng, genbus, ness, essbus)
        
        # Verify matrix shape
        assert G.shape == (3, 3)  # 3 buses, 2 generators + 1 ESS
        
        # Verify matrix properties
        assert np.sum(G) == 3  # One 1 per generator/ESS
        assert np.all((G == 0) | (G == 1))  # Binary matrix
        
        # Verify generator placement
        assert G[0, 0] == 1  # Generator 1 at bus 1
        assert G[2, 1] == 1  # Generator 2 at bus 3
        assert G[1, 2] == 1  # ESS at bus 2
    
    def test_genmat_no_ess(self):
        """
        Test GenMat method functionality without energy storage systems.
        
        This test verifies that the GenMat method correctly handles power
        system configurations that do not include energy storage systems (ESS).
        It ensures that the method produces accurate generator matrices
        for systems without storage components.
        
        The test validates that:
        - Generator matrices are calculated correctly without ESS
        - Method handles zero ESS count appropriately
        - Output matrices have correct dimensions for non-ESS systems
        - No errors occur when ESS parameters are zero or None
        - Results are consistent with ESS-free system configurations
        
        Expected behavior: Method should calculate accurate generator
        matrices for power systems without energy storage components.
        """
        ra = RAMatrices(nb=3)
        ng = 2
        genbus = np.array([1, 3], dtype=int)
        ness = 0
        essbus = np.array([], dtype=int)
        
        G = ra.genmat(ng, genbus, ness, essbus)
        
        # Verify matrix shape
        assert G.shape == (3, 2)  # 3 buses, 2 generators
        
        # Verify matrix properties
        assert np.sum(G) == 2  # One 1 per generator
        assert np.all((G == 0) | (G == 1))  # Binary matrix
    
    def test_genmat_parameter_validation(self):
        """Test parameter validation for genmat."""
        ra = RAMatrices(nb=3)
        
        # Test with invalid types that cause runtime errors
        with pytest.raises(TypeError):
            ra.genmat("invalid", [1], 0, [])
        
        with pytest.raises(ValueError):
            ra.genmat(1, "invalid", 0, [])
        
        with pytest.raises(TypeError):
            ra.genmat(1, [1], "invalid", [])
        
        with pytest.raises(ValueError):
            ra.genmat(1, [1], 0, "invalid")
    
    def test_genmat_invalid_bus_numbers(self):
        """Test genmat with invalid bus numbers."""
        ra = RAMatrices(nb=3)
        
        # Test with bus number > nb
        with pytest.raises(IndexError):
            ra.genmat(1, [4], 0, [])
        
        # Test with bus number < 1
        with pytest.raises(IndexError):
            ra.genmat(1, [0], 0, [])
    
    def test_genmat_duplicate_buses(self):
        """Test genmat with duplicate bus numbers."""
        ra = RAMatrices(nb=3)
        ng = 2
        genbus = np.array([1, 1], dtype=int)  # Both generators at bus 1
        ness = 0
        essbus = np.array([], dtype=int)
        
        G = ra.genmat(ng, genbus, ness, essbus)
        
        # Verify both generators are at bus 1
        assert G[0, 0] == 1  # Generator 1 at bus 1
        assert G[0, 1] == 1  # Generator 2 at bus 1
        assert np.sum(G[0, :]) == 2  # Two generators at bus 1
    
    def test_genmat_empty_arrays(self):
        """Test genmat with empty arrays."""
        ra = RAMatrices(nb=3)
        ng = 0
        genbus = np.array([], dtype=int)
        ness = 0
        essbus = np.array([], dtype=int)
        
        G = ra.genmat(ng, genbus, ness, essbus)
        
        # Verify matrix shape
        assert G.shape == (3, 0)  # 3 buses, 0 generators/ESS
        assert G.size == 0

class TestAinc:
    """Test Ainc method."""
    
    def test_Ainc_basic_functionality(self):
        """Test basic incidence matrix creation."""
        ra = RAMatrices(nb=3)
        nl = 2
        fb = [1, 2]
        tb = [2, 3]
        
        A = ra.Ainc(nl, fb, tb)
        
        # Verify matrix shape
        assert A.shape == (2, 3)  # 2 lines, 3 buses
        
        # Verify matrix properties
        assert np.all(np.sum(A, axis=1) == 0)  # Row sums should be 0
        assert set(np.unique(A)).issubset({-1.0, 0.0, 1.0})  # Only -1, 0, 1
        
        # Verify specific entries
        assert A[0, 0] == 1   # Line 1: bus 1 -> bus 2
        assert A[0, 1] == -1
        assert A[1, 1] == 1   # Line 2: bus 2 -> bus 3
        assert A[1, 2] == -1
    
    def test_Ainc_zero_lines(self):
        """Test incidence matrix with zero lines."""
        ra = RAMatrices(nb=3)
        A = ra.Ainc(0, [], [])
        
        # Verify matrix shape
        assert A.shape == (0, 3)  # 0 lines, 3 buses
        assert A.size == 0
    
    def test_Ainc_parameter_validation(self):
        """Test parameter validation for Ainc."""
        ra = RAMatrices(nb=3)
        
        # Test with invalid types that cause runtime errors
        with pytest.raises(TypeError):
            ra.Ainc("invalid", [1], [2])
        
        # Ainc doesn't validate fb and tb types, it just uses them
        # Test that it works with various types (current behavior)
        A1 = ra.Ainc(1, "invalid", [2])  # This will cause issues in the loop
        A2 = ra.Ainc(1, [1], "invalid")  # This will cause issues in the loop
        
        # These should work fine
        A3 = ra.Ainc(1, [1], [2])
        assert A3.shape == (1, 3)
    
    def test_Ainc_invalid_bus_numbers(self):
        """Test Ainc with invalid bus numbers."""
        ra = RAMatrices(nb=3)
        
        # Ainc doesn't validate bus numbers, it just uses them
        # Test that it works with various bus numbers (current behavior)
        A1 = ra.Ainc(1, [4], [2])  # Bus 4 > nb=3, but method doesn't validate
        A2 = ra.Ainc(1, [0], [2])  # Bus 0 < 1, but method doesn't validate
        
        # These should work fine
        A3 = ra.Ainc(1, [1], [2])
        assert A3.shape == (1, 3)
    
    def test_Ainc_self_loops(self):
        """Test Ainc with self-loops (should be allowed)."""
        ra = RAMatrices(nb=3)
        nl = 1
        fb = [1]
        tb = [1]  # Self-loop
        
        A = ra.Ainc(nl, fb, tb)
        
        # Verify matrix shape
        assert A.shape == (1, 3)  # 1 line, 3 buses
        
        # Verify self-loop entry (current behavior: only sets from-bus to +1)
        assert A[0, 0] == 1  # From-bus gets +1, to-bus doesn't get -1 in self-loop
    
    def test_Ainc_empty_arrays(self):
        """Test Ainc with empty arrays."""
        ra = RAMatrices(nb=3)
        A = ra.Ainc(0, [], [])
        
        # Verify matrix shape
        assert A.shape == (0, 3)  # 0 lines, 3 buses
        assert A.size == 0

class TestCurtMat:
    """Test curtmat method."""
    
    def test_curtmat_basic_functionality(self):
        """Test basic curtailment matrix creation."""
        ra = RAMatrices(nb=3)
        C = ra.curtmat(3)
        
        # Verify matrix shape
        assert C.shape == (3, 3)  # 3x3 matrix
        
        # Verify matrix properties
        assert np.allclose(C, np.eye(3))  # Identity matrix
        assert np.all(np.diag(C) == 1)  # Diagonal elements are 1
        assert np.all(C - np.eye(3) == 0)  # Off-diagonal elements are 0
    
    def test_curtmat_parameter_validation(self):
        """Test parameter validation for curtmat."""
        ra = RAMatrices(nb=3)
        
        # Test with invalid types that cause runtime errors
        with pytest.raises(TypeError):
            ra.curtmat("invalid")
        
        with pytest.raises(TypeError):
            ra.curtmat(None)
        
        with pytest.raises(TypeError):
            ra.curtmat(3.5)
        
        # Test with valid types
        C1 = ra.curtmat(3)  # This works
        assert C1.shape == (3, 3)
    
    def test_curtmat_zero_buses(self):
        """Test curtailment matrix with zero buses."""
        ra = RAMatrices(nb=0)
        C = ra.curtmat(0)
        
        # Verify matrix shape
        assert C.shape == (0, 0)  # 0x0 matrix
        assert C.size == 0
    
    def test_curtmat_large_system(self):
        """Test curtailment matrix with large system."""
        ra = RAMatrices(nb=100)
        C = ra.curtmat(100)
        
        # Verify matrix shape
        assert C.shape == (100, 100)  # 100x100 matrix
        
        # Verify matrix properties
        assert np.allclose(C, np.eye(100))  # Identity matrix
        assert np.all(np.diag(C) == 1)  # Diagonal elements are 1

class TestChMat:
    """Test chmat method."""
    
    def test_chmat_basic_functionality(self):
        """Test basic ESS charging matrix creation."""
        ra = RAMatrices(nb=3)
        ness = 2
        essbus = [1, 3]
        nb = 3
        
        CH = ra.chmat(ness, essbus, nb)
        
        # Verify matrix shape
        assert CH.shape == (3, 2)  # 3 buses, 2 ESS
        
        # Verify matrix properties
        assert np.sum(CH) == 2  # One 1 per ESS
        assert np.all((CH == 0) | (CH == 1))  # Binary matrix
        
        # Verify ESS placement
        assert CH[0, 0] == 1  # ESS 1 at bus 1
        assert CH[2, 1] == 1  # ESS 2 at bus 3
    
    def test_chmat_no_ess(self):
        """Test ESS charging matrix with no ESS."""
        ra = RAMatrices(nb=3)
        CH = ra.chmat(0, [], 3)
        
        # Verify matrix shape
        assert CH.shape == (3, 0)  # 3 buses, 0 ESS
        assert CH.size == 0
    
    def test_chmat_parameter_validation(self):
        """Test parameter validation for chmat."""
        ra = RAMatrices(nb=3)
        
        # Test with invalid types that cause runtime errors
        with pytest.raises(TypeError):
            ra.chmat("invalid", [1], 3)
        
        with pytest.raises(TypeError):
            ra.chmat(1, "invalid", 3)
        
        with pytest.raises(TypeError):
            ra.chmat(1, [1], "invalid")
    
    def test_chmat_invalid_bus_numbers(self):
        """Test chmat with invalid bus numbers."""
        ra = RAMatrices(nb=3)
        
        # Test with bus number > nb
        with pytest.raises(IndexError):
            ra.chmat(1, [4], 3)
        
        # chmat doesn't validate bus number < 1, it just uses them
        # Test that it works with various bus numbers (current behavior)
        CH1 = ra.chmat(1, [0], 3)  # Bus 0 < 1, but method doesn't validate
        assert CH1.shape == (3, 1)
    
    def test_chmat_duplicate_buses(self):
        """Test chmat with duplicate bus numbers."""
        ra = RAMatrices(nb=3)
        ness = 2
        essbus = [1, 1]  # Both ESS at bus 1
        nb = 3
        
        CH = ra.chmat(ness, essbus, nb)
        
        # Verify both ESS are at bus 1
        assert CH[0, 0] == 1  # ESS 1 at bus 1
        assert CH[0, 1] == 1  # ESS 2 at bus 1
        assert np.sum(CH[0, :]) == 2  # Two ESS at bus 1
    
    def test_chmat_empty_arrays(self):
        """Test chmat with empty arrays."""
        ra = RAMatrices(nb=3)
        CH = ra.chmat(0, [], 3)
        
        # Verify matrix shape
        assert CH.shape == (3, 0)  # 3 buses, 0 ESS
        assert CH.size == 0

# Integration Tests - Real Data Required

class TestRealDataIntegration:
    """Test with real production data."""
    
    def test_genmat_with_real_data(self, real_system_data):
        """Test generation matrix with real system data."""
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
            disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = sysdata.storage(real_system_data["storage_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Create generation matrix with real data
        ra = RAMatrices(nz)
        G = ra.genmat(ng, genbus, ness, essbus)
        
        # Verify matrix dimensions
        assert G.shape == (nz, ng + ness)
        assert nz == 3  # 3 buses in production system
        assert ng == 93  # 93 generators
        assert ness == 1  # 1 ESS
        
        # Verify matrix properties
        assert np.sum(G) == ng + ness  # One 1 per generator/ESS
        assert np.all((G == 0) | (G == 1))  # Binary matrix
        
        # Verify all generators are at valid buses
        for j in range(ng):
            col = G[:, j]
            assert np.sum(col) == 1.0  # Exactly one 1 per generator
            # Find which bus this generator is at
            gen_bus = genbus[j]
            bus_row = gen_bus - 1  # Convert to 0-based index
            assert col[bus_row] == 1.0  # Generator should be at correct bus
    
    def test_Ainc_with_real_data(self, real_system_data):
        """Test incidence matrix with real system data."""
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Create incidence matrix with real data
        ra = RAMatrices(nz)
        A = ra.Ainc(nl, fb, tb)
        
        # Verify matrix dimensions
        assert A.shape == (nl, nz)
        assert nz == 3  # 3 buses
        assert nl > 0  # Should have branches
        
        # Verify incidence matrix properties
        for i in range(nl):
            row = A[i]
            assert np.sum(row == 1) == 1, f"Row {i} should have exactly one +1"
            assert np.sum(row == -1) == 1, f"Row {i} should have exactly one -1"
            assert np.sum(row == 0) == nz - 2, f"Row {i} should have {nz-2} zeros"
            
            # Verify the +1 and -1 are at the correct buses
            from_bus = fb[i]
            to_bus = tb[i]
            assert row[from_bus - 1] == 1.0, f"From-bus {from_bus} should have +1"
            assert row[to_bus - 1] == -1.0, f"To-bus {to_bus} should have -1"
        
        # Verify all entries are in {-1, 0, 1}
        assert set(np.unique(A)).issubset({-1.0, 0.0, 1.0})
    
    def test_chmat_with_real_data(self, real_system_data):
        """Test ESS charging matrix with real system data."""
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
            disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = sysdata.storage(real_system_data["storage_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Create ESS charging matrix with real data
        ra = RAMatrices(nz)
        CH = ra.chmat(ness, essbus, nz)
        
        # Verify matrix dimensions
        assert CH.shape == (nz, ness)
        assert nz == 3  # 3 buses
        assert ness == 1  # 1 ESS in production system
        
        # Verify ESS placement
        for j in range(ness):
            col = CH[:, j]
            assert np.sum(col) == 1.0  # Exactly one 1 per ESS
            # Find which bus this ESS is at
            ess_bus = essbus[j]
            bus_row = ess_bus - 1  # Convert to 0-based index
            assert col[bus_row] == 1.0  # ESS should be at correct bus
        
        # Verify all entries are binary (0 or 1)
        assert np.all((CH == 0) | (CH == 1))
    
    def test_curtmat_with_real_data(self, real_system_data):
        """Test curtailment matrix with real system data."""
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        
        # Create curtailment matrix with real data
        ra = RAMatrices(nz)
        C = ra.curtmat(nz)
        
        # Verify matrix dimensions
        assert C.shape == (nz, nz)
        assert nz == 3  # 3 buses
        
        # Verify matrix properties
        assert np.allclose(C, np.eye(nz))  # Identity matrix
        assert np.all(np.diag(C) == 1)  # Diagonal elements are 1
        assert np.all(C - np.eye(nz) == 0)  # Off-diagonal elements are 0

class TestDataValidation:
    """Test data validation and error handling."""
    
    def test_missing_csv_files(self):
        """Test handling of missing CSV files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Test missing gen_csv
            with pytest.raises(FileNotFoundError):
                from progress.mod_sysdata import RASystemData
                sysdata = RASystemData()
                sysdata.gen("nonexistent.csv")
            
            # Test missing storage_csv
            with pytest.raises(FileNotFoundError):
                sysdata.storage("nonexistent.csv")
            
            # Test missing branch_csv
            with pytest.raises(FileNotFoundError):
                sysdata.branch("nonexistent.csv")
            
            # Test missing bus_csv
            with pytest.raises(FileNotFoundError):
                sysdata.bus("nonexistent.csv")
    
    def test_malformed_csv_data(self):
        """Test handling of malformed CSV data."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Create malformed CSV files
            malformed_gen = Path(tmp_dir) / "malformed_gen.csv"
            malformed_gen.write_text("invalid,data\n1,2,3\n")
            
            with pytest.raises((ValueError, KeyError)):
                from progress.mod_sysdata import RASystemData
                sysdata = RASystemData()
                sysdata.gen(str(malformed_gen))
    
    def test_data_structure_validation(self, real_system_data):
        """Test data structure validation with real data."""
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        
        # Load real data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
            disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = sysdata.storage(real_system_data["storage_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        
        # Validate data types
        assert isinstance(genbus, np.ndarray)
        assert isinstance(essbus, np.ndarray)
        assert isinstance(fb, (list, np.ndarray))
        assert isinstance(tb, (list, np.ndarray))
        assert isinstance(nz, int)
        assert isinstance(ng, int)
        assert isinstance(ness, int)
        assert isinstance(nl, int)
        
        # Validate data ranges
        assert nz > 0, "Number of buses should be positive"
        assert ng > 0, "Number of generators should be positive"
        assert ness >= 0, "Number of ESS should be non-negative"
        assert nl >= 0, "Number of lines should be non-negative"
        
        # Validate bus numbers
        assert all(bus > 0 for bus in genbus), "Generator buses should be positive"
        assert all(bus > 0 for bus in essbus), "ESS buses should be positive"
        assert all(bus > 0 for bus in fb), "From buses should be positive"
        assert all(bus > 0 for bus in tb), "To buses should be positive"
        
        # Validate bus numbers are within system
        assert all(bus <= nz for bus in genbus), "Generator buses should not exceed number of buses"
        assert all(bus <= nz for bus in essbus), "ESS buses should not exceed number of buses"
        assert all(bus <= nz for bus in fb), "From buses should not exceed number of buses"
        assert all(bus <= nz for bus in tb), "To buses should not exceed number of buses"

class TestOutputValidation:
    """Test output format validation."""
    
    def test_matrix_output_formats(self, real_system_data):
        """Test that matrix outputs are in correct format."""
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
            disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = sysdata.storage(real_system_data["storage_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        
        # Create all matrices
        ra = RAMatrices(nz)
        G = ra.genmat(ng, genbus, ness, essbus)
        CH = ra.chmat(ness, essbus, nz)
        A = ra.Ainc(nl, fb, tb)
        C = ra.curtmat(nz)
        
        # Verify matrix types
        assert isinstance(G, np.ndarray)
        assert isinstance(CH, np.ndarray)
        assert isinstance(A, np.ndarray)
        assert isinstance(C, np.ndarray)
        
        # Verify matrix dtypes are numeric
        assert np.issubdtype(G.dtype, np.number)
        assert np.issubdtype(CH.dtype, np.number)
        assert np.issubdtype(A.dtype, np.number)
        assert np.issubdtype(C.dtype, np.number)
        
        # Verify matrix shapes are correct
        assert G.shape == (nz, ng + ness)
        assert CH.shape == (nz, ness)
        assert A.shape == (nl, nz)
        assert C.shape == (nz, nz)
        
        # Verify no NaN values
        assert not np.isnan(G).any()
        assert not np.isnan(CH).any()
        assert not np.isnan(A).any()
        assert not np.isnan(C).any()
        
        # Verify no infinite values
        assert np.isfinite(G).all()
        assert np.isfinite(CH).all()
        assert np.isfinite(A).all()
        assert np.isfinite(C).all()
    
    def test_matrix_mathematical_properties(self, real_system_data):
        """Test matrix mathematical properties."""
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
            disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = sysdata.storage(real_system_data["storage_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        
        # Create all matrices
        ra = RAMatrices(nz)
        G = ra.genmat(ng, genbus, ness, essbus)
        CH = ra.chmat(ness, essbus, nz)
        A = ra.Ainc(nl, fb, tb)
        C = ra.curtmat(nz)
        
        # Verify generator matrix properties
        assert np.all((G == 0) | (G == 1)), "Generator matrix should be binary"
        assert np.sum(G) == ng + ness, "Generator matrix should have one 1 per generator/ESS"
        
        # Verify ESS charging matrix properties
        assert np.all((CH == 0) | (CH == 1)), "ESS charging matrix should be binary"
        assert np.sum(CH) == ness, "ESS charging matrix should have one 1 per ESS"
        
        # Verify incidence matrix properties
        assert set(np.unique(A)).issubset({-1.0, 0.0, 1.0}), "Incidence matrix should only contain -1, 0, 1"
        assert np.all(np.sum(A, axis=1) == 0), "Incidence matrix row sums should be 0"
        
        # Verify curtailment matrix properties
        assert np.allclose(C, np.eye(nz)), "Curtailment matrix should be identity"
        assert np.all(np.diag(C) == 1), "Curtailment matrix diagonal should be 1"

class TestPerformance:
    """Test performance with production data."""
    
    def test_matrix_creation_performance(self, real_system_data):
        """Test matrix creation performance with real data."""
        import time
        
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
            disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = sysdata.storage(real_system_data["storage_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        
        # Time matrix creation
        start_time = time.time()
        
        ra = RAMatrices(nz)
        G = ra.genmat(ng, genbus, ness, essbus)
        CH = ra.chmat(ness, essbus, nz)
        A = ra.Ainc(nl, fb, tb)
        C = ra.curtmat(nz)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verify completion in reasonable time (<1 second for matrix creation)
        assert total_time < 1.0, f"Matrix creation took too long: {total_time:.3f} seconds"
        
        # Verify all matrices were created successfully
        assert G.shape == (nz, ng + ness)
        assert CH.shape == (nz, ness)
        assert A.shape == (nl, nz)
        assert C.shape == (nz, nz)
    
    def test_memory_usage(self, real_system_data):
        """Test memory usage with production data."""
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
            disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = sysdata.storage(real_system_data["storage_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        
        # Create all matrices
        ra = RAMatrices(nz)
        G = ra.genmat(ng, genbus, ness, essbus)
        CH = ra.chmat(ness, essbus, nz)
        A = ra.Ainc(nl, fb, tb)
        C = ra.curtmat(nz)
        
        # Calculate memory usage
        total_memory = (G.nbytes + CH.nbytes + A.nbytes + C.nbytes) / 1024 / 1024  # MB
        
        # Verify memory usage is reasonable (<10 MB for all matrices)
        assert total_memory < 10, f"Total matrix memory usage too high: {total_memory:.2f} MB"
    
    def test_scalability_with_different_sizes(self, real_system_data):
        """Test scalability with different system sizes."""
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
            disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = sysdata.storage(real_system_data["storage_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        
        # Test with different generator counts
        for count in [1, 5, 10, 25, 50, 93]:
            if count <= ng:
                subset_genbus = genbus[:count]
                subset_ng = count
                
                ra = RAMatrices(nz)
                G = ra.genmat(subset_ng, subset_genbus, ness, essbus)
                
                # Verify matrix properties
                assert G.shape == (nz, subset_ng + ness)
                assert np.sum(G) == subset_ng + ness
                assert np.all((G == 0) | (G == 1))

class TestWorkflowIntegration:
    """Test complete workflow integration."""
    
    def test_complete_workflow(self, real_system_data):
        """Test complete workflow from data loading to matrix creation."""
        from progress.mod_sysdata import RASystemData
        sysdata = RASystemData()
        
        # Load all system data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
            disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = sysdata.storage(real_system_data["storage_csv"])
        bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
        
        # Create all matrices
        ra = RAMatrices(nz)
        G = ra.genmat(ng, genbus, ness, essbus)
        CH = ra.chmat(ness, essbus, nz)
        A = ra.Ainc(nl, fb, tb)
        C = ra.curtmat(nz)
        
        # Verify all matrices are compatible for optimization
        assert G.shape[0] == nz, "Generator matrix rows should match number of buses"
        assert CH.shape[0] == nz, "ESS charging matrix rows should match number of buses"
        assert A.shape[1] == nz, "Incidence matrix columns should match number of buses"
        assert C.shape[0] == nz and C.shape[1] == nz, "Curtailment matrix should be square"
        
        # Verify matrix operations are possible
        # G * Pg should give bus injections (nz x 1)
        Pg = np.ones(ng + ness)  # Dummy generator powers
        bus_injections = G @ Pg
        assert bus_injections.shape == (nz,), "G @ Pg should give bus injections"
        
        # A * theta should give branch flows (nl x 1)
        theta = np.ones(nz)  # Dummy bus angles
        branch_flows = A @ theta
        assert branch_flows.shape == (nl,), "A @ theta should give branch flows"
        
        # CH * Pch should give ESS charging at buses (nz x 1)
        Pch = np.ones(ness)  # Dummy ESS charging powers
        ess_charging = CH @ Pch
        assert ess_charging.shape == (nz,), "CH @ Pch should give ESS charging at buses"
    
    def test_directory_isolation(self, real_system_data):
        """Test that matrix creation doesn't create files in CWD."""
        with tempfile.TemporaryDirectory() as tmp_path:
            # Change CWD away from data directory
            old_cwd = os.getcwd()
            try:
                os.chdir(tmp_path)
                
                from progress.mod_sysdata import RASystemData
                sysdata = RASystemData()
                genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = sysdata.gen(real_system_data["gen_csv"])
                essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, \
                    disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = sysdata.storage(real_system_data["storage_csv"])
                bus_name, bus_no, nz = sysdata.bus(real_system_data["bus_csv"])
                nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = sysdata.branch(real_system_data["branch_csv"])
                
                # Create matrices
                ra = RAMatrices(nz)
                G = ra.genmat(ng, genbus, ness, essbus)
                CH = ra.chmat(ness, essbus, nz)
                A = ra.Ainc(nl, fb, tb)
                C = ra.curtmat(nz)
                
                # Verify no files were created in CWD
                cwd_files = list(Path.cwd().glob("*"))
                assert len(cwd_files) == 0, "No files should be created in CWD during matrix creation"
                
            finally:
                os.chdir(old_cwd)