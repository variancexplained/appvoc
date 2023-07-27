#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/infrastructure/web/base.py                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 03:22:06 am                                                 #
# Modified   : Tuesday July 25th 2023 01:04:50 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Web Infrastructure Base Module"""
from __future__ import annotations
from abc import ABC, abstractmethod
import logging


# ------------------------------------------------------------------------------------------------ #
class Header(ABC):
    """Interface for classes that serve up HTTP Headers."""

    @abstractmethod
    def __iter__(self):
        """Initializes the iteration"""

    @abstractmethod
    def __next__(self):
        """Returns a randomly selected header."""


# ------------------------------------------------------------------------------------------------ #
class Throttle(ABC):
    """Base class for HTTP request rate limiters"""

    def __init__(self) -> None:
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @abstractmethod
    def delay(self, *args, **kwargs) -> int:
        """Returns a delay time in milliseconds"""


# ------------------------------------------------------------------------------------------------ #
# Servers provided courtesy of Geonode
PROXY_SERVERS = [
    "rotating-residential.geonode.com:9000",
    "rotating-residential.geonode.com:9001",
    "rotating-residential.geonode.com:9002",
    "rotating-residential.geonode.com:9003",
    "rotating-residential.geonode.com:9004",
    "rotating-residential.geonode.com:9005",
    "rotating-residential.geonode.com:9006",
    "rotating-residential.geonode.com:9007",
    "rotating-residential.geonode.com:9008",
    "rotating-residential.geonode.com:9009",
    "rotating-residential.geonode.com:9010",
]
