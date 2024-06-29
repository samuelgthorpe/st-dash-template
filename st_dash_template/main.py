"""
Main entry to run primary st_dash_template experiment.

# NOTES
# ----------------------------------------------------------------------------|


Written by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import argparse
from dash import Dash, html
from sampy.utils.logger import init_log
from st_dash_template import BASE_DIR


# # Main Method
# -----------------------------------------------------|
def main(cfg_file, **kwrgs):
    """Run main method."""
    init_log(BASE_DIR)
    app = Dash()
    app.layout = [html.Div(children='Hello World')]

    return app


# # Main Entry
# -----------------------------------------------------|
if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-cfg',
        type=str,
        help='path to app cfg',
        default="st_dash_template/cfg.yaml")
    args = parser.parse_args()
    app = main(args.cfg)
    app.run(debug=True)
