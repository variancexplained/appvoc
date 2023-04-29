#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/base/project.py                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 01:07:32 am                                                #
# Modified   : Saturday April 29th 2023 06:56:05 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod

from dependency_injector.wiring import inject, Provide

from aimobile.data.repo.uow import UoW
from aimobile.container import AIMobileContainer


# ------------------------------------------------------------------------------------------------ #
class Project(ABC):
    """Scraper Project responsible for scraping and persisting a target or series of URLs."""

    @inject
    def __init__(
        self,
        uow: UoW = Provide[AIMobileContainer.data.uow],
    ) -> None:
        self.uow = uow
        self._project = None

    @property
    def uow(self) -> UoW:
        return self._uow

    @uow.setter
    def uow(self, uow: UoW) -> None:
        self._uow = uow

    @property
    def scraper(self, scraper: Scraper) -> Scraper:
        return self._scraper

    @scraper.setter
    def scraper(self, scraper)

    @abstractmethod
    def scrape(self, *args, **kwargs) -> None:
        """Scrapes data from the target url"""

    def start_project(self, term: str) -> int:
        """Starts a project, adds it to the repository, and returns the start page.

        A project is identified by the concatenation of the Project and the term
        parameter. The project repository tracks each project, recording the start, end,
        and number of pages processed. Each project starts by checking the
        repository for an existing project or projects with the same identity
        and if one or more exist, the end_page is obtained from the project with the
        last start datetime and this becomes the current project start page.
        If no project with the same id is found, zero is assigned as the current
        project start page, and is returned to the calling method.

        Args:
            term (str): The term or category for the project.

        Returns: start_page

        """
        start_page = 0
        id = self.__class__.__name__ + "_" + term
        self._project = Project(id=id, Project=self.__class__.__name__, searchagory=term)
        df = self.uow.project_repository.get(id=id)
        if len(df) > 0:
            df.sort_values(by="started", ascending=False, inplace=True)
            start_page = df["end_page"][0]
            self._project.start_page = start_page

        self.uow.project_repository.add(data=self._project)
        return start_page

    def update_project(self, pages: int) -> None:
        self._project.update(pages=pages)
        self.uow.project_repository.update(data=self._project)

    def complete_project(self) -> None:
        self._project.complete()
        self.uow.project_repository.update(data=self._project)
