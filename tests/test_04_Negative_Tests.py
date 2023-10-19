import os
import sys
import unittest
import inspect
# ---------------------------------------------------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from ex_01a_unit_tests_codebase import json_to_pandas_v01
# ---------------------------------------------------------------------------------------------------------------------
class TestJsonToPandas(unittest.TestCase):
    
    def test_empty_list(self):
        self.assertIsNone(json_to_pandas_v01([]))
    
    def test_invalid_input(self):
        self.assertIsNone(json_to_pandas_v01(None))
        self.assertIsNone(json_to_pandas_v01("invalid input"))
        self.assertIsNone(json_to_pandas_v01(123))
    
    def test_valid_input(self):
        dct = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Alice", "age": 25, "city": "Los Angeles"},{"name": "Bob", "age": 35, "city": "Chicago"}]
        df = json_to_pandas_v01(dct)
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (3, 3))
        self.assertEqual(list(df.columns), ['name', 'age', 'city'])
        self.assertListEqual(list(df['name']), ['John', 'Alice', 'Bob'])
        self.assertListEqual(list(df['age']), [30, 25, 35])
        self.assertListEqual(list(df['city']), ['New York', 'Los Angeles', 'Chicago'])

if __name__ == '__main__':
    unittest.main()
