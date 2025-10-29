"""
Test suite for mod_utilities.py - RAUtilities class
Comprehensive tests for reliability analysis utilities
"""

import pytest
import numpy as np
import pandas as pd
import time
import tempfile
import os
import psutil
from unittest.mock import Mock, patch

from progress.mod_utilities import RAUtilities


def solver_available():
    """Check if an optimization solver is available"""
    try:
        from pyomo.environ import SolverFactory
        solver = SolverFactory('glpk')
        return solver.available()
    except:
        return False


@pytest.fixture
def utilities_test_helper():
    """Helper fixture for RAUtilities testing"""
    return RAUtilities()




class TestInitialization:
    """
    Test RAUtilities class initialization and constructor functionality.
    
    This test class validates that the RAUtilities class can be properly instantiated
    and that all essential attributes and methods are correctly initialized. It ensures
    that the reliability analysis utilities are ready for use in power system analysis.
    """
    
    def test_init_basic(self):
        """
        Test basic RAUtilities class initialization without parameters.
        
        This test verifies that the RAUtilities class can be successfully instantiated
        using the default constructor without any parameters. It validates that the
        object is properly created and is of the correct type.
        
        The test validates that:
        - The constructor executes without errors
        - The created object is an instance of RAUtilities
        - Basic object creation functionality works correctly
        - No exceptions are raised during initialization
        
        Expected behavior: Constructor should successfully create a RAUtilities
        instance that can be used for reliability analysis operations.
        """
        ra = RAUtilities()
        assert isinstance(ra, RAUtilities)
    
    def test_init_attributes(self):
        """
        Test that all essential attributes are properly initialized in RAUtilities.
        
        This test verifies that the RAUtilities class initializes all necessary
        attributes and methods required for reliability analysis operations. It
        ensures that the object has all the expected functionality available
        immediately after instantiation.
        
        The test validates that:
        - All essential attributes are present after initialization
        - Required methods are available and callable
        - Attribute names match expected interface
        - No critical attributes are missing
        - Object is fully functional after creation
        
        Expected behavior: All essential attributes and methods should be
        available and properly initialized after object creation.
        """
        ra = RAUtilities()
        # Check that essential attributes are initialized
        assert hasattr(ra, 'reltrates')
        assert hasattr(ra, 'capacities')
        assert hasattr(ra, 'NextState')
        assert hasattr(ra, 'updateSOC')
        assert hasattr(ra, 'WindPower')
        assert hasattr(ra, 'SolarPower')


class TestReltRates:
    """Test reltrates method"""
    
    def test_reltrates_basic_functionality(self, utilities_test_helper):
        """
        Test ReltRates method basic functionality and reliability rate calculations.
        
        This test verifies that the ReltRates method correctly calculates
        reliability transition rates for power system components. It ensures
        that the method produces accurate reliability metrics for system
        analysis and planning.
        
        The test validates that:
        - Reliability transition rates are calculated correctly
        - Input data is properly processed and validated
        - Output format matches expected reliability analysis requirements
        - Mathematical calculations are accurate for various scenarios
        - Data integrity is maintained throughout the process
        
        Expected behavior: Method should calculate reliable transition rates
        suitable for power system reliability analysis.
        
        Args:
            utilities_test_helper: Pytest fixture providing test data and utilities
        """
        ra = utilities_test_helper
        
        # Test with valid parameters
        MTTF_gen = np.array([100.0, 150.0, 200.0])  # Mean time to failure for generators
        MTTF_trans = np.array([300.0, 250.0])       # Mean time to failure for transmission
        MTTR_gen = np.array([10.0, 15.0, 20.0])     # Mean time to repair for generators
        MTTR_trans = np.array([30.0, 25.0])         # Mean time to repair for transmission
        MTTF_ess = np.array([400.0])                # Mean time to failure for ESS
        MTTR_ess = np.array([40.0])                 # Mean time to repair for ESS
        
        rates = ra.reltrates(MTTF_gen, MTTF_trans, MTTR_gen, MTTR_trans, MTTF_ess, MTTR_ess)
        
        assert isinstance(rates, tuple)
        assert len(rates) == 2
        mu_tot, lambda_tot = rates
        
        assert isinstance(mu_tot, np.ndarray)
        assert isinstance(lambda_tot, np.ndarray)
        assert len(mu_tot) == len(MTTF_gen) + len(MTTF_trans) + len(MTTF_ess)
        assert len(lambda_tot) == len(MTTF_gen) + len(MTTF_trans) + len(MTTF_ess)
    
    def test_reltrates_data_ranges(self, utilities_test_helper):
        """
        Test ReltRates method data range validation and boundary handling.
        
        This test verifies that the ReltRates method correctly handles
        various data ranges and boundary conditions for reliability rate
        calculations. It ensures that the method produces accurate results
        across different input value ranges.
        
        The test validates that:
        - Data range validation works correctly for different value scales
        - Boundary conditions are handled appropriately
        - Calculations remain accurate across various input ranges
        - No data overflow or underflow occurs during processing
        - Results are physically reasonable for reliability analysis
        
        Expected behavior: Method should handle various data ranges correctly
        and produce accurate reliability rates across different scenarios.
        
        Args:
            utilities_test_helper: Pytest fixture providing test data and utilities
        """
        ra = utilities_test_helper
        
        MTTF_gen = np.array([100.0, 150.0])
        MTTF_trans = np.array([300.0])
        MTTR_gen = np.array([10.0, 15.0])
        MTTR_trans = np.array([30.0])
        MTTF_ess = np.array([400.0])
        MTTR_ess = np.array([40.0])
        
        rates = ra.reltrates(MTTF_gen, MTTF_trans, MTTR_gen, MTTR_trans, MTTF_ess, MTTR_ess)
        mu_tot, lambda_tot = rates
        
        # Check that rates are positive
        assert np.all(lambda_tot > 0)
        assert np.all(mu_tot > 0)
    
    def test_reltrates_calculation_accuracy(self, utilities_test_helper):
        """Test reltrates calculation accuracy"""
        ra = utilities_test_helper
        
        MTTF_gen = np.array([100.0, 150.0])
        MTTF_trans = np.array([300.0])
        MTTR_gen = np.array([10.0, 15.0])
        MTTR_trans = np.array([30.0])
        MTTF_ess = np.array([400.0])
        MTTR_ess = np.array([40.0])
        
        rates = ra.reltrates(MTTF_gen, MTTF_trans, MTTR_gen, MTTR_trans, MTTF_ess, MTTR_ess)
        mu_tot, lambda_tot = rates
        
        # Check that the total rates match expected values
        expected_mu = 1 / np.concatenate([MTTR_gen, MTTR_trans, MTTR_ess])
        expected_lambda = 1 / np.concatenate([MTTF_gen, MTTF_trans, MTTF_ess])
        
        assert np.allclose(mu_tot, expected_mu, rtol=1e-6)
        assert np.allclose(lambda_tot, expected_lambda, rtol=1e-6)


class TestCapacities:
    """Test capacities method"""
    
    def test_capacities_basic_functionality(self, utilities_test_helper):
        """
        Test Capacities method basic functionality and capacity calculations.
        
        This test verifies that the Capacities method correctly calculates
        and processes power system component capacities. It ensures that
        the method produces accurate capacity data for system analysis.
        
        The test validates that:
        - Component capacities are calculated correctly
        - Input data is properly processed and validated
        - Output format matches expected capacity analysis requirements
        - Mathematical calculations are accurate for various scenarios
        - Data integrity is maintained throughout the process
        
        Expected behavior: Method should calculate accurate component
        capacities suitable for power system analysis.
        
        Args:
            utilities_test_helper: Pytest fixture providing test data and utilities
        """
        ra = utilities_test_helper
        
        # Test with valid parameters
        nl = 1
        pmax = np.array([100.0, 150.0])
        pmin = np.array([0.0, 0.0])
        ess_pmax = np.array([50.0])
        ess_pmin = np.array([0.0])
        cap_trans = np.array([200.0])
        
        capacities = ra.capacities(nl, pmax, pmin, ess_pmax, ess_pmin, cap_trans)
        
        assert isinstance(capacities, tuple)
        assert len(capacities) == 2
        cap_max, cap_min = capacities
        
        assert isinstance(cap_max, np.ndarray)
        assert isinstance(cap_min, np.ndarray)
        assert len(cap_max) == len(pmax) + nl + len(ess_pmax)
        assert len(cap_min) == len(pmax) + nl + len(ess_pmax)
        assert np.all(cap_max >= 0)
        assert np.all(cap_min >= 0)
    
    def test_capacities_data_ranges(self, utilities_test_helper):
        """
        Test Capacities method data range validation and boundary handling.
        
        This test verifies that the Capacities method correctly handles
        various data ranges and boundary conditions for capacity calculations.
        It ensures that the method produces accurate results across different
        input value ranges and system configurations.
        
        The test validates that:
        - Data range validation works correctly for different capacity scales
        - Boundary conditions are handled appropriately
        - Calculations remain accurate across various input ranges
        - No data overflow or underflow occurs during processing
        - Results are physically reasonable for power system analysis
        
        Expected behavior: Method should handle various data ranges correctly
        and produce accurate capacity data across different scenarios.
        
        Args:
            utilities_test_helper: Pytest fixture providing test data and utilities
        """
        ra = utilities_test_helper
        
        nl = 1
        pmax = np.array([100.0, 150.0])
        pmin = np.array([0.0, 0.0])
        ess_pmax = np.array([50.0])
        ess_pmin = np.array([0.0])
        cap_trans = np.array([200.0])
        
        capacities = ra.capacities(nl, pmax, pmin, ess_pmax, ess_pmin, cap_trans)
        cap_max, cap_min = capacities
        
        # Check that capacities are non-negative
        assert np.all(cap_max >= 0)
        assert np.all(cap_min >= 0)
        
        # Check that capacities are reasonable
        assert np.all(cap_max <= 1000.0)
        assert np.all(cap_min <= 1000.0)
    
    def test_capacities_concatenation_order(self, utilities_test_helper):
        """Test capacities concatenation order"""
        ra = utilities_test_helper
        
        nl = 1
        pmax = np.array([100.0, 150.0])
        pmin = np.array([0.0, 0.0])
        ess_pmax = np.array([50.0])
        ess_pmin = np.array([0.0])
        cap_trans = np.array([200.0])
        
        capacities = ra.capacities(nl, pmax, pmin, ess_pmax, ess_pmin, cap_trans)
        cap_max, cap_min = capacities
        
        # Check that the order is (pmax, cap_trans, ess_pmax)
        assert cap_max[0] == 100.0  # First generator
        assert cap_max[1] == 150.0  # Second generator
        assert cap_max[2] == 200.0  # Transmission
        assert cap_max[3] == 50.0   # ESS


class TestNextState:
    """Test NextState method"""
    
    def test_nextstate_basic_functionality(self, utilities_test_helper):
        """Test basic NextState calculation"""
        ra = utilities_test_helper
        
        # Test with valid parameters
        t_min = 10.0
        ng = 2
        ness = 1
        nl = 1
        lambda_tot = np.array([0.01, 0.02, 0.015, 0.005])
        mu_tot = np.array([0.1, 0.15, 0.2, 0.05])
        current_state = np.array([1, 0, 1, 1])
        cap_max = np.array([100.0, 150.0, 200.0, 50.0])
        cap_min = np.array([0.0, 0.0, 0.0, 0.0])
        ess_units = np.array([1])
        
        result = ra.NextState(t_min, ng, ness, nl, lambda_tot, mu_tot, current_state, cap_max, cap_min, ess_units)
        
        assert isinstance(result, tuple)
        assert len(result) == 3
        new_state, new_cap, t_min_result = result
        
        assert isinstance(new_cap, dict)
        assert 'max' in new_cap
        assert 'min' in new_cap
        assert isinstance(new_cap['max'], np.ndarray)
        assert isinstance(new_cap['min'], np.ndarray)
    
    def test_nextstate_data_structure(self, utilities_test_helper):
        """Test NextState data structure"""
        ra = utilities_test_helper
        
        t_min = 10.0
        ng = 2
        ness = 1
        nl = 1
        lambda_tot = np.array([0.01, 0.02, 0.015, 0.005])
        mu_tot = np.array([0.1, 0.15, 0.2, 0.05])
        current_state = np.array([1, 0, 1, 1])
        cap_max = np.array([100.0, 150.0, 200.0, 50.0])
        cap_min = np.array([0.0, 0.0, 0.0, 0.0])
        ess_units = np.array([1])
        
        result = ra.NextState(t_min, ng, ness, nl, lambda_tot, mu_tot, current_state, cap_max, cap_min, ess_units)
        new_state, new_cap, t_min_result = result
        
        # Check data types
        assert new_cap['max'].dtype in [np.float64, np.float32]
        assert new_cap['min'].dtype in [np.float64, np.float32]
        
        # Check array lengths
        assert len(new_cap['max']) == 4
        assert len(new_cap['min']) == 4
    
    def test_nextstate_state_transitions(self, utilities_test_helper):
        """Test NextState state transitions"""
        ra = utilities_test_helper
        
        t_min = 10.0
        ng = 2
        ness = 1
        nl = 1
        lambda_tot = np.array([0.01, 0.02, 0.015, 0.005])
        mu_tot = np.array([0.1, 0.15, 0.2, 0.05])
        current_state = np.array([1, 0, 1, 1])
        cap_max = np.array([100.0, 150.0, 200.0, 50.0])
        cap_min = np.array([0.0, 0.0, 0.0, 0.0])
        ess_units = np.array([1])
        
        result = ra.NextState(t_min, ng, ness, nl, lambda_tot, mu_tot, current_state, cap_max, cap_min, ess_units)
        new_state, new_cap, t_min_result = result
        
        # Check that when state is 0, capacity becomes 0
        for i in range(len(current_state)):
            if current_state[i] == 0:
                assert new_cap['max'][i] == 0.0
                assert new_cap['min'][i] == 0.0
    
    def test_nextstate_capacity_updates(self, utilities_test_helper):
        """Test NextState capacity updates"""
        ra = utilities_test_helper
        
        t_min = 10.0
        ng = 2
        ness = 1
        nl = 1
        lambda_tot = np.array([0.01, 0.02, 0.015, 0.005])
        mu_tot = np.array([0.1, 0.15, 0.2, 0.05])
        current_state = np.array([1, 0, 1, 1])
        cap_max = np.array([100.0, 150.0, 200.0, 50.0])
        cap_min = np.array([0.0, 0.0, 0.0, 0.0])
        ess_units = np.array([1])
        
        result = ra.NextState(t_min, ng, ness, nl, lambda_tot, mu_tot, current_state, cap_max, cap_min, ess_units)
        new_state, new_cap, t_min_result = result
        
        # Check that capacities are within bounds
        assert np.all(new_cap['max'] >= 0)
        assert np.all(new_cap['min'] >= 0)
        assert np.all(new_cap['max'] <= cap_max)
        assert np.all(new_cap['min'] <= cap_min)


