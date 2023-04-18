#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/tests/test_internet/test_sessions.py                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 10:53:07 am                                                 #
# Modified   : Monday April 10th 2023 06:36:26 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging
import requests

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.http
@pytest.mark.sessions
class TestSessionHandler:  # pragma: no cover
    # ============================================================================================ #
    def test_sessions(self, container, http_request, caplog):
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
        handler = container.session.handler()
        session = handler.get(url=http_request["url"], params=http_request["params"])
        assert session.url == http_request["url"]
        assert isinstance(session.headers, dict)
        assert session.status_code == 200
        assert isinstance(session.proxy, str)
        assert isinstance(session.sessions, int)
        assert isinstance(session.requested, datetime)
        assert isinstance(session.responded, datetime)
        assert isinstance(session.response_time, float)
        assert isinstance(session.content_length, int)
        assert isinstance(session.response, requests.Response)
        headers = session.headers
        proxies = session.proxy
        logger.debug(f"\nHeaders\n{session.headers}")
        logger.debug(f"\nProxies\n{session.proxy}")

        # Get next page
        http_request["params"]["offset"] += 1
        session = handler.get(url=http_request["url"], params=http_request["params"])
        headers2 = session.headers
        proxies2 = session.proxy
        assert headers != headers2
        assert proxies != proxies2
        assert isinstance(session.headers, dict)
        assert session.status_code == 200
        assert isinstance(session.proxy, str)
        assert isinstance(session.sessions, int)
        assert isinstance(session.requested, datetime)
        assert isinstance(session.responded, datetime)
        assert isinstance(session.response_time, float)
        assert isinstance(session.content_length, int)

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
