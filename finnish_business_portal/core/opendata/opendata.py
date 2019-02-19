import urllib
from typing import Dict, List, AnyStr
import logging
from collections import OrderedDict

from .formatting import set_parameter_case, append_default_parameters, split_to_arg_kwarg_params, set_parameter_order
from .validation import validate_parameter_keys, validate_parameter_values

from ...utils.basic_operations import list_of_lists, list_of_dicts

from ..connection import get_page

logger = logging.getLogger(__name__)


class DataStructure:
    """Blueprints for the Open data API

    This class takes care of the structure
    of the API: what operations (queries)
    are possible, what are their parameters,
    what are required parameters et cetera.

    New operations (queries), changes in parameters,
    et cetera should not affect to the use of this
    class. In case of structural changes in the Open 
    Data API, this class SHOULD be reviewed.

    Attributes:
    -----------
        base_url -- Website for the Open data
        base_slugs -- Slugs (URL paths) for all of the
                      possible APIs
        contents -- Raw content of the APIs
        query_options [List] -- All possible queries/operations

    Terms API, operation and query may be used interchangably
    """
    
    #TODO: Turn the use of API, operation & query straightforward    
    
    base_url = "http://avoindata.prh.fi"
    base_slugs = ('/bis_v1.fi.json', '/tr_v1.fi.json')

    def __init__(self):
        "Get the structure of the Open data interface"
        url = self.base_url
        slugs = self.base_slugs

        urls = [url+slug for slug in slugs]

        logger.info(f"Initializing structure using {urls}...")
        conts = []
        for url in urls:
            page = get_page(url)
            page.raise_for_status()
            conts.append(page.json())

        self.contents = conts

    def get_parameters(self, name, as_type=List[Dict]):
        """Get parameters of the API specified in name
        
        Arguments:
            name {str} -- name of the API/query/operation
            as_type {type} -- structure of the output
        
        Returns:
            [List[Dict]] -- if as_type == list
            [Dict[Dict]] -- if as_type == dict
        """
        params_as_list = self.queries[name]["parameters"]
        if as_type == List[Dict]:
            return params_as_list
        elif as_type == Dict[AnyStr, Dict]:
            return {cont["name"]: cont for cont in params_as_list}
        elif as_type == List[AnyStr]:
            return [cont["name"] for cont in params_as_list]
        else:
            raise NotImplementedError(f"Conversion not implemeted for {as_type}")

    def get_url(self, name):
        slug = self.queries[name]["path"]
        return self.base_url+slug
    
    def form_url(self, name, search_params:Dict):
        """Generate URL from given parameters
        
        Arguments:
            name {str} -- Name of the query/operation
            search_params {Dict} -- Parameters to use in conducting web query
        
        Returns:
            [str] -- URL to Open data
        """


        val_parser = urllib.parse.quote

        api_params = self.get_parameters(name, as_type=Dict[AnyStr, Dict])

        # Format parameters
        search_params = set_parameter_case(search_params)
        search_params = append_default_parameters(search_params, api_params)
        arg_params, kwarg_params = split_to_arg_kwarg_params(search_params, api_params)
        kwarg_params = set_parameter_order(kwarg_params, order=self.get_parameters(name, as_type=List[AnyStr]))

        # Validate parameters
        self.validate_parameters(name=name, input_params={**arg_params, **kwarg_params})

        # Asseble URL from parameters
        base_url = self.get_url(name).format(**arg_params)
        params_url = '&'.join([
            f'{param}={val_parser(str(val))}' 
            for param, val in kwarg_params.items()
        ])
        return f'{base_url}?{params_url}'


    def validate_query_name(self, name:str):
        "Validate that the query (aka. API/operation) name exists "
        valid = name in self.query_options
        if not valid:
            raise KeyError(f"API does not have: {name}. All: {self.query_options}")

    @property
    def apis(self):
        if hasattr(self, "_apis"):
            return self._apis
        
        list_apis = [cont["apis"] for cont in self.contents]
        apis = list_of_lists.flatten(list_apis)
        self._apis = apis
        return apis

    @property
    def queries(self) -> Dict:
        if hasattr(self, "_queries"):
            return self._queries
        
        self._queries = {
            operation["type"]: {**dict(path=api["path"]), **operation}
            for api in self.apis
            for operation in api["operations"]
        }
        return self._queries

    def validate_parameters(self, name, input_params):
        "Validate the input parameters to be as required"
        api_params = self.get_parameters(name, as_type=Dict[AnyStr, Dict])

        validate_parameter_keys(input_params, api_params)
        validate_parameter_values(input_params, api_params)

# Non necessities:
    @property
    def specs(self):
        if hasattr(self, "_specs"):
            return self._specs
        
        list_specs = [cont for key, cont in self.contents if key != "apis"]
        specs = list_of_lists.flatten(list_specs)
        self._specs = specs
        return specs

    @property
    def query_options(self):
        return list(self.queries.keys())

    @property
    def query_infos(self):
        queries = self.queries
        return {
            name: {
                key: val for key, val in cont.items() 
                if key in ("summary", "method", "nickname")
            }
            for name, cont in self.queries.items()
        }

    @property
    def query_descriptions(self):
        queries = self.queries
        return {
            name: cont["summary"]
            for name, cont in self.queries.items()
        }



# FORMATTING



