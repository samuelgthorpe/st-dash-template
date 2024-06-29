"""
Module housing common vis methods.

# NOTES
# ----------------------------------------------------------------------------|


Written by Samuel Thorpe
"""

# # Imports
# -----------------------------------------------------|
import numpy as np
from matplotlib.colors import ListedColormap


# # Globals
# -----------------------------------------------------|
VisException = type('VisException', (Exception,), {})
HOTNCOLD_ARRAY = np.zeros([256, 3])
HOTNCOLD_ARRAY[:128, 2] = np.linspace(0, 1, 128)[::-1]
HOTNCOLD_ARRAY[128:, 0] = np.linspace(0, 1, 128)
HOTNCOLD = ListedColormap(HOTNCOLD_ARRAY)


# # Common Visualization Tools
# -----------------------------------------------------|
def prettify(axi, grid_ax='y', grid_alpha=0.25):  # pragma: no cover
    """Make axes pretty.

    Args:
        axi (matplotlib axis object): axis to prettify
        grid_ax (str, optional): axis specifier; x or y
        grid_alpha (float, optional): alpha value for grid (0 - 1)
    """
    color_lines_neutral = '#858585'  # dark grey
    axi.spines['left'].set_color(color_lines_neutral)
    axi.spines['bottom'].set_color(color_lines_neutral)
    axi.spines['top'].set_visible(False)
    axi.spines['right'].set_visible(False)
    axi.spines['left'].set_position(('outward', 10))
    axi.tick_params(right=False, left=False, top=False, bottom=False)
    axi.grid(b=True, which='both', axis=grid_ax, alpha=grid_alpha, ls='solid')
