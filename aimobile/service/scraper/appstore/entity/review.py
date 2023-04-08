#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/service/scraper/appstore/entity/review.py                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 2nd 2023 08:43:21 pm                                                   #
# Modified   : Saturday April 8th 2023 03:08:13 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
from datetime import datetime
from types import SimpleNamespace

from aimobile.service.scraper.base import Entity, AbstractScraperProject


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreReview(Entity):
    id: str = None
    app_id: str = None
    app_name: str = None
    collection_id: int = None
    collection: str = None
    category: str = None
    author_id: str = None
    author_name: str = None
    rating: float = None
    review_text: str = None
    helpful: int = None
    reviewed_at: str = None
    source: str = None
    created: datetime = None

    def from_result(self, result: dict, project: AbstractScraperProject) -> None:
        """Builds the Review object from the request and results

        Args:
            result (dict): Results from HTTP request
            request (AbstractRequest): Contains the HTTP request parameters
        """
        self.id = result["id"]
        self.app_id = self._extract_app_id(result["link"]["attributes"]["href"])
        self.app_name = app_name
        self.category = category
        self.author_id = result["author"]["uri"]["label"].split("id")[1]
        self.author_name = result["author"]["name"]["label"]
        self.rating = float(result["im:rating"]["label"])
        self.review_text = result["content"]["label"]
        self.helpful = int(result["im:voteSum"]["label"])
        self.reviewed_at = result["updated"]["label"]
        self.project_id = project_id
        self.source = "appstore"
        self.created = datetime.now()

    def _extract_app_id(self, url) -> str:
        """Extracts the app_id from the review url

        Args:
            url (str): A URL for the itunes review, containing the app_id
        """
        part = url.split("id=")[1]
        return part.split("&")[0]
