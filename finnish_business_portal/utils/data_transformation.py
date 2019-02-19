
import pandas as pd
import numpy as np

def transform_result(data):
    data_type = type(data).__name__.lower()

    data_transf_func = {
        "dataframe": flat_dataframe,
        "list": return_itself,
        "dict": return_itself,
        None: return_itself,
    }[data_type]

    return data_transf_func(data)

def flat_dataframe(df):
    has_unflat_cols = any(
        df[col].apply(lambda x: isinstance(x, (tuple, list, dict))).any()
        for col in df.columns
    )
    if has_unflat_cols:
        return pd.concat([flat_series(df[col]) for col in df.columns], axis=1)
    else:
        return df

def flat_series(series):
    "Turn a series containing list of dicts to multi-index dataframe"
    is_flat = series.apply(lambda x: not isinstance(x, (tuple, list, dict))).all()
    if is_flat:
        return pd.concat([series.to_frame()], keys=[series.name], axis=1)
    
    column_name = series.name
    df_partial_flat = series.apply(pd.Series)
    if df_partial_flat.empty:
        df_partial_flat[series.name] = np.nan
        return pd.concat([df_partial_flat], keys=[series.name], axis=1)
    
    return pd.concat(
        [df_partial_flat[col].apply(pd.Series) for col in df_partial_flat.columns], 
        axis=1, sort=False, 
        keys=[f'{column_name} {n_col}' for n_col in df_partial_flat.columns]
    )



def return_itself(data, *args, **kwargs):
    return data