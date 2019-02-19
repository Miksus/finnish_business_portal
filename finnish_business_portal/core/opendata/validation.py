import urllib



def validate_parameter_keys(input_params, api_params):
    invalid_param_keys = [
        name
        for name in input_params
        if name not in api_params.keys()
    ]
    missing_required_params = [
        name
        for name, info in api_params.items()
        if info["required"] and name not in input_params
    ]
    if invalid_param_keys:
        raise KeyError(f"Invalid parameters: {invalid_param_keys}")
    if missing_required_params:
        raise KeyError(f"Missing required parameter(s): {missing_required_params}")

def validate_parameter_values(input_params, api_params, case_sensitive=False):
    common_parser = lambda val: urllib.parse.quote(str(val if case_sensitive else val.lower()))

    def is_in_valid_range(input_, minimum=None, maximum=None):
        not_lower_than_min = float(input_) >= float(minimum) if minimum is not None else True
        not_higher_than_max = float(input_) <= float(maximum) if maximum is not None else True
        return not_lower_than_min and not_higher_than_max
    
    def is_in_valid_list(input_, list_of_values=None):

        if list_of_values is None:
            return True
            
        list_of_values = [common_parser(value) for value in list_of_values]
        return common_parser(input_) in list_of_values

    def is_valid(input_value, value_info):

        valid_by_range = is_in_valid_range(
            input_value, minimum=value_info.get("minimum", None), maximum=value_info.get("maximum", None)
        )

        valid_by_list = is_in_valid_list(
            input_value, list_of_values=value_info.get("enum", None)
        )

        return valid_by_range and valid_by_list


    invalid_param_values = {
        key: value
        for key, value in input_params.items()
        if not is_valid(value, api_params[key])
    }

    if invalid_param_values:
        raise ValueError(f"Invalid parameter value for {invalid_param_values}")
