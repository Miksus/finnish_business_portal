
from ...utils.stringcase import to_camelcase
from collections import OrderedDict

def set_parameter_case(input_params):
    return {to_camelcase(key): val for key, val in input_params.items()}

def append_default_parameters(input_params, api_params):
    input_params = {to_camelcase(key): val for key, val in input_params.items()}

    # Appending default parameters to input parameters
    default_params = {
        key: info["defaultValue"] 
        for key, info in api_params.items()
        if "defaultValue" in info
    }

    # Form parameters
    not_found_default_params = {
        param: val for param, val in default_params.items() 
        if param not in input_params
    }

    return {**not_found_default_params, **input_params}

def split_to_arg_kwarg_params(input_params, api_params):

    # Splitting parameters to URL arguments and 
    # URL keyword arguments. Arguments are inserted to 
    # the URL as is and keyword arguments inserted with
    # a key. 
    # Arguments (according to research conducted
    # by the author of this package) are the ones marked as
    # "required" by the API.
    # TODO: Check if the above comment is true

    arg_param_list = [key for key, info in api_params.items() if info["required"]]
    kwarg_param_list = [key for key, info in api_params.items() if key not in arg_param_list]

    arg_params = {}
    kwarg_params = {}
    for key, val in input_params.items():
        if key in arg_param_list:
            arg_params[key] = val
        elif key in kwarg_param_list:
            kwarg_params[key] = val
        else:
            raise KeyError(f"Parameter {key} not found.")
    return arg_params, kwarg_params

def set_parameter_order(input_params, order):

    params_ordered = OrderedDict([
        (key, input_params[key])
        for key in order
        if key in input_params
    ])
    missing = [key for key in input_params if key not in params_ordered]
    if missing:
        raise KeyError(f"Ordering failed. Keys missing in the order: {missing}")
    return params_ordered