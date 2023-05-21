#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/dataset/base.py                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday May 21st 2023 03:00:19 am                                                    #
# Modified   : Sunday May 21st 2023 04:19:27 am                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod
import logging

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

from aimobile.data.dataset.visual import VisualConfig
from aimobile.data.repo.base import Repo

sns.set_style(VisualConfig.style)
sns.set_palette = sns.dark_palette(VisualConfig.palette.blue, reverse=True, as_cmap=True)


# ------------------------------------------------------------------------------------------------ #
#                                            DATASET                                               #
# ------------------------------------------------------------------------------------------------ #
class Dataset(ABC):
    """Provides data and visualizations for a Fog Dataset.

    Args:
        filepath (str): Path to metadata file
    """

    def __init__(self, repo: Repo) -> None:
        self._repo = repo
        self._df = self._repo.getall()
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    # -------------------------------------------------------------------------------------------- #
    @property
    def overview(self) -> pd.DataFrame:
        """Provides an overview at the dataset level."""

        nvars = self._df.shape[1]
        nrows = self._df.shape[0]
        ncells = nvars * nrows
        nmissing = self._df.isna().sum().sum()
        pmissing = nmissing / ncells * 100
        ndups = nrows - self._df.drop_duplicates().shape[0]
        pdups = ndups / nrows * 100
        size = self._df.memory_usage(deep=True).sum().sum()
        d = {
            "Number of Observations": nrows,
            "Number of Variables": nvars,
            "Number of Cells": ncells,
            "Missing Cells": nmissing,
            "Missing Cells (%)": round(pmissing, 2),
            "Duplicate Rows": ndups,
            "Duplicate Rows (%)": round(pdups, 2),
            "Size (Bytes)": size,
        }
        overview = pd.DataFrame.from_dict(data=d, orient="index").reset_index()
        overview.columns = ["Characteristic", "Total"]
        return overview

    # ------------------------------------------------------------------------------------------------ #
    @property
    def info(self) -> pd.DataFrame:
        """Returns a DataFrame with basic dataset statistics"""

        info = self._df.dtypes.to_frame().reset_index()
        info.columns = ["Column", "Dtype"]
        info["Valid"] = self._df.count().values
        info["Null"] = self._df.isna().sum().values
        info["Validity"] = info["Valid"] / self._df.shape[0]
        info["Unique"] = self._df.nunique().values
        info["Cardinality"] = info["Unique"] / self._df.shape[0]
        info["Size"] = self._df.memory_usage(deep=True, index=False).to_frame().reset_index()[0]
        info = round(info, 2)
        return info

    # ------------------------------------------------------------------------------------------------ #
    @property
    @abstractmethod
    def summary(self) -> pd.DataFrame:
        """Returns a summary of the repository in DataFrame format"""

    # ------------------------------------------------------------------------------------------------ #
    def head(self, n: int = 5) -> pd.DataFrame:
        return self._df.head(n)

    # ------------------------------------------------------------------------------------------------ #
    def sample(
        self, n: int = 5, frac: float = None, replace: bool = False, random_state: int = None
    ) -> pd.DataFrame:
        """Returns a sample from the FOG Dataset

        Args:
            n (int): Number of items to return. Defaults to five.
            frac (float): Proportion of items to return
            replace (bool): Whether to sample with replacement
            random_state (int): Pseudo random seed.
        """
        return self._df.sample(n=n, frac=frac, replace=replace, random_state=random_state)

    # ------------------------------------------------------------------------------------------------ #
    def describe(self, column: str = None, groupby: str = None) -> pd.DataFrame:
        """Produces descriptive statistics

        Args:
            column (str): Optional column upon which descriptive statistics will be computed.
            groupby (str): Name of a column by which descriptive statistics will be grouped.

        """
        if column is None:
            if groupby is None:
                return self._df.describe().T
            else:
                return self._df.groupby(by=groupby).describe().T
        else:
            if groupby is None:
                return self._df[column].describe().to_frame().T
            else:
                return self._df.groupby(by=groupby)[column].describe()

    # ------------------------------------------------------------------------------------------------ #
    #                                    VISUALIZATION METHODS                                         #
    # ------------------------------------------------------------------------------------------------ #
    def countplot(
        self,
        x: str,
        y: str = None,
        hue: str = None,
        title: str = None,
        orient: str = "v",
        ax: plt.axes = None,
    ) -> plt.axes:
        """Produces plot of counts of observations in each categorical bin using bars.

        Args:
            x (str): The name of the variable to be plotted along the x axis.
            y (str): The name of the variable to be plotted along the y axis.
            hue (str): The name of the groupby variable.
            title (str): The title for the plot.
            orient (str): The vertical or horizontal orientation of the plot.
            ax (plt.axes): A matplotlib axes object.

        """
        ax = ax or VisualConfig.canvas().ax
        title = title or x
        sns.countplot(
            data=self._df,
            x=x,
            y=y,
            hue=hue,
            orient=orient,
            palette=VisualConfig.palette.blues_r,
            ax=ax,
        ).set(title=title)
        ax.bar_label(ax.containers[0], label_type="edge")
        return ax

    # ------------------------------------------------------------------------------------------------ #
    def histplot(
        self,
        x: str,
        y: str = None,
        hue: str = None,
        multiple: str = None,
        title: str = None,
        ax: plt.axes = None,
    ) -> plt.axes:
        """Produces univariate and bivariate histograms to show distributions of datasets.

        Args:
            x (str): The name of the variable to be plotted along the x axis.
            y (str): The name of the variable to be plotted along the y axis.
            hue (str): The name of the groupby variable.
            multiple (str): Approach to resolving multiple elements when semantic mapping creates subsets. Only relevant with univariate data.
            title (str): A title for the plot.
            ax (plt.axes): A matplotlib axes object.

        """
        if title is None:
            title = x if hue is None else x + " by " + hue
        ax = ax or VisualConfig.canvas().ax
        sns.histplot(
            data=self._df,
            x=x,
            y=y,
            hue=hue,
            multiple=multiple,
            palette=VisualConfig.palette.blues_r,
            kde=True,
            ax=ax,
        ).set(title=title)
        return ax

    # ------------------------------------------------------------------------------------------------ #
    def boxplot(
        self, x: str, y: str = None, hue: str = None, title: str = None, ax: plt.axes = None
    ) -> plt.axes:
        """Produces univariate and bivariate histograms to show distributions of datasets.

        Args:
            x (str): The name of the variable to be plotted along the x axis.
            y (str): The name of the variable to be plotted along the y axis.
            hue (str): The name of the groupby variable.
            title (str): A title for the plot.
            ax (plt.axes): A matplotlib axes object.

        """
        if title is None:
            title = x if hue is None else x + " by " + hue
        ax = ax or VisualConfig.canvas().ax
        sns.boxplot(
            data=self._df, x=x, y=y, hue=hue, palette=VisualConfig.palette.blues_r, ax=ax
        ).set(title=title)
        return ax

    # ------------------------------------------------------------------------------------------------ #
    def barplot(
        self,
        x: str,
        y: str = None,
        hue: str = None,
        errorbar: str = None,
        title: str = None,
        ax: plt.axes = None,
    ) -> plt.axes:
        """Produces barplot.

        Args:
            x (str): The name of the variable to be plotted along the x axis.
            y (str): The name of the variable to be plotted along the y axis.
            hue (str): The name of the groupby variable.
            errorbar (str): Name of variable containing error bar information.
            title (str): A title for the plot.
            ax (plt.axes): A matplotlib axes object.

        """
        if title is None:
            title = x if hue is None else x + " by " + hue
        ax = ax or VisualConfig.canvas().ax
        sns.barplot(
            data=self._df,
            x=x,
            y=y,
            hue=hue,
            palette=VisualConfig.palette.blues_r,
            ax=ax,
            errorbar=errorbar,
        ).set(title=title)
        return ax

    # ------------------------------------------------------------------------------------------------ #
    def scatterplot(self, x: str, y: str, title: str = None, ax: plt.axes = None) -> plt.axes:
        """Returns a matplotlib axes object containing a univariate or bivariate boxplot

        Args:
            x (str): The variables that specify positions on the x axes
            y (str): The variables that specify positions on the y axes
            title (str): Optional title for the axes object
            ax (plt.axes): Optional axes object upon which the plot will be rendered.
        """
        ax = ax or VisualConfig.canvas().ax
        sns.scatterplot(data=self._df, x=x, y=y, ax=ax)
        if title is not None:
            ax.set_title(title)
        return ax

    # ------------------------------------------------------------------------------------------------ #
    def jointplot(
        self, x: str, y: str, groupby: str = None, title: str = None, ax: plt.axes = None
    ) -> plt.figure:
        """Plots distributions of two numeric variables with univariate and bivariate graphs

        Args:
            x (str): The variables that specify positions on the x axes
            y (str): The variables that specify positions on the y axes
            groupby (str): Optional variable by which data distributions will be grouped
            title (str): Optional title for the axes object
            ax (plt.axes): Optional axes object upon which the plot will be rendered.
        """

        p = sns.jointplot(
            data=self._data, x=x, y=y, hue=groupby, palette=VisualConfig.palette.blues_r
        )

        if title is not None:
            p.fig.suptitle(title)
        p.fig.tight_layout()
        return p

    # ------------------------------------------------------------------------------------------------ #
    def wordcloud(
        self, x: str, max_words: int = 100, title: str = None, random_state: int = None
    ) -> None:
        """Produces a word cloud indicating the frequency distribution of words

        Args:
            x (str): The variables that specify positions on the x axes
            max_words (int): Maximum number of words to plot
            title (str): Optional title for the axes object
        """
        text = " ".join(word for word in self._data[x].values)
        plt.figure(figsize=VisualConfig.figsize)
        wc = WordCloud(
            width=VisualConfig.figsize[0] * 100,
            height=VisualConfig.figsize[1] * 100,
            max_words=max_words,
            random_state=random_state,
            stopwords=STOPWORDS,
            background_color="white",
        ).generate(text)
        plt.imshow(wc, interpolation="bilinear")
        if title is not None:
            plt.title(title)
        plt.axis("off")
        plt.show()
