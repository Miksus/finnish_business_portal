# TODO
# Possibility to loop through the pages
# provided by the Open Data API. Currently
# too many

from .core.connection import get_page
from .core.url import form_url

from .settings import url as url_strs 
from .settings import json_keys

from .core.format_output import get_formatter
from .core.parameter_validation import format_params

"""
Stage: 
"""

def search_companies(output_="dataframe", display_=None, loop_results_=False, wait_time_=2, **search_params):
    """Search company information with given search parameters

    Leading underscore (ie. output_) indicate a function parameter
    and not Open Data API parameter

    Parameters:
        output_ : {'dataframe', 'list', 'dict'}
            data type of the outputed results 
            (ie. pandas dataframe, dict of lists)
        display_: {'debug', 'process', None}
            print progress of the searches
        loop_results_ : bool
            whether to loop all found results pages
            If True "total_results" specifies batch size
        wait_time : int
            Time in seconds to wait before each call
        **search_params : list or str
            Parameters of the Open Data API 
            in snake_case. All lists must be same lengths 
            each query is created from nth element from
            all inputed search_params lists. Strings are
            considered repeated length of the lists.
            See show_search_parameters() for options

    NOTE: length of list == number of web queries
    ie. ["comp 1", "comp 2"] cause two web queries

    >>> search_companies(business_id=["012312-12", "012312-00"], 
    ...                  company_form="OYJ", 
    ...                  street_address_post_code=["Espoo", "Helsinki"])
    """
    
    pageformat_func = get_formatter(output_)
    data_out = None
    
    search_params = format_params(**search_params)
    
    for search in search_params:
        
        url = form_url(**search)
        page = get_page(url=url, wait=wait_time_)
        url_next = page.json()[json_keys.URL_NEXT_RESULTS]

        data_out = pageformat_func(page, main=data_out)

        _print_progress(page, url, display_, is_subsearch=False)

        while loop_results_ and url_next:
            page = get_page(url=url_next, wait=wait_time_)
            data_out = pageformat_func(page, main=data_out, index=json_keys.RESULT_BUSINESSID)
            url_next = page.json()[json_keys.URL_NEXT_RESULTS]

            _print_progress(page, url_next, display_, is_subsearch=True)

        
    return data_out


def search_companies_deep(output_="dataframe", register_=None, **search_params):
    """Multi-layer search for all information from all available registers

    NOTE: Each set of search_params (nth element in the lists)
    cause one query to get Business IDs and found each Business ID
    cause additional queries (for registers BIS and/or TR).
        --> Searching from many companies may take time

    Parameters:
        from_registers_ : {'bis', 'tr', None}, default None
            if None, both registers are used

    """
    registers = (
        url_strs.parameters.REGISTERS if register_ is None 
        else {register_} if isinstance(register_, str)
        else register_
    )

    # Get dict of the companies 
    # --> get their business id's 
    # --> get each's info from registers
    comps_json = search_companies(output_="dict", register="bis", **search_params)
    business_ids = comps_json[json_keys.RESULT_BUSINESSID]
    
    format_func = get_formatter(output_)
    data_out = None
    for bus_id in business_ids:
        for reg in registers:
            print(bus_id)
            data_batch = search_companies(business_id=bus_id, register=reg)
            data_out = format_func(data_batch, data_out, register=reg)

    return data_out


# Non-core functions
def _print_progress(page, url, mode=None, is_subsearch=False):
    
    if mode is None:
        return
    page_json = page.json()
    if mode == "debug":
        print(f'Status: {page.status_code} for {url}')
        meta = {key: val for key, val in page_json.items() if key != json_keys.RESULT}
        print(meta)

    elif mode == "progress":
        print(f'Status: {page.status_code}')
        if not is_subsearch:
            print(f'Found {page_json[json_keys.TOTAL_RESULTS]}')
            print(f'At {page_json[json_keys.RESULTS_FROM]}')
        else:
            print(f'At {page_json[json_keys.RESULTS_FROM]}')
        print()

    else:
        raise KeyError(f"Invalid mode {mode}")