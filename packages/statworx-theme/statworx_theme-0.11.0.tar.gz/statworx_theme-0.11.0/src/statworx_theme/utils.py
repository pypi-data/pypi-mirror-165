import os
import warnings
from os.path import dirname, join

# get path to config files
from shutil import copy
from typing import Any, Dict, List, Optional

import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import Cycler
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.style.core import reload_library
from seaborn.palettes import MPL_QUAL_PALS

import statworx_theme


def register_listed_cmap(colors: List[str], name: str) -> ListedColormap:
    """Register a listed colormat in matplotlib.

    Args:
        colors: Color of the colormap
        name: Name of the colormap

    Returns:
        Registered Colormap
    """
    # register color map
    cmap = ListedColormap(colors, N=len(colors), name=name)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.register_cmap(name, cmap)

    # dark magic shit
    MPL_QUAL_PALS.update({name: len(colors)})
    return cmap


def register_blended_cmap(colors: List[str], name: str) -> LinearSegmentedColormap:
    """Register a blended colormap to matplotlib.

    Args:
        colors: Colors of the colormap
        name: Name of the colormap

    Returns:
        Registered Colormap
    """
    cmap = LinearSegmentedColormap.from_list(name, colors)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.register_cmap(name, cmap)
    return cmap


def _install_styles() -> None:
    """Install matplotlib style files with suffix `.mplstyle` to the matplotlib config dir."""
    # list all theme files
    config_path = join(dirname(statworx_theme.__file__), "styles")
    theme_files = [join(config_path, f) for f in os.listdir(config_path)]

    # get config directory
    config_dir = mpl.get_configdir()
    style_dir = join(config_dir, "stylelib")
    os.makedirs(style_dir, exist_ok=True)

    # copy theme files into config directory
    for file in theme_files:
        copy(file, style_dir)

    # reload matplotlib
    reload_library()


def apply_style() -> None:
    """Apply the statworx color style."""
    _install_styles()
    plt.style.use("statworx")


def apply_custom_colors(
    colors: List[str], cmap_name: str = "stwx:custom", **kwargs: Any
) -> None:
    """Apply custom custom colors to statworx style.

    Args:
        colors: List of custom colors as hex codes
        cmap_name: Custom name of new colormap. Defaults to "stwx:custom".
        **kwargs: Addition parameters that are passed to the style config
    """
    # apply statworx style
    apply_style()

    # add colors as a custom cmap
    register_listed_cmap(colors, cmap_name)

    # add colors to current style
    color_list = [{"color": c} for c in colors]
    mpl.rcParams["axes.prop_cycle"] = Cycler(color_list)

    # apply kwargs
    mpl.rcParams.update(kwargs)


def get_stwx_cmaps(as_hex=True) -> Dict[str, Any]:
    """Gets the registered colormaps as hex or cmap.

    Args:
        as_hex (bool, optional): Should the cmaps be returned as hexadecimal list or as a cmap. Defaults to True.

    Returns:
        Dict[str, Any]: Dictionary with the colormap name as a key and the hex-list or cmap as value.
    """
    cmap_names = [cmap for cmap in plt.colormaps() if cmap.startswith("stwx:")]
    cmaps = [plt.get_cmap(cmap) for cmap in cmap_names]
    if as_hex:
        cmap_hex_codes = [
            [mpl.colors.rgb2hex(cmap(i)) for i in range(cmap.N)] for cmap in cmaps
        ]
        return dict(zip(cmap_names, cmap_hex_codes))
    else:
        return dict(zip(cmap_names, cmaps))


def apply_style_altair(n_groups_ordinal: int = 10) -> None:
    """Apply the statworx color style for Altair.

    Args:
        n_groups_ordinal (int): The number of groups to be plotted for the ordinal
            color map. Defaults to 10.
    """
    import altair as alt

    apply_style()

    stwx_cmaps = get_stwx_cmaps()

    _create_altair_theme(
        primary=stwx_cmaps["stwx:alternative"][0],
        category=stwx_cmaps["stwx:alternative"],
        diverging=stwx_cmaps["stwx:BlRd_diverging"],
        heatmap=stwx_cmaps["stwx:BlRd_diverging"],
        ramp=stwx_cmaps["stwx:Bl_rise"],
        ordinal=_shrink_cmap(stwx_cmaps["stwx:bad2good"], n_groups=n_groups_ordinal),
        name="statworx_altair_theme",
    )

    alt.themes.enable("statworx_altair_theme")


