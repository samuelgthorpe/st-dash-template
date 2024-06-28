"""
Module housing example vis experiment block class.

Note there is absolutely nothing special about a vis block relative to a
processing block, or whatever, this is just a demo. Real experiment
architecture is intended to be whatever it needs to be.

# NOTES
# ----------------------------------------------------------------------------|
Example data/visualization taken from:
https://matplotlib.org/stable/gallery/mplot3d/
stem3d_demo.html#sphx-glr-gallery-mplot3d-stem3d-demo-py


Written by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import os
from logging import getLogger
import matplotlib.pyplot as plt
from st_dash_template.experiment import Block
from st_dash_template import try_catch_fail


# # Globals
# -----------------------------------------------------|
logger = getLogger(__name__)


# # Experiment Block Example Class 1
# -----------------------------------------------------|
class ExampleVisBlock(Block):
    """Example experiment visualization block class."""

    def __init__(self, **params):
        """Instantiate class."""
        logger.info(f'initializing {self.__class__.__name__}')
        super().__init__(**params)
        os.makedirs(self._out_dir, exist_ok=True)

    @try_catch_fail()
    def run(self):
        """Run main method."""
        logger.info(f'running {self.__class__.__name__}')

        # make figure
        fig, axi = plt.subplots(subplot_kw=dict(projection='3d'))
        axi.stem(self._exp_data['x'], self._exp_data['y'], self._exp_data['z'])
        axi.set_title('Example 3D Stem Plot', fontsize=15, fontstyle='italic')

        # save out
        vis_fn = os.path.join(self._out_dir, 'example.png')
        fig.savefig(vis_fn)
        plt.close(fig)
        logger.info(f'saved {vis_fn}')
