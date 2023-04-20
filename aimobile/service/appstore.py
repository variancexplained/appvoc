#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/service/appstore.py                                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday April 20th 2023 05:33:57 am                                                #
# Modified   : Thursday April 20th 2023 07:26:54 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from typing import Union
import logging

import pandas as pd
from aimobile.service.base import Scraper
from aimobile.infrastructure.dal.uow import UnitofWork
from aimobile.infrastructure.web.session import SessionHandler


# ------------------------------------------------------------------------------------------------ #
class AppStoreScraper(Scraper):
    """AppStore Scraper

    Scraper objects are responsible for iteratively obtaining, parsing, and returning page data
    from target urls to a controller responsible for persisting the results and managing the
    data acquisition effort. Much has been inspired by the itunes-app-scraper,
    which can be found at  https://github.com/digitalmethodsinitiative/itunes-app-scraper

    """

    def __init__(
        self, rest: SessionHandler, max_pages: int = None, limit: int = None, verbose: int = 10
    ) -> None:
        super().__init__()
        self._rest = rest
        self._max_pages = max_pages
        self._limit = limit
        self._verbose = verbose
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def search(self, term: str, page: int = 0) -> None:
        """Searches all apps matching the search term, parses and returns the result.

        Args:
            term (str): Search term
            verbose (int): Logging and progress verbosity factor, indicating the number of pages
                between progress resports to std.out.

        Return: Page data are parsed and returned in DataFrame format.
        """
        self._setup(term=term, page=page)

        # Iterate over the rest handler, collecting responses
        for rest in self._rest(
            term=term, page=page, max_pages=max_pages, limit=limit, handler=self._session_handler
        ):
            if request.status_code == 200:
                self._update_stats(request=request)
                self._persist(request=request)
                self._announce(request=request, verbose=verbose)

    def reviews(self, id: Union[int, str], verbose: int = 200, *args, **kwargs) -> pd.DataFrame:
        """Returns pages of reviews for the app designated by the id

        Args:
            id (Union[int,str]): App id
            verbose (int): Logging and progress verbosity factor, indicating the number of pages

        Return: Page data are parsed and returned in DataFrame format.between progress resports to std.out.
        """
