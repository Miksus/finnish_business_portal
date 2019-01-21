
"""
Stage: Early prototype

"""
from .search_funcs import search_companies, search_companies_deep

from .core.parameter_validation import validate_params
from .supplementary.file_io import load_params, save_results

from .help import show_search_parameters


from .core.parameter_validation import validate_params
from .search_funcs import search_companies, search_companies_deep
from .supplementary.file_io import load_params, save_results

class SearchModel:
    """
    params: Dict[List] OR Dict[Str]

    """
    wait_time = 2

    _search_funcs = {
        None: search_companies,
        "deep":search_companies_deep
    }

    def __init__(self, search_type=None, wait_time=2):
        self.params = None
        self.searchfunc = self._search_funcs[search_type]
        self.wait_time = wait_time
        pass

    def search(self):
        self.result = self.searchfunc(self.params, wait_time_=self.wait_time)

    def params_from_file(self, filename):
        self.params = load_params(filename)
    
    def save(self, filename):
        save_results(data=self.result, filename=filename)


    @property
    def parameters(self):
        pass