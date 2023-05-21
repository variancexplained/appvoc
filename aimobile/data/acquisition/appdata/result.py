#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/appstore/appdata/result.py                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Thursday May 4th 2023 11:37:14 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for AppData Requests"""
from dataclasses import dataclass
import pandas as pd

from aimobile.data.acquisition.base import Result


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppDataResult(Result):
    page: int  # The result page
    pages: int  # The number of pages cumulatively processed up to this result
    size: int  # Size of result in bytes
    results: int  # The number of records returned
    content: pd.DataFrame  # The content of the response.
