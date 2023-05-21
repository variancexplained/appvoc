#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /tests/test_data_acquisition/test_appstore/test_scrapers/test_rating_scraper.py     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 24th 2023 08:26:10 am                                                  #
# Modified   : Thursday May 18th 2023 08:22:59 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

import pandas as pd

from aimobile.data.acquisition.rating.scraper import AppStoreRatingScraper
from aimobile.data.acquisition.rating.result import RatingResult

CATEGORIES = [6000, 6012, 6013]
# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.scraper
@pytest.mark.rating_scraper
class TestRatingScraper:  # pragma: no cover
    # ============================================================================================ #
    def test_scraper(self, uow, caplog):
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
        repo = uow.appdata_repo
        apps = repo.getall()

        projects = pd.DataFrame()
        results = pd.DataFrame()

        for result in AppStoreRatingScraper(apps=apps):
            assert isinstance(result, RatingResult)
            assert isinstance(result.projects, pd.DataFrame)
            assert isinstance(result.results, pd.DataFrame)
            # assert result.projects.shape[0] == result.results.shape[0]
            projects = pd.concat([projects, result.projects], axis=0)
            results = pd.concat([results, result.results], axis=0)
        logger.debug(f"\nProjects:\n{projects}")
        logger.debug(f"\nResults:\n{results}")
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
