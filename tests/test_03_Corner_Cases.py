import unittest
# ---------------------------------------------------------------------------------------------------------------------
from ex_01a_unit_tests_codebase import json_to_pandas_v01
# ---------------------------------------------------------------------------------------------------------------------
class TestJsonToPandas(unittest.TestCase):
    def test_corner_cases(self):
        dct = [
            {"name": "John", "age": 30, "city": "New York"},
            {"name": "Alice", "age": 25, "city": "Los Angeles"},
            {"name": "Bob", "age": 35, "city": "Chicago"},
            {},  # Empty dictionary
            {"name": "Mary", "age": 40},  # Missing city key
            {"name": "Peter", "age": 20, "city": "Miami", "gender": "Male"}  # Extra gender key
        ]
        df1 = json_to_pandas_v01(dct)
        df2 = json_to_pandas_v01(dct)
        self.assertTrue(df1 is not None)
        self.assertTrue(df2 is not None)
        self.assertEqual(df1.shape, (6, 3))
        self.assertEqual(df2.shape, (6, 3))
        self.assertListEqual(list(df1.columns), list(df2.columns))
        self.assertListEqual(list(df1['name']), ['John', 'Alice', 'Bob', None, 'Mary', 'Peter'])
        self.assertListEqual(list(df2['name']), ['John', 'Alice', 'Bob', None, 'Mary', 'Peter'])
        self.assertListEqual(list(df1['age']), [30, 25, 35, None, 40, 20])
        self.assertListEqual(list(df2['age']), [30, 25, 35, None, 40, 20])
        self.assertListEqual(list(df1['city']), ['New York', 'Los Angeles', 'Chicago', None, None, 'Miami'])
        self.assertListEqual(list(df2['city']), ['New York', 'Los Angeles', 'Chicago', None, None, 'Miami'])
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
