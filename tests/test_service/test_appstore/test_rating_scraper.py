#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /tests/test_service/test_appstore/test_rating_scraper.py                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 24th 2023 08:26:10 am                                                  #
# Modified   : Saturday April 29th 2023 06:56:05 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

import pandas as pd

from aimobile.data.acquisition.appstore.rating import AppStoreRatingScraper


# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.scraper
@pytest.mark.rating_scraper
class TestRatingScraper:  # pragma: no cover
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
        results = []
        apps = apps[0:3]
        scraper = AppStoreRatingScraper(apps=apps)
        for scrape in scraper:
            results.append(scrape.result)
        assert len(results) == 3
        for result in results:
            assert isinstance(result["id"], int)
            assert isinstance(result["name"], str)
            assert isinstance(result["category_id"], int)
            assert isinstance(result["category"], str)
            assert isinstance(result["rating"], (int, float))
            assert isinstance(result["reviews"], int)
            assert isinstance(result["ratings"], int)
            assert isinstance(result["onestar"], int)
            assert isinstance(result["twostar"], int)
            assert isinstance(result["threestar"], int)
            assert isinstance(result["fourstar"], int)
            assert isinstance(result["fivestar"], int)
            assert isinstance(result["source"], str)

        results = pd.DataFrame(data=results)
        logger.debug(results)
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
