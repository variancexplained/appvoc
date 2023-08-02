#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /tests/test_data_acquisition/test_review/test_review_controller.py                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday August 2nd 2023 07:02:13 am                                               #
# Modified   : Wednesday August 2nd 2023 08:40:22 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

import pandas as pd

from appstore.data.acquisition.review.controller import ReviewController


# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.rating_ctrl
class TestRatingController:  # pragma: no cover
    # ============================================================================================ #
    def test_controller(self, review_repo, review_jobrun_repo, job_repo, caplog):
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
        ctrl = ReviewController(min_ratings=5, max_pages=4, max_results_per_page=10, verbose=2)
        ctrl.scrape()
        repo = review_repo()
        df = repo.getall()
        assert isinstance(df, pd.DataFrame)
        logging.debug(df)

        repo = review_jobrun_repo()
        df = repo.getall()
        assert isinstance(df, pd.DataFrame)
        logging.debug(df)

        repo = job_repo()
        df = repo.getall()
        assert isinstance(df, pd.DataFrame)
        logging.debug(df)

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