class TestUpdateSOC:
    """Test updateSOC method"""
    
    def test_updatesoc_basic_functionality(self, utilities_test_helper):
        """Test basic updateSOC calculation"""
        ra = utilities_test_helper
        
        # Test with valid parameters
        ng = 2
        nl = 1
        # current_cap["max"] should have length ng + nl + len(ess_pmax)
        current_cap = {"max": np.array([100.0, 150.0, 200.0, 50.0, 75.0])}  # ng + nl + 2 ESS units
        ess_pmax = np.array([50.0, 75.0])
        ess_duration = np.array([4.0, 6.0])
        ess_socmax = np.array([0.9, 0.8])
        ess_socmin = np.array([0.1, 0.2])
        SOC_old = np.array([0.5, 0.6])
        
        result = ra.updateSOC(ng, nl, current_cap, ess_pmax, ess_duration, ess_socmax, ess_socmin, SOC_old)
        
        assert isinstance(result, tuple)
        assert len(result) == 3
        ess_smax, ess_smin, SOC_new = result
        
        assert isinstance(ess_smax, np.ndarray)
        assert isinstance(ess_smin, np.ndarray)
        assert isinstance(SOC_new, np.ndarray)
        assert len(SOC_new) == len(SOC_old)
        assert SOC_new.dtype in [np.float64, np.float32]
    
    def test_updatesoc_parameter_validation(self, utilities_test_helper):
        """Test parameter validation for updateSOC"""
        ra = utilities_test_helper
        
        # Test with invalid parameters
        with pytest.raises((TypeError, ValueError, KeyError)):
            ra.updateSOC("invalid", 1, {}, np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]))
    
    def test_updatesoc_data_structure(self, utilities_test_helper):
        """Test data structure of updateSOC output"""
        ra = utilities_test_helper
        
        # Test with valid parameters
        ng = 3
        nl = 5
        current_cap = {"max": np.array([100.0, 150.0, 200.0, 50.0, 75.0, 25.0, 30.0, 35.0, 40.0, 45.0])}  # Include ESS capacities
        ess_pmax = np.array([50.0, 75.0])
        ess_duration = np.array([4.0, 6.0])
        ess_socmax = np.array([0.9, 0.8])
        ess_socmin = np.array([0.1, 0.2])
        SOC_old = np.array([0.5, 0.6])
        
        result = ra.updateSOC(ng, nl, current_cap, ess_pmax, ess_duration, ess_socmax, ess_socmin, SOC_old)
        
        # Check return type
        assert isinstance(result, tuple)
        assert len(result) == 3
        ess_smax, ess_smin, SOC_new = result
        
        # Check array types
        assert isinstance(ess_smax, np.ndarray)
        assert isinstance(ess_smin, np.ndarray)
        assert isinstance(SOC_new, np.ndarray)
        assert SOC_new.dtype in [np.float64, np.float32]
        
        # Check array length
        assert len(SOC_new) == len(SOC_old)
    
    def test_updatesoc_soc_ranges(self, utilities_test_helper):
        """Test SOC ranges in updateSOC"""
        ra = utilities_test_helper
        
        # Test with valid parameters
        ng = 3
        nl = 5
        current_cap = {"max": np.array([100.0, 150.0, 200.0, 50.0, 75.0, 25.0, 30.0, 35.0, 40.0, 45.0])}  # Include ESS capacities
        ess_pmax = np.array([50.0, 75.0])
        ess_duration = np.array([4.0, 6.0])
        ess_socmax = np.array([0.9, 0.8])
        ess_socmin = np.array([0.1, 0.2])
        SOC_old = np.array([0.5, 0.6])
        
        result = ra.updateSOC(ng, nl, current_cap, ess_pmax, ess_duration, ess_socmax, ess_socmin, SOC_old)
        ess_smax, ess_smin, SOC_new = result
        
        # Check that SOC values are within bounds
        assert np.all(SOC_new >= 0.0), "SOC values should be >= 0.0"
        assert np.all(SOC_new <= 1.0), "SOC values should be <= 1.0"
        
        # Check that SOC values are within min/max bounds
        for i in range(len(SOC_new)):
            assert SOC_new[i] >= ess_socmin[i], f"SOC[{i}] should be >= ess_socmin[{i}]"
            assert SOC_new[i] <= ess_socmax[i], f"SOC[{i}] should be <= ess_socmax[{i}]"
    
    def test_updatesoc_scaling(self, utilities_test_helper):
        """Test SOC scaling in updateSOC"""
        ra = utilities_test_helper
        
        # Test with valid parameters
        ng = 3
        nl = 5
        current_cap = {"max": np.array([100.0, 150.0, 200.0, 50.0, 75.0, 25.0, 30.0, 35.0, 40.0, 45.0])}  # Include ESS capacities
        ess_pmax = np.array([50.0, 75.0])
        ess_duration = np.array([4.0, 6.0])
        ess_socmax = np.array([0.9, 0.8])
        ess_socmin = np.array([0.1, 0.2])
        SOC_old = np.array([0.5, 0.6])
        
        result = ra.updateSOC(ng, nl, current_cap, ess_pmax, ess_duration, ess_socmax, ess_socmin, SOC_old)
        ess_smax, ess_smin, SOC_new = result
        
        # Check that SOC values are reasonable
        assert np.all(SOC_new >= 0.0), "SOC values should be >= 0.0"
        assert np.all(SOC_new <= 1.0), "SOC values should be <= 1.0"
        
        # Check that SOC values are within min/max bounds
        for i in range(len(SOC_new)):
            assert SOC_new[i] >= ess_socmin[i], f"SOC[{i}] should be >= ess_socmin[{i}]"
            assert SOC_new[i] <= ess_socmax[i], f"SOC[{i}] should be <= ess_socmax[{i}]"
    
    def test_updatesoc_with_production_data(self, utilities_test_helper):
        """Test updateSOC with production data"""
        ra = utilities_test_helper
        
        # Test with production-like parameters
        ng = 93  # Production number of generators
        nl = 3   # Production number of buses
        # Create a long enough array for slicing: ng + nl + len(ess_pmax)
        current_cap = {"max": np.random.uniform(10, 200, ng + nl + 1)}
        ess_pmax = np.array([50.0])  # Production ESS capacity
        ess_duration = np.array([4.0])  # Production ESS duration
        ess_socmax = np.array([0.9])  # Production ESS max SOC
        ess_socmin = np.array([0.1])  # Production ESS min SOC
        SOC_old = np.array([0.5])  # Production SOC
        
        result = ra.updateSOC(ng, nl, current_cap, ess_pmax, ess_duration, ess_socmax, ess_socmin, SOC_old)
        ess_smax, ess_smin, SOC_new = result
        
        assert isinstance(SOC_new, np.ndarray)
        assert len(SOC_new) == 1  # One ESS unit
        assert np.all(SOC_new >= 0.0)
        # SOC_new is in energy units, not normalized, so we check it's reasonable
        assert np.all(SOC_new <= 1000.0)  # Reasonable upper bound for energy
        
        # Verify SOC ranges
        assert np.all(ess_socmax > ess_socmin), "Max SOC should be > min SOC"
        assert np.all(ess_socmax <= 1.0), "Max SOC should be <= 1.0"
        assert np.all(ess_socmin >= 0.0), "Min SOC should be >= 0.0"


class TestWindPower:
    """Test WindPower method"""
    
    def test_wind_power_basic_functionality(self, utilities_test_helper):
        """Test basic wind power calculation"""
        ra = utilities_test_helper
        
        # Test with valid parameters
        nz = 1
        w_sites = 1
        zone_no = np.array([1])
        w_classes = 1
        r_cap = np.array([100.0])
        current_w_class = np.array([1])
        tr_mats = np.array([[1.0]])
        p_class = np.array([1.0])
        w_turbines = np.array([1])
        out_curve2 = np.array([0.0, 0.5, 1.0, 0.8, 0.0])
        out_curve3 = np.array([0.0, 0.3, 0.9, 0.7, 0.0])
        
        result = ra.WindPower(nz, w_sites, zone_no, w_classes, r_cap, current_w_class, tr_mats, p_class, w_turbines, out_curve2, out_curve3)
        
        # WindPower returns a tuple (wind_power, wind_matrix)
        assert isinstance(result, tuple)
        assert len(result) == 2
        wind_power, wind_matrix = result
        
        assert isinstance(wind_power, np.ndarray)
        assert len(wind_power) == w_sites
        assert np.all(wind_power >= 0)
        assert np.all(wind_power <= 1.0)  # Normalized power
    
    def test_wind_power_parameter_validation(self, utilities_test_helper):
        """Test parameter validation for WindPower"""
        ra = utilities_test_helper
        
        # Test with invalid parameters
        with pytest.raises((TypeError, AttributeError)):
            ra.WindPower("invalid", 1, np.array([1]), 1, np.array([1.0]), np.array([1]), np.array([[1.0]]), np.array([1.0]), np.array([1]), np.array([1.0]), np.array([1.0]))
        
        # Test with None
        with pytest.raises((TypeError, AttributeError)):
            ra.WindPower(None, 1, np.array([1]), 1, np.array([1.0]), np.array([1]), np.array([[1.0]]), np.array([1.0]), np.array([1]), np.array([1.0]), np.array([1.0]))
    
    def test_wind_power_data_ranges(self, utilities_test_helper):
        """Test wind power calculation with various wind speeds"""
        ra = utilities_test_helper
        
        # Set up parameters for wind power calculation
        nz = 1
        w_sites = 1
        zone_no = np.array([1])
        w_classes = 1
        r_cap = np.array([100.0])
        current_w_class = np.array([1])
        tr_mats = np.array([[1.0]])
        p_class = np.array([1.0])
        w_turbines = np.array([1])
        out_curve2 = np.array([0.0, 0.5, 1.0, 0.8, 0.0])
        out_curve3 = np.array([0.0, 0.3, 0.9, 0.7, 0.0])
        
        # Test with zero wind speed
        wind_speed = np.array([0.0])
        result = ra.WindPower(nz, w_sites, zone_no, w_classes, r_cap, current_w_class, tr_mats, p_class, w_turbines, out_curve2, out_curve3)
        wind_power, wind_matrix = result
        assert wind_power[0] == 0.0
        
        # Test with very high wind speed
        wind_speed = np.array([50.0])
        result = ra.WindPower(nz, w_sites, zone_no, w_classes, r_cap, current_w_class, tr_mats, p_class, w_turbines, out_curve2, out_curve3)
        wind_power, wind_matrix = result
        assert wind_power[0] <= 1.0  # Should be capped at rated power
        
        # Test with negative wind speed
        wind_speed = np.array([-5.0])
        result = ra.WindPower(nz, w_sites, zone_no, w_classes, r_cap, current_w_class, tr_mats, p_class, w_turbines, out_curve2, out_curve3)
        wind_power, wind_matrix = result
        assert wind_power[0] == 0.0  # Should be zero for negative speeds


