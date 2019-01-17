from core.settings.url import PARAMS_SEARCH, PARAMS_REGISTERS
from core.support import to_snakecase

import pandas as pd

def load_params(filename, **kwargs) -> dict:
    """
    return Dict(param1=[str, str], param2=[str, str])
    """
    file_format = filename.split('.')[-1]
    reader_func = MAPPING_FILE_FORMATS_READ[file_format]
    params = reader_func(filename, **kwargs)
    return params

def _from_excel(filename, **kwargs):
    df = pd.read_excel(filename, **kwargs)

    # to snake_case
    df.columns = [to_snakecase(col) for col in df.columns]
    param_cols = [col for col in df.columns if col in PARAMS_SEARCH or col in PARAMS_REGISTERS]
    return df[param_cols].to_dict(orient="list")

def _from_csv(filename):
    df = pd.read_csv(filename, **kwargs)

    # to snake_case
    df.columns = [to_snakecase(col) for col in df.columns]
    param_cols = [col for col in df.columns if col in PARAMS_SEARCH or col in PARAMS_REGISTERS]
    return df[param_cols].to_dict(orient="list")



def save_results(data, filename, **kwargs):
    file_format = filename.split('.')[-1]
    writer_func = MAPPING_FILE_FORMATS_WRITE[file_format]
    writer_func(data, filename, **kwargs)


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


# GLOBALS

MAPPING_FILE_FORMATS_READ = {
    "xlsx": _from_excel,
    "csv": _from_csv,
}

MAPPING_FILE_FORMATS_WRITE = {
    "xlsx": _to_excel,
    "csv": _to_csv,
}