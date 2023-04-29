#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/base/scraper.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 01:11:30 am                                                #
# Modified   : Saturday April 29th 2023 06:59:15 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import ABC, abstractmethod


# ------------------------------------------------------------------------------------------------ #
class Scraper(ABC):
    """Defines the Scraper interface for app scraper objects returning app data in batch pages"""

    @abstractmethod
    def __iter__(self) -> Scraper:
        """Returns a RequestGenerator object"""

    @abstractmethod
    def __next__(self) -> Scraper:
        """Generates the next Request object"""
