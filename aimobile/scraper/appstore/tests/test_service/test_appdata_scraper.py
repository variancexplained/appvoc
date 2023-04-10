#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/tests/test_service/test_appdata_scraper.py               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 02:57:14 pm                                                 #
# Modified   : Monday April 10th 2023 06:42:36 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import inspect
from datetime import datetime
import pytest
import logging

import pandas as pd

from aimobile.scraper.appstore.entity.project import AppStoreProject
from aimobile.scraper.appstore.service.appdata import AppStoreScraper
from aimobile.scraper.appstore import home

DBFILE = os.path.join(home, "envs/test/data/database.db")
# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"
# ------------------------------------------------------------------------------------------------ #
TERM = "health"
MAX_PAGES = 2
LIMIT = 5


@pytest.mark.appstore
@pytest.mark.appdata_scraper
@pytest.mark.service
class TestAppStoreScraper:  # pragma: no cover
    # ============================================================================================ #
    def test_setup(self, container, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        if os.path.exists(DBFILE):
            os.remove(DBFILE)
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\nCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_scraper(self, container, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        dc = container.datacentre.repo()
        scraper = AppStoreScraper()
        scraper.search(term=TERM, max_pages=MAX_PAGES, limit=LIMIT)

        # Evaluate project
        project = dc.project_repository.get_by_name(name=TERM)
        assert isinstance(project, AppStoreProject)
        logger.debug(f"\nProject: \n{project}")
        logger.debug(project)

        # Evaluate appdata
        appdata = dc.appdata_repository.getall()
        assert isinstance(appdata, pd.DataFrame)
        assert appdata.shape[0] == MAX_PAGES * LIMIT
        logger.debug(f"Appdata head: \n{appdata.head()}")
        logger.debug(f"Appdata info: \n{appdata.info()}")

        # Evaluate Requests
        requests = dc.request_repository.getall()
        assert isinstance(requests, pd.DataFrame)
        logger.debug(f"Requests head: \n{requests.head()}")
        logger.debug(f"Requests info: \n{requests.info()}")

        # Summarize
        logger.debug(scraper.summarize())

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\nCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)
