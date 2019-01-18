
'''
This file contains formatting functions
for cumulating the extracted data

General logic:
    function "get_formatter": 
        acquires the user specified
        data type (ie. list of list, dict of list, 
        pandas dataframe etc.)

    The other functions transforms
    the "data" to specified type and,
    if "main" is specified, the "data"
    is appended to it
'''

try:
    import pandas as pd
except ModuleNotFoundError:
    raise ImportWarning("Pandas not found: cannot use dataframes")
import requests

from ..settings import json_keys

# Formatting function
def get_formatter(output_format) -> callable:
    return {
        "dataframe":_to_dataframe,
        "list":_to_list,
        "dict":_to_dict
    }[output_format]


# Data type conversion and data cumulation functions

def _to_dataframe(data, main=None, index=None, **kwargs) -> pd.DataFrame:
    "data: requests.request or pd.DataFrame"
    if isinstance(data, requests.models.Response):
        json = data.json()[json_keys.RESULT]
        data = pd.DataFrame(json, **kwargs)
    if main is None:
        main = data
        if index:
            main = main.set_index(index)
    else:
        main = main.append(data, sort=False, **kwargs)
    return main

def _to_list(data, main=None, **kwargs) -> list:
    "data: requests.request or list"
    if isinstance(data, requests.models.Response):
        data = data.json()[json_keys.RESULT]
    if main is None:
        main = data
    else:
        main = main + data
    return main

def _to_dict(data, main=None, **kwargs) -> dict:
    "data: requests.request or dict"
    if isinstance(data, requests.models.Response):
        data = data.json()[json_keys.RESULT]

        # List of Dict to Dict of Lists
        # Credit to https://stackoverflow.com/a/33046935
        data = {key: [dic[key] for dic in data] for key in data[0]}
        
    if main is None:
        main = data
    else:
        for key, val in data.items():
            if key not in main:
                main[key] = val
                continue
            main[key] += val
    return main