#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /tests/test_data_acquisition/test_review/test_review_scraper.py                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday August 2nd 2023 01:27:54 am                                               #
# Modified   : Saturday June 29th 2024 10:25:52 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
import logging
from datetime import datetime

import pandas as pd
import pytest

from appvoc.data.acquisition.review.result import ReviewResponse
from appvoc.data.acquisition.review.scraper import ReviewScraper

KEYS = [
    "id",
    "app_id",
    "app_name",
    "category_id",
    "category",
    "author",
    "rating",
    "title",
    "content",
    "vote_sum",
    "vote_count",
    "date",
]

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.review_scraper
class TestReviewScraper:  # pragma: no cover
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
        # Reset review repo
        repo = container.data.review_repo()
        repo.reset(force=True)

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_scraper(self, apps, caplog):
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
        app_count = 0
        page_count = 0
        for app in apps:
            if app.category_id == "6002":
                app_count += 1
                msg = f"\n\nProcessing App #: {app_count}"
                logger.debug(msg)
                for result in ReviewScraper(app=app, max_pages=4):
                    page_count += 1
                    msg = f"\n\tProcessing Page #: {page_count}"
                    logger.debug(msg)
                    assert isinstance(result, ReviewResponse)
                    assert result.app == app
                    assert result.reviews > 0
                    assert isinstance(result.content, list)
                    assert isinstance(result.get_result(), pd.DataFrame)
                    assert isinstance(result.index, int)
                    for review in result.content:
                        for key in KEYS:
                            assert key in review

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
