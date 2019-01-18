
from ..settings.url import parameters
# .url import PARAMS_SEARCH, PARAMS_REGISTERS
ALLOWED_CONTAINERS = (list,)
ALLOWED_SEQUENCES = (str, int, float)

def format_params(**params) -> str:
    """Format params for mass search
    
    >>> _format_params(dict(my_param1="value", my_param2="value2"))
        [dict(my_param1="value", my_param2="value2")]
        
    >>> _format_params(dict(my_param1="value", my_param2=["value2a", "value2b"]))
        [dict(my_param1="value", my_param2="value2a"),
        dict(my_param1="value", my_param2="value2b")]
    """
    allowed_containers = ALLOWED_CONTAINERS
    allowed_sequences = ALLOWED_SEQUENCES
    
    validate_params(**params)
    param_lens = [len(val) for param, val in params.items() if isinstance(val, allowed_containers)]
    if param_lens:
        maxlen = max(param_lens)
        params = {
            param: [val]*maxlen if isinstance(val, allowed_sequences) else val
            for param, val in params.items()
        }
        
        # To List of Dict
        params = [dict(zip(params, val)) for val in zip(*params.values())]
    else:
        # To List of Dict
        params = [params]
    
    return params


def validate_params(**params) -> None:

    allowed_containers = ALLOWED_CONTAINERS
    allowed_sequences = ALLOWED_SEQUENCES
    
    def _validate_types(params):
        if not all(isinstance(val, allowed_containers + allowed_sequences) for param, val in params.items()):
            raise TypeError("Search Parameters can only have lists or strings as values")
            
    def _validate_sizes(params):
        param_lens = [len(val) for param, val in params.items() if isinstance(val, allowed_containers)]
        if not param_lens:
            return
        if min(param_lens) != max(param_lens):
            raise TypeError(f"List type search parameters unequal lengths: {param_lens}")

    def _validate_keys(params):
        valid_params = {**parameters.SEARCH, **parameters.META}
        keys_valid = all(
            key in valid_params
            for key in params
        )
        if not keys_valid:
            invalid_params = [key for key in params if key not in valid_params]
            raise KeyError(f"Key(s) {invalid_params} invalid (not approved by the API)")

    
    _validate_types(params)
    _validate_sizes(params)
    _validate_keys(params)