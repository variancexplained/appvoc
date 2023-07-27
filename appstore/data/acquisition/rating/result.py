#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/rating/result.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Wednesday July 26th 2023 01:28:56 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for AppData Requests"""
from dataclasses import dataclass
from typing import List

import pandas as pd
from appstore.data.acquisition.base import Result


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingResult(Result):
    scraper: str
    projects: List[pd.DataFrame]
    results: List[pd.DataFrame]
    total: int = 0
    success: int = 0
    fail: int = 0
