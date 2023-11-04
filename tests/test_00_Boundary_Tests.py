import pandas as pd
import unittest
import inspect

# ----------------------------------------------------------------------------------------------------------------------
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
import tools_time_profiler
import tools_DF
# ----------------------------------------------------------------------------------------------------------------------
TP = tools_time_profiler.Time_Profiler()
# ---------------------------------------------------------------------------------------------------------------------
def json_to_pandas_v01(list_of_dct, N=1):
    TP.tic(inspect.currentframe().f_code.co_name, reset=True)
    df_res = None
    if len(list_of_dct) > 0:
        for n in range(N):
            df_res = pd.DataFrame.from_dict(list_of_dct, orient='columns')
    TP.print_duration(inspect.currentframe().f_code.co_name)
    return df_res
# ---------------------------------------------------------------------------------------------------------------------
def json_to_pandas_v02(list_of_dct, N=1):
    TP.tic(inspect.currentframe().f_code.co_name, reset=True)
    df_res = None
    if len(list_of_dct) > 0:
        for n in range(N):
            keys = [k for k in list_of_dct[0].keys()]
            values = [[dct[k] for dct in list_of_dct] for k in keys]
            df_res = pd.DataFrame(dict(zip(keys, values)))
    TP.print_duration(inspect.currentframe().f_code.co_name)
    return df_res
# ---------------------------------------------------------------------------------------------------------------------
def benchmark():
    dct = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Alice", "age": 25, "city": "Los Angeles"},{"name": "Panas", "age": 35, "city": "Kyiv"}]
    print(tools_DF.prettify(json_to_pandas_v01(dct, N=5000), showindex=False))
    print(tools_DF.prettify(json_to_pandas_v02(dct, N=5000), showindex=False))
    return

class TestJsonToPandas(unittest.TestCase):
    def test_json_to_pandas_v01(self):
        # Test empty input
        self.assertIsNone(json_to_pandas_v01([]))

        # Test single input
        dct = [{"name": "John", "age": 30, "city": "New York"}]
        df = json_to_pandas_v01(dct)
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (1, 3))

        # Test multiple input
        dct_list = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Alice", "age": 25, "city": "Los Angeles"},{"name": "Panas", "age": 35, "city": "Kyiv"}]
        df = json_to_pandas_v01(dct_list)
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (3, 3))

    def test_json_to_pandas_v02(self):
        # Test empty input
        self.assertIsNone(json_to_pandas_v02([]))

        # Test single input
        dct = [{"name": "John", "age": 30, "city": "New York"}]
        df = json_to_pandas_v02(dct)
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (1, 3))

        # Test multiple input
        dct_list = [{"name": "John", "age": 30, "city": "New York"}, {"name": "Alice", "age": 25, "city": "Los Angeles"},{"name": "Panas", "age": 35, "city": "Kyiv"}]
        df = json_to_pandas_v02(dct_list)
        self.assertIsNotNone(df)
        self.assertEqual(df.shape, (3, 3))

if __name__ == '__main__':
    unittest.main()