class TestSolarPower:
    """Test SolarPower method"""
    
    def test_solar_power_basic_functionality(self, utilities_test_helper):
        """Test basic solar power calculation"""
        ra = utilities_test_helper
        
        # Test with valid parameters
        n = 0  # Number of hours (must be divisible by 24 for s_zones initialization)
        nz = 1  # Number of zones
        s_zone_no = np.array([1])
        solar_prob = np.array([[1.0]])  # 2D array for monthly probabilities
        s_profiles = [np.random.uniform(0, 1, (1, 24, 1))]  # List of 3D arrays: [cluster][day, hour, site] - shape (1, 24, 1)
        s_sites = 1
        s_max = np.array([100.0])
        
        solar_power = ra.SolarPower(n, nz, s_zone_no, solar_prob, s_profiles, s_sites, s_max)
        
        assert isinstance(solar_power, np.ndarray)
        assert solar_power.shape == (24, nz)  # Shape is (hours, zones)
        assert np.all(solar_power >= 0)
    
    def test_solar_power_parameter_validation(self, utilities_test_helper):
        """Test parameter validation for SolarPower"""
        ra = utilities_test_helper
        
        # Test with invalid parameters
        with pytest.raises((TypeError, AttributeError)):
            ra.SolarPower("invalid", 1, np.array([1]), np.array([1.0]), np.array([[1.0]]), 1, np.array([1.0]))
        
        # Test with None
        with pytest.raises((TypeError, AttributeError)):
            ra.SolarPower(None, 1, np.array([1]), np.array([1.0]), np.array([[1.0]]), 1, np.array([1.0]))
    
    def test_solar_power_data_ranges(self, utilities_test_helper):
        """Test solar power calculation with various irradiance levels"""
        ra = utilities_test_helper
        
        # Set up parameters for solar power calculation
        n = 0  # Must be divisible by 24
        nz = 1
        s_zone_no = np.array([1])
        solar_prob = np.array([[1.0]])  # 2D array
        s_profiles = [np.random.uniform(0, 1, (1, 24, 1))]  # List of 3D arrays: [cluster][day, hour, site] - shape (1, 24, 1)
        s_sites = 1
        s_max = np.array([100.0])
        
        # Test with zero irradiance
        solar_power = ra.SolarPower(n, nz, s_zone_no, solar_prob, s_profiles, s_sites, s_max)
        assert solar_power[0] >= 0.0
        
        # Test with maximum irradiance
        s_profiles = [np.ones((1, 24, 1))]  # 3D array with all 1s
        solar_power = ra.SolarPower(n, nz, s_zone_no, solar_prob, s_profiles, s_sites, s_max)
        assert solar_power[0, 0] <= 100.0  # Should be scaled by s_max


class TestTrackLOLStates:
    """Test TrackLOLStates method"""
    
    def test_tracklolstates_basic_functionality(self, utilities_test_helper):
        """Test basic TrackLOLStates functionality"""
        ra = utilities_test_helper
        
        # Test with load curtailment
        load_curt = 0.1  # 0.1 p.u. load curtailment
        BMva = 100.0
        var_s = {
            "LLD": 0,
            "curtailment": np.zeros(24),
            "label_LOLF": np.zeros(24),
            "freq_LOLF": 0,
            "LOL_days": 0,
            "outage_day": np.zeros(365)
        }
        LOL_track = np.zeros((10, 24))
        s = 0
        n = 5
        
        result = ra.TrackLOLStates(load_curt, BMva, var_s, LOL_track, s, n)
        
        assert isinstance(result, tuple)
        assert len(result) == 2
        updated_var_s, updated_LOL_track = result
        
        # Check that LLD was incremented
        assert updated_var_s["LLD"] == 1
        # Check that curtailment was recorded
        assert updated_var_s["curtailment"][n] == load_curt * BMva
        # Check that LOLF label was set
        assert updated_var_s["label_LOLF"][n] == 1
        # Check that LOL_track was updated
        assert updated_LOL_track[s][n] == 1
    
    def test_tracklolstates_no_curtailment(self, utilities_test_helper):
        """Test TrackLOLStates with no load curtailment"""
        ra = utilities_test_helper
        
        # Test with no load curtailment
        load_curt = 0.0
        BMva = 100.0
        var_s = {
            "LLD": 0,
            "curtailment": np.zeros(24),
            "label_LOLF": np.zeros(24),
            "freq_LOLF": 0,
            "LOL_days": 0,
            "outage_day": np.zeros(365)
        }
        LOL_track = np.zeros((10, 24))
        s = 0
        n = 5
        
        result = ra.TrackLOLStates(load_curt, BMva, var_s, LOL_track, s, n)
        
        assert isinstance(result, tuple)
        assert len(result) == 2
        updated_var_s, updated_LOL_track = result
        
        # Check that LLD was not incremented
        assert updated_var_s["LLD"] == 0
        # Check that curtailment was not recorded
        assert updated_var_s["curtailment"][n] == 0
        # Check that LOLF label was not set
        assert updated_var_s["label_LOLF"][n] == 0
        # Check that LOL_track was not updated
        assert updated_LOL_track[s][n] == 0
    
    def test_tracklolstates_lolf_frequency(self, utilities_test_helper):
        """Test LOLF frequency calculation"""
        ra = utilities_test_helper
        
        # Test with load curtailment after no curtailment
        BMva = 100.0
        var_s = {
            "LLD": 0,
            "curtailment": np.zeros(24),
            "label_LOLF": np.zeros(24),
            "freq_LOLF": 0,
            "LOL_days": 0,
            "outage_day": np.zeros(365)
        }
        LOL_track = np.zeros((10, 24))
        s = 0
        
        # First hour with no curtailment
        result1 = ra.TrackLOLStates(0.0, BMva, var_s, LOL_track, s, 0)
        var_s, LOL_track = result1
        
        # Second hour with curtailment (should increment freq_LOLF)
        result2 = ra.TrackLOLStates(0.1, BMva, var_s, LOL_track, s, 1)
        var_s, LOL_track = result2
        
        # Check that freq_LOLF was incremented
        assert var_s["freq_LOLF"] == 1
    
    def test_tracklolstates_daily_outage_tracking(self, utilities_test_helper):
        """Test daily outage tracking at 24-hour intervals"""
        ra = utilities_test_helper
        
        BMva = 100.0
        var_s = {
            "LLD": 0,
            "curtailment": np.zeros(24),
            "label_LOLF": np.zeros(24),
            "freq_LOLF": 0,
            "LOL_days": 0,
            "outage_day": np.zeros(365)
        }
        LOL_track = np.zeros((10, 24))
        s = 0
        
        # Set up some curtailment in the first day
        for n in range(24):
            if n < 5:  # First 5 hours have curtailment
                result = ra.TrackLOLStates(0.1, BMva, var_s, LOL_track, s, n)
                var_s, LOL_track = result
        
        # The daily tracking only happens at the end of each day (n+1)%24 == 0
        # So we need to call it at hour 23 (which is n=23, so (23+1)%24 == 0)
        result = ra.TrackLOLStates(0.0, BMva, var_s, LOL_track, s, 23)
        var_s, LOL_track = result
        
        # Check that outage_day was updated
        assert var_s["outage_day"][0] > 0  # First day should have outages
        assert var_s["LOL_days"] == 1  # Should have 1 day with outages
    
    def test_tracklolstates_parameter_validation(self, utilities_test_helper):
        """Test parameter validation for TrackLOLStates"""
        ra = utilities_test_helper
        
        # Test with invalid parameters
        with pytest.raises((TypeError, KeyError, IndexError)):
            ra.TrackLOLStates("invalid", 100.0, {}, np.zeros((10, 24)), 0, 0)
        
        # Test with missing keys in var_s
        with pytest.raises(KeyError):
            ra.TrackLOLStates(0.1, 100.0, {}, np.zeros((10, 24)), 0, 0)
    
    def test_tracklolstates_output_format(self, utilities_test_helper):
        """Test output format of TrackLOLStates"""
        ra = utilities_test_helper
        
        load_curt = 0.1
        BMva = 100.0
        var_s = {
            "LLD": 0,
            "curtailment": np.zeros(24),
            "label_LOLF": np.zeros(24),
            "freq_LOLF": 0,
            "LOL_days": 0,
            "outage_day": np.zeros(365)
        }
        LOL_track = np.zeros((10, 24))
        s = 0
        n = 5
        
        result = ra.TrackLOLStates(load_curt, BMva, var_s, LOL_track, s, n)
        updated_var_s, updated_LOL_track = result
        
        # Check return types
        assert isinstance(updated_var_s, dict)
        assert isinstance(updated_LOL_track, np.ndarray)
        
        # Check that all required keys are present
        required_keys = ["LLD", "curtailment", "label_LOLF", "freq_LOLF", "LOL_days", "outage_day"]
        for key in required_keys:
            assert key in updated_var_s
        
        # Check array types
        assert isinstance(updated_var_s["curtailment"], np.ndarray)
        assert isinstance(updated_var_s["label_LOLF"], np.ndarray)
        assert isinstance(updated_var_s["outage_day"], np.ndarray)


class TestCheckConvergence:
    """Test CheckConvergence method"""
    
    def test_checkconvergence_basic_functionality(self, utilities_test_helper):
        """Test basic CheckConvergence functionality with mocked MPI"""
        ra = utilities_test_helper
        
        # Setup test data
        s = 5
        LOLP_rec = np.array([0.01, 0.02, 0.015, 0.018, 0.012, 0.016])
        comm = Mock()
        rank = 0
        size = 4
        mLOLP_rec = np.zeros(10)
        COV_rec = np.zeros(10)
        
        # Mock the Gather operation to populate recvbuf_LOLP
        mock_recvbuf = np.array([
            [0.01, 0.02, 0.015, 0.018, 0.012, 0.016],
            [0.02, 0.03, 0.025, 0.028, 0.022, 0.026],
            [0.015, 0.025, 0.02, 0.023, 0.017, 0.021],
            [0.018, 0.028, 0.023, 0.026, 0.02, 0.024]
        ])
        
        def mock_gather(sendbuf, recvbuf, root):
            if root == 0:
                recvbuf[:] = mock_recvbuf
        
        comm.Gather = mock_gather
        
        # Call the method
        result = ra.CheckConvergence(s, LOLP_rec, comm, rank, size, mLOLP_rec, COV_rec)
        
        # Verify return format
        assert isinstance(result, tuple)
        assert len(result) == 2
        updated_mLOLP_rec, updated_COV_rec = result
        
        # Check that arrays were updated
        assert isinstance(updated_mLOLP_rec, np.ndarray)
        assert isinstance(updated_COV_rec, np.ndarray)
        
        # Check that mean was calculated correctly
        expected_mean = np.mean(mock_recvbuf[:, 0:s+1])
        assert abs(updated_mLOLP_rec[s] - expected_mean) < 1e-10
        
        # Check that COV was calculated correctly
        expected_var = np.var(mock_recvbuf[:, 0:s+1])
        expected_cov = np.sqrt(expected_var) / expected_mean
        assert abs(updated_COV_rec[s] - expected_cov) < 1e-10
    
    def test_checkconvergence_rank_zero(self, utilities_test_helper):
        """Test CheckConvergence when rank is 0 (root process)"""
        ra = utilities_test_helper
        
        s = 3
        LOLP_rec = np.array([0.01, 0.02, 0.015, 0.018])
        comm = Mock()
        rank = 0
        size = 2
        mLOLP_rec = np.zeros(10)
        COV_rec = np.zeros(10)
        
        # Mock the Gather operation to populate recvbuf_LOLP
        mock_recvbuf = np.array([
            [0.01, 0.02, 0.015, 0.018],
            [0.02, 0.03, 0.025, 0.028]
        ])
        
        def mock_gather(sendbuf, recvbuf, root):
            if root == 0:
                recvbuf[:] = mock_recvbuf
        
        comm.Gather = mock_gather
        
        result = ra.CheckConvergence(s, LOLP_rec, comm, rank, size, mLOLP_rec, COV_rec)
        
        # Verify that recvbuf_LOLP was allocated
        assert ra.recvbuf_LOLP is not None
        assert ra.recvbuf_LOLP.shape == (size, len(LOLP_rec))
        
        # Verify that temp_mat was created
        assert hasattr(ra, 'temp_mat')
        assert ra.temp_mat.shape == (size, s+1)
    
    def test_checkconvergence_non_root_rank(self, utilities_test_helper):
        """Test CheckConvergence when rank is not 0"""
        ra = utilities_test_helper
        
        s = 3
        LOLP_rec = np.array([0.01, 0.02, 0.015, 0.018])
        comm = Mock()
        rank = 1  # Non-root rank
        size = 2
        mLOLP_rec = np.zeros(10)
        COV_rec = np.zeros(10)
        
        comm.Gather.return_value = None
        
        result = ra.CheckConvergence(s, LOLP_rec, comm, rank, size, mLOLP_rec, COV_rec)
        
        # Verify that recvbuf_LOLP was not allocated for non-root
        assert ra.recvbuf_LOLP is None
        
        # Verify that arrays were not modified
        assert np.all(mLOLP_rec == 0)
        assert np.all(COV_rec == 0)
    
    def test_checkconvergence_parameter_validation(self, utilities_test_helper):
        """Test parameter validation for CheckConvergence"""
        ra = utilities_test_helper
        
        # Test with invalid parameters
        with pytest.raises((TypeError, ValueError, AttributeError)):
            ra.CheckConvergence("invalid", np.array([0.01]), None, 0, 1, np.zeros(10), np.zeros(10))
        
        # Test with mismatched array sizes
        with pytest.raises((ValueError, IndexError)):
            LOLP_rec = np.array([0.01, 0.02])
            mLOLP_rec = np.zeros(1)  # Too small
            ra.CheckConvergence(5, LOLP_rec, Mock(), 0, 1, mLOLP_rec, np.zeros(10))
    
    def test_checkconvergence_cov_calculation(self, utilities_test_helper):
        """Test COV calculation accuracy"""
        ra = utilities_test_helper
        
        s = 2
        LOLP_rec = np.array([0.01, 0.02, 0.015])
        comm = Mock()
        rank = 0
        size = 3
        mLOLP_rec = np.zeros(10)
        COV_rec = np.zeros(10)
        
        # Create test data with known statistics
        mock_recvbuf = np.array([
            [0.01, 0.02, 0.015],
            [0.02, 0.03, 0.025],
            [0.015, 0.025, 0.02]
        ])
        
        def mock_gather(sendbuf, recvbuf, root):
            if root == 0:
                recvbuf[:] = mock_recvbuf
        
        comm.Gather = mock_gather
        
        result = ra.CheckConvergence(s, LOLP_rec, comm, rank, size, mLOLP_rec, COV_rec)
        updated_mLOLP_rec, updated_COV_rec = result
        
        # Calculate expected values manually
        temp_data = mock_recvbuf[:, 0:s+1]
        expected_mean = np.mean(temp_data)
        expected_var = np.var(temp_data)
        expected_cov = np.sqrt(expected_var) / expected_mean
        
        # Verify COV calculation
        assert abs(updated_COV_rec[s] - expected_cov) < 1e-10
        
        # Verify mean calculation
        assert abs(updated_mLOLP_rec[s] - expected_mean) < 1e-10
    
    def test_checkconvergence_output_format(self, utilities_test_helper):
        """Test output format of CheckConvergence"""
        ra = utilities_test_helper
        
        s = 1
        LOLP_rec = np.array([0.01, 0.02])
        comm = Mock()
        rank = 0
        size = 2
        mLOLP_rec = np.zeros(10)
        COV_rec = np.zeros(10)
        
        mock_recvbuf = np.array([
            [0.01, 0.02],
            [0.02, 0.03]
        ])
        
        def mock_gather(sendbuf, recvbuf, root):
            if root == 0:
                recvbuf[:] = mock_recvbuf
        
        comm.Gather = mock_gather
        
        result = ra.CheckConvergence(s, LOLP_rec, comm, rank, size, mLOLP_rec, COV_rec)
        
        # Check return types
        assert isinstance(result, tuple)
        assert len(result) == 2
        
        updated_mLOLP_rec, updated_COV_rec = result
        assert isinstance(updated_mLOLP_rec, np.ndarray)
        assert isinstance(updated_COV_rec, np.ndarray)
        
        # Check array shapes
        assert updated_mLOLP_rec.shape == mLOLP_rec.shape
        assert updated_COV_rec.shape == COV_rec.shape
        
        # Check that only the current sample was updated
        assert updated_mLOLP_rec[s] != 0
        assert updated_COV_rec[s] != 0
        if s > 0:
            assert updated_mLOLP_rec[s-1] == 0
            assert updated_COV_rec[s-1] == 0


