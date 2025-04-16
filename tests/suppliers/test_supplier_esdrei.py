"""EsDrei supplier test module"""

from pytest_attributes import attributes

from chempare.datatypes import TypeProduct
from chempare.suppliers.supplier_esdrei import SupplierEsDrei as Supplier


@attributes(supplier="supplier_esdrei", mock_data="query-wasser")
def test_name_query():
    try:
        results = Supplier("Wasser")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


@attributes(supplier="supplier_esdrei", mock_data="query-nonsense")
def test_nonsense_query():
    try:
        results = Supplier("this_should_return_no_search_result")
    except Exception as e:
        results = e

    assert isinstance(results, Exception) is False, "query returned an exception"


# # Base test class
# @pytest.mark.supplier
# class TestClass:
#     _query = "Wasser"
#     _results = None

#     @pytest.fixture
#     def results(self):
#         if not self._results:
#             try:
#                 self._results = Supplier(self._query)
#             except Exception as e:
#                 self._results = e

#         return self._results


# # Test cases for a valid search for this supplier
# class TestValidSearch(TestClass):
#     _results = None

#     def test_query(self, results):
#         assert isinstance(results, Exception) is False
#         assert hasattr(results, "__iter__") is True
#         assert hasattr(results, "products") is True
#         assert isinstance(results.products, list) is True, "Return data is not instance of TypeProduct"

#     def test_results(self, results):
#         assert len(results) > 0, "No product results found"
#         assert isinstance(results.products[0], TypeProduct) is True


# # Test cases for invalid searches for this supplier
# class TestInvalidSearch(TestClass):
#     _query = "This_should_return_no_results"
#     _results = None

#     def test_query(self, results):
#         assert isinstance(results, Exception) is False
#         assert hasattr(results, "__iter__") is True
#         assert hasattr(results, "products") is True
#         assert isinstance(results.products, list) is True, "Return data is not instance of TypeProduct"

#     def test_results(self, results):
#         assert len(results) == 0


# Test cases for a valid CAS search for this supplier
# @pytest.mark.skip(reason="EsDrei does not support CAS Searches")
# class TestValidCASSearch(TestClass):
#     _query = "7732-18-5"
#     _results = None

#
#     def test_query(self, results):
#         assert isinstance(results, Exception) is False

#
#     def test_results(self, results):
#         assert len(results) > 0, "No product results found"


# # Test cases for an invalid CAS search for this supplier
# @pytest.mark.skip(reason="EsDrei does not support CAS Searches")
# class TestInvalidCASSearch(TestClass):
#     _query = "7782-77-6"  # Nitrous acid, too stable to be sold
#     _results = None

#
#     def test_query(self, results):
#         assert isinstance(results, Exception) is False

#
#     def test_results(self, results):
#         assert len(results) == 0
