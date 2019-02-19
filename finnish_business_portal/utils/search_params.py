
from typing import List, Dict, Union

def format_query_params(params:Dict[str, Union[List, str]]) -> List[Dict]:
    """Format params for mass search
    
    >>> _format_params(dict(my_param1="value", my_param2="value2"))
        [dict(my_param1="value", my_param2="value2")]
        
    >>> _format_params(dict(my_param1="value", my_param2=["value2a", "value2b"]))
        [dict(my_param1="value", my_param2="value2a"),
        dict(my_param1="value", my_param2="value2b")]
    """
    allowed_containers = (list,)
    allowed_sequences = (str, int, float)
    
    value_len = validate_query_params(params)
    if value_len:
        params = {
            param: [val]*value_len if isinstance(val, allowed_sequences) else val
            for param, val in params.items()
        }
        # To List of Dict
        params = [dict(zip(params, val)) for val in zip(*params.values())]
    else:
        # To List of Dict
        params = [params]
    
    return params


def validate_query_params(params) -> None:

    allowed_containers = (list,)
    allowed_sequences = (str, int, float)

    def _validate_types(params):
        allowed_types = allowed_containers + allowed_sequences
        invalid_values = {
            param: value
            for key, value in params.items()
            if not isinstance(value, allowed_types)
        }
        if invalid_values:
            allowed = ', '.join(allowed_types)
            raise TypeError(f"Invalid type of value(s): {invalid_values}. Must be in {allowed}")
            
    def _validate_lengths(params):
        container_param_lens = {
            key: len(value)
            for key, value in params.items()
            if isinstance(value, allowed_containers)
        }
        if container_param_lens:
            lens = list(container_param_lens.values())

            # Credit: https://stackoverflow.com/a/3844948
            is_equal_lengths = lens.count(lens[0]) == len(lens)

            if not is_equal_lengths:
                raise ValueError(f"Inequal lengths of values: {container_param_lens}")
            return lens[0] if lens else []

    _validate_types(params)
    value_len = _validate_lengths(params)
    return value_len
