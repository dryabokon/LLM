import pandas as pd
import unittest
# ----------------------------------------------------------------------------------------------------------------------
from ex_01a_unit_tests_codebase import json_to_pandas_v01
# ----------------------------------------------------------------------------------------------------------------------
class TestJsonToPandasV01(unittest.TestCase):
    def test_empty_list(self):
        self.assertIsNone(json_to_pandas_v01([]))

    def test_single_dict(self):
        expected_output = pd.DataFrame.from_dict({"name": ["John"], "age": [30], "city": ["New York"]})
        input_data = [{"name": "John", "age": 30, "city": "New York"}]
        self.assertTrue(expected_output.equals(json_to_pandas_v01(input_data)))

    def test_multiple_dicts(self):
        expected_output = pd.DataFrame.from_dict({"name": ["John", "Alice", "Bob"], "age": [30, 25, 35], "city": ["New York", "Los Angeles", "Chicago"]})
        input_data = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Alice", "age": 25, "city": "Los Angeles"}, {"name": "Bob", "age": 35, "city": "Chicago"}]
        self.assertTrue(expected_output.equals(json_to_pandas_v01(input_data)))
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
