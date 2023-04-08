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
# Modified   : Saturday April 8th 2023 03:15:25 pm                                                 #
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


@pytest.mark.internet
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
        response = handler.get(url=http_request["url"], params=http_request["params"])
        headers = handler.headers
        proxies = handler.proxies
        assert isinstance(response, requests.Response)
        assert response.status_code == 200
        assert isinstance(handler.headers, dict)
        assert isinstance(handler.proxies, dict)
        assert isinstance(handler.url, str)
        assert isinstance(handler.sessions, int)
        logger.debug(f"\nHeaders\n{handler.headers}")
        logger.debug(f"\nProxies\n{handler.proxies}")

        # Get next page
        http_request["params"]["offset"] += 1
        response = handler.get(url=http_request["url"], params=http_request["params"])
        headers2 = handler.headers
        proxies2 = handler.proxies
        assert headers != headers2
        assert proxies != proxies2
        assert response.status_code == 200

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
