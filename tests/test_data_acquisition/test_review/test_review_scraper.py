#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /tests/test_data_acquisition/test_review/test_review_scraper.py                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday August 2nd 2023 01:27:54 am                                               #
# Modified   : Wednesday August 2nd 2023 02:03:36 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

import pandas as pd

from appstore.data.acquisition.review.scraper import ReviewScraper
from appstore.data.acquisition.review.result import ReviewResult

KEYS = [
    "userReviewId",
    "name",
    "rating",
    "title",
    "body",
    "voteSum",
    "voteCount",
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
    def test_setup(self, apps, caplog):
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
        for result in ReviewScraper(app=apps[0], max_pages=2):
            assert isinstance(result, ReviewResult)
            assert result.app == apps[0]
            assert result.reviews > 0
            assert isinstance(result.content, list)
            assert isinstance(result.get_result(), pd.DataFrame)
            for review in result.content:
                logger.debug(review)
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
