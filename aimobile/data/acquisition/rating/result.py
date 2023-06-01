#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /aimobile/data/acquisition/rating/result.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Thursday June 1st 2023 11:16:25 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for AppData Requests"""
from dataclasses import dataclass
from typing import List

import pandas as pd
from aimobile.data.acquisition.base import Result


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingResult(Result):
    scraper: str
    projects: List[pd.DataFrame]
    results: List[pd.DataFrame]
