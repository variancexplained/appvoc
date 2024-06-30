#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/domain/app/response.py                                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Sunday June 30th 2024 02:01:39 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Response Object for AppData Requests"""
from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import requests

from appvoc.data.acquisition.base import Response


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppDataResponse(Response):
    page: int = 0  # The response page
    size: int = 0  # Size of result in bytes
    records: int = 0  # The number of records returned
    content: pd.DataFrame = None  # The content of the response.

    def add_response(self, response: requests.Response, page: int) -> None:
        """Adds result content to the instance"""
        records_list = []
        records = response.json()["results"]
        for record in records:
            self.records += 1
            app = {}
            app["id"] = record["trackId"]
            app["name"] = record["trackName"]
            app["description"] = record["description"].strip()
            app["category_id"] = record["primaryGenreId"]
            app["category"] = record["primaryGenreName"]
            app["price"] = record.get("price", 0)
            app["developer_id"] = record["artistId"]
            app["developer"] = record["artistName"]
            app["rating"] = record["averageUserRating"]
            app["ratings"] = record["userRatingCount"]
            app["released"] = datetime.strptime(
                record["releaseDate"], "%Y-%m-%dT%H:%M:%f%z"
            )
            records_list.append(app)
        self.content = pd.DataFrame(data=records_list)
        self.size = self.content.memory_usage(deep=True)
        self.page = page
