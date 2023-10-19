import unittest
from ex_01a_unit_tests_codebase import json_to_pandas_v01
# ----------------------------------------------------------------------------------------------------------------------
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
class TestJsonToPandas(unittest.TestCase):
  
    def test_json_to_pandas_v01(self):
        dct = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Alice", "age": 25, "city": "Los Angeles"},{"name": "Bob", "age": 35, "city": "Chicago"}]
        self.assertIsNotNone(json_to_pandas_v01(dct))

    def test_json_to_pandas_v01_boundary(self):
        dct = []
        self.assertIsNone(json_to_pandas_v01(dct))
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)