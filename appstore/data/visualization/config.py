#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/dataset/visual.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday May 20th 2023 06:27:45 pm                                                  #
# Modified   : Tuesday July 25th 2023 01:05:13 pm                                                  #
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
    link: str = "https://colorhunt.co/palette/002b5b2b4865256d858fe3cf"


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
