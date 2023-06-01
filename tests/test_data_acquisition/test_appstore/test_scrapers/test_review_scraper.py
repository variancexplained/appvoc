#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /tests/test_data_acquisition/test_appstore/test_scrapers/test_review_scraper.py     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 22nd 2023 10:39:34 am                                                #
# Modified   : Thursday June 1st 2023 11:15:56 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging
import pandas as pd

from aimobile.data.acquisition.review.scraper import ReviewScraper


# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"
# ------------------------------------------------------------------------------------------------ #
ID = 1095999436
NAME = "RVC Pet Diabetes App"
CATEGORY_ID = 6020
CATEGORY = "Health & Fitness"


# ------------------------------------------------------------------------------------------------ #
@pytest.mark.scraper
@pytest.mark.review_scraper
class TestReviewScraper:  # pragma: no cover
    # ============================================================================================ #
    def test_scraper(self, container, mode, caplog):
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
        scraper = ReviewScraper(
            app_id=ID, app_name=NAME, category_id=CATEGORY_ID, category=CATEGORY
        )
        for i, scrape in enumerate(scraper, start=1):
            result = scrape.result
            assert isinstance(result, pd.DataFrame)
            assert result.shape[0] > 0
            assert "author" in result.columns
            assert "content" in result.columns
            assert "rating" in result.columns
            assert scrape.results > 0
            assert scrape.page == i
            assert scrape.status_code == 200
            assert str(ID) in scrape.url
            logger.debug(f"\n\nThe {i}th page returned {scrape.results} results.")
            logger.debug(f"\nResult:\n{scrape.result}\n")

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
