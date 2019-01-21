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

import requests

def search_companies(output_="dataframe", display_=None, loop_results_=False, wait_time_=2, **search_params):
    """Search company information with given search parameters

    Leading underscore (ie. output_) indicate a function parameter
    and not Open Data API parameter

    Parameters:
        output_ : {'dataframe', 'list', 'dict'}
            data type of the outputed results 
            (ie. pandas dataframe, dict of lists)
        display_: {'debug', 'default', None}
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

    NOTE: length of lists = number of web queries
    ie. ["comp 1", "comp 2"] cause two web queries

    Example
    >>> search_companies(business_id=["012312-12", "012312-00"], 
    ...                  company_form="OYJ", 
    ...                  street_address_post_code=["Espoo", "Helsinki"])
    """
    
    pageformat_func = get_formatter(output_)
    data_out = None
    format_func_kwds = dict(index=json_keys.RESULT_BUSINESSID)
    
    search_params = format_params(**search_params)
    
    for search in search_params:
        
        url = form_url(**search)
        page = get_page(url=url, wait=wait_time_)
        url_next = page.json()[json_keys.URL_NEXT_RESULTS]

        data_out = pageformat_func(page, main=data_out, **format_func_kwds)


        _printprog(page, url, loop_results_, mode=display_)

        if loop_results_:
            while url_next:
                page = get_page(url=url_next, wait=wait_time_)
                data_out = pageformat_func(page, main=data_out, **format_func_kwds)
                url_next = page.json()[json_keys.URL_NEXT_RESULTS]

                _printprog_step(page, url_next, mode=display_)

        
    return data_out


def search_companies_deep(output_="dataframe", register_=None, display_=None, wait_time_=2, **search_params):
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
    registers = tuple(registers)

    # Get dict of the companies 
    # --> get their business id's 
    # --> get each's info from registers
    comps_json = search_companies(output_="dict", register="bis", wait_time_=wait_time_, **search_params)
    business_ids = comps_json[json_keys.RESULT_BUSINESSID]
    
    format_func = get_formatter(output_)
    data_out = None
    nth_search = 0
    total_searches = len(business_ids) * len(registers)
    _printprog_deep_start(business_ids, registers, wait_time=wait_time_, mode=display_)

    for reg in registers:
        data_batch = None
        for bus_id in business_ids:
            try:
                data_company = search_companies(business_id=bus_id, register=reg, output_=output_, display_=None)

            except requests.HTTPError as err:
                print(err)

            else:
                data_batch = format_func(
                    data_company, data_batch, 
                    index=json_keys.RESULT_BUSINESSID, axis=0
                )

            finally:
                nth_search += 1
                _printprog_deep_step(at=nth_search, total_searches=total_searches, mode=display_)
        try:
            data_out = format_func(data_batch, data_out, axis=1, keys=registers)
        except TypeError:
            # data_batch should be None
            pass


    return data_out


# Printing functions for informing about progress

def _printprog_deep_start(business_ids, registers, wait_time, mode):

    def print_debug(business_ids, registers, wait_time):
        print(f"Found business IDs: {business_ids}")
        print(f"Registers to go through: {registers}")

    def print_default(business_ids, registers, wait_time):
        estimated_time = wait_time*len(business_ids)*len(registers)
        print(f"Time taken at least: {estimated_time} seconds")

    {
        "debug": print_debug, 
        "default":print_default,
        None: lambda *args: args
    }[mode](business_ids, registers, wait_time)

def _printprog_deep_step(at, total_searches, mode):

    def print_debug(at, total_searches):
        print(f"At: {at}")
        print(f"Total: {total_searches}")
    
    def print_default(at, total_searches):
        nth_to_print = int(total_searches/10)
        nth_to_print = 1 if nth_to_print == 0 else nth_to_print
        if at >= total_searches:
            return
        elif at % nth_to_print == 0:
            print(f'Progress: {at/total_searches*100:.0f} %')

    {
        "debug": print_debug, 
        "default":print_default,
        None: lambda *args: args
    }[mode](at, total_searches)


# Print page

def _printprog(page, url, loop_all, mode=None):

    def print_debug(page, url, *args):
        page_json = page.json()
        print(f'Status: {page.status_code} for {url}')
        meta = {key: val for key, val in page_json.items() if key != json_keys.RESULT}
        print(meta)

    def print_default(page, url, loop_all):
        page_json = page.json()
        total_results = page_json[json_keys.TOTAL_RESULTS]
        print(f'Status: {page.status_code}')
        if loop_all:
            print(f'Found {total_results} companies')
            print('Looping through...')
        else:
            len_results = len(page_json[json_keys.RESULT])
            if len_results < total_results:
                print(f'Showing {len_results} of {total_results} companies.')


    
    {
        "debug": print_debug,
        "default": print_default,
        None: lambda *args: args
    }[mode](page, url, loop_all)


def _printprog_step(page, url, mode):

    def print_debug(page, url):
        _printprog(page, url, None, mode="debug")

    def print_default(page, url):
        page_json = page.json()
        at = page_json[json_keys.RESULTS_FROM]
        total_searches = page_json[json_keys.TOTAL_RESULTS]

        nth_to_print = int(total_searches/10)
        nth_to_print = 1 if nth_to_print == 0 else nth_to_print

        if at >= total_searches:
            return
        elif at % nth_to_print == 0:
            print(f'Progress: {at/total_searches*100:.0f} %')

    {
        "debug": print_debug,
        "default": print_default,
        None: lambda *args: args
    }[mode](page, url)

