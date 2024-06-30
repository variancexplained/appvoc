#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.14                                                                             #
# Filename   : /appvoc/domain/response.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday June 29th 2024 09:48:25 pm                                                 #
# Modified   : Saturday June 29th 2024 10:35:03 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Response Module"""
import logging
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

import pandas as pd

from appvoc.domain.entity import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Response(Entity):
    """Abstract base class encapsulating an HTTP response."""

    content: Any = None
    size: int = 0

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @abstractmethod
    def add_response(self, response: Any, *args, **kwargs) -> None:
        """Adds HTTP response content to the instance"""

    def get_result(self) -> pd.DataFrame:
        """Returns the result in DataFrame format"""
        return pd.DataFrame(self.content)

    def is_valid(self) -> bool:
        if self.content is None:
            return False
        else:
            return len(self.content) > 0
