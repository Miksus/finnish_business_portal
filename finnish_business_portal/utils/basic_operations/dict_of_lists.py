
def check(obj):
    is_dict = isinstance(obj, dict)
    has_lists_as_values = all(isinstance(value, list) for value in obj.values()) if is_dict else False
    return is_dict and has_lists_as_values

def to_list_of_dicts(obj):
    return [dict(zip(obj, t)) for t in zip(*obj.values())]