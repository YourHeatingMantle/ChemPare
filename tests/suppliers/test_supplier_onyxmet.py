#!/usr/bin/env python3 
import pytest
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from suppliers.supplier_onyxmet import SupplierOnyxmet as Supplier

# Base test class
class TestClass:
    _query = 'carbonate'
    _results = None

    @pytest.fixture
    def results(self):
        if not self._results:
            try:
                self._results = Supplier(self._query)
            except Exception as e:
                self._results = e
        
        return self._results  

# Test cases for a valid search for this supplier
class TestValidSearch(TestClass):
    _results = None
    
    @pytest.mark.first
    def test_query(self, results):
        assert isinstance(results, Exception) is False
    
    @pytest.mark.second
    def test_results(self, results):
        assert len(results) > 0

# Test cases for invalid searches for this supplier
class TestInvalidSearch(TestClass):
    _query = 'This_should_return_no_results'
    _results = None

    @pytest.mark.first
    def test_query(self, results):
        assert isinstance(results, Exception) is False
    
    @pytest.mark.second
    def test_results(self, results):
        assert len(results) == 0

# Test cases for a valid CAS search for this supplier
class TestValidCASSearch(TestClass):
    _query = '7440-23-5' # Sodium
    _results = None

    @pytest.mark.first
    def test_query(self, results):
        assert isinstance(results, Exception) is False
    
    @pytest.mark.second
    def test_results(self, results):
        assert len(results) > 0


# Test cases for an invalid CAS search for this supplier
class TestInvalidCASSearch(TestClass):
    _query = '7782-77-6' # Nitrous acid, too stable to be sold
    _results = None

    @pytest.mark.first
    def test_query(self, results):
        assert isinstance(results, Exception) is False
    
    @pytest.mark.second
    def test_results(self, results):
        assert len(results) == 0