""" mplsettings : a module to make configuring matplotlib easy to remember """

import os
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

SMALL_SIZE = 7
MEDIUM_SIZE = 9
BIGGER_SIZE = 11


def load_fonts(path=None, verbose=False):
    """Function to load fonts"""

    paths = [] if path is None else path
    paths = [paths] if not isinstance(paths, list) else paths
    paths = [Path(x) for x in paths]

    default_path = Path(f"{os.environ['HOME']}/.mplsettings/fonts")
    paths.insert(0, default_path)

    for path_entry in paths:
        if path_entry.exists():
            path_name = path_entry.as_posix()
            font_files = font_manager.findSystemFonts(path_name)
            font_names = [
                font_manager.ttfFontProperty(font_manager.get_font(x)).name
                for x in font_files
            ]
            if len(font_files) > 0 and verbose:
                print(
                    f"Loading from {path_name}: " + f"{sorted(list(set(font_names)))}"
                )

            if (len(font_files) == 0) & (path != default_path):
                warnings.warn(f"No usable fonts found in {path_name}")

            for font_file in font_files:
                font_manager.fontManager.addfont(font_file)

        else:
            if path_entry != default_path:
                warnings.warn(f"User-specified path {path_entry} does not exist.")


def list_fonts():
    """Function to list fonts"""
    fonts = font_manager.fontManager.ttflist
    return sorted(list({x.name for x in fonts}))


def setup_plots(dpi=300, font=None):
    """Function to set default figure dpi, font family, and sizes

    This function sets up a nice looking plot
    """

    # Setup figure dpi
    rcParams["figure.dpi"] = dpi

    # Setup font family
    if font is not None:
        load_fonts()
        assert font in list_fonts(), (
            f"Font '{font}' is not available. "
            + "Check font paths and add font if necessary "
            + "using `mplsettings.load_fonts()`."
        )
        rcParams["font.family"] = font

    # Embed font and text in PDF if saved
    rcParams["pdf.fonttype"] = 42.0

    # Modify default font sizes
    plt.rc("font", size=SMALL_SIZE)  # controls default text sizes
    plt.rc("axes", titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc("axes", labelsize=SMALL_SIZE)  # fontsize of the x and y labels
    plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title
