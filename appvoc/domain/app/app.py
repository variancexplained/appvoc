#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/domain/app/app.py                                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 10th 2023 11:42:46 pm                                               #
# Modified   : Sunday June 30th 2024 12:02:54 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from appvoc.domain.entity import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class App(Entity):
    """Encapsulates data for an app."""

    id: str
    name: str
    description: str
    category_id: str
    category: str
    price: float
    developer_id: str
    developer: str
    rating: float
    ratings: int
    released: datetime

    @classmethod
    def from_dict(cls, app: dict) -> App:
        return cls(
            id=app["id"],
            name=app["name"],
            description=app["description"],
            category_id=app["category_id"],
            category=app["category"],
            price=app["price"],
            developer_id=app["developer_id"],
            developer=app["developer"],
            rating=app["rating"],
            ratings=app["ratings"],
            released=app["released"],
        )
