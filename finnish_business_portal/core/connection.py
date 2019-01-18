

import time
import requests


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