def _shrink_cmap(cmap: List[str], n_groups: int) -> List[str]:
    """Shrinks the cmap for a fixed number of groups.

    Args:
        cmap (List[str]): The colormap.
        n_groups (int): The number of groups in the data to plot.

    Returns:
        List[str]: Shrunken cmap.
    """
    nth_element_to_keep = int(len(cmap) / n_groups)
    return cmap[::nth_element_to_keep]


def _create_altair_theme(
    primary: str,
    category: List[str],
    diverging: List[str],
    heatmap: List[str],
    ramp: List[str],
    ordinal: List[str],
    name: str,
) -> None:
    """Creates the altair theme and registeres it.

    Args:
        primary (str): The primary color as hexadecimal string (e.g. "#d9d9d9").
        category (List[str]): Categorical colors as list of hexadecimal strings.
        diverging (List[str]): Diverging color palette as list of hexadecimal strings.
        heatmap (List[str]): Heatmap color palette as list of hexadecimal strings.
        ramp (List[str]): Ramp color palette as list of hexadecimal strings.
        ordinal (List[str]): Ordinal color plaette as list of hexadecimal strings.
        name (str): The name of the theme.
    """
    import altair as alt

    def statworx_altair_theme() -> dict:
        """STATWORX altair theme.

        Returns:
            altair theme
        """
        font = "Arial"
        primary_color = primary
        font_color = "#000000"
        grey_color = "#d9d9d9"
        base_size = 20
        lg_font = base_size * 1.25
        sm_font = base_size * 0.8
        # xl_font = base_size * 1.75
        config = {
            "config": {
                "view": {
                    "stroke": False,
                },
                "background": "white",  # None for transparent
                "arc": {"fill": primary_color},
                "area": {"fill": primary_color},
                "bar": {"fill": primary_color},
                "boxplot": {"fill": primary_color},
                "circle": {"fill": primary_color},
                "line": {"stroke": primary_color},
                "mark": {"tooltip": True},
                "path": {"stroke": primary_color},
                "point": {"stroke": primary_color},
                "rect": {"fill": primary_color},
                "rule": {"fill": primary_color},
                "shape": {"stroke": primary_color},
                "square": {"stroke": primary_color},
                "symbol": {"fill": primary_color},
                "title": {
                    "font": font,
                    "color": font_color,
                    "fontSize": lg_font,
                    "anchor": "start",
                    "offset": 10,
                },
                "axis": {
                    "titleFont": font,
                    "titleColor": font_color,
                    "titleFontSize": sm_font,
                    "labelFont": font,
                    "labelColor": font_color,
                    "labelFontSize": sm_font,
                    "gridColor": grey_color,
                    "domainColor": font_color,
                    "tickColor": "#fff",
                    "labelPadding": 10,
                    "titlePadding": 10,
                    "ticks": False,
                    "domain": False,
                    # "offset": 10
                },
                "header": {
                    "labelFont": font,
                    "titleFont": font,
                    "labelFontSize": base_size,
                    "titleFontSize": base_size,
                },
                "legend": {
                    "titleFont": font,
                    "titleColor": font_color,
                    "titleFontSize": sm_font,
                    "labelFont": font,
                    "labelColor": font_color,
                    "labelFontSize": sm_font,
                },
                "range": {
                    "category": category,
                    "diverging": diverging,
                    "heatmap": heatmap,
                    "ramp": ramp,
                    "ordinal": ordinal,
                },
            }
        }
        return config

    alt.themes.register(
        name,
        statworx_altair_theme,
    )


def apply_custom_colors_altair(
    primary: Optional[str] = None,
    category: Optional[List[str]] = None,
    diverging: Optional[List[str]] = None,
    heatmap: Optional[List[str]] = None,
    ramp: Optional[List[str]] = None,
    ordinal: Optional[List[str]] = None,
    n_groups_ordinal: int = 10,
) -> None:
    """Applies a custom altair theme with custom color palettes to the statworx style.

    Args:
        primary (str, optional): The primary color as hexadecimal string (e.g. "#d9d9d9").
            Defaults to None (statworx style is kept).
        category (List[str], optional): Categorical colors as list of hexadecimal strings.
            Defaults to None (statworx style is kept).
        diverging (List[str], optional): Diverging color palette as list of hexadecimal strings.
            Defaults to None (statworx style is kept).
        heatmap (List[str], optional): Heatmap color palette as list of hexadecimal strings.
            Defaults to None (statworx style is kept).
        ramp (List[str], optional): Ramp color palette as list of hexadecimal strings.
            Defaults to None (statworx style is kept).
        ordinal (List[str], optional): Ordinal color plaette as list of hexadecimal strings.
            Defaults to None (statworx style is kept).
        n_groups_ordinal (int): The number of groups to be plotted using the ordinal color map.
            Defaults to 10.
    """
    import altair as alt  # type: ignore

    stwx_cmaps = get_stwx_cmaps()
    _create_altair_theme(
        primary=stwx_cmaps["stwx:alternative"][0] if primary is None else primary,
        category=stwx_cmaps["stwx:alternative"] if category is None else category,
        diverging=stwx_cmaps["stwx:BlRd_diverging"] if diverging is None else diverging,
        heatmap=stwx_cmaps["stwx:BlRd_diverging"] if heatmap is None else heatmap,
        ramp=stwx_cmaps["stwx:BlRd_diverging"] if ramp is None else ramp,
        ordinal=_shrink_cmap(stwx_cmaps["stwx:bad2good"], n_groups=n_groups_ordinal)
        if ordinal is None
        else _shrink_cmap(ordinal, n_groups=n_groups_ordinal),
        name="custom_altair_theme",
    )

    alt.themes.enable("custom_altair_theme")


