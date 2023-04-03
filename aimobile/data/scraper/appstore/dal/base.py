#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/scraper/appstore/dal/base.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 06:00:34 am                                                  #
# Modified   : Sunday April 2nd 2023 07:51:17 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class Repo(ABC):
    """Abstract base class for app data, review repositories."""

    @abstractmethod
    def get(self, *args, **kwargs) -> pd.DataFrame:
        """Queries the database and returns a result in DataFrame format."""

    @abstractmethod
    def add(self, data: pd.DataFrame) -> None:
        """Adds a DataFrame to the Database

        Args:
            data (pd.DataFrame): The data
        """

    @abstractmethod
    def update(self, data: pd.DataFrame) -> None:
        """Updates the table with the existing data.  This is essentially a replace operation

        Args:
            data (pd.DataFrame): The data to replace existing data

        """
