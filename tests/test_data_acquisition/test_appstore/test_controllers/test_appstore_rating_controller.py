#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /tests/test_data_acquisition/test_appstore/test_controllers/test_appstore_rating_controller.py #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday May 3rd 2023 02:39:32 pm                                                  #
# Modified   : Tuesday July 25th 2023 01:04:25 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

from appstore.data.acquisition.rating.controller import RatingController


# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.rating_ctrl
class TestRatingController:  # pragma: no cover
    # ============================================================================================ #
    def test_controller(self, uow, caplog):
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
        project_repo = uow.rating_project_repo
        project_repo.delete_all()
        rating_repo = uow.rating_repo
        rating_repo.delete_all()
        controller = RatingController(batchsize=5)
        controller.scrape(category_ids=[6000, 6012, 6013])

        projects = project_repo.getall()
        ratings = rating_repo.getall()
        assert projects.shape[0] == 60
        assert ratings.shape[0] == 60
        logger.debug(projects)
        logger.debug(ratings)
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
