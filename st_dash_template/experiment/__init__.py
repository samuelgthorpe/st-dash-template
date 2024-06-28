"""
Module housing class to run basic blocked DS experiment.

# NOTES
# ----------------------------------------------------------------------------|


Written by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import os
import importlib
from logging import getLogger
from st_dash_template import BASE_DIR
from sampy.utils import load_yaml
from st_dash_template import try_catch_fail


# # Globals
# -----------------------------------------------------|
run_dir = os.path.join(BASE_DIR, 'run')
logger = getLogger(__name__)


# # Primary Class
# -----------------------------------------------------|
class Experiment:
    """Class to run basic blocked DS experiment."""

    out_dir = os.path.join(run_dir, 'batch')

    def __init__(self, cfg_file: str, **kwrgs):
        """Initialize class.

        Args:
            cfg_file (str): path to experiment config .yaml
            **kwrgs
        """
        logger.info('initializing experiment')
        self.exc = type(f'{self.__class__.__name__}Exception', (Exception,), {}) 
        self.cfg = load_yaml(cfg_file)
        self.src = self._build()
        self.data = {}
        self.blocks = {}

    def _build(self):
        """Build experiment from cfg."""
        for block_idx, (cls_name, block_params) in enumerate(self.cfg.items()):
            block_src = importlib.import_module(block_params['module'])
            block_obj = getattr(block_src, cls_name)
            block_obj._exp_data = self.data
            block_obj._out_dir = f'{self.out_dir}/{block_idx}-{cls_name}'
            yield (block_obj, block_params)

    # # Run Entry
    # -----------------------------------------------------|
    @try_catch_fail(verbose=True)
    def run(self):
        """Run the experiment."""
        logger.info('running experiment')

        for block_idx, (block_obj, params) in enumerate(self.src):
            self.blocks[block_idx] = block_obj(**params)
            self.blocks[block_idx].run()

    def fail(self, msg):
        """Raise custom class exception on failure."""
        raise self.exc(msg)


# # Experiment Block Base Class
# -----------------------------------------------------|
class Block:
    """Initialize class."""

    def __init__(self, **params):
        """Instantiate class.

        Args:
            **params: Dict of params set in config
        """
        self.exc = type(f'{self.__class__.__name__}Exception', (Exception,), {}) 

        # make out_dir and attach params
        os.makedirs(self._out_dir, exist_ok=True)
        for key, val in params.items():
            setattr(self, f'_{key}', val)

    @try_catch_fail()
    def run(self):
        """Overwrite run method."""
        pass

    def fail(self, msg):
        """Raise custom class exception on failure."""
        raise self.exc(msg)
