#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/tests/test_service/test_review_scraper.py                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 02:57:14 pm                                                 #
# Modified   : Sunday April 16th 2023 04:54:54 pm                                                  #
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

from aimobile.scraper.appstore.service.reviews import AppStoreReviewScraper
from aimobile.scraper.appstore.service.appdata import AppStoreScraper
from aimobile.scraper.appstore import home

DBFILE = os.path.join(home, "envs/test/data/database.db")
# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"
# ------------------------------------------------------------------------------------------------ #
CATEGORY_ID = 6013
CATEGORY_NAME = "6013-HEALTH_AND_FITNESS"
TERM = "health"
MAX_PAGES = 2
LIMIT = 5


@pytest.mark.appstore
@pytest.mark.review_scraper
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
        dc = container.datacentre.repo()
        dc.appdata_repository.drop()
        dc.review_repository.remove(app_id=1208224953)  # Leave some behind to test restart
        dc.save()
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
    def test_appdata_scraper(self, container, caplog):
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

        # Evaluate appdata
        appdata = dc.appdata_repository.getall()
        assert isinstance(appdata, pd.DataFrame)
        assert appdata.shape[0] == MAX_PAGES * LIMIT
        logger.debug(f"Appdata head: \n{appdata.head()}")
        logger.debug(f"Appdata info: \n{appdata.info()}")

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
    def test_review_scraper(self, container, caplog):
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
        scraper = AppStoreReviewScraper()
        scraper.search(category_id=CATEGORY_ID, max_pages=MAX_PAGES)

        # Evaluate appdata
        reviews = dc.review_repository.getall()
        assert isinstance(reviews, pd.DataFrame)
        logger.debug(f"Appdata head: \n{reviews.head()}")
        logger.debug(f"Appdata info: \n{reviews.info()}")

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