def apply_style_plotly() -> None:
    """Apply the statworx color style for plotly."""
    import plotly.io as pio  # type: ignore

    apply_style()

    stwx_cmaps = get_stwx_cmaps()
    _create_plotly_theme(
        category=stwx_cmaps["stwx:alternative"],
        diverging=stwx_cmaps["stwx:BlRd_diverging"],
        sequential=stwx_cmaps["stwx:bad2good"],
        sequential_minus=stwx_cmaps["stwx:good2bad"],
        heatmap=stwx_cmaps["stwx:BlRd_diverging"],
        name="statworx_plotly_theme",
    )

    pio.templates.default = "statworx_plotly_theme"


def _create_plotly_theme(
    category: List[str],
    diverging: List[str],
    sequential: List[str],
    sequential_minus: List[str],
    heatmap: List[str],
    name: str,
):
    """Creates the plotly theme and registeres it.

    Args:
        category (List[str]): Categorical colors as list of hexadecimal strings.
        diverging (List[str]): Diverging color palette as list of hexadecimal strings.
        sequential (List[str]): Sequential color palette as list of hexadecimal strings.
        sequential_minus (List[str]): Downwards sequential color palette as list of hexadecimal strings.
        heatmap (List[str]): Heatmap color plaette as list of hexadecimal strings.
        name (str): The name of the theme.
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    plotly_template = go.layout.Template(pio.templates["plotly_white"])

    plotly_template.layout.colorway = category
    plotly_template.layout.colorscale.diverging = diverging
    plotly_template.layout.colorscale.sequential = sequential
    plotly_template.layout.colorscale.sequentialminus = sequential_minus
    plotly_template.data.heatmap[0].colorscale = heatmap

    pio.templates[name] = go.layout.Template(plotly_template)


def apply_custom_colors_plotly(
    category: Optional[List[str]] = None,
    diverging: Optional[List[str]] = None,
    sequential: Optional[List[str]] = None,
    sequential_minus: Optional[List[str]] = None,
    heatmap: Optional[List[str]] = None,
):
    """Applies a custom plotly theme with custom color palettes to the statworx style.

    Args:
        category (List[str]): Categorical colors as list of hexadecimal strings.
            Defaults to None (statworx style is kept).
        diverging (List[str]): Diverging color palette as list of hexadecimal strings.
            Defaults to None (statworx style is kept).
        sequential (List[str]): Sequential color palette as list of hexadecimal strings.
            Defaults to None (statworx style is kept).
        sequential_minus (List[str]): Downwards sequential color palette as list of hexadecimal strings.
            Defaults to None (statworx style is kept).
        heatmap (List[str]): Heatmap color plaette as list of hexadecimal strings.
            Defaults to None (statworx style is kept).
    """
    import plotly.io as pio  # type: ignore

    stwx_cmaps = get_stwx_cmaps()
    _create_plotly_theme(
        category=stwx_cmaps["stwx:alternative"] if category is None else category,
        diverging=stwx_cmaps["stwx:BlRd_diverging"] if diverging is None else category,
        sequential=stwx_cmaps["stwx:bad2good"] if sequential is None else sequential,
        sequential_minus=stwx_cmaps["stwx:good2bad"]
        if sequential_minus is None
        else sequential_minus,
        heatmap=stwx_cmaps["stwx:BlRd_diverging"] if heatmap is None else heatmap,
        name="custom_plotly_theme",
    )

    pio.templates.default = "custom_plotly_theme"
