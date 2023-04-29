#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/scraper/base/request.py                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 06:09:20 am                                                #
# Modified   : Saturday April 29th 2023 06:47:45 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Request(ABC):
    url: str = None
    params: Dict[str:str] = field(default_factory=dict)
    headers: Dict[str:str] = field(default_factory=dict)


# ------------------------------------------------------------------------------------------------ #


class RequestGenerator(ABC):
    @abstractmethod
    def __iter__(self) -> RequestGenerator:
        """Returns a RequestGenerator object"""

    @abstractmethod
    def __next__(self) -> Request:
        """Generates the next Request object"""
