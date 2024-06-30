#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/domain/app/request.py                                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday August 9th 2023 04:52:24 pm                                               #
# Modified   : Sunday June 30th 2024 02:01:39 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

from dataclasses import dataclass

from appvoc.domain.request import Request


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppDataRequest(Request):
    id: str = None
    category_id: str = None
    last_index: int = 0

    @classmethod
    def from_dict(cls, request: dict) -> AppDataRequest:

        return cls(
            id=request["id"],
            category_id=request["category_id"],
            last_index=request["last_index"],
        )
