#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/analysis/base.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 17th 2023 10:43:00 am                                                 #
# Modified   : Wednesday May 17th 2023 12:15:03 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Base Analysis Module"""
from abc import ABC
import logging
from functools import cached_property

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class Analyzer(ABC):
    """Abstract Base Class for data analytics subclasses.

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

    def describe(self, x: str) -> pd.DataFrame:
        """Computes descriptive statistics for the designated variable.

        Args:
            x (str)" A valid variable in the dataset.

        """
        return self._data[x].describe().to_frame().T
