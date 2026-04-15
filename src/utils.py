import logging
import time

def get_logger(name: str) -> logging.Logger:
    """Configures and returns a basic logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def retry_api_call(func, max_retries=3, backoff_factor=1.5):
    """Simple wrapper to retry API functions."""
    def wrapper(*args, **kwargs):
        retries = 0
        while retries < max_retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                retries += 1
                if retries == max_retries:
                    raise e
                time.sleep(backoff_factor ** retries)
    return wrapper
