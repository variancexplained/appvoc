#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.14                                                                             #
# Filename   : /appvoc/visual/seaborn.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday June 29th 2024 06:43:31 pm                                                 #
# Modified   : Saturday June 29th 2024 07:16:20 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from studioai.analysis.visualize.visualizer import (
    Visualizer as VisualizerBase,
    SeabornCanvas,
)


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Canvas(SeabornCanvas):
    """Inherits from Seaborn Canvas"""


# ------------------------------------------------------------------------------------------------ #
class Visualizer(VisualizerBase):
    def __init__(self, canvas: type[Canvas] = Canvas):
        super().__init__(canvas())

    def topn_plot(
        self,
        x: str,
        n: list[int],
        data: pd.DataFrame = None,
        hue: str = None,
        title: str = None,
        ax: plt.Axes = None,
        *args,
        **kwargs,
    ) -> None:
        """Bar plot showing the top n values for a continuous or discrete variable.

        Plots a range of top n values in the logspace for the designated column. Top n
        values are displayed as percent of total value and percent of observations
        represented by the top n group.

        Args:
            x (str): Keys in data.
            n (list(int)): List of top n values to report.
            data (pd.DataFrame): Input data frame. Optional. If not provided here, must be
                provided via the data setter, inherited from the base class.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.

        """
        data = data or self._data

        sns.set_style(style=self._canvas.style)
        sns.set_palette(palette=self._canvas.palette)

        if ax is None:
            fig, ax = self._canvas.get_figaxes()

        palette = self._canvas.palette if hue is not None else None

        values = []
        total = data[x].sum(axis=0)
        sorted_values = data.sort_values(by=x, ascending=False, axis=0)

        n = np.array(n)

        for idx in n:
            values.append(sorted_values[x][:idx].sum())

        # Normalize the values and counts by total and number of observations.
        values_pct = values / total * 100
        obs_pct = n / data.shape[0] * 100

        d = {
            "Top-N": n,
            "% Total": np.round(values_pct, 2),
            "% Observations": np.round(obs_pct, 2),
        }
        df = pd.DataFrame(data=d)

        ax = sns.barplot(
            data=df,
            x="Top-N",
            y="% Total",
            ax=ax,
            hue=hue,
            color=self._canvas.colors.dark_blue,
            palette=palette,
            *args,
            **kwargs,
        )
        title = title or f"Top-N {x.capitalize()} Analysis"
        if title is not None:
            ax.set_title(title)

        for idx, bar in enumerate(ax.patches):
            ax.annotate(
                f"{np.round(values_pct[idx],2)}% ({np.round(obs_pct[idx],2)}%)",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center",
                va="center",
                xytext=(0, 10),
                textcoords="offset points",
            )
