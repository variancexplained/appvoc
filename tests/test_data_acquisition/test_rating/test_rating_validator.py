#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /tests/test_data_acquisition/test_rating/test_rating_validator.py                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday August 2nd 2023 02:40:52 am                                               #
# Modified   : Wednesday August 2nd 2023 02:56:29 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

from appstore.data.acquisition.rating.validator import RatingValidator
from appstore.data.acquisition.base import ErrorCodes


# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.rating_validator
@pytest.mark.validator
class TestRatingValidator:  # pragma: no cover
    # ============================================================================================ #
    def test_setup(self, rating_responses, caplog):
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
        validator = RatingValidator()
        for idx, response in enumerate(rating_responses):
            if idx == 0:
                assert not validator.is_valid(response)
                assert validator.msg == "No response"
            elif idx == 1:
                assert not validator.is_valid(response)
                assert validator.error_code == ErrorCodes.response_type_error
            elif idx == 2:
                assert not validator.is_valid(response)
                assert validator.error_code == ErrorCodes.data_error
            elif idx == 3:
                assert not validator.is_valid(response)
                assert validator.error_code == ErrorCodes.data_error
            elif idx == 4:
                assert validator.is_valid(response)
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
