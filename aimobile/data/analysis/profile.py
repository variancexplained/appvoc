#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/analysis/profile.py                                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 17th 2023 10:31:14 am                                                 #
# Modified   : Wednesday May 17th 2023 12:13:49 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Data Profile Module."""
from typing import Union

import pandas as pd

from aimobile.data.analysis.base import Analyzer


class Profiler(Analyzer):
    """Encapsulates methods designed to discover and analyze data quality within a dataset.

    Args:
        data (pd.DataFrame): Data to be profiled in pandas DataFrame format.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        self._data = data

    def value_counts(self, x: Union[str, list], threshold: int = None) -> pd.DataFrame:
        """Returns the value counts for the designated variable or list of variables.

        Args:
            x (Union[str, list[str]]): A string or list of strings denoting variable(s) in the dataset.
            threshold (int): The minimum threshold for value counts to return

        """
        x = [x] if isinstance(x, str) else x

        counts = self._data[x].value_counts().reset_index()
        x.append("count")
        counts.columns = x
        if threshold is not None:
            counts = counts[counts["count"] >= threshold]
        return counts
