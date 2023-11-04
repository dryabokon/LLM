Here's the python file routine with one unit test for function json_to_pandas_v01:

```python
import pandas as pd
import inspect
import unittest

# import the function to be tested
from my_module import json_to_pandas_v01

# sample data
list_of_dct = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Alice", "age": 25, "city": "Los Angeles"},{"name": "Panas", "age": 35, "city": "Kyiv"}]

class TestJsonToPandas(unittest.TestCase):

    def test_json_to_pandas_v01(self):
        # Test logic for empty list
        result = json_to_pandas_v01([])
        self.assertIsNone(result)
        
        # Test logic for non-empty list
        result = json_to_pandas_v01(list_of_dct)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)
        self.assertEqual(list(result.columns), ['name', 'age', 'city'])

if __name__ == '__main__':
    unittest.main()
```

To execute this in the console, save the code above in a file named `test_json_to_pandas.py` and run `python test_json_to_pandas.py` in the console. This will execute the unit test and output the results.