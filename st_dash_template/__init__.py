"""
Empty init.

# NOTES
# ----------------------------------------------------------------------------|


Written by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
from os.path import dirname
import logging
import traceback


# # Globals
# -----------------------------------------------------|
BASE_DIR = dirname(dirname(__file__))


# # Def
# -----------------------------------------------------|
def try_catch_fail(*dec_args, **dec_kwrgs):
    """Wrap a class instance method in a try, catch, fail, log statement.

    Note: it is assumed the first argument is self, i.e. class instance, 
    AND that self has a fail method, e.g. Experiment or Block

    Args:
        *dec_args:
        **dec_kwrgs:

    Returns:
        method: method with try-catch-log details
    """
    def _try_catch_log_decorator(method):
        """Decorate the wrapped method with try_catch_log params."""
        logger = logging.getLogger(__name__)
        verbose = dec_kwrgs.get('verbose', False)

        def wrap_method(*args, **kwrgs):
            """Wrap method in try-catch with standardized logging."""
            meth_str = method.__str__().split()[1]
            if verbose:
                logger.info(f'Running: {meth_str}')

            try:
                outputs = method(*args, **kwrgs)
                if verbose:
                    logger.info(f'Success: {meth_str}')
                return outputs
            except Exception as err:  # pylint: disable=broad-except
                logger.error(traceback.format_exception(err))
                args[0].fail(err)

        return wrap_method
    return _try_catch_log_decorator
