#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /tests/test_infrastructure/test_web/test_rest_handler.py                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday April 18th 2023 02:52:16 pm                                                 #
# Modified   : Thursday April 20th 2023 07:27:05 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

import requests

from aimobile.infrastructure.web.session import SessionHandler

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.rest
class TestSessionHandler:  # pragma: no cover
    # ============================================================================================ #
    def test_get_w_params(self, container, request_appdata, caplog):
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
        handler = container.web.handler()
        handler.get(url=request_appdata["url"], params=request_appdata["params"])
        proxy = handler.proxy
        header = handler.header

        assert isinstance(handler.response, requests.Response)
        assert isinstance(handler.response.json(), dict)
        assert handler.status_code == 200
        assert isinstance(handler.sessions, int)
        assert handler.sessions < 4

        # --------------------------
        handler.get(url=request_appdata["url"], params=request_appdata["params"])
        assert handler.proxy != proxy
        assert handler.header != header

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
    def test_get_w_headers(self, request_ratings, container, caplog):
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
        handler = container.web.handler()
        handler.get(url=request_ratings["url"], header=request_ratings["headers"])

        assert isinstance(handler.response, requests.Response)
        assert isinstance(handler.response.json(), dict)
        assert handler.status_code == 200
        assert isinstance(handler.sessions, int)
        assert handler.sessions < 4
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
    def test_get_exception(self, container, request_appdata, caplog):
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
        handler = container.web.handler()

        request_appdata["params"]["lang"] = "xx-12"
        request_appdata["params"]["media"] = "video"
        h = handler.get(url=request_appdata["url"], params=request_appdata["params"])
        assert isinstance(h, SessionHandler)

        assert isinstance(handler.response, requests.Response)
        assert handler.status_code != 200
        assert isinstance(handler.sessions, int)
        assert handler.sessions == 1

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
