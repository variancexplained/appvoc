#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/appstore/tests/test_http/test_reviews.py                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday April 10th 2023 06:43:20 am                                                  #
# Modified   : Tuesday April 18th 2023 06:42:38 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

import pandas as pd


from aimobile.data.appstore.http.review import AppStoreReviewRequest

ID = 297606951
PAGE = 1
AFTER = datetime.fromisoformat("2010-01-01T05:00:00")
MAX_PAGES = 2
# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.http
@pytest.mark.review
class TestAppStoreReviewRequest:  # pragma: no cover
    # ============================================================================================ #
    def test_search(self, container, caplog):
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
        session_handler = container.session.handler()
        search = AppStoreReviewRequest(
            app_id=ID,
            app_name="some_app_name",
            category_id=6013,
            category="HEALTH_AND_FITNESS",
            handler=session_handler,
            page=PAGE,
            max_pages=MAX_PAGES,
        )
        for request in search:
            assert isinstance(request.result, pd.DataFrame)
            logger.debug(f"\nResult\n{request.result}")
            logger.debug(f"URL:\n{request.url}")

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
