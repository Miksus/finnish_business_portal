

import time
import requests
import logging


# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

#formatter = logging.Formatter('%(levelno)s: %(asctime)s %(name)s: %(message)s')

#filehandler = logging.FileHandler("querying.log")
#filehandler.setFormatter(formatter)

#logger.addHandler(filehandler)


def get_page(url, user_agent="Google Chrome", wait_time=None, **kwargs):
    "Get requests page from url"
    user_agent = {
        "Google Chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla Firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "Microsoft Edge": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        "Google Bot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Bing Bot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
    }.get(user_agent, user_agent)

    if wait_time:
        logger.debug(f"Waiting {wait_time} seconds")
        time.sleep(wait_time)

    headers = {
        'User-Agent': user_agent
    }

    logger.debug(f"Connecting to {url}...")
    page = requests.get(url, headers=headers, **kwargs)
    
    if not page.ok:
        logger.warning(f"Failed to connect to {url}")
    logging.debug(f"Status code: {page.status_code}")
    return page
