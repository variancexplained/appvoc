#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/data/acquisition/appdata/result.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 01:59:31 pm                                                  #
# Modified   : Tuesday August 29th 2023 09:09:52 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines the Result Object for AppData Requests"""
from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import requests

from appvoc.data.acquisition.base import Result


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppDataResult(Result):
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
            appdata = {}
            appdata["id"] = result["trackId"]
            appdata["name"] = result["trackName"]
            appdata["description"] = result["description"].strip()
            appdata["category_id"] = result["primaryGenreId"]
            appdata["category"] = result["primaryGenreName"]
            appdata["price"] = result.get("price", 0)
            appdata["developer_id"] = result["artistId"]
            appdata["developer"] = result["artistName"]
            appdata["rating"] = result["averageUserRating"]
            appdata["ratings"] = result["userRatingCount"]
            appdata["released"] = datetime.strptime(
                result["releaseDate"], "%Y-%m-%dT%H:%M:%f%z"
            )
            result_list.append(appdata)
        self.content = pd.DataFrame(data=result_list)
        self.size = self.content.memory_usage(deep=True)
        self.page = page
        self.pages = pages
