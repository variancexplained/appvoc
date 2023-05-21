#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/dataset/visual.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday May 20th 2023 06:27:45 pm                                                  #
# Modified   : Sunday May 21st 2023 04:10:17 am                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Visualization of Data Module"""
from dataclasses import dataclass, field
from typing import List

import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------------------------ #
#                                            PALETTE                                               #
# ------------------------------------------------------------------------------------------------ #


@dataclass
class Palette:
    blue: str = "#69d"
    blues: str = "Blues"
    blues_r: str = "Blues_r"
    dark_blue: str = "dark:b"
    dark_blue_reversed: str = "dark:b_r"
    heatmap: str = "mako"
    bluegreen: str = "crest"


# ------------------------------------------------------------------------------------------------ #
#                                            CANVAS                                                #
# ------------------------------------------------------------------------------------------------ #


@dataclass
class Canvas:
    nrows: int = 1
    ncols: int = 1
    fig: plt.figure = None
    ax: plt.axes = None
    axs: List = field(default_factory=lambda: [plt.axes])

    def __post_init__(self) -> None:
        if self.nrows > 1 or self.ncols > 1:
            figsize = []
            figsize.append(VisualConfig.figsize[0])
            figsize.append(VisualConfig.figsize[1] * self.nrows)
            self.fig, self.axs = plt.subplots(self.nrows, self.ncols, figsize=figsize)
        else:
            self.fig, self.ax = plt.subplots(self.nrows, self.ncols, figsize=VisualConfig.figsize)


# ------------------------------------------------------------------------------------------------ #
#                                            CONFIG                                                #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class VisualConfig:
    style = "whitegrid"
    figsize: tuple = (12, 3)
    palette: Palette = Palette()
    canvas: type[Canvas] = Canvas
