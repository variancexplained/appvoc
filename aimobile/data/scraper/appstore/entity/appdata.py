#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Opportunity Discovery in Mobile Applications                             #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/scraper/appstore/entity/appdata.py                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 2nd 2023 08:43:21 pm                                                   #
# Modified   : Friday April 7th 2023 06:31:24 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
from datetime import datetime

from aimobile.data.scraper.base import Entity


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreAppData(Entity):
    id: str = None
    name: str = None
    subtitle: str = None
    category_id: int = None
    category: str = None
    price: float = None
    ave_rating: float = None
    ratings: int = None
    ipad: bool = False
    iphone: bool = False
    ipod: bool = False
    developer_name: str = None
    source: str = None
    created: datetime = None

    @classmethod
    def from_dict(cls, appdata: dict) -> None:
        """Builds the AppStore AppData object from an appstore results

        Args:
            appdata (dict): Results from HTTP request
        """
        watch = True if "watch" in appdata["deviceFamilies"] else False
        ipad = True if "ipad" in appdata["deviceFamilies"] else False
        iphone = True if "iphone" in appdata["deviceFamilies"] else False
        ipod = True if "ipod" in appdata["deviceFamilies"] else False

        return cls(
            id=appdata["id"],
            name=appdata["name"],
            subtitle=appdata["subtitle"],
            category_id=appdata["category_id"],
            category=appdata["category"],
            price=appdata["offers"][0]["price"],
            ave_rating=appdata["userRating"].get("value", 0),
            ratings=appdata["userRating"].get("ratingCount", 0),
            watch=watch,
            ipad=ipad,
            iphone=iphone,
            ipod=ipod,
            developer_name=appdata["artistName"],
            developer_id=appdata["artistId"],
            source="appstore",
            created=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        )
