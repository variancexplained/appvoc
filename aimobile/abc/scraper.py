#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/abc/scraper.py                                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 19th 2023 06:42:28 am                                               #
# Modified   : Thursday April 20th 2023 01:04:38 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod
from typing import Union


# ------------------------------------------------------------------------------------------------ #
class Scraper(ABC):
    """Abstract base class defining the interface for Scraper objects"""

    @abstractmethod
    def search(self, term: str, *args, **kwargs) -> list[dict]:
        """Returns a DataFrame containing app data.

        Args:
            term (str): The search term
        """

    @abstractmethod
    def get_reviews(self, id: Union(int, str), *args, **kwargs) -> list[dict]:
        """Returns reviews for app designated by the id

        Args:
            id (Union[str,int]): The app id.
        """
