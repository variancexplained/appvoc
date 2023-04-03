#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/scraper/appstore/entity/appdata.py                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 2nd 2023 08:43:21 pm                                                   #
# Modified   : Monday April 3rd 2023 06:26:29 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
from datetime import datetime

from aimobile.data.scraper.base import Entity, AbstractRequest


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreAppData(Entity):
    id: str = None
    name: str = None
    description: str = None
    collection_id: int = None
    collection: str = None
    category: str = None
    price: float = None
    average_rating: float = None
    ratings: int = None
    developer_id: str = None
    developer_name: str = None
    source: str = None
    created: datetime = None

    def from_result(self, result: dict, request: AbstractRequest) -> None:
        """Builds the AppData object from an appstore request and results

        Args:
            result (dict): Results from HTTP request
            request (AbstractRequest): Contains the HTTP request parameters
        """
        self.id = result["trackId"]
        self.name = result["trackName"]
        self.description = result["description"]
        self.collection_id = project.collection_id
        self.collection = project.collection
        self.category = result["primaryGenreName"]
        self.price = result["price"]
        self.average_rating = result["averageUserRating"]
        self.ratings = result["userRatingCount"]
        self.developer_id = result["artistId"]
        self.developer_name = result["artistName"]
        self.source = "appstore"
        self.created = datetime.now()