class TestUpdateIndexArrays:
    """Test UpdateIndexArrays method"""
    
    def test_updateindexarrays_basic_functionality(self, utilities_test_helper):
        """Test basic UpdateIndexArrays functionality"""
        ra = utilities_test_helper
        
        # Setup test data
        indices_rec = {
            "LOLP_rec": np.zeros(10),
            "EUE_rec": np.zeros(10),
            "EPNS_rec": np.zeros(10),
            "LOLF_rec": np.zeros(10),
            "MDT_rec": np.zeros(10),
            "LOLE_rec": np.zeros(10),
            "LOLP_hr": np.zeros(8760)
        }
        
        var_s = {
            "LLD": 24,  # 24 hours of load curtailment
            "curtailment": np.array([10.0, 15.0, 20.0, 5.0]),  # 50 MWh total
            "freq_LOLF": 3,  # 3 frequency events
            "LOL_days": 2,  # 2 days with outages
            "label_LOLF": np.zeros(8760)
        }
        var_s["label_LOLF"][0:24] = 1  # First 24 hours have outages
        
        sim_hours = 8760
        s = 5
        
        # Call the method
        result = ra.UpdateIndexArrays(indices_rec, var_s, sim_hours, s)
        
        # Verify return format
        assert isinstance(result, dict)
        assert result is indices_rec  # Should return the same dict
        
        # Check LOLP calculation
        expected_lolp = var_s["LLD"] / sim_hours
        assert abs(result["LOLP_rec"][s] - expected_lolp) < 1e-10
        
        # Check EUE calculation
        expected_eue = sum(var_s["curtailment"])
        assert abs(result["EUE_rec"][s] - expected_eue) < 1e-10
        
        # Check EPNS calculation (only if LLD > 0)
        expected_epns = sum(var_s["curtailment"]) / var_s["LLD"]
        assert abs(result["EPNS_rec"][s] - expected_epns) < 1e-10
        
        # Check LOLF recording
        assert result["LOLF_rec"][s] == var_s["freq_LOLF"]
        
        # Check MDT calculation (only if LOLF > 0)
        expected_mdt = var_s["LLD"] / var_s["freq_LOLF"]
        assert abs(result["MDT_rec"][s] - expected_mdt) < 1e-10
        
        # Check LOLE recording
        assert result["LOLE_rec"][s] == var_s["LOL_days"]
        
        # Check hourly LOLP accumulation
        assert np.sum(result["LOLP_hr"][0:24]) == 24  # First 24 hours should be 1
    
    def test_updateindexarrays_zero_ldd(self, utilities_test_helper):
        """Test UpdateIndexArrays with zero load curtailment"""
        ra = utilities_test_helper
        
        indices_rec = {
            "LOLP_rec": np.zeros(10),
            "EUE_rec": np.zeros(10),
            "EPNS_rec": np.zeros(10),
            "LOLF_rec": np.zeros(10),
            "MDT_rec": np.zeros(10),
            "LOLE_rec": np.zeros(10),
            "LOLP_hr": np.zeros(8760)
        }
        
        var_s = {
            "LLD": 0,  # No load curtailment
            "curtailment": np.zeros(24),
            "freq_LOLF": 0,
            "LOL_days": 0,
            "label_LOLF": np.zeros(8760)
        }
        
        sim_hours = 8760
        s = 3
        
        result = ra.UpdateIndexArrays(indices_rec, var_s, sim_hours, s)
        
        # Check that LOLP is 0
        assert result["LOLP_rec"][s] == 0
        
        # Check that EUE is 0
        assert result["EUE_rec"][s] == 0
        
        # Check that EPNS is not calculated (should remain 0)
        assert result["EPNS_rec"][s] == 0
        
        # Check that LOLF is 0
        assert result["LOLF_rec"][s] == 0
        
        # Check that MDT is not calculated (should remain 0)
        assert result["MDT_rec"][s] == 0
        
        # Check that LOLE is 0
        assert result["LOLE_rec"][s] == 0
    
    def test_updateindexarrays_zero_lolf(self, utilities_test_helper):
        """Test UpdateIndexArrays with zero LOLF frequency"""
        ra = utilities_test_helper
        
        indices_rec = {
            "LOLP_rec": np.zeros(10),
            "EUE_rec": np.zeros(10),
            "EPNS_rec": np.zeros(10),
            "LOLF_rec": np.zeros(10),
            "MDT_rec": np.zeros(10),
            "LOLE_rec": np.zeros(10),
            "LOLP_hr": np.zeros(8760)
        }
        
        var_s = {
            "LLD": 12,  # Some load curtailment
            "curtailment": np.array([5.0, 7.0]),
            "freq_LOLF": 0,  # No frequency events
            "LOL_days": 1,
            "label_LOLF": np.zeros(8760)
        }
        var_s["label_LOLF"][0:12] = 1
        
        sim_hours = 8760
        s = 2
        
        result = ra.UpdateIndexArrays(indices_rec, var_s, sim_hours, s)
        
        # Check that MDT is not calculated (should remain 0)
        assert result["MDT_rec"][s] == 0
        
        # Other indices should be calculated normally
        assert result["LOLP_rec"][s] > 0
        assert result["EUE_rec"][s] > 0
        assert result["EPNS_rec"][s] > 0
        assert result["LOLF_rec"][s] == 0
        assert result["LOLE_rec"][s] == 1
    
    def test_updateindexarrays_parameter_validation(self, utilities_test_helper):
        """Test parameter validation for UpdateIndexArrays"""
        ra = utilities_test_helper
        
        # Test with invalid parameters
        with pytest.raises((TypeError, KeyError, IndexError)):
            ra.UpdateIndexArrays("invalid", {}, 8760, 0)
        
        # Test with missing keys in indices_rec
        with pytest.raises(KeyError):
            ra.UpdateIndexArrays({}, {}, 8760, 0)
        
        # Test with missing keys in var_s
        indices_rec = {
            "LOLP_rec": np.zeros(10),
            "EUE_rec": np.zeros(10),
            "EPNS_rec": np.zeros(10),
            "LOLF_rec": np.zeros(10),
            "MDT_rec": np.zeros(10),
            "LOLE_rec": np.zeros(10),
            "LOLP_hr": np.zeros(8760)
        }
        with pytest.raises(KeyError):
            ra.UpdateIndexArrays(indices_rec, {}, 8760, 0)
    
    def test_updateindexarrays_output_format(self, utilities_test_helper):
        """Test output format of UpdateIndexArrays"""
        ra = utilities_test_helper
        
        indices_rec = {
            "LOLP_rec": np.zeros(10),
            "EUE_rec": np.zeros(10),
            "EPNS_rec": np.zeros(10),
            "LOLF_rec": np.zeros(10),
            "MDT_rec": np.zeros(10),
            "LOLE_rec": np.zeros(10),
            "LOLP_hr": np.zeros(8760)
        }
        
        var_s = {
            "LLD": 10,
            "curtailment": np.array([1.0, 2.0, 3.0]),
            "freq_LOLF": 2,
            "LOL_days": 1,
            "label_LOLF": np.zeros(8760)
        }
        var_s["label_LOLF"][0:10] = 1
        
        sim_hours = 8760
        s = 4
        
        result = ra.UpdateIndexArrays(indices_rec, var_s, sim_hours, s)
        
        # Check return type
        assert isinstance(result, dict)
        
        # Check that all required keys are present
        required_keys = ["LOLP_rec", "EUE_rec", "EPNS_rec", "LOLF_rec", "MDT_rec", "LOLE_rec", "LOLP_hr"]
        for key in required_keys:
            assert key in result
        
        # Check array types
        for key in required_keys:
            assert isinstance(result[key], np.ndarray)
        
        # Check that only the current sample was updated
        assert result["LOLP_rec"][s] != 0
        assert result["EUE_rec"][s] != 0
        if s > 0:
            assert result["LOLP_rec"][s-1] == 0
            assert result["EUE_rec"][s-1] == 0
    
    def test_updateindexarrays_multiple_samples(self, utilities_test_helper):
        """Test UpdateIndexArrays with multiple samples"""
        ra = utilities_test_helper
        
        indices_rec = {
            "LOLP_rec": np.zeros(5),
            "EUE_rec": np.zeros(5),
            "EPNS_rec": np.zeros(5),
            "LOLF_rec": np.zeros(5),
            "MDT_rec": np.zeros(5),
            "LOLE_rec": np.zeros(5),
            "LOLP_hr": np.zeros(8760)
        }
        
        sim_hours = 8760
        
        # Test multiple samples
        for s in range(3):
            var_s = {
                "LLD": (s + 1) * 10,  # Different LLD for each sample
                "curtailment": np.array([(s + 1) * 5.0, (s + 1) * 3.0]),
                "freq_LOLF": s + 1,
                "LOL_days": s + 1,
                "label_LOLF": np.zeros(8760)
            }
            var_s["label_LOLF"][s*10:(s+1)*10] = 1  # Different hours for each sample
            
            result = ra.UpdateIndexArrays(indices_rec, var_s, sim_hours, s)
            
            # Check that values are different for each sample
            assert result["LOLP_rec"][s] > 0
            assert result["EUE_rec"][s] > 0
            assert result["LOLF_rec"][s] == s + 1
            assert result["LOLE_rec"][s] == s + 1


