#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/appdata/result.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Tuesday July 25th 2023 01:05:03 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for AppData Requests"""
from dataclasses import dataclass
import pandas as pd

from appstore.data.acquisition.base import Result


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppDataResult(Result):
    page: int  # The result page
    pages: int  # The number of pages cumulatively processed up to this result
    size: int  # Size of result in bytes
    results: int  # The number of records returned
    content: pd.DataFrame  # The content of the response.
