#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/scraper/base/controller.py                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 06:48:14 am                                                #
# Modified   : Saturday April 29th 2023 06:34:30 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod
import requests
from typing import Union

from aimobile.data.acquisition.scraper.base.request import RequestGenerator, Request
from aimobile.data.acquisition.scraper.base.result import Result


# ------------------------------------------------------------------------------------------------ #
class Controller(ABC):
    @abstractmethod
    def create_generator(self) -> RequestGenerator:
        """Creete Request Generator"""

    @abstractmethod
    def submit_request(self, request: Request) -> requests.Response:
        """Submit request and return Response object."""

    @abstractmethod
    def parse_response(self, response: requests.Response) -> Result:
        """Parse the response and return a Result object"""

    @abstractmethod
    def persist_result(self, result: Result) -> None:
        """Save the result to the target repository."""

    @abstractmethod
    def register_tasks(self, result: Result) -> None:
        """Register the Project and Task objects."""

    @abstractmethod
    def start_project(self, result: Result) -> None:
        """Create the project repository"""

    @abstractmethod
    def update_project(self, result: Result) -> None:
        """Create the project repository"""

    @abstractmethod
    def complete_project(self, result: Result) -> None:
        """Create the project repository"""

    @abstractmethod
    def _get_progress(self) -> Union[list, int]:
        """Adjust Generator, eliminating redundancy."""
