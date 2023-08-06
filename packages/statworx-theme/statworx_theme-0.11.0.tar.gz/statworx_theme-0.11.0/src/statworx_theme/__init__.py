"""statworx_theme module
"""

from .colormaps import *
from .utils import (  # unimport:skip
    apply_custom_colors,
    apply_custom_colors_altair,
    apply_custom_colors_plotly,
    apply_style,
    apply_style_altair,
    apply_style_plotly,
    get_stwx_cmaps,
    register_blended_cmap,
    register_listed_cmap,
)

__version__ = "0.11.0"
