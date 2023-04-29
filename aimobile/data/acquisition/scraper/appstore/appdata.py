#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/scraper/appstore/appdata.py                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 06:04:51 am                                                #
# Modified   : Saturday April 29th 2023 06:47:39 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations
import logging
from dataclasses import dataclass, field
import sys
from typing import Union, Dict
from datetime import datetime

import pandas as pd
import requests

from aimobile.data.repo.uow import UoW
from aimobile.infrastructure.web.session import SessionHandler
from aimobile.data.acquisition.scraper.base.controller import Controller
from aimobile.data.acquisition.scraper.base.response import ResponseParser
from aimobile.data.acquisition.scraper.base.request import RequestGenerator, Request
from aimobile.data.acquisition.scraper.base.result import Result
from aimobile.data.acquisition.scraper.base.management import Project, Task


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreAppDataRequest(Request):
    url: str = None
    params: Dict[str:str] = field(default_factory=dict)
    headers: Dict[str:str] = field(default_factory=dict)


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppStoreAppDataResult(Result):
    controller: str = None
    term: str = None
    page: int = 0
    pages: int = 0
    valid: bool = False
    size: int = 0
    content: pd.DataFrame = None


# ------------------------------------------------------------------------------------------------ #
class AppStoreAppDataRequestGenerator(RequestGenerator):
    """App Store App Data Request Generator

    Args:
        uow (UoW): Unit of Work class Containing the Source, Target, Project and Task Repos
        term (str): The search term or category for the task.
        start_page (int): The page at which scraping starts.
        limit (int): The maximum number of records to return on a request.
    """

    __scheme = "https"
    __host = "itunes.apple.com"
    __command = "search?"
    __media = "software"
    __country = "us"
    __explicit = "yes"
    __lang = "en-us"
    __limit = 200

    def __init__(
        self,
        term: str,
        start_page: int = 0,
        limit: int = 200,
    ) -> None:
        super().__init__()
        self._term = term
        self._start_page = start_page
        self._page = start_page
        self._limit = limit or self.__limit

        self._url = f"{self.__scheme}://{self.__host}/{self.__command}"
        self._pages = 1

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def __iter__(self) -> RequestGenerator:
        return self

    def __next__(self) -> Request:
        """Returns the next Request object."""
        return self._generate_request()

    def _generate_request(self) -> None:
        """Creates the request object."""
        params = {
            "media": self.__media,
            "term": self._term,
            "country": self.__country,
            "lang": self.__lang,
            "explicit": self.__explicit,
            "limit": self._limit,
            "offset": self._page * self._limit,
        }

        request = AppStoreAppDataRequest(
            url=self._url,
            start_page=self._start_page,
            page=self._page,
            pages=self._pages,
            limit=self._limit,
            params=params,
        )
        self._page += 1
        self._pages += 1
        return request


# ------------------------------------------------------------------------------------------------ #
class AppStoreAppDataParser(ResponseParser):
    """Parses the response from an requests.Response object"""

    def __init__(self, response: requests.Response) -> None:
        self._response = response

    def parse_response(
        self, request: Request, response: requests.Response
    ) -> AppStoreAppDataResult:
        """Parses the requests.Response object and returns a Result object."""
        if response.status_code == 200:
            result_list = []
            results = response.json()["results"]
            for result in results:
                appdata = {}
                appdata["id"] = result["trackId"]
                appdata["name"] = result["trackName"]
                appdata["description"] = result["description"]
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
                appdata["source"] = self.__host
                result_list.append(appdata)
            df = pd.DataFrame(data=result_list)
            return AppStoreAppDataResult(request=request, valid=True, size=len(df), content=df)
        else:
            msg = f"Invalid response encountered. Status code = {response.status_code}"
            self._logger.error(msg)
            return AppStoreAppDataResult(request=request, valid=False, size=0, content=None)


# ------------------------------------------------------------------------------------------------ #
class AppStoreAppDataController(Controller):
    def __init__(
        self,
        uow: UoW,
        term: str,
        max_pages: int = sys.maxsize,
        session: SessionHandler = SessionHandler,
    ) -> None:
        super().__init__()
        self._uow = uow
        self._term = term
        self._max_pages = max_pages
        self._request_generator = None
        self._response = None
        self._result = None
        self._project = None
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def create_generator(self) -> RequestGenerator:
        """Create Request Generator"""
        start_page = self._get_progress()
        generator = AppStoreAppDataRequestGenerator(term=self._term, start_page=start_page)
        self._request_generator = iter(generator)

    def submit_request(self) -> requests.Response:
        """Submit request and return Response object."""
        self._request = next(self._request_generator)
        if self._request.page < self._max_pages:
            self._response = self._session.get(url=self._request.url, params=self._request.params)
        else:
            msg = f"Task terminated: Reached {self._request.page} pages, the maximum."
            self._logger.info(msg)

    def parse_response(self) -> Result:
        """Parse the response and return a Result object"""
        self._result = AppStoreAppDataParser(self._request, self._response)
        self._result.controller = self.__class__.__name__
        self._result.term = self._term

    def persist_result(self) -> None:
        """Save the result to the target repository."""
        self._uow.target_repo.add(data=self._result.content)

    def create_tasks(self) -> None:
        """Register the Project and Task objects."""
        lod = []
        results = self._result.content
        id = self._result.controller + "_" + self._result.term
        for i, row in results.iterrows:
            task = Task.create(
                id=id,
                controller=self._result.controller,
                term=self._result.term,
                app_id=row["id"],
                page=self._result.request.page,
            )
            d = task.as_dict()
            lod.append(d)
        tasks = pd.DataFrame(data=lod)
        self._uow.task_repo.add(data=tasks)

    def create_project(self) -> Project:
        """Create the project repository"""
        id = self._result.controller + "_" + self._result.term
        self._project = Project(
            id=id,
            controller=self._result.controller,
            term=self._result.term,
            start_page=self._result.request.start_page,
            pages=self._result.request.pages,
        )
        self._uow.project_repo.add(data=self._project)

    def update_project(self) -> Project:
        self._project.end_page += self._result.request.pages
        self._project.pages += self._result.request.pages
        self._project.ended = datetime.now()
        self._uow.project_repo.update(data=self._project)

    def _get_progress(self) -> Union[list, int]:
        """Adjust Generator, eliminating redundancy."""
        project_id = self.__class__.__name__ + "_" + self._term
        projects = self._uow.project_repo.get(id=project_id)
        if len(projects) > 0:
            projects.sort_values(by="started", ascending=False, inplace=True)
            return projects["end_page"][0]
        else:
            return 0
