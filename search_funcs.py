try:
    from .core.connection import get_page, form_url

    from .core.settings.url import PARAMS_REGISTERS 
    from .core.settings import json_keys

    from .core.format_output import get_formatter
    from .core.parameter_validation import format_params
except ImportError:
    from core.connection import get_page, form_url

    from core.settings.url import PARAMS_REGISTERS 
    from core.settings import json_keys

    from core.format_output import get_formatter
    from core.parameter_validation import format_params



def search_companies(output="dataframe", **search_params):
    """Search companies with given search parameters
    search_params: [List, Str]
    >>> search_companies(business_id=["012312-12", "012312-00"], 
    ...                  company_form="OYJ", 
    ...                  street_address_post_code=["Espoo", "Helsinki"])
    """
    
    pageformat_func = get_formatter(output)
    data_out = None
    
    search_params = format_params(**search_params)
    
    for search in search_params:
        url = form_url(**search)
        page = get_page(url=url, wait=2)
        print(f'{page.status_code} {url}')
        data_out = pageformat_func(page, main=data_out)
    return data_out


def search_companies_deep(output="dataframe", **search_params):
    """Multi-layer search
    NOTE: Each found company cause two own search (from BIS and TR)
    Getting information from many companies might take time

    Mechanism:
        1. Get all business IDs
        2. Loop through all of the business IDs
            a) from BIS
            b) from TR
    """
    registers = PARAMS_REGISTERS
    comps_json = search_companies(output="dict", register="bis", **search_params)
    business_ids = comps_json[json_keys.RESULT_BUSINESSID]
    
    format_func = get_formatter(output)
    data_out = None
    for bus_id in business_ids:
        for reg in registers:
            data_batch = search_companies(business_id=bus_id, register=reg)
            data_out = format_func(data_batch, data_out, register=reg)
    return data_out