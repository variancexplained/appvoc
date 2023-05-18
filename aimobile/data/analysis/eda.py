#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/analysis/eda.py                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday May 16th 2023 09:35:22 pm                                                   #
# Modified   : Wednesday May 17th 2023 08:29:41 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging
from functools import cache, cached_property

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

from aimobile import Visual

sns.set_style(Visual.style)
sns.set_palette = sns.dark_palette(
    Visual.palette.color, reverse=Visual.palette.reverse, as_cmap=Visual.palette.as_cmap
)

# ------------------------------------------------------------------------------------------------ #


class EDA:
    """Class used to perform exploratory data analysis on a pandas Dataset.

    Args:
        data (pd.DataFrame): The data to be profiled in pandas DataFrame format.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        self._data = data
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @cached_property
    def overview(self) -> pd.DataFrame:
        """Provides an overview at the dataset level."""
        nvars = self._data.shape[1]
        nrows = self._data.shape[0]
        ncells = nvars * nrows
        nmissing = self._data.isna().sum().sum()
        pmissing = nmissing / ncells * 100
        ndups = nrows - self._data.drop_duplicates().shape[0]
        pdups = ndups / nrows * 100
        size = self._data.memory_usage(deep=True).sum().sum()
        d = {
            "Number of Variables": nvars,
            "Number of Observations": nrows,
            "Number of Cells": ncells,
            "Missing Cells": nmissing,
            "Missing Cells (%)": round(pmissing, 2),
            "Duplicate Rows": ndups,
            "Duplicate Rows (%)": round(pdups, 2),
            "Size (Bytes)": size,
        }
        return pd.DataFrame.from_dict(data=d, orient="index", columns=[""])

    @cached_property
    def summary(self) -> pd.DataFrame:
        """Prints an overview containing dataset statistics and insights."""
        overview = self._data.dtypes.to_frame().reset_index()
        overview.columns = ["Column", "Dtype"]
        overview["Valid"] = self._data.count().values
        overview["Missing"] = self._data.isna().sum().values
        overview["Validity"] = overview["Valid"] / self._data.shape[0]
        overview["Unique"] = self._data.nunique().values
        overview["Cardinality"] = overview["Unique"] / self._data.shape[0]
        overview["Size"] = (
            self._data.memory_usage(deep=True, index=False).to_frame().reset_index()[0]
        )
        overview = round(overview, 2)
        return overview

    def astype(self, vars: list, dtype: str) -> None:
        """Converts a list of variables to the designated data type.

        Args:
            vars (list[str]): List of variables to convert to the designated data type.
            dtype (str): The pandas dtype to which the variables will be converted.
        """

        self._data[vars] = self._data[vars].astype(dtype)

    @cache
    def describe(self, x: str) -> pd.DataFrame:
        """Computes descriptive statistics for the designated variable.

        Args:
            x (str)" A valid variable in the dataset.

        """
        return self._data[x].describe().to_frame().T

    @cache
    def describe_text(self, x: str) -> pd.DataFrame:
        """Computes descriptive statistics for the designated text variable.

        Args:
            x (str)" A valid variable in the dataset.

        """

        return self._data[x].str.len().describe().to_frame().T

    @cache
    def value_counts(self, x: str, threshold: int = None) -> pd.DataFrame:
        """Returns the value counts for the designated variable

        Args:
            x (str)" A valid variable in the dataset.
            threshold (int): The minimum threshold for value counts to return

        """
        counts = self._data[x].value_counts().reset_index()
        counts.columns = [x, "count"]
        if threshold is not None:
            counts = counts[counts["count"] >= threshold]
        return counts

    @cache
    def histogram(
        self, x: str, grouping: str = None, kde: bool = True, title: str = None, ax: plt.axes = None
    ) -> plt.axes:
        """Returns a matplotlib axes object containing a univariate or bivariate histogram

        Args:
            x (str): The variables that specify positions on the x axes
            grouping (str): Optional variable by which data distributions will be grouped
            kde (bool): Whether to plot kernel density estimation.
            title (str): Optional title for the axes object
            ax (plt.axes): Optional axes object upon which the plot will be rendered.
        """
        ax = ax or self._getax()
        sns.histplot(data=self._data, x=x, hue=grouping, ax=ax, kde=kde)
        if title is not None:
            ax.set_title(title)
        return ax

    @cache
    def barplot(self, x: str, y: str, title: str = None, ax: plt.axes = None) -> plt.axes:
        """Returns a matplotlib axes object containing a univariate or bivariate histogram

        Args:
            x (str): The variables that specify positions on the x axes.
            y (str): The variables that specify positions on the y axes.
            title (str): Optional title for the axes object
            ax (plt.axes): Optional axes object upon which the plot will be rendered.
        """
        ax = ax or self._getax()
        sns.barplot(data=self._data, x=x, y=y, ax=ax, palette=Visual.palette.name)
        if title is not None:
            ax.set_title(title)
        return ax

    @cache
    def boxplot(
        self, x: str, grouping: str = None, title: str = None, ax: plt.axes = None
    ) -> plt.axes:
        """Returns a matplotlib axes object containing a univariate or bivariate boxplot

        Args:
            x (str): The variables that specify positions on the x axes
            grouping (str): Optional variable by which data distributions will be grouped
            title (str): Optional title for the axes object
            ax (plt.axes): Optional axes object upon which the plot will be rendered.
        """
        ax = ax or self._getax()
        sns.boxplot(data=self._data, x=x, y=grouping, ax=ax)
        if title is not None:
            ax.set_title(title)
        return ax

    @cache
    def scatterplot(self, x: str, y: str, title: str = None, ax: plt.axes = None) -> plt.axes:
        """Returns a matplotlib axes object containing a univariate or bivariate boxplot

        Args:
            x (str): The variables that specify positions on the x axes
            y (str): The variables that specify positions on the y axes
            title (str): Optional title for the axes object
            ax (plt.axes): Optional axes object upon which the plot will be rendered.
        """
        ax = ax or self._getax()
        sns.scatterplot(data=self._data, x=x, y=y, ax=ax)
        if title is not None:
            ax.set_title(title)
        return ax

    @cache
    def jointplot(self, x: str, y: str, grouping: str = None, title: str = None) -> plt.figure:
        """Plots distributions of two numeric variables with univariate and bivariate graphs

        Args:
            x (str): The variables that specify positions on the x axes
            y (str): The variables that specify positions on the y axes
            grouping (str): Optional variable by which data distributions will be grouped
            title (str): Optional title for the axes object
            ax (plt.axes): Optional axes object upon which the plot will be rendered.
        """

        p = sns.jointplot(data=self._data, x=x, y=y, hue=grouping, palette="Blues")

        if title is not None:
            p.fig.suptitle(title)
        p.fig.tight_layout()
        return p

    @cache
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
        plt.figure(figsize=Visual.figsize)
        wc = WordCloud(
            width=Visual.figsize[0] * 100,
            height=Visual.figsize[1] * 100,
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

    def _getax(self) -> plt.axes:
        """Returns a standard plt axes object"""
        _, ax = plt.subplots(figsize=Visual.figsize)
        return ax