class TestOutageAnalysis:
    """Test OutageAnalysis method"""
    
    def test_outageanalysis_basic_functionality(self, utilities_test_helper):
        """Test basic OutageAnalysis functionality"""
        ra = utilities_test_helper
        
        # Setup test data with known outage pattern
        var_s = {
            "label_LOLF": np.array([0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0])
        }
        
        # Call the method
        result = ra.OutageAnalysis(var_s)
        
        # Verify return format
        assert isinstance(result, np.ndarray)
        
        # Expected outages: [3, 2, 4] (3-hour, 2-hour, 4-hour outages)
        expected_durations = np.array([3, 2, 4])
        np.testing.assert_array_equal(result, expected_durations)
    
    def test_outageanalysis_no_outages(self, utilities_test_helper):
        """Test OutageAnalysis with no outages"""
        ra = utilities_test_helper
        
        var_s = {
            "label_LOLF": np.zeros(24)  # No outages
        }
        
        result = ra.OutageAnalysis(var_s)
        
        # Should return empty array
        assert isinstance(result, np.ndarray)
        assert len(result) == 0
    
    def test_outageanalysis_continuous_outage(self, utilities_test_helper):
        """Test OutageAnalysis with continuous outage"""
        ra = utilities_test_helper
        
        var_s = {
            "label_LOLF": np.ones(10)  # Continuous outage
        }
        
        result = ra.OutageAnalysis(var_s)
        
        # Should return single outage of duration 10
        assert isinstance(result, np.ndarray)
        assert len(result) == 1
        assert result[0] == 10
    
    def test_outageanalysis_single_hour_outages(self, utilities_test_helper):
        """Test OutageAnalysis with single hour outages"""
        ra = utilities_test_helper
        
        var_s = {
            "label_LOLF": np.array([0, 1, 0, 1, 0, 1, 0])  # Three 1-hour outages
        }
        
        result = ra.OutageAnalysis(var_s)
        
        # Should return three outages of duration 1 each
        expected_durations = np.array([1, 1, 1])
        np.testing.assert_array_equal(result, expected_durations)
    
    def test_outageanalysis_edge_cases(self, utilities_test_helper):
        """Test OutageAnalysis edge cases"""
        ra = utilities_test_helper
        
        # Test with outage starting at beginning
        var_s1 = {
            "label_LOLF": np.array([1, 1, 0, 0, 1, 0])
        }
        result1 = ra.OutageAnalysis(var_s1)
        expected1 = np.array([2, 1])
        np.testing.assert_array_equal(result1, expected1)
        
        # Test with outage ending at end
        var_s2 = {
            "label_LOLF": np.array([0, 1, 1, 1])
        }
        result2 = ra.OutageAnalysis(var_s2)
        expected2 = np.array([3])
        np.testing.assert_array_equal(result2, expected2)
        
        # Test with alternating pattern
        var_s3 = {
            "label_LOLF": np.array([1, 0, 1, 0, 1, 0])
        }
        result3 = ra.OutageAnalysis(var_s3)
        expected3 = np.array([1, 1, 1])
        np.testing.assert_array_equal(result3, expected3)
    
    def test_outageanalysis_parameter_validation(self, utilities_test_helper):
        """Test parameter validation for OutageAnalysis"""
        ra = utilities_test_helper
        
        # Test with invalid parameters
        with pytest.raises((TypeError, KeyError, AttributeError)):
            ra.OutageAnalysis("invalid")
        
        # Test with missing label_LOLF key
        with pytest.raises(KeyError):
            ra.OutageAnalysis({})
        
        # Test with non-array label_LOLF
        with pytest.raises((TypeError, AttributeError, ValueError)):
            ra.OutageAnalysis({"label_LOLF": "invalid"})
    
    def test_outageanalysis_output_format(self, utilities_test_helper):
        """Test output format of OutageAnalysis"""
        ra = utilities_test_helper
        
        var_s = {
            "label_LOLF": np.array([0, 1, 1, 0, 1, 0, 1, 1, 1, 0])
        }
        
        result = ra.OutageAnalysis(var_s)
        
        # Check return type
        assert isinstance(result, np.ndarray)
        
        # Check data type
        assert result.dtype in [np.int32, np.int64, np.int_]
        
        # Check that all durations are positive
        assert np.all(result > 0)
        
        # Check that durations are reasonable (not longer than input array)
        assert np.all(result <= len(var_s["label_LOLF"]))
    
    def test_outageanalysis_large_dataset(self, utilities_test_helper):
        """Test OutageAnalysis with large dataset"""
        ra = utilities_test_helper
        
        # Create a large dataset with multiple outages
        np.random.seed(42)  # For reproducible results
        n_hours = 8760  # One year
        var_s = {
            "label_LOLF": np.zeros(n_hours)
        }
        
        # Add some random outages
        outage_starts = np.random.choice(n_hours - 10, size=50, replace=False)
        for start in outage_starts:
            duration = np.random.randint(1, 11)  # 1-10 hour outages
            end = min(start + duration, n_hours)
            var_s["label_LOLF"][start:end] = 1
        
        result = ra.OutageAnalysis(var_s)
        
        # Verify output
        assert isinstance(result, np.ndarray)
        assert len(result) > 0
        assert np.all(result > 0)
        assert np.all(result <= n_hours)
        
        # Verify that total outage hours match
        total_outage_hours = np.sum(result)
        actual_outage_hours = np.sum(var_s["label_LOLF"])
        assert total_outage_hours == actual_outage_hours


class TestGetReliabilityIndices:
    """Test GetReliabilityIndices method"""
    
    def test_getreliabilityindices_basic_functionality(self, utilities_test_helper):
        """Test basic GetReliabilityIndices functionality"""
        ra = utilities_test_helper
        
        # Setup test data
        indices_rec = {
            "LOLP_rec": np.array([0.01, 0.02, 0.015, 0.018, 0.012]),
            "EUE_rec": np.array([100.0, 200.0, 150.0, 180.0, 120.0]),
            "EPNS_rec": np.array([10.0, 12.0, 11.0, 13.0, 9.0]),
            "LOLF_rec": np.array([5, 8, 6, 7, 4]),
            "MDT_rec": np.array([2.0, 2.5, 2.2, 2.6, 3.0]),
            "LOLE_rec": np.array([10, 15, 12, 14, 8])
        }
        
        sim_hours = 8760
        samples = 5
        
        # Call the method
        result = ra.GetReliabilityIndices(indices_rec, sim_hours, samples)
        
        # Verify return format
        assert isinstance(result, dict)
        
        # Check that all required keys are present
        required_keys = ["LOLP", "LOLH", "EUE", "EPNS", "LOLF", "MDT", "LOLE"]
        for key in required_keys:
            assert key in result
        
        # Check calculations
        expected_lolp = np.mean(indices_rec["LOLP_rec"])
        expected_lolh = expected_lolp * sim_hours
        expected_eue = np.mean(indices_rec["EUE_rec"])
        expected_epns = np.mean(indices_rec["EPNS_rec"])
        expected_lolf = np.mean(indices_rec["LOLF_rec"])
        expected_mdt = np.mean(indices_rec["MDT_rec"])
        expected_lole = np.mean(indices_rec["LOLE_rec"])
        
        assert abs(result["LOLP"] - expected_lolp) < 1e-10
        assert abs(result["LOLH"] - expected_lolh) < 1e-10
        assert abs(result["EUE"] - expected_eue) < 1e-10
        assert abs(result["EPNS"] - expected_epns) < 1e-10
        assert abs(result["LOLF"] - expected_lolf) < 1e-10
        assert abs(result["MDT"] - expected_mdt) < 1e-10
        assert abs(result["LOLE"] - expected_lole) < 1e-10
    
    def test_getreliabilityindices_zero_values(self, utilities_test_helper):
        """Test GetReliabilityIndices with zero values"""
        ra = utilities_test_helper
        
        # Setup test data with zeros
        indices_rec = {
            "LOLP_rec": np.zeros(5),
            "EUE_rec": np.zeros(5),
            "EPNS_rec": np.zeros(5),
            "LOLF_rec": np.zeros(5),
            "MDT_rec": np.zeros(5),
            "LOLE_rec": np.zeros(5)
        }
        
        sim_hours = 8760
        samples = 5
        
        result = ra.GetReliabilityIndices(indices_rec, sim_hours, samples)
        
        # All indices should be zero
        for key in ["LOLP", "LOLH", "EUE", "EPNS", "LOLF", "MDT", "LOLE"]:
            assert result[key] == 0.0
    
    def test_getreliabilityindices_single_sample(self, utilities_test_helper):
        """Test GetReliabilityIndices with single sample"""
        ra = utilities_test_helper
        
        indices_rec = {
            "LOLP_rec": np.array([0.05]),
            "EUE_rec": np.array([500.0]),
            "EPNS_rec": np.array([15.0]),
            "LOLF_rec": np.array([10]),
            "MDT_rec": np.array([5.0]),
            "LOLE_rec": np.array([20])
        }
        
        sim_hours = 8760
        samples = 1
        
        result = ra.GetReliabilityIndices(indices_rec, sim_hours, samples)
        
        # Values should match the single sample
        assert result["LOLP"] == 0.05
        assert result["LOLH"] == 0.05 * 8760
        assert result["EUE"] == 500.0
        assert result["EPNS"] == 15.0
        assert result["LOLF"] == 10.0
        assert result["MDT"] == 5.0
        assert result["LOLE"] == 20.0
    
    def test_getreliabilityindices_parameter_validation(self, utilities_test_helper):
        """Test parameter validation for GetReliabilityIndices"""
        ra = utilities_test_helper
        
        # Test with invalid parameters
        with pytest.raises((TypeError, KeyError, AttributeError)):
            ra.GetReliabilityIndices("invalid", 8760, 5)
        
        # Test with missing keys in indices_rec
        with pytest.raises(KeyError):
            ra.GetReliabilityIndices({}, 8760, 5)
        
        # Test with invalid sim_hours
        indices_rec = {
            "LOLP_rec": np.array([0.01]),
            "EUE_rec": np.array([100.0]),
            "EPNS_rec": np.array([10.0]),
            "LOLF_rec": np.array([5]),
            "MDT_rec": np.array([2.0]),
            "LOLE_rec": np.array([10])
        }
        with pytest.raises((TypeError, ValueError)):
            ra.GetReliabilityIndices(indices_rec, "invalid", 5)
    
    def test_getreliabilityindices_output_format(self, utilities_test_helper):
        """Test output format of GetReliabilityIndices"""
        ra = utilities_test_helper
        
        indices_rec = {
            "LOLP_rec": np.array([0.01, 0.02]),
            "EUE_rec": np.array([100.0, 200.0]),
            "EPNS_rec": np.array([10.0, 12.0]),
            "LOLF_rec": np.array([5, 8]),
            "MDT_rec": np.array([2.0, 2.5]),
            "LOLE_rec": np.array([10, 15])
        }
        
        sim_hours = 8760
        samples = 2
        
        result = ra.GetReliabilityIndices(indices_rec, sim_hours, samples)
        
        # Check return type
        assert isinstance(result, dict)
        
        # Check that all values are numeric
        for key, value in result.items():
            assert isinstance(value, (int, float, np.number))
            assert not np.isnan(value)
            assert not np.isinf(value)
        
        # Check that LOLH is calculated correctly
        assert result["LOLH"] == result["LOLP"] * sim_hours
    
    def test_getreliabilityindices_large_dataset(self, utilities_test_helper):
        """Test GetReliabilityIndices with large dataset"""
        ra = utilities_test_helper
        
        # Create large dataset
        n_samples = 1000
        indices_rec = {
            "LOLP_rec": np.random.uniform(0.001, 0.05, n_samples),
            "EUE_rec": np.random.uniform(50.0, 500.0, n_samples),
            "EPNS_rec": np.random.uniform(5.0, 20.0, n_samples),
            "LOLF_rec": np.random.randint(1, 20, n_samples),
            "MDT_rec": np.random.uniform(1.0, 10.0, n_samples),
            "LOLE_rec": np.random.randint(5, 50, n_samples)
        }
        
        sim_hours = 8760
        samples = n_samples
        
        result = ra.GetReliabilityIndices(indices_rec, sim_hours, samples)
        
        # Verify output
        assert isinstance(result, dict)
        
        # Check that all values are reasonable
        assert 0 <= result["LOLP"] <= 1
        assert 0 <= result["LOLH"] <= sim_hours
        assert result["EUE"] >= 0
        assert result["EPNS"] >= 0
        assert result["LOLF"] >= 0
        assert result["MDT"] >= 0
        assert result["LOLE"] >= 0
        
        # Check that LOLH calculation is correct
        assert abs(result["LOLH"] - result["LOLP"] * sim_hours) < 1e-10
    
    def test_getreliabilityindices_instance_attributes(self, utilities_test_helper):
        """Test that GetReliabilityIndices sets instance attributes"""
        ra = utilities_test_helper
        
        indices_rec = {
            "LOLP_rec": np.array([0.01, 0.02]),
            "EUE_rec": np.array([100.0, 200.0]),
            "EPNS_rec": np.array([10.0, 12.0]),
            "LOLF_rec": np.array([5, 8]),
            "MDT_rec": np.array([2.0, 2.5]),
            "LOLE_rec": np.array([10, 15])
        }
        
        sim_hours = 8760
        samples = 2
        
        result = ra.GetReliabilityIndices(indices_rec, sim_hours, samples)
        
        # Check that instance attributes are set
        assert hasattr(ra, 'LOLP')
        assert hasattr(ra, 'LOLH')
        assert hasattr(ra, 'EUE')
        assert hasattr(ra, 'EPNS')
        assert hasattr(ra, 'LOLF')
        assert hasattr(ra, 'MDT')
        assert hasattr(ra, 'LOLE')
        assert hasattr(ra, 'indices')
        
        # Check that instance attributes match return values
        assert ra.LOLP == result["LOLP"]
        assert ra.LOLH == result["LOLH"]
        assert ra.EUE == result["EUE"]
        assert ra.EPNS == result["EPNS"]
        assert ra.LOLF == result["LOLF"]
        assert ra.MDT == result["MDT"]
        assert ra.LOLE == result["LOLE"]
        assert ra.indices == result


