#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/data/acquisition/appdata/result.py                                          #
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
    page: int = 0  # The result page
    pages: int = 0  # The number of pages cumulatively processed up to this result
    size: int = 0  # Size of result in bytes
    results: int = 0  # The number of records returned
    content: pd.DataFrame = None  # The content of the response.

    def add_response(self, response: requests.Response, page: int, pages: int) -> None:
        """Adds result content to the instance"""
        result_list = []
        results = response.json()["results"]
        for result in results:
            self.results += 1
            app = {}
            app["id"] = result["trackId"]
            app["name"] = result["trackName"]
            app["description"] = result["description"].strip()
            app["category_id"] = result["primaryGenreId"]
            app["category"] = result["primaryGenreName"]
            app["price"] = result.get("price", 0)
            app["developer_id"] = result["artistId"]
            app["developer"] = result["artistName"]
            app["rating"] = result["averageUserRating"]
            app["ratings"] = result["userRatingCount"]
            app["released"] = datetime.strptime(
                result["releaseDate"], "%Y-%m-%dT%H:%M:%f%z"
            )
            result_list.append(app)
        self.content = pd.DataFrame(data=result_list)
        self.size = self.content.memory_usage(deep=True)
        self.page = page
        self.pages = pages
