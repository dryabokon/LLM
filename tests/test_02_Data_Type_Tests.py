import os
import sys
import pandas as pd
import unittest
import inspect
# ---------------------------------------------------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from ex_01a_unit_tests_codebase import json_to_pandas_v01
# ---------------------------------------------------------------------------------------------------------------------
class TestJsonToPandas(unittest.TestCase):
    
    def test_data_type(self):
        list_of_dct = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Alice", "age": 25, "city": "Los Angeles"},{"name": "Bob", "age": 35, "city": "Chicago"}]
        df_res = json_to_pandas_v01(list_of_dct)
        self.assertIsInstance(df_res, pd.DataFrame)
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
