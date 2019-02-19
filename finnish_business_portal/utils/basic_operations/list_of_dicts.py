from typing import List, Dict

def find_keyvals(obj:List[Dict], keyvals:Dict, **kwargs):
    keyvals = {**keyvals, **kwargs}
    return [
        dict_ for dict_ in obj 
        if all(dict_.get(key, None) == val for key, val in keyvals.items())
    ]