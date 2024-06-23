#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /tests/test_data_acquisition/test_rating/test_rating_scraper.py                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday July 31st 2023 02:04:35 am                                                   #
# Modified   : Wednesday August 2nd 2023 03:24:01 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

from appvoc.data.acquisition.rating.scraper import RatingScraper


# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"

KEYS = ["name", "reviews", "onestar", "fivestar"]


@pytest.mark.rating
@pytest.mark.rating_scraper
@pytest.mark.asyncio
class TestRatingScraper:  # pragma: no cover
    # ============================================================================================ #
    async def test_setup(self, container, appdata_repo, caplog):
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
        repo = appdata_repo
        df = repo.sample(10)

        async for result in RatingScraper(apps=df, batch_size=5):
            assert isinstance(result.content, list)
            assert result.apps + result.errors == 5
            assert isinstance(result.size, int)
            for data in result.content:
                for key in KEYS:
                    assert key in data
                logger.debug(data)

            logger.debug(result.get_result())
            logger.debug(result)

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
