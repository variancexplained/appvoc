#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/http/reviews.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 05:01:05 am                                                  #
# Modified   : Monday April 10th 2023 09:06:23 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Review Request Module"""
from __future__ import annotations
import logging
from datetime import datetime

import pandas as pd

from aimobile.scraper.appstore.http.base import RequestIterator, Handler, HTTPDefault
from aimobile.scraper.appstore.entity.request import AppStoreRequest


# ------------------------------------------------------------------------------------------------ #
class AppStoreReviewRequest(RequestIterator):
    def __init__(
        self,
        id: int,
        handler: Handler,
        page: int = 1,
        after: datetime = datetime.fromtimestamp(HTTPDefault.EPOCH),
        max_pages: int = HTTPDefault.MAX_PAGES,
    ) -> None:
        self._id = id  # App id
        self._handler = handler
        self._page = page
        self._after = after
        self._max_pages = max_pages
        self._pages = 0
        self._results = 0
        self._content_length = 0
        self._sessions = 1
        self._params = {}
        self._status_code = None
        self._result = None
        self._proxy = None

        self._host = "itunes.apple.com"
        self._url = None
        self._params = None
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def host(self) -> int:
        """Returns the current page processed."""
        return self._host

    @property
    def url(self) -> int:
        """Returns the current page processed."""
        return self._url

    @property
    def content_length(self) -> int:
        """Returns the length of the response"""
        return self._content_length

    @property
    def sessions(self) -> int:
        """Returns the length of the response"""
        return self._sessions

    @property
    def status_code(self) -> int:
        """Returns the length of the response"""
        return self._status_code

    @property
    def term(self) -> int:
        """Returns the search term"""
        return self._term

    @property
    def page(self) -> int:
        """Returns the current page processed."""
        return self._page

    @property
    def pages(self) -> int:
        """Returns the number of pages processed. May not be the same as page if started at nonzero.."""
        return self._pages

    @property
    def request(self) -> AppStoreRequest:
        return self._request

    @property
    def results(self) -> int:
        """Returns the number of results returned."""
        return self._results

    @property
    def result(self) -> int:
        """Returns result in DataFrame format."""
        return self._result

    @property
    def requested(self) -> int:
        """Datetime string at which the request was made."""
        return self._requested

    @property
    def responded(self) -> int:
        """Datetime string at which the response was received."""
        return self._responded

    @property
    def response_time(self) -> int:
        """Response time in microseconds."""
        return self._response_time

    @property
    def proxy(self) -> str:
        """Returns the proxy server used."""
        return self._proxy

    def __iter__(self) -> AppStoreReviewRequest:
        self._setup()
        return self

    def __next__(self) -> None:
        """Formats an itunes request for the next page"""
        while True:
            random_404s = 0
            if self._pages < self._max_pages:
                session = self._handler.get(url=self._url, params=self._params)
                response = session.response.json()["feed"]
                if session.status_code == 404:
                    random_404s += 1
                    if random_404s > 5:
                        self._teardown()
                else:
                    self._result = self._parse_response(response)
                    self._parse_session(session)
                    self._request = self._create_request_object()
                    self._page += 1
                    self._pages += 1
                    self._set_next_url()
                return self
            else:
                self._teardown()
                return self

    def summarize(self) -> None:
        """Prints a summary of the review scraping project."""
        print(self._project)

    def _setup(self) -> None:
        """Initializes the iterator"""
        self._pages = 0
        self._results = 0
        self._content_length = 0
        self._status_code = None
        self._result = None
        self._proxy = None
        self._set_url()

    def _teardown(self) -> None:
        raise StopIteration

    def _set_url(self) -> None:
        """Sets the initial request url"""
        self._url = (
            f"http://itunes.apple.com/us/rss/customerreviews/id={self._id}/sortBy=mostHelpful/json"
        )

    def _set_next_url(self) -> None:
        """Sets the URL based upon the starting page."""
        self._url = f"http://itunes.apple.com/us/rss/customerreviews/page={self._page}/id={self._id}/sortby=mosthelpful/json"

    def _parse_response(self, response: dict) -> pd.DataFrame:
        """Accepts a requests Response object and returns a DataFrame

        Args:
            response (dict): A requests Response object.

        """
        result_list = []
        for result in response["entry"]:
            review = {}
            review["app_id"] = self._id
            review["id"] = int(result["id"]["label"])
            review["author"] = result["author"]["name"]["label"]
            review["rating"] = int(result["im:rating"]["label"])
            review["title"] = result["title"]["label"]
            review["content"] = result["content"]["label"]
            review["vote_sum"] = int(result["im:voteSum"]["label"])
            review["vote_count"] = int(result["im:voteCount"]["label"])
            review["date"] = datetime.fromisoformat(result["updated"]["label"])
            review["source"] = self._host
            result_list.append(review)
        df = pd.DataFrame(data=result_list)
        self._results = len(result_list)
        return df

    def _parse_session(self, session: Handler):
        """Extracts data from the sesion object"""
        self._requested = session.requested
        self._responded = session.responded
        self._response_time = session.response_time
        self._content_length = session.content_length
        self._status_code = int(session.response.status_code)
        self._sessions = session.sessions
        self._proxy = session.proxy
        self._content_length = session.content_length

    def _create_request_object(self) -> AppStoreReviewRequest:
        """Creates the request object"""
        data = {
            "host": self._host,
            "term": self._id,
            "page": self._page,
            "content_length": self._content_length,
            "results": self._results,
            "requested": self._requested,
            "responded": self._responded,
            "response_time": self._response_time,
            "sessions": self._sessions,
            "proxy": self._proxy,
            "status_code": self._status_code,
        }

        return AppStoreRequest.from_dict(data=data)
