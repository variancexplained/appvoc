#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/project.py                                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 03:47:36 pm                                                  #
# Modified   : Tuesday July 25th 2023 01:05:09 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
import itertools
from datetime import datetime

import pandas as pd

# ------------------------------------------------------------------------------------------------ #
IMMUTABLE_TYPES: tuple = (str, int, float, bool, type(None))
SEQUENCE_TYPES: tuple = (list, tuple)
# ------------------------------------------------------------------------------------------------ #
counter = itertools.count()
# ------------------------------------------------------------------------------------------------ #


@dataclass
class Project(ABC):
    """Project"""

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> Project:
        """Takes a DataFrame and creates a Project object."""

    def as_dict(self) -> dict:
        """Returns a dictionary representation of the the Config object."""
        return {k: self._export_config(v) for k, v in self.__dict__.items()}

    @classmethod
    def _export_config(cls, v):  # pragma: no cover
        """Returns v with Configs converted to dicts, recursively."""
        if isinstance(v, IMMUTABLE_TYPES):
            return v
        elif isinstance(v, SEQUENCE_TYPES):
            return type(v)(map(cls._export_config, v))
        elif isinstance(v, datetime):
            return v
        elif isinstance(v, dict):
            return v
        elif hasattr(v, "as_dict"):
            return v.as_dict()
        else:
            """Else nothing. What do you want?"""

    def as_df(self) -> pd.DataFrame:
        """Returns the project in DataFrame format"""
        d = self.as_dict()
        return pd.DataFrame(data=d, index=[0])
