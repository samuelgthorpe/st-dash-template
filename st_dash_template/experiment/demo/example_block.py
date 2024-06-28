"""
Module housing example experiment block classes.

# NOTES
# ----------------------------------------------------------------------------|
Example data/visualization taken from:
https://matplotlib.org/stable/gallery/mplot3d/
stem3d_demo.html#sphx-glr-gallery-mplot3d-stem3d-demo-py


Written by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
from logging import getLogger
import numpy as np
from st_dash_template.experiment import Block
from st_dash_template import try_catch_fail


# # Globals
# -----------------------------------------------------|
logger = getLogger(__name__)


# # Experiment Block Example Class 1
# -----------------------------------------------------|
class ExampleBlock1(Block):
    """Example experiment block class."""

    def __init__(self, **params):
        """Instantiate class.

        Args:
            **params: Dict of params set in config
        """
        logger.info(f'initializing {self.__class__.__name__}')
        super().__init__(**params)

    @try_catch_fail()
    def run(self):
        """Run main method.

        NOTE: _exp_data allows data to persist in-memory across blocks.
              For large blocks that take a long time to execute it may be
              more convenient in development to cache intermediate outputs
              to disk and load as needed in subsequent blocks.
        """
        logger.info(f'running {self.__class__.__name__}')
        self._exp_data['theta'] = np.linspace(0, 2*np.pi)


# # Experiment Block Example Class 2
# -----------------------------------------------------|
class ExampleBlock2(Block):
    """Example experiment block class."""

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
        self._exp_data['x'] = np.cos(self._exp_data['theta'] - np.pi/2)
        self._exp_data['y'] = np.sin(self._exp_data['theta'] - np.pi/2)
        self._exp_data['z'] = self._exp_data['theta']
