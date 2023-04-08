#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Opportunity Discovery in Mobile Applications                             #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/scraper/appstore/service/builder.py                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 5th 2023 04:44:18 am                                                #
# Modified   : Thursday April 6th 2023 12:56:27 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module responsible for construction of the App Store Scraper Service"""
from abc import ABC, abstractmethod
from urllib3.util import Retry

from dependency_injector.wiring import Provide, inject

from aimobile.data.scraper.utils.io import IOService
from aimobile.data.scraper.utils.http import TimeoutHTTPAdapter
from aimobile.data.scraper.utils.http import HTTPRequest
from aimobile.data.scraper.appstore.service.appdata import AppStoreScraper
from aimobile.data.scraper.appstore.entity.project import AppStoreProject
from aimobile.data.scraper.appstore.dal.datacentre import DataCentre
from aimobile.container import AIMobile


# ------------------------------------------------------------------------------------------------ #
class Builder(ABC):
    """Builder interface for creating scraper objects"""

    @property
    @abstractmethod
    def config(self) -> dict:
        """Returns the project configuration"""

    @config.setter
    @abstractmethod
    def config(self, config_filepath) -> None:
        """Reads and sets the configuration"""

    @abstractmethod
    def build_project(self) -> None:
        """Builds the Project"""

    @abstractmethod
    def build_retry_strategy(self) -> None:
        """Constructs the request retry object from  config."""

    @abstractmethod
    def build_timeout_adapter(self) -> None:
        """Constructs the HTTP timeout adapteer with the retry object."""

    @abstractmethod
    def build_requests_class(self) -> None:
        """Constructs the class that executes the http requests"""

    @abstractmethod
    def build_scraper(self) -> None:
        """Constructs the appstore app data scraper"""


# ------------------------------------------------------------------------------------------------ #
class AppStoreAppDataScraperBuilder(Builder):
    """Constructs the builder for the app store scraper."""

    @inject
    def __init__(self, datacentre: DataCentre = Provide[AIMobile.datacentre.appstore]) -> None:
        self._config = None
        self._datacentre = datacentre

    @property
    def project(self) -> AppStoreProject:
        return self._project

    @property
    def retry_strategy(self) -> Retry:
        return self._retry

    @property
    def timeout(self) -> TimeoutHTTPAdapter:
        return self._timeout

    @property
    def http_requests(self) -> HTTPRequest:
        return self._http_request

    @property
    def scraper(self) -> AppStoreScraper:
        return self._scraper

    @property
    def config(self) -> dict:
        """Returns the project configuration"""
        return self._config

    def build_project(self, config_filepath: str) -> None:
        """Builds the Project"""
        self._config = IOService.read(config_filepath)
        project = self._config["scraper"]["appstore"]["project"]
        self._project = AppStoreProject(
            name=project["name"],
            description=project["description"],
            term=project["term"],
            max_pages=project["max_pages"],
            page_limit=project["page_limit"],
            country=project["country"],
            lang=project["lang"],
            timeout=project["timeout"],
            delay=project["delay"],
            sessions=project["sessions"],
            source=project["source"],
        )

    def build_retry_strategy(self) -> None:
        """Constructs the request retry object from  config."""
        retry_params = self._config["scraper"]["appstore"]["project"]["retry"]
        self._retry = Retry(
            total=retry_params["total_retries"],
            backoff_factor=retry_params["backoff_factor"],
            status_forcelist=retry_params["status_forcelist"],
            allowed_methods=retry_params["allowed_methods"],
            raise_on_redirect=retry_params["raise_on_redirect"],
            raise_on_status=retry_params["raise_on_status"],
        )

    def build_timeout_adapter(self) -> None:
        """Constructs the HTTP timeout adapteer with the retry object."""
        self._timeout = TimeoutHTTPAdapter(
            timeout=self._config["scraper"]["appstore"]["project"]["timeout"],
            max_retries=self._retry,
        )

    def build_requests_class(self) -> None:
        """Constructs the class that executes the http requests"""
        self._http_request = HTTPRequest(
            timeout=self._timeout,
            delay=self._config["scraper"]["appstore"]["project"]["delay"],
        )

    def build_scraper(self) -> None:
        """Constructs the appstore app data scraper"""
        self._scraper = AppStoreScraper(
            project=self._project, requests=self._http_request, datacentre=self._datacentre
        )
