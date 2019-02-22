

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


def get_page(url, user_agent=None, wait_time=None, **kwargs):
    "Get requests page from url"
    user_agent = {
        None: "FBP Search: https://github.com/Miksus/finnish_business_portal",
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
