from ..supplementary.stringcase import to_camelcase

from ..settings.url.base import DEFAULT as URL_DEFAULT
from ..settings.url.base import BY_BUSINESSID as URL_BY_BUSID

from ..settings.url.parameters import SEARCH as PARAM_SEARCH
# url import URL_BASE, PARAMS_SEARCH
# from ..settings.url import URL_BASE_BY_BUSINESSID

import urllib

def form_url(*args, register="bis", total_results=True, **search_params):
    """
    args: List[str], synonym to business_id (allowed arguments: 1)
    register: str, Open Data register to use
    total_results: bool, whether to show count of total results
    search_params: Dict[str], 
    
    """
    # Turn special characters, spaces etc. to HTML format
    parser = urllib.parse.quote
    args = [parser(str(arg)) for arg in args]
    search_params = {param: parser(str(val)) for param, val in search_params.items()}
    
    if len(args) == 1:
        "Exactly 1 arguments refers to search by business_id"
        return _form_url_from_business_id(register=register, business_id=args[0])
    
    else:
        return _form_url_from_params(register=register, total_results=total_results, **search_params)
    


def _form_url_from_business_id(**kwargs):
    return URL_BY_BUSID.format(**kwargs)

def _form_url_from_params(register, total_results, **search_params):
    url_string = URL_DEFAULT
    base = url_string.format(register=register, total_results=str(total_results).lower())

    search_params = [
        f'&{to_camelcase(param)}={search_params[param]}'
        for param in PARAM_SEARCH 
        if param in search_params
    ]
    return base + ''.join(search_params)