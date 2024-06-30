#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/domain/request.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday August 9th 2023 04:52:24 pm                                               #
# Modified   : Saturday June 29th 2024 10:00:39 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass

import pandas as pd

from appvoc.domain.entity import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Request(Entity):
    """Abstract base class encapsulating a request to be sent to web infrastructure layer"""

    @classmethod
    @abstractmethod
    def from_series(cls, request: pd.Series) -> Request:
        """Abstract class method creating a Request object."""
