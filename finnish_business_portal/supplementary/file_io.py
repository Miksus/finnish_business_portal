
from ..settings.url.parameters import SEARCH as PARAMS_SEARCH, REGISTERS as PARAMS_REGISTERS
from ..supplementary.stringcase import to_snakecase

import pandas as pd


"""
State: Untested

This module is independend from search functions and
meant to support GUI, CLI or other kind of interface.

This module is for loading search parameters for search_funcs
from disk and saving results from search_funcs to disk
"""

# Master functions
def load_params(filename, **kwargs) -> dict:
    """
    return Dict(param1=[str, str], param2=[str, str])
    """
    file_format = filename.split('.')[-1]
    reader_func = {
        "xlsx": _from_excel,
        "csv": _from_csv,
    }[file_format]

    params = reader_func(filename, **kwargs)
    return params

def save_results(data, filename, **kwargs):
    file_format = filename.split('.')[-1]
    writer_func = {
        "xlsx": _to_excel,
        "csv": _to_csv,
    }[file_format]

    writer_func(data, filename, **kwargs)


# Input
def _from_excel(filename, **kwargs):
    df = pd.read_excel(filename, **kwargs)

    # to snake_case
    df.columns = [to_snakecase(col) for col in df.columns]
    param_cols = [col for col in df.columns if col in PARAMS_SEARCH or col in PARAMS_REGISTERS]
    return df[param_cols].to_dict(orient="list")

def _from_csv(filename, **kwargs):
    df = pd.read_csv(filename, **kwargs)

    # to snake_case
    df.columns = [to_snakecase(col) for col in df.columns]
    param_cols = [col for col in df.columns if col in PARAMS_SEARCH or col in PARAMS_REGISTERS]
    return df[param_cols].to_dict(orient="list")


# Output
def _to_excel(data, filename, **kwargs):
    if hasattr(data, "to_excel"):
        data.to_excel(filename, **kwargs)
    else:
        raise NotImplementedError

def _to_csv(data, filename, **kwargs):
    if hasattr(data, "to_csv"):
        data.to_excel(filename, **kwargs)
    else:
        raise NotImplementedError