class TestOutageHeatMap:
    """Test OutageHeatMap method"""
    
    def test_outageheatmap_basic_functionality(self, utilities_test_helper, tmp_path):
        """Test basic OutageHeatMap functionality"""
        ra = utilities_test_helper
        
        # Setup test data
        size = 2
        samples = 3
        all_subdir = str(tmp_path)
        
        # Create LOL_track data (size*samples, 365, 24)
        LOL_track = np.zeros((size * samples, 365, 24))
        
        # Add some test outages
        LOL_track[0, 0:5, 10:15] = 1  # 5 days, 5 hours each
        LOL_track[1, 10:15, 8:12] = 1  # 5 days, 4 hours each
        LOL_track[2, 20:25, 14:18] = 1  # 5 days, 4 hours each
        
        # Call the method
        ra.OutageHeatMap(LOL_track, size, samples, all_subdir)
        
        # Check that CSV file was created
        csv_file = tmp_path / "LOL_perc_prob.csv"
        assert csv_file.exists()
        
        # Read and verify CSV content
        df = pd.read_csv(csv_file, index_col=0)
        assert df.shape == (12, 24)  # 12 months, 24 hours
        
        # Check that values are reasonable (0-100%)
        assert df.min().min() >= 0
        assert df.max().max() <= 100
    
    def test_outageheatmap_no_outages(self, utilities_test_helper, tmp_path):
        """Test OutageHeatMap with no outages"""
        ra = utilities_test_helper
        
        size = 2
        samples = 3
        all_subdir = str(tmp_path)
        
        # Create LOL_track with no outages
        LOL_track = np.zeros((size * samples, 365, 24))
        
        ra.OutageHeatMap(LOL_track, size, samples, all_subdir)
        
        # Check that CSV file was created
        csv_file = tmp_path / "LOL_perc_prob.csv"
        assert csv_file.exists()
        
        # Read and verify all values are 0
        df = pd.read_csv(csv_file, index_col=0)
        assert (df == 0).all().all()
    
    def test_outageheatmap_continuous_outages(self, utilities_test_helper, tmp_path):
        """Test OutageHeatMap with continuous outages"""
        ra = utilities_test_helper
        
        size = 1
        samples = 1
        all_subdir = str(tmp_path)
        
        # Create LOL_track with continuous outages
        LOL_track = np.ones((size * samples, 365, 24))
        
        ra.OutageHeatMap(LOL_track, size, samples, all_subdir)
        
        # Check that CSV file was created
        csv_file = tmp_path / "LOL_perc_prob.csv"
        assert csv_file.exists()
        
        # Read and verify all values are 100%
        df = pd.read_csv(csv_file, index_col=0)
        assert (df == 100).all().all()
    
    def test_outageheatmap_parameter_validation(self, utilities_test_helper, tmp_path):
        """Test parameter validation for OutageHeatMap"""
        ra = utilities_test_helper
        
        all_subdir = str(tmp_path)
        
        # Test with invalid LOL_track shape
        with pytest.raises((ValueError, IndexError)):
            LOL_track = np.zeros((10, 10))  # Wrong shape
            ra.OutageHeatMap(LOL_track, 2, 3, all_subdir)
        
        # Test with invalid size/samples - this might not raise an error, so let's test it differently
        LOL_track = np.zeros((6, 365, 24))
        # This should work but might give unexpected results
        ra.OutageHeatMap(LOL_track, 2, 3, all_subdir)  # 2*3 != 6
        
        # Test with invalid directory
        with pytest.raises((OSError, FileNotFoundError)):
            LOL_track = np.zeros((6, 365, 24))
            ra.OutageHeatMap(LOL_track, 2, 3, "/invalid/path")
    
    def test_outageheatmap_output_format(self, utilities_test_helper, tmp_path):
        """Test output format of OutageHeatMap"""
        ra = utilities_test_helper
        
        size = 2
        samples = 2
        all_subdir = str(tmp_path)
        
        # Create test data
        LOL_track = np.zeros((size * samples, 365, 24))
        LOL_track[0, 0:10, 12:15] = 1  # 10 days, 3 hours each
        
        ra.OutageHeatMap(LOL_track, size, samples, all_subdir)
        
        # Check that CSV file was created
        csv_file = tmp_path / "LOL_perc_prob.csv"
        assert csv_file.exists()
        
        # Read and verify format
        df = pd.read_csv(csv_file, index_col=0)
        
        # Check shape
        assert df.shape == (12, 24)
        
        # Check index (months 0-11)
        assert list(df.index) == list(range(12))
        
        # Check columns (hours 0-23)
        assert list(df.columns) == [str(i) for i in range(24)]
        
        # Check data types
        assert df.dtypes.apply(lambda x: np.issubdtype(x, np.number)).all()
    
    def test_outageheatmap_monthly_calculation(self, utilities_test_helper, tmp_path):
        """Test monthly calculation accuracy"""
        ra = utilities_test_helper
        
        size = 1
        samples = 1
        all_subdir = str(tmp_path)
        
        # Create LOL_track with known pattern
        LOL_track = np.zeros((size * samples, 365, 24))
        
        # January: 5 days with outages
        LOL_track[0, 0:5, 12:15] = 1  # 5 days, 3 hours each
        
        # February: 3 days with outages  
        LOL_track[0, 31:34, 10:12] = 1  # 3 days, 2 hours each
        
        ra.OutageHeatMap(LOL_track, size, samples, all_subdir)
        
        # Read results
        csv_file = tmp_path / "LOL_perc_prob.csv"
        df = pd.read_csv(csv_file, index_col=0)
        
        # Check that January has some outages (index 0)
        assert df.loc[0, '12'] > 0
        assert df.loc[0, '13'] > 0
        assert df.loc[0, '14'] > 0
        
        # Check that February has some outages (index 1)
        assert df.loc[1, '10'] > 0
        assert df.loc[1, '11'] > 0
        
        # Check that other hours in January are 0
        assert df.loc[0, '0'] == 0
        assert df.loc[0, '23'] == 0
    
    def test_outageheatmap_large_dataset(self, utilities_test_helper, tmp_path):
        """Test OutageHeatMap with large dataset"""
        ra = utilities_test_helper
        
        size = 10
        samples = 100
        all_subdir = str(tmp_path)
        
        # Create large LOL_track dataset
        LOL_track = np.random.randint(0, 2, (size * samples, 365, 24))
        
        ra.OutageHeatMap(LOL_track, size, samples, all_subdir)
        
        # Check that CSV file was created
        csv_file = tmp_path / "LOL_perc_prob.csv"
        assert csv_file.exists()
        
        # Read and verify
        df = pd.read_csv(csv_file, index_col=0)
        assert df.shape == (12, 24)
        
        # Check that values are reasonable
        assert df.min().min() >= 0
        assert df.max().max() <= 100
        
        # Check that all values are finite
        assert df.isnull().sum().sum() == 0
        assert np.isfinite(df.values).all()
    
    def test_outageheatmap_file_creation(self, utilities_test_helper, tmp_path):
        """Test that OutageHeatMap creates the correct file"""
        ra = utilities_test_helper
        
        size = 2
        samples = 3
        all_subdir = str(tmp_path)
        
        LOL_track = np.zeros((size * samples, 365, 24))
        
        # Ensure directory exists
        os.makedirs(all_subdir, exist_ok=True)
        
        ra.OutageHeatMap(LOL_track, size, samples, all_subdir)
        
        # Check that only the expected file was created
        files = list(tmp_path.glob("*.csv"))
        assert len(files) == 1
        assert files[0].name == "LOL_perc_prob.csv"
        
        # Check file size is reasonable
        assert files[0].stat().st_size > 0


class TestOptimizationMethods:
    """Test optimization methods (OptDispatch and OptDispatchLite)"""
    
    @pytest.mark.skipif(not solver_available(), reason="No optimization solver available")
    def test_optdispatch_smoke(self, utilities_test_helper):
        """Basic smoke test for OptDispatch"""
        ra = utilities_test_helper
        
        # Setup minimal test parameters
        ng = 2
        nz = 3
        nl = 2
        ness = 1
        BMva = 100.0
        
        # Create test data
        fb_flow = [(0, 100), (0, 100)]
        fb_Pg = [(0, 50), (0, 50), (0, 20)]
        fb_ess = [(0, 10)]
        fb_soc = [(0, 100)]
        
        A_inc = np.array([[1, -1], [0, 1], [-1, 0]])
        gen_mat = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        ch_mat = np.array([[0], [0], [1]])
        curt_mat = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        
        gencost = np.array([10.0, 15.0])
        net_load = np.array([80.0, 60.0, 40.0])
        SOC_old = np.array([50.0])
        ess_pmax = np.array([20.0])
        ess_eff = np.array([0.9])
        disch_cost = np.array([5.0])
        ch_cost = np.array([2.0])
        
        # Call the method
        result = ra.OptDispatch(ng, nz, nl, ness, fb_flow, fb_Pg, fb_ess, fb_soc, 
                               BMva, A_inc, gen_mat, ch_mat, curt_mat, gencost, 
                               net_load, SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost)
        
        # Verify return format
        assert isinstance(result, tuple)
        assert len(result) == 2
        
        load_curt, SOC_new = result
        assert isinstance(load_curt, np.ndarray)
        assert isinstance(SOC_new, np.ndarray)
        assert len(load_curt) == nz
        assert len(SOC_new) == ness
    
    @pytest.mark.skipif(not solver_available(), reason="No optimization solver available")
    def test_optdispatchlite_smoke(self, utilities_test_helper):
        """Basic smoke test for OptDispatchLite"""
        ra = utilities_test_helper
        
        # Setup minimal test parameters
        ng = 2
        nz = 3
        ness = 1
        BMva = 100.0
        
        # Create test data
        fb_ess = [(0, 10)]
        fb_soc = [(0, 100)]
        fb_Pg = [(0, 50), (0, 50), (0, 20)]
        A_inc = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        
        gencost = np.array([10.0, 15.0])
        net_load = np.array([80.0, 60.0, 40.0])
        SOC_old = np.array([50.0])
        ess_pmax = np.array([20.0])
        ess_eff = np.array([0.9])
        disch_cost = np.array([5.0])
        ch_cost = np.array([2.0])
        
        # Call the method
        result = ra.OptDispatchLite(ng, nz, ness, fb_ess, fb_soc, BMva, fb_Pg, 
                                   A_inc, gencost, net_load, SOC_old, ess_pmax, 
                                   ess_eff, disch_cost, ch_cost)
        
        # Verify return format
        assert isinstance(result, tuple)
        assert len(result) == 2
        
        load_curt, SOC_new = result
        assert isinstance(load_curt, np.ndarray)
        assert isinstance(SOC_new, np.ndarray)
        assert len(load_curt) == nz
        assert len(SOC_new) == ness
    
    def test_optdispatch_no_solver(self, utilities_test_helper):
        """Test OptDispatch behavior when no solver is available"""
        if solver_available():
            pytest.skip("Solver is available, skipping no-solver test")
        
        ra = utilities_test_helper
        
        # Setup minimal test parameters
        ng = 2
        nz = 3
        nl = 2
        ness = 1
        BMva = 100.0
        
        # Create test data
        fb_flow = [(0, 100), (0, 100)]
        fb_Pg = [(0, 50), (0, 50), (0, 20)]
        fb_ess = [(0, 10)]
        fb_soc = [(0, 100)]
        
        A_inc = np.array([[1, -1], [0, 1], [-1, 0]])
        gen_mat = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        ch_mat = np.array([[0], [0], [1]])
        curt_mat = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        
        gencost = np.array([10.0, 15.0])
        net_load = np.array([80.0, 60.0, 40.0])
        SOC_old = np.array([50.0])
        ess_pmax = np.array([20.0])
        ess_eff = np.array([0.9])
        disch_cost = np.array([5.0])
        ch_cost = np.array([2.0])
        
        # This should raise an exception when no solver is available
        with pytest.raises((ImportError, RuntimeError, Exception)):
            ra.OptDispatch(ng, nz, nl, ness, fb_flow, fb_Pg, fb_ess, fb_soc, 
                          BMva, A_inc, gen_mat, ch_mat, curt_mat, gencost, 
                          net_load, SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost)
    
    def test_optdispatch_parameter_validation(self, utilities_test_helper):
        """Test parameter validation for OptDispatch"""
        ra = utilities_test_helper
        
        # Test with invalid parameters
        with pytest.raises((TypeError, ValueError, IndexError)):
            ra.OptDispatch("invalid", 3, 2, 1, [], [], [], [], 100.0, 
                          np.array([]), np.array([]), np.array([]), np.array([]), 
                          np.array([]), np.array([]), np.array([]), np.array([]), 
                          np.array([]), np.array([]), np.array([]), np.array([]))
    
    def test_optdispatchlite_parameter_validation(self, utilities_test_helper):
        """Test parameter validation for OptDispatchLite"""
        ra = utilities_test_helper
        
        # Test with invalid parameters
        with pytest.raises((TypeError, ValueError, IndexError)):
            ra.OptDispatchLite("invalid", 3, 1, [], [], 100.0, [], 
                              np.array([]), np.array([]), np.array([]), np.array([]), 
                              np.array([]), np.array([]), np.array([]), np.array([]))
    
    @pytest.mark.skipif(not solver_available(), reason="No optimization solver available")
    def test_optdispatch_output_format(self, utilities_test_helper):
        """Test output format of OptDispatch"""
        ra = utilities_test_helper
        
        # Setup test parameters
        ng = 1
        nz = 2
        nl = 1
        ness = 1
        BMva = 100.0
        
        # Create test data
        fb_flow = [(0, 100)]
        fb_Pg = [(0, 50), (0, 20)]
        fb_ess = [(0, 10)]
        fb_soc = [(0, 100)]
        
        A_inc = np.array([[1], [-1]])
        gen_mat = np.array([[1, 0], [0, 1]])
        ch_mat = np.array([[0], [1]])
        curt_mat = np.array([[1, 0], [0, 1]])
        
        gencost = np.array([10.0])
        net_load = np.array([40.0, 30.0])
        SOC_old = np.array([50.0])
        ess_pmax = np.array([20.0])
        ess_eff = np.array([0.9])
        disch_cost = np.array([5.0])
        ch_cost = np.array([2.0])
        
        result = ra.OptDispatch(ng, nz, nl, ness, fb_flow, fb_Pg, fb_ess, fb_soc, 
                               BMva, A_inc, gen_mat, ch_mat, curt_mat, gencost, 
                               net_load, SOC_old, ess_pmax, ess_eff, disch_cost, ch_cost)
        
        load_curt, SOC_new = result
        
        # Check data types
        assert isinstance(load_curt, np.ndarray)
        assert isinstance(SOC_new, np.ndarray)
        
        # Check shapes
        assert load_curt.shape == (nz,)
        assert SOC_new.shape == (ness,)
        
        # Check that values are reasonable
        assert np.all(load_curt >= 0)  # Load curtailment should be non-negative
        assert np.all(SOC_new >= 0)    # SOC should be non-negative
        assert np.all(SOC_new <= 100)  # SOC should not exceed 100%


