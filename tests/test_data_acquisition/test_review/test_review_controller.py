#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /tests/test_data_acquisition/test_review/test_review_controller.py                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 8th 2023 07:30:54 am                                                 #
# Modified   : Sunday August 27th 2023 12:36:06 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

import pandas as pd

from appvoc.infrastructure.file.io import IOService
from appvoc.data.acquisition.review.controller import ReviewController

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
        logger.debug(df.sample(n=5))

        appdata = df.loc[df["id"].isin(ids)]
        # Load appdata into repository
        repo = container.data.appdata_repo()
        repo.replace(data=appdata)
        df = repo.getall()
        assert df.shape[0] == 2

        # Reset review repo
        filepath = "tests/data/review/reviews.pkl"
        df = IOService.read(filepath=filepath)
        repo = container.data.review_repo()
        repo.replace(data=df)

        # Reset job to complete is False
        repo = container.data.job_repo()
        job = repo.get(id="review-6002")
        job.complete = False
        repo.update(job=job)

        # Reset jobrun
        repo = container.data.review_jobrun_repo()
        repo.reset(force=True)

        # Reset review request
        repo = container.data.review_request_repo()
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

        ctrl = ReviewController(max_pages=4, verbose=1)
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

    # ============================================================================================ #
    def test_restart(self, container, caplog):
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
        # Reset job to complete is False
        repo = container.data.job_repo()
        job = repo.get(id="review-6002")
        job.complete = False
        repo.update(job=job)

        # Get current latest index
        repo = container.data.review_request_repo()
        request = repo.get(id="284815942")
        assert request.last_index > 0
        idx = request.last_index

        ctrl = ReviewController(max_pages=4, verbose=1)
        ctrl.scrape()

        request = repo.get(id="284815942")
        assert request.last_index > idx

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
