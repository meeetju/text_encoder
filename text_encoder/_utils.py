"""Utils."""

import time
import logging


def time_it(original_function):
    """Log time of executed function.

    :param original_function: function which execution time is measured
    :type original_function: function
    :return: wrapper
    :rtype: function
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        original_function(*args, **kwargs)
        end_time = time.time()
        logging.info('{} complete in {:.2f} seconds.'.format(original_function.__name__,
                                                             end_time - start_time))

    return wrapper