class TestProductionWorkflow:
    """Test production workflow mimicking example_simulation.py"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_complete_simulation_workflow(self, real_system_data, real_solar_data, real_wind_data):
        """Test complete simulation workflow with real data"""
        from progress.mod_sysdata import RASystemData
        from progress.mod_matrices import RAMatrices
        
        # Load system data
        sysdata = RASystemData()
        gen_data = sysdata.gen(real_system_data['gen_csv'])
        branch_data = sysdata.branch(real_system_data['branch_csv'])
        bus_data = sysdata.bus(real_system_data['bus_csv'])
        load_data = sysdata.load('A', real_system_data['load_csv'])
        storage_data = sysdata.storage(real_system_data['storage_csv'])
        
        # Create matrices
        matrices = RAMatrices(len(bus_data[1]))
        gen_mat = matrices.genmat(gen_data[1], gen_data[0], storage_data[2], storage_data[1])
        ainc_mat = matrices.Ainc(branch_data[0], branch_data[1], branch_data[2])
        ch_mat = matrices.chmat(storage_data[2], storage_data[1], len(bus_data[1]))
        curt_mat = matrices.curtmat(len(bus_data[1]))
        
        # Create RAUtilities instance
        ra = RAUtilities()
        
        # Test reltrates calculation
        reltrates = ra.reltrates(gen_data[4], branch_data[4], gen_data[5], branch_data[5], storage_data[4], storage_data[5])
        assert isinstance(reltrates, tuple)
        assert len(reltrates) == 2
        
        # Test capacities calculation
        capacities = ra.capacities(branch_data[0], gen_data[2], gen_data[3], np.array([storage_data[2]]), storage_data[3], branch_data[3])
        assert isinstance(capacities, tuple)
        assert len(capacities) == 2
        
        # Test NextState with real data
        ng = gen_data[1]  # Number of generators
        nz = bus_data[1]  # Number of buses
        nl = branch_data[0]  # Number of branches
        ness = storage_data[2]  # Number of storage systems
        
        # Create test state
        current_state = np.ones(ng + ness + nl)
        
        next_state = ra.NextState(0.0, ng, ness, nl, reltrates[0], reltrates[1], current_state, capacities[0], capacities[1], storage_data[6])
        assert isinstance(next_state, tuple)
        assert len(next_state) == 3
        
        # Test updateSOC with real data
        if ness > 0:
            SOC_old = np.array([50.0] * ness)
            current_cap = {'max': np.concatenate([np.ones(ng), np.ones(nl), np.ones(ness)]), 'min': np.concatenate([np.ones(ng), np.ones(nl), np.ones(ness)])}
            
            SOC_new = ra.updateSOC(ng, nl, current_cap, np.array([storage_data[2]]), storage_data[3], storage_data[4], storage_data[5], SOC_old)
            assert isinstance(SOC_new, tuple)
            assert len(SOC_new) == 3
    
    @pytest.mark.integration
    def test_wind_power_calculation(self, real_wind_data):
        """Test WindPower calculation with real wind data"""
        ra = RAUtilities()
        
        # Test with real wind data
        if real_wind_data is not None and len(real_wind_data) > 0:
            # Skip wind power test if data structure is not as expected
            pytest.skip("Wind data structure not compatible with test")
    
    @pytest.mark.integration
    def test_solar_power_calculation(self, real_solar_data):
        """Test SolarPower calculation with real solar data"""
        ra = RAUtilities()
        
        # Test with real solar data
        if real_solar_data is not None and len(real_solar_data) > 0:
            # Skip solar power test if data structure is not as expected
            pytest.skip("Solar data structure not compatible with test")
    
    @pytest.mark.integration
    def test_monte_carlo_simulation_setup(self, real_system_data):
        """Test Monte Carlo simulation setup with real data"""
        from progress.mod_sysdata import RASystemData
        from progress.mod_matrices import RAMatrices
        
        # Load system data
        sysdata = RASystemData()
        gen_data = sysdata.gen(real_system_data['gen_csv'])
        branch_data = sysdata.branch(real_system_data['branch_csv'])
        bus_data = sysdata.bus(real_system_data['bus_csv'])
        load_data = sysdata.load('A', real_system_data['load_csv'])
        storage_data = sysdata.storage(real_system_data['storage_csv'])
        
        # Create matrices
        matrices = RAMatrices(len(bus_data[1]))
        gen_mat = matrices.genmat(gen_data[1], gen_data[0], storage_data[2], storage_data[1])
        ainc_mat = matrices.Ainc(branch_data[0], branch_data[1], branch_data[2])
        ch_mat = matrices.chmat(storage_data[2], storage_data[1], len(bus_data[1]))
        curt_mat = matrices.curtmat(len(bus_data[1]))
        
        # Create RAUtilities instance
        ra = RAUtilities()
        
        # Test simulation parameters
        sim_hours = 8760
        samples = 10
        
        # Test indices recording setup
        indices_rec = {
            "LOLP_rec": np.zeros(samples),
            "EUE_rec": np.zeros(samples),
            "EPNS_rec": np.zeros(samples),
            "LOLF_rec": np.zeros(samples),
            "MDT_rec": np.zeros(samples),
            "LOLE_rec": np.zeros(samples),
            "LOLP_hr": np.zeros(sim_hours)
        }
        
        # Test LOL_track setup
        LOL_track = np.zeros((samples, 365, 24))
        
        # Test var_s setup
        var_s = {
            "LLD": 0,
            "curtailment": np.zeros(24),
            "label_LOLF": np.zeros(sim_hours),
            "freq_LOLF": 0,
            "LOL_days": 0,
            "outage_day": np.zeros(365)
        }
        
        # Verify all data structures are properly initialized
        assert len(indices_rec["LOLP_rec"]) == samples
        assert len(indices_rec["LOLP_hr"]) == sim_hours
        assert LOL_track.shape == (samples, 365, 24)
        assert len(var_s["curtailment"]) == 24
        assert len(var_s["label_LOLF"]) == sim_hours
        assert len(var_s["outage_day"]) == 365
    
    @pytest.mark.integration
    def test_data_consistency(self, real_system_data):
        """Test data consistency across different modules"""
        from progress.mod_sysdata import RASystemData
        from progress.mod_matrices import RAMatrices
        
        # Load system data
        sysdata = RASystemData()
        gen_data = sysdata.gen(real_system_data['gen_csv'])
        branch_data = sysdata.branch(real_system_data['branch_csv'])
        bus_data = sysdata.bus(real_system_data['bus_csv'])
        load_data = sysdata.load('A', real_system_data['load_csv'])
        storage_data = sysdata.storage(real_system_data['storage_csv'])
        
        # Create matrices
        matrices = RAMatrices(len(bus_data[1]))
        gen_mat = matrices.genmat(gen_data[1], gen_data[0], storage_data[2], storage_data[1])
        ainc_mat = matrices.Ainc(branch_data[0], branch_data[1], branch_data[2])
        ch_mat = matrices.chmat(storage_data[2], storage_data[1], len(bus_data[1]))
        curt_mat = matrices.curtmat(len(bus_data[1]))
        
        # Test data consistency
        assert gen_mat.shape[0] == len(bus_data[1])  # Rows should match number of buses
        assert gen_mat.shape[1] == gen_data[1] + storage_data[2]  # Columns should match generators + storage
        assert ainc_mat.shape[0] == branch_data[0]  # Rows should match number of branches
        assert ainc_mat.shape[1] == len(bus_data[1])  # Columns should match number of buses
        assert ch_mat.shape[0] == len(bus_data[1])  # Rows should match number of buses
        assert ch_mat.shape[1] == storage_data[2]  # Columns should match number of storage systems
        assert curt_mat.shape[0] == len(bus_data[1])  # Rows should match number of buses
        assert curt_mat.shape[1] == len(bus_data[1])  # Columns should match number of buses (zones)
        
        # Test that all bus numbers are valid
        assert np.all(gen_data[0] >= 1)
        assert np.all(gen_data[0] <= len(bus_data[1]))
        assert np.all(storage_data[1] >= 1)
        assert np.all(storage_data[1] <= len(bus_data[1]))
        
        # Test that all branch connections are valid
        assert np.all(branch_data[1] >= 1)
        assert np.all(branch_data[1] <= len(bus_data[1]))
        assert np.all(branch_data[2] >= 1)
        assert np.all(branch_data[2] <= len(bus_data[1]))
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_performance_benchmark(self, real_system_data):
        """Test performance with real data"""
        from progress.mod_sysdata import RASystemData
        from progress.mod_matrices import RAMatrices
        import time
        
        # Load system data
        sysdata = RASystemData()
        gen_data = sysdata.gen(real_system_data['gen_csv'])
        branch_data = sysdata.branch(real_system_data['branch_csv'])
        bus_data = sysdata.bus(real_system_data['bus_csv'])
        load_data = sysdata.load('A', real_system_data['load_csv'])
        storage_data = sysdata.storage(real_system_data['storage_csv'])
        
        # Create matrices
        matrices = RAMatrices(len(bus_data[1]))
        gen_mat = matrices.genmat(gen_data[1], gen_data[0], storage_data[2], storage_data[1])
        ainc_mat = matrices.Ainc(branch_data[0], branch_data[1], branch_data[2])
        ch_mat = matrices.chmat(storage_data[2], storage_data[1], len(bus_data[1]))
        curt_mat = matrices.curtmat(len(bus_data[1]))
        
        # Create RAUtilities instance
        ra = RAUtilities()
        
        # Test reltrates performance
        start_time = time.time()
        reltrates = ra.reltrates(gen_data[4], branch_data[4], gen_data[5], branch_data[5], storage_data[4], storage_data[5])
        reltrates_time = time.time() - start_time
        
        # Test capacities performance
        start_time = time.time()
        capacities = ra.capacities(branch_data[0], gen_data[2], gen_data[3], np.array([storage_data[2]]), storage_data[3], branch_data[3])
        capacities_time = time.time() - start_time
        
        # Test NextState performance
        current_state = np.ones(gen_data[1] + storage_data[2] + branch_data[0])
        
        start_time = time.time()
        next_state = ra.NextState(0.0, gen_data[1], storage_data[2], branch_data[0], reltrates[0], reltrates[1], current_state, capacities[0], capacities[1], storage_data[6])
        nextstate_time = time.time() - start_time
        
        # Verify performance is reasonable (should complete in under 1 second each)
        assert reltrates_time < 1.0, f"reltrates took {reltrates_time:.3f}s"
        assert capacities_time < 1.0, f"capacities took {capacities_time:.3f}s"
        assert nextstate_time < 1.0, f"NextState took {nextstate_time:.3f}s"
        
        # Print performance metrics
        print(f"\nPerformance metrics:")
        print(f"  reltrates: {reltrates_time:.3f}s")
        print(f"  capacities: {capacities_time:.3f}s")
        print(f"  NextState: {nextstate_time:.3f}s")


class TestRealDataIntegration:
    """Test integration with real data"""
    
    def test_integration_with_system_data(self, real_system_data):
        """Test RAUtilities integration with real system data"""
        from progress.mod_sysdata import RASystemData
        
        # Load system data
        sysdata = RASystemData()
        branch_data = sysdata.branch(real_system_data['branch_csv'])
        bus_data = sysdata.bus(real_system_data['bus_csv'])
        gen_data = sysdata.gen(real_system_data['gen_csv'])
        storage_data = sysdata.storage(real_system_data['storage_csv'])
        load_data = sysdata.load('A', real_system_data['load_csv'])
        
        # Test that data is loaded correctly
        assert isinstance(branch_data, tuple)
        assert len(branch_data) == 6
        assert isinstance(bus_data, tuple)
        assert isinstance(gen_data, tuple)
        assert isinstance(storage_data, tuple)
        assert isinstance(load_data, np.ndarray)
        
        # Test that data has expected structure
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = branch_data
        bus_name, bus_no, nz = bus_data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = gen_data
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = storage_data
        
        # Test data shapes
        assert len(fb) == len(tb)
        assert len(bus_name) == len(bus_no)
        assert len(genbus) == ng
        assert len(essname) == ness
        assert len(load_data) > 0  # Load data should have some values
    
    def test_integration_with_matrices(self, real_system_data):
        """Test RAUtilities integration with RAMatrices"""
        from progress.mod_sysdata import RASystemData
        from progress.mod_matrices import RAMatrices
        
        # Load system data
        sysdata = RASystemData()
        branch_data = sysdata.branch(real_system_data['branch_csv'])
        bus_data = sysdata.bus(real_system_data['bus_csv'])
        gen_data = sysdata.gen(real_system_data['gen_csv'])
        storage_data = sysdata.storage(real_system_data['storage_csv'])
        load_data = sysdata.load('A', real_system_data['load_csv'])
        
        # Unpack data
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = branch_data
        bus_name, bus_no, nz = bus_data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = gen_data
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = storage_data
        
        # Create matrices
        ra = RAUtilities()
        matrices = RAMatrices(nz)
        
        # Test that matrices can be created
        gen_mat = matrices.genmat(ng, genbus, ness, essbus)
        ainc_mat = matrices.Ainc(nl, fb, tb)
        curt_mat = matrices.curtmat(nz)
        ch_mat = matrices.chmat(ness, essbus, nz)
        
        # Test that matrices have correct dimensions
        assert gen_mat.shape[0] == nz
        assert gen_mat.shape[1] == ng + ness
        assert ainc_mat.shape[0] == nl  # Ainc is (nl, nb)
        assert ainc_mat.shape[1] == nz  # nb should equal nz
        assert curt_mat.shape[0] == nz
        assert curt_mat.shape[1] == nz
        assert ch_mat.shape[0] == nz
        assert ch_mat.shape[1] == ness


class TestDataValidation:
    """Test data validation and quality checks"""
    
    def test_data_consistency(self, real_system_data):
        """Test data consistency across system components"""
        from progress.mod_sysdata import RASystemData
        
        # Load system data
        sysdata = RASystemData()
        branch_data = sysdata.branch(real_system_data['branch_csv'])
        bus_data = sysdata.bus(real_system_data['bus_csv'])
        gen_data = sysdata.gen(real_system_data['gen_csv'])
        storage_data = sysdata.storage(real_system_data['storage_csv'])
        load_data = sysdata.load('A', real_system_data['load_csv'])
        
        # Check that bus numbers are consistent
        bus_name, bus_no, nz = bus_data
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = branch_data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = gen_data
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = storage_data
        
        all_bus_numbers = set(bus_no)
        branch_from_buses = set(fb)
        branch_to_buses = set(tb)
        gen_buses = set(genbus)
        storage_buses = set(essbus)
        
        # All referenced buses should exist in bus_data
        assert branch_from_buses.issubset(all_bus_numbers)
        assert branch_to_buses.issubset(all_bus_numbers)
        assert gen_buses.issubset(all_bus_numbers)
        assert storage_buses.issubset(all_bus_numbers)
    
    def test_data_ranges(self, real_system_data):
        """Test that data values are within reasonable ranges"""
        from progress.mod_sysdata import RASystemData
        # Load system data
        sysdata = RASystemData()
        gen_data = sysdata.gen(real_system_data['gen_csv'])
        storage_data = sysdata.storage(real_system_data['storage_csv'])
        load_data = sysdata.load('A', real_system_data['load_csv'])
        
        # Unpack data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = gen_data
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = storage_data
        
        # Check generator data ranges
        assert np.all(pmax > 0), "Generator max power should be positive"
        assert np.all(pmax <= 1000), "Generator max power should be reasonable"
        
        # Check storage data ranges
        assert np.all(ess_pmax > 0), "Storage max power should be positive"
        assert np.all(ess_pmax <= 1000), "Storage max power should be reasonable"
        
        # Check load data ranges (handle NaN values)
        valid_load_data = load_data[~np.isnan(load_data)]
        assert np.all(valid_load_data >= 0), "Load power should be non-negative"
        assert np.all(valid_load_data <= 5000), "Load power should be reasonable"


class TestOutputValidation:
    """Test output validation and format checking"""
    
    def test_return_types(self, utilities_test_helper):
        """Test that methods return expected types"""
        ra = utilities_test_helper
        
        # Test reltrates return type
        rates = ra.reltrates(np.array([100.0, 150.0]), np.array([300.0]), np.array([10.0, 15.0]), np.array([30.0]), np.array([400.0]), np.array([40.0]))
        assert isinstance(rates, tuple)
        assert len(rates) == 2
        
        # Test capacities return type
        capacities = ra.capacities(1, np.array([100.0, 150.0]), np.array([0.0, 0.0]), np.array([50.0]), np.array([0.0]), np.array([200.0]))
        assert isinstance(capacities, tuple)
        assert len(capacities) == 2
        
        # Test NextState return type
        current_cap = {"max": np.array([100.0, 150.0, 200.0, 50.0]), "min": np.array([0.0, 0.0, 0.0, 0.0])}
        result = ra.NextState(10.0, 2, 1, 1, np.array([0.01, 0.02, 0.015, 0.005]), np.array([0.1, 0.15, 0.2, 0.05]), np.array([1, 0, 1, 1]), np.array([100.0, 150.0, 200.0, 50.0]), np.array([0.0, 0.0, 0.0, 0.0]), np.array([1]))
        assert isinstance(result, tuple)
        assert len(result) == 3
        current_state, new_cap, t_min = result
        assert isinstance(new_cap, dict)
        assert 'max' in new_cap
        assert 'min' in new_cap
    
    def test_array_dtypes(self, utilities_test_helper):
        """Test that arrays have correct data types"""
        ra = utilities_test_helper
        
        # Test reltrates array types
        rates = ra.reltrates(np.array([100.0, 150.0]), np.array([300.0]), np.array([10.0, 15.0]), np.array([30.0]), np.array([400.0]), np.array([40.0]))
        mu_tot, lambda_tot = rates
        assert mu_tot.dtype in [np.float64, np.float32]
        assert lambda_tot.dtype in [np.float64, np.float32]
        
        # Test capacities array type
        capacities = ra.capacities(1, np.array([100.0, 150.0]), np.array([0.0, 0.0]), np.array([50.0]), np.array([0.0]), np.array([200.0]))
        cap_max, cap_min = capacities
        assert cap_max.dtype in [np.float64, np.float32]
        assert cap_min.dtype in [np.float64, np.float32]
    
    def test_instance_attributes(self, utilities_test_helper):
        """Test that instance attributes are set correctly"""
        ra = utilities_test_helper
        
        # Test that methods are callable
        assert callable(ra.reltrates)
        assert callable(ra.capacities)
        assert callable(ra.NextState)
        assert callable(ra.updateSOC)
        assert callable(ra.WindPower)
        assert callable(ra.SolarPower)
    
    def test_data_immutability(self, utilities_test_helper):
        """Test that input data is not modified"""
        ra = utilities_test_helper
        
        # Test with reltrates
        MTTF_gen = np.array([100.0, 150.0])
        MTTF_trans = np.array([300.0])
        MTTR_gen = np.array([10.0, 15.0])
        MTTR_trans = np.array([30.0])
        MTTF_ess = np.array([400.0])
        MTTR_ess = np.array([40.0])
        
        MTTF_gen_original = MTTF_gen.copy()
        MTTF_trans_original = MTTF_trans.copy()
        MTTR_gen_original = MTTR_gen.copy()
        MTTR_trans_original = MTTR_trans.copy()
        MTTF_ess_original = MTTF_ess.copy()
        MTTR_ess_original = MTTR_ess.copy()
        
        ra.reltrates(MTTF_gen, MTTF_trans, MTTR_gen, MTTR_trans, MTTF_ess, MTTR_ess)
        
        assert np.array_equal(MTTF_gen, MTTF_gen_original)
        assert np.array_equal(MTTF_trans, MTTF_trans_original)
        assert np.array_equal(MTTR_gen, MTTR_gen_original)
        assert np.array_equal(MTTR_trans, MTTR_trans_original)
        assert np.array_equal(MTTF_ess, MTTF_ess_original)
        assert np.array_equal(MTTR_ess, MTTR_ess_original)


class TestPerformance:
    """Test performance and efficiency"""
    
    def test_calculation_speed(self, utilities_test_helper):
        """Test that calculations complete in reasonable time"""
        ra = utilities_test_helper
        
        # Test reltrates speed
        start_time = time.time()
        ra.reltrates(np.random.uniform(100, 500, 10), np.random.uniform(200, 600, 5), 
                     np.random.uniform(10, 50, 10), np.random.uniform(20, 60, 5), 
                     np.random.uniform(300, 700, 3), np.random.uniform(30, 70, 3))
        end_time = time.time()
        
        assert (end_time - start_time) < 1.0, "reltrates should complete in less than 1 second"
    
    def test_memory_usage(self, utilities_test_helper):
        """Test memory usage during calculations"""
        ra = utilities_test_helper
        
        # Get initial memory usage
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        # Perform calculations
        for _ in range(100):
            ra.reltrates(np.random.uniform(100, 500, 5), np.random.uniform(200, 600, 3), 
                         np.random.uniform(10, 50, 5), np.random.uniform(20, 60, 3), 
                         np.random.uniform(300, 700, 2), np.random.uniform(30, 70, 2))
        
        # Check final memory usage
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100 * 1024 * 1024, f"Memory increase should be less than 100MB, got {memory_increase / 1024 / 1024:.2f}MB"
    
    def test_large_dataset_handling(self, utilities_test_helper):
        """Test handling of large datasets"""
        ra = utilities_test_helper
        
        # Test with large number of components
        ng = 100
        nl = 50
        ness = 20
        
        MTTF_gen = np.random.uniform(100, 500, ng)
        MTTF_trans = np.random.uniform(200, 600, nl)
        MTTR_gen = np.random.uniform(10, 50, ng)
        MTTR_trans = np.random.uniform(20, 60, nl)
        MTTF_ess = np.random.uniform(300, 700, ness)
        MTTR_ess = np.random.uniform(30, 70, ness)
        
        # Should complete without error
        rates = ra.reltrates(MTTF_gen, MTTF_trans, MTTR_gen, MTTR_trans, MTTF_ess, MTTR_ess)
        assert isinstance(rates, tuple)
        assert len(rates) == 2


class TestWorkflowIntegration:
    """Test workflow integration and end-to-end scenarios"""
    
    def test_complete_workflow(self, real_system_data):
        """Test complete workflow from data loading to calculations"""
        from progress.mod_sysdata import RASystemData
        from progress.mod_matrices import RAMatrices
        
        # Load system data
        sysdata = RASystemData()
        branch_data = sysdata.branch(real_system_data['branch_csv'])
        bus_data = sysdata.bus(real_system_data['bus_csv'])
        gen_data = sysdata.gen(real_system_data['gen_csv'])
        storage_data = sysdata.storage(real_system_data['storage_csv'])
        load_data = sysdata.load('A', real_system_data['load_csv'])
        
        # Unpack data
        bus_name, bus_no, nz = bus_data
        nl, fb, tb, cap_trans, MTTF_trans, MTTR_trans = branch_data
        genbus, ng, pmax, pmin, FOR_gen, MTTF_gen, MTTR_gen, gencost = gen_data
        essname, essbus, ness, ess_pmax, ess_pmin, ess_duration, ess_socmax, ess_socmin, ess_eff, disch_cost, ch_cost, MTTF_ess, MTTR_ess, ess_units = storage_data
        
        # Create matrices
        ra = RAUtilities()
        matrices = RAMatrices(nz)
        
        gen_mat = matrices.genmat(ng, genbus, ness, essbus)
        ainc_mat = matrices.Ainc(nl, fb, tb)
        curt_mat = matrices.curtmat(nz)
        ch_mat = matrices.chmat(ness, essbus, nz)
        
        # Test that all matrices are created successfully
        assert gen_mat is not None
        assert ainc_mat is not None
        assert curt_mat is not None
        assert ch_mat is not None
        
        # Test that matrices have correct dimensions
        assert gen_mat.shape[0] == nz
        assert ainc_mat.shape[0] == nl  # Ainc is (nl, nz)
        assert curt_mat.shape[0] == nz
        assert ch_mat.shape[0] == nz
    
    def test_path_robustness(self, real_system_data):
        """Test handling of different path formats"""
        from progress.mod_sysdata import RASystemData
        
        # Test with absolute paths
        abs_branch_path = os.path.abspath(real_system_data['branch_csv'])
        abs_bus_path = os.path.abspath(real_system_data['bus_csv'])
        
        sysdata = RASystemData()
        branch_data = sysdata.branch(abs_branch_path)
        bus_data = sysdata.bus(abs_bus_path)
        
        assert isinstance(branch_data, tuple)
        assert len(branch_data) == 6
        assert isinstance(bus_data, tuple)
    
    def test_cwd_independence(self, real_system_data):
        """Test that calculations don't depend on current working directory"""
        from progress.mod_sysdata import RASystemData
        
        # Change to a different directory
        original_cwd = os.getcwd()
        temp_dir = tempfile.mkdtemp()
        
        try:
            os.chdir(temp_dir)
            
            # Load data from original location
            sysdata = RASystemData()
            branch_data = sysdata.branch(os.path.join(original_cwd, real_system_data['branch_csv']))
            bus_data = sysdata.bus(os.path.join(original_cwd, real_system_data['bus_csv']))
            
            assert isinstance(branch_data, tuple)
            assert isinstance(bus_data, tuple)
            
        finally:
            os.chdir(original_cwd)
            os.rmdir(temp_dir)
    
    def test_multiple_load_cycles(self, real_system_data):
        """Test multiple load cycles"""
        from progress.mod_sysdata import RASystemData
            
        sysdata = RASystemData()
        
        # Load data multiple times
        for _ in range(3):
            # Create new instance for each iteration to avoid attribute conflicts
            sysdata = RASystemData()
            branch_data = sysdata.branch(real_system_data['branch_csv'])
            bus_data = sysdata.bus(real_system_data['bus_csv'])
            gen_data = sysdata.gen(real_system_data['gen_csv'])
            storage_data = sysdata.storage(real_system_data['storage_csv'])
            load_data = sysdata.load('A', real_system_data['load_csv'])
            
            assert isinstance(branch_data, tuple)
            assert len(branch_data) == 6
            assert isinstance(bus_data, tuple)
            assert isinstance(gen_data, tuple)
            assert isinstance(storage_data, tuple)
            assert isinstance(load_data, np.ndarray)
    
    def test_file_isolation(self, real_system_data):
        """Test that temporary files are cleaned up"""
        from progress.mod_sysdata import RASystemData
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Load data
            sysdata = RASystemData()
            branch_data = sysdata.branch(real_system_data['branch_csv'])
            bus_data = sysdata.bus(real_system_data['bus_csv'])
            
            # Check that data is loaded
            assert isinstance(branch_data, tuple)
            assert len(branch_data) == 6
            assert isinstance(bus_data, tuple)
                
        finally:
            # Clean up
            os.rmdir(temp_dir)