"""
Main entry to run primary st_dash_template experiment.

# NOTES
# ----------------------------------------------------------------------------|


Written by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import argparse
from sampy.utils.logger import init_log
from st_dash_template import BASE_DIR
from st_dash_template.experiment import Experiment


# # Main Method
# -----------------------------------------------------|
def main(cfg_file, **kwrgs):
    """Run main method."""
    init_log(BASE_DIR)
    exp = Experiment(cfg_file, **kwrgs)
    exp.run()

    return exp


# # Main Entry
# -----------------------------------------------------|
if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-cfg',
        type=str,
        help='path to experiment cfg',
        default="st_dash_template/cfg.yaml")
    args = parser.parse_args()
    exp = main(args.cfg)
