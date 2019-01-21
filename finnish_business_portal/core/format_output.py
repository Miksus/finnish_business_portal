
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
    is merge with it
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
def _validate_data(func):
    def check_status(data, *args, **kwargs):
        if hasattr(data, "raise_for_status"):
            data.raise_for_status()
        return func(data, *args, **kwargs)
    return check_status

@_validate_data
def _to_dataframe(data, main=None, index=None, **kwargs) -> pd.DataFrame:
    """ Turn data to pandas dataframe and merge with main
    Parameters:
    -----------
        data: pd.DataFrame, requests.models.Response
            Variable to turn to dataframe and combine
            with main if specified
        main: pd.DataFrame
            Main dataframe to cumulate data with
        index: str
            Column to turn index in data
        **kwargs
            Keyword arguments for merging the 
            data frames

    """
    if isinstance(data, requests.models.Response):
        json = data.json()[json_keys.RESULT]
        data = pd.DataFrame(json, **kwargs)
    elif isinstance(data, pd.DataFrame):
        pass
    elif data is None:
        # Something went wrong in the
        # search function which returned None
        # (could not find a business id et cetera). 
        raise TypeError("Data incorrect type")
    else:
        raise NotImplementedError(f"Conversion for type {type(data)} not implemented")

    index_is_specified = index is not None
    index_is_set_in_data = index in data.index.names
    if index_is_specified and not index_is_set_in_data:
        data = data.set_index(index)


    if main is None:
        main = data

    else:
        if "sort" not in kwargs:
            kwargs["sort"] = False
        main = pd.concat([main, data], **kwargs)
    return main

@_validate_data
def _to_list(data, main=None, **kwargs) -> list:
    """ Turn data to list of dicts and merge with main
    Parameters:
    -----------
        data: list, requests.models.Response
            Variable to turn to dataframe and combine
            with main if specified
        main: list
            Main list to cumulate data with

    """
    if isinstance(data, requests.models.Response):
        # API should give the results in list of dicts
        data = data.json()[json_keys.RESULT]
    if main is None:
        main = data
    else:
        main = main + data
    return main

@_validate_data
def _to_dict(data, main=None, **kwargs) -> dict:
    """ Turn data to dict of lists and merge with main
    Parameters:
    -----------
        data: dict, requests.models.Response
            Variable to turn to dataframe and combine
            with main if specified
        main: dict
            Main dict to cumulate data with

    """
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