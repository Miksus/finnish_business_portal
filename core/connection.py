
from .support import to_camelcase
from .settings.url import URL_BASE, PARAMS_SEARCH
from .settings.url import URL_BASE_BY_BUSINESSID

import time
import requests
import urllib

def get_page(url, user_agent="Google Chrome", wait=None, **kwargs):
    "Get requests page from url"
    user_agent = {
        "Google Chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla Firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "Microsoft Edge": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        "Google Bot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Bing Bot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
    }[user_agent]

    if wait is not None:
        time.sleep(wait)

    headers = {
        'User-Agent': user_agent
    }
    return requests.get(url, headers=headers, **kwargs)



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
    return URL_BASE_BY_BUSINESSID.format(**kwargs)

def _form_url_from_params(register, total_results, **search_params):
    base = URL_BASE.format(register=register, total_results=str(total_results).lower())

    search_params = [
        f'&{to_camelcase(param)}={search_params[param]}'
        for param in PARAMS_SEARCH 
        if param in search_params
    ]
    return base + ''.join(search_params)