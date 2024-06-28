"""
Module housing experiment block template for dev.

# NOTES
# ----------------------------------------------------------------------------|

Written by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
from logging import getLogger
from st_dash_template.experiment import Block
from st_dash_template import try_catch_fail


# # Globals
# -----------------------------------------------------|
logger = getLogger(__name__)


# # Experiment Block Example Class 1
# -----------------------------------------------------|
class DevBlock(Block):
    """Experiment block class."""

    def __init__(self, **params):
        """Instantiate class.

        Args:
            **params: Dict of params set in config
        """
        logger.info(f'initializing {self.__class__.__name__}')
        super().__init__(**params)

    @try_catch_fail()
    def run(self):
        """Run main method."""
        logger.info(f'running {self.__class__.__name__}')

        from sampy.common import keyboard
        keyboard(locals(), globals())
