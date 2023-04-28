#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/service/appstore/base.py                                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 09:57:42 am                                                 #
# Modified   : Thursday April 27th 2023 03:04:18 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Service Base Module."""
from __future__ import annotations
from abc import ABC, abstractmethod


# ------------------------------------------------------------------------------------------------ #
class Header(ABC):
    """Base class for subclasses that provide HTTP Header Rotation"""

    @abstractmethod
    def __iter__(self) -> Header:
        """Initializes the iteration and returns an instance of itself."""

    @abstractmethod
    def __next__(self) -> dict:
        """Returns a header dictionary on each iteration."""
