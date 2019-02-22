from typing import List, Dict

def check(obj):
    is_list = isinstance(obj, list)
    has_dicts_as_values = all(isinstance(value, dict) for value in obj) if is_list else False
    return is_list and has_dicts_as_values

def find_keyvals(obj:List[Dict], keyvals:Dict, **kwargs):
    keyvals = {**keyvals, **kwargs}
    return [
        dict_ for dict_ in obj 
        if all(dict_.get(key, None) == val for key, val in keyvals.items())
    ]

def to_dict_of_lists(obj):
    return {key: [dic[key] for dic in obj] for key in obj}