import functools
import logging
import time

import requests.exceptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def retry_on_http_error(retries=5, delay=60, codes_to_retry=None):
    if codes_to_retry is None:
        codes_to_retry = []

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            last_exception = None
            for i in range(retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except requests.exceptions.HTTPError as e:
                    logger.warning("Exception encountered", exc_info=e)
                    status_code = e.response.status_code
                    if status_code in codes_to_retry:
                        logger.warning("Retryable exception encountered"
                                       " on attempt {1+i} of {retry_count + 1}")
                        last_exception = e
                    else:
                        raise e
                    logger.debug("Waiting for %s seconds before retrying again")
                    time.sleep(delay)

            if last_exception is not None:
                logger.error("Reraising exception")
                raise last_exception

            return result

        return wrapper
    return decorator
