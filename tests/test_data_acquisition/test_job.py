#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /tests/test_data_acquisition/test_job.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday July 29th 2023 09:19:19 pm                                                 #
# Modified   : Sunday July 30th 2023 04:28:52 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

from appstore.data.acquisition.job import Job


# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.job
class TestJob:  # pragma: no cover
    # ============================================================================================ #
    def test_from_df(self, job_df, caplog):
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
        job = Job.from_df(df=job_df)
        assert isinstance(job, Job)
        assert job.id == job_df["id"][0]
        assert job.controller == job_df["controller"][0]
        assert job.category_id == job_df["category_id"][0]
        assert job.category == job_df["category"][0]
        assert isinstance(job.started, datetime)
        assert isinstance(job.ended, datetime)
        assert job.status == "not_started"

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
    def test_as_dict(self, job_df, caplog):
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
        job = Job.from_df(df=job_df)
        job_dict = job.as_dict()
        assert isinstance(job_dict, dict)

        assert job_dict["id"] == job_df["id"][0]
        assert job_dict["controller"] == job_df["controller"][0]
        assert job_dict["category_id"] == job_df["category_id"][0]
        assert job_dict["category"] == job_df["category"][0]
        assert isinstance(job_dict["started"], datetime)
        assert isinstance(job_dict["updated"], datetime)
        assert isinstance(job_dict["ended"], datetime)
        assert isinstance(job_dict["status"], str)
        assert job_dict["status"] == "not_started"
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
    def test_start_end(self, job, caplog):
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
        assert job.status == "not_started"
        assert job.started < datetime.strptime("2000-01-01", "%Y-%m-%d")
        assert job.ended < datetime.strptime("2000-01-01", "%Y-%m-%d")
        job.start()
        started = job.started
        assert job.status == "in_progress"
        assert job.started > datetime.strptime("2000-01-01", "%Y-%m-%d")
        assert job.ended < datetime.strptime("2000-01-01", "%Y-%m-%d")
        job.start()
        assert job.started == started
        assert job.updated > job.started
        job.end()
        assert job.status == "completed"
        assert job.started > datetime.strptime("2000-01-01", "%Y-%m-%d")
        assert job.ended > datetime.strptime("2000-01-01", "%Y-%m-%d")

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
