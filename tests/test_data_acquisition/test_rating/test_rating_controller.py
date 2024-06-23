#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /tests/test_data_acquisition/test_rating/test_rating_controller.py                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 8th 2023 07:30:54 am                                                 #
# Modified   : Sunday August 27th 2023 12:35:57 am                                                 #
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
from appvoc.data.acquisition.rating.controller import RatingController

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"
# ------------------------------------------------------------------------------------------------ #
FP_JOBS = "tests/data/rating/jobs.csv"  # noqa
FP_RATING_JOBRUNS = "tests/data/rating/rating_jobrun.csv"  # noqa
FP_RATINGS = "data/archive/rating/rating_07-29-2023_17-17-07.pkl"
# ------------------------------------------------------------------------------------------------ #


@pytest.mark.rating_ctrl
class TestRatingCtrl:  # pragma: no cover
    # ============================================================================================ #
    @pytest.mark.asyncio
    async def test_setup(self, container, caplog):
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
        # Get ratings
        FP_RATINGS = "data/archive/rating/rating_07-29-2023_17-17-07.pkl"  # noqa
        df = IOService.read(FP_RATINGS, index=False)
        s1 = df.loc[(df["category_id"] == "6015") & (df["ratings"] > 100)].sample(
            n=5, random_state=5
        )
        s2 = df.loc[(df["category_id"] == "6020") & (df["ratings"] > 100)].sample(
            n=5, random_state=5
        )
        s3 = df.loc[(df["category_id"] == "6013") & (df["ratings"] > 10)].sample(
            n=5, random_state=5
        )
        ratings = pd.concat([s1, s2, s3], axis=0)
        ids = list(ratings["id"].values)
        # get app data
        FP = "tests/data/archive/appdata/appdata_07-29-2023_17-16-45.pkl"  # noqa
        df = IOService.read(FP)
        appdata = pd.DataFrame()

        # Add ids for whicch no ratings exist
        s1 = df.loc[(df["category_id"] == "6017")].sample(n=5, random_state=5)
        newids = list(s1["id"].values)
        for newid in newids:
            ids.append(newid)
        for id in ids:  # noqa
            data = df[df["id"] == id]
            appdata = pd.concat([appdata, data], axis=0)

        # Store app data for recovery and replace with selected data
        repo = container.data.appdata_repo()
        repo.replace(data=appdata)
        # Reset jobs repo
        FP = "tests/data/rating/jobs.csv"  # noqa
        df = IOService.read(FP)
        repo = container.data.job_repo()
        repo.replace(data=df)
        # Reset jobrun repo
        repo = container.data.rating_jobrun_repo()
        repo.reset(force=True)
        # Reset ratings repo
        ids = [
            "779656557",
            "353763955",
            "952516687",
            "1456472751",
            "1071223674",
            "1097859459",
        ]
        repo = container.data.rating_repo()
        ratings = pd.DataFrame()
        for id in ids:  # noqa
            df = repo.get(id=id)
            if df.shape[0] > 0:
                ratings = pd.concat([ratings, df], axis=0)
        repo.replace(ratings)

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
    @pytest.mark.asyncio
    async def test_ctrl(self, container, caplog):
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

        ctrl = RatingController(batchsize=5, verbose=1, failure_threshold=2)
        await ctrl.scrape()

        repo = container.data.rating_repo()
        df = repo.getall()
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] > 1
        logging.debug(df)

        repo = container.data.rating_jobrun_repo()
        df = repo.getall()
        assert isinstance(df, pd.DataFrame)
        assert sum(df["complete"]) == df.shape[0]

        repo = container.data.job_repo()
        df = repo.getall()
        assert isinstance(df, pd.DataFrame)
        assert sum(df["complete"]) == df.shape[0]

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
