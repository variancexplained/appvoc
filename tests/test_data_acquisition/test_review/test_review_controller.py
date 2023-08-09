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
# Created    : Tuesday August 8th 2023 07:30:54 am                                                 #
# Modified   : Wednesday August 9th 2023 04:13:21 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

import pandas as pd

from appstore.infrastructure.io.local import IOService
from appstore.data.acquisition.review.controller import ReviewController

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"
# ------------------------------------------------------------------------------------------------ #


@pytest.mark.review_ctrl
class TestReviewCtrl:  # pragma: no cover
    # ============================================================================================ #
    def test_setup(self, container, apps, caplog):
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
        # Configure AppData
        ids = []
        for app in apps:
            if app.category_id == "6002":
                ids.append(app.id)

        # Extract target appdata from archive
        filepath = "tests/data/archive/appdata/appdata_07-29-2023_17-16-45.pkl"
        df = IOService.read(filepath=filepath)
        df = df[df["category_id"] == "6002"]

        appdata = df.loc[df["id"].isin(ids)]
        # Load appdata into repository
        repo = container.data.appdata_repo()
        repo.replace(data=appdata)
        df = repo.getall()
        assert df.shape[0] == 2

        # Reset review repo
        repo = container.data.review_repo()
        repo.reset(force=True)

        # Reset job to complete is False
        repo = container.data.job_repo()
        job = repo.get(id="review-6002")
        job.complete = False
        repo.update(job=job)

        # Reset jobrun
        repo = container.data.review_jobrun_repo()
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
    def test_ctrl(self, container, caplog):
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

        ctrl = ReviewController(max_pages=5, verbose=1)
        ctrl.scrape()

        repo = container.data.review_repo()
        df = repo.getall()
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] > 500

        repo = container.data.review_jobrun_repo()
        df = repo.getall()
        assert isinstance(df, pd.DataFrame)
        assert sum(df["complete"]) == df.shape[0]

        repo = container.data.job_repo()
        job = repo.get(id="review-6002")
        assert job.complete == True  # noqa

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
