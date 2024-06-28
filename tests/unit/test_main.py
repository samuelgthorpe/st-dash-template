"""
Module housing main unit test classes.

# NOTES
# ----------------------------------------------------------------------------|


By Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
from os.path import dirname, join
import unittest
from st_dash_template.main import main
from st_dash_template.experiment import Experiment
from st_dash_template.utils import logger as log_module
from st_dash_template.experiment.example_block import \
    ExampleBlock1, ExampleBlock2
from st_dash_template.experiment.vis.example_vis_block import \
    ExampleVisBlock


# # Globals
# -----------------------------------------------------|
test_dir = dirname(__file__)
test_cfg = join(test_dir, 'test_cfg.yaml')


# # Main Class
# -----------------------------------------------------|
class TestMain(unittest.TestCase):
    """Class object description."""

    @classmethod
    def setUpClass(cls):
        """Set up class for unit tests."""
        log_module.log_dir = join(test_dir, 'run', 'logs')
        Experiment.out_dir = join(test_dir, 'run', 'batch')

    def test_main(self):
        """Test main."""
        exp = main(test_cfg)
        self._example_block1_test(exp.blocks[0])
        self._example_block2_test(exp.blocks[1])
        self._example_vis_block_test(exp.blocks[2])

    @staticmethod
    def _example_block1_test(block):
        """Test example block1."""
        assert isinstance(block, ExampleBlock1)
        assert 'theta' in block._exp_data
        assert hasattr(block, '_example_param')
        assert block._example_param == 'dummy'

    @staticmethod
    def _example_block2_test(block):
        """Test example block2."""
        assert isinstance(block, ExampleBlock2)
        for key in ['x', 'y', 'z']:
            assert key in block._exp_data
        assert hasattr(block, '_example_params_list')
        for idx, val in enumerate(block._example_params_list):
            assert val == f'dummy{idx}'

    @staticmethod
    def _example_vis_block_test(block):
        """Test example vis block."""
        assert isinstance(block, ExampleVisBlock)
        assert hasattr(block, '_example_params_dict')
        for idx, (key, val) in enumerate(block._example_params_dict.items()):
            assert key == f'key{idx}'
            assert val == f'val{idx}'


# # Main Entry
# -----------------------------------------------------|
if __name__ == "__main__":
    unittest.main()
