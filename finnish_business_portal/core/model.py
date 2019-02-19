
import logging
import copy
from typing import List, Dict, Union, AnyStr

import pandas as pd

from .opendata import opendata
from ..utils.data_transformation import flat_dataframe
from ..utils.search_params import format_query_params
from .connection import get_page

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelno)s: %(asctime)s %(name)s: %(message)s')

#filehandler = logging.FileHandler("querying.log")
#filehandler.setFormatter(formatter)

#logger.addHandler(filehandler)


class SearchModel:
    """Interface to YTJ and PRH open data
    
    Attributes:
    -----------
        query_name [str] -- Name of the operation for search
                            See query_options
        wait_time [int, float] -- Wait time in seconds before each connection attempt.
                                  Be nice to the API and have fair time before each call.
        deep [bool] -- Whether to acquire the detailed version of each company.
                       Requires visiting each company's own URL thus takes longer.
                       Ignored if the used query/operation returns only one row.
        loop_results [bool] -- Whether to loop all rows from the query. Might cause
                               the search to take longer than estimated. 
        inplace [bool] -- Whether to return copy of itself after each search or
                          modify "in place" returning None.
        results [List[Dict]] -- Results of a search where each element of the list
                                represent row and each key in inner dictionary represents
                                a column.
        _api_structure -- Blueprint for the API


    """


    _api_structure = opendata.DataStructure()
    api_infos = _api_structure.query_descriptions
    api_options = _api_structure.query_options

    def __init__(self, api, wait_time=2, deep=False, loop_results=False):
        """Initialize Search Interface
        
        Keyword Arguments:
            query_name {str} -- Name of the API to use (default: {None})
            wait_time {int} -- Wait time between web queries (default: {2})
            deep {bool} -- Whether to look for all the details (cause more web queries) (default: {True})
            loop_results {bool} -- Whether to loop all found by the API (default: {False})
            inplace {bool} -- Whether to change this object in place (default: {False})
        """

        self.api = api
        self.wait_time = wait_time
        self.deep = deep
        self.loop_results = loop_results

        self.results = None


    def search(self, **search_param:Dict[str, Union[List, str]]):
        """Search from the Open Data API using search_param

        Keyword Arguments:
            **search_param [str, List[str]] -- Parameters to use in conducting the search.
                                               Lists represent different queries (first element
                                               in ALL inputted lists is the parameters for first
                                               query/search, second elements for second query et 
                                               cetera). Strings are considered the same for each 
                                               query.
                                               Pythonic (snake_case) parameters are also allowed
                                               as keys.
                                               NOTE: All keyword arguments inputted as lists
                                               must share the same length. 
        
        Example:
            self.search(name=["Fortum", "Nokia"], organization_type="Oy")
        
        Returns:
            [type] -- [description]
        """

        query_kwds = dict(wait_time=self.wait_time, loop_results=self.loop_results)
        queries = format_query_params(search_param)

        query_urls = [self._api_structure.form_url(self.api, query_params) for query_params in queries]
        
        query_result = _query(query_urls, **query_kwds)
        if self.deep:
            query_urls = [result["detailsUri"] for result in query_result if result["detailsUri"]]
            if query_urls:
                query_result = _query(query_urls, **query_kwds)


        self.results = query_result
        return self

    def to_frame(self, flatten=False):
        """Results to pandas dataframe
        
        Keyword Arguments:
            flatten [bool] -- Whether to turn dicts inside the frame to multi-index
        
        Returns:
            [type] -- [description]
        """

        if self.results is None:
            raise AttributeError("Missing results. Try execute search first.")

        df = pd.DataFrame(self.results).set_index("businessId")
        if flatten:
            df = flat_dataframe(df)

        # Returning copy of self for 
        # being nice for mistakes
        self_copy = copy.deepcopy(self)
        self_copy.results = df
        return self_copy

    @property
    def api(self):
        return self._query_name
        
    @api.setter
    def api(self, name):
        self._api_structure.validate_query_name(name)
        self._query_name = name

    @property
    def parameter_options(self):
        "Parameters for selected query"
        return self._api_structure.get_parameters(self.api, as_type=List[AnyStr])

    @property
    def parameter_infos(self):
        "Parameters for selected query"
        return self._api_structure.get_parameters(self.api, as_type=Dict[AnyStr, Dict])

    def help(self):
        relevant_fields = ("description", "required", "minimum", "maximum", "enum", "defaultValue")
        intend = '\t'
        out = ''
        out += f'Selected query: {self.api}\n'
        out += '------------------------\n'
        out += f'Parameters for the query:\n'
        for name, info in self.parameter_infos.items():
            out += f'{intend}{name}:\n'
            info = {key:val for key, val in info.items() if key in relevant_fields}
            for key, cont in info.items():
                out += f'{intend*2}{key}: \n'
                max_rowlen = 50

                cont = str(cont)
                vals = [cont[i:i+max_rowlen] for i in range(0, len(cont), max_rowlen)]
                for val in vals:
                    out += f'{intend*3}{val}\n'

        out += '------------------------\n'
        out += f'All queries: {self.api_options}\n'
        out += 'Set using: "model.query_name = {intended query}"'
        print(out)

def _query(urls, wait_time, loop_results=False):
    logger.info(f"{len(urls)} queries to make (time taken > {len(urls*wait_time)})...")
    query_result = []
    for url in urls:
        page = get_page(url, wait_time=wait_time)
        json = page.json()
        
        next_url, result = json["nextResultsUri"], json["results"]

        query_result += result
        if loop_results:
            while next_url:
                page = get_page(next_url, wait_time=wait_time)
                json = page.json()

                next_url, result = json["nextResultsUri"], json["results"]

                query_result += result
        elif next_url:
            # Showing Warning for not capturing all
            total_count = json["totalResults"]
            return_count = len(result)
            if total_count >= 0:
                msg = f"Not all entries in the API searched ({return_count} vs {total_count}), set loop_results=True to get all."
            else:
                msg = f"Not all entries in the API searched ({return_count}), set loop_results=True to get all."
            logger.warning(msg)
    return query_result