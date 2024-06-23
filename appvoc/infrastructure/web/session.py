#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/infrastructure/web/session.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 03:15:52 am                                                 #
# Modified   : Tuesday August 1st 2023 10:36:04 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import logging
from dotenv import load_dotenv

import requests

from appvoc.infrastructure.web.throttle import LatencyThrottle
from appvoc.infrastructure.web.adapter import TimeoutHTTPAdapter
from appvoc.infrastructure.web.headers import BrowserHeader


load_dotenv()


# ------------------------------------------------------------------------------------------------ #
class SessionHandler:
    """Encapsulates an HTTP Session with retry capability.

    Args:
        timeout (TimeoutHTTPAdapter): An HTTP Adapter for managing timeouts and retries at request level.
        retries (int): Number of sessions to retry if timeout retry maximum has been reached.
        delay (tuple): The lower and upper bound on time between requests.
    """

    def __init__(
        self,
        timeout: TimeoutHTTPAdapter,
        throttle: LatencyThrottle,
        headers: BrowserHeader,
        session_retries: int = 3,
    ) -> None:
        self._timeout = timeout
        self._throttle = throttle
        self._headers = iter(headers)

        self._session_retries = session_retries

        self._proxy = None  # The proxy used for the current request
        self._header = None  # The header used for the current request.

        self._session = None

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def get(self, url: str, header: dict = None, params: dict = None):  # noqa: C901
        """Executes the http request and returns a Response object.

        Args:
            url (str): The base url for the http request
            header (dict): A dictionary containing header parameters.If None provided, standard rotating headers will be used.
            params (dict): The parameters to be added to the url

        """

        session_retry = 0

        while session_retry < self._session_retries:
            self._setup(header=header)

            try:
                self._throttle.start()
                response = self._session.get(
                    url=url, headers=self._header, params=params, proxies=self._proxy
                )
                self._throttle.stop()
                self._throttle.delay()

            except Exception as e:  # pragma: no cover
                session_retry += 1
                msg = f"A {type(e)} exception occurred. \n{e}\nRetrying with retry #{session_retry}."
                self._logger.exception(msg)
            else:
                return response

        self._logger.exception(
            "All retry and session limits have been reached. Exiting."
        )

    def _setup(self, header: dict = None) -> None:
        """Conducts pre-request initializations"""

        self._proxy = self._get_proxy()  # From rotating proxies
        self._header = header or next(self._headers)  # From rotating headers

        # Construct session object
        self._session = requests.Session()
        self._session.mount("https://", self._timeout)
        self._session.mount("http://", self._timeout)

    def _get_proxy(self) -> dict:
        """Returns proxy servers"""
        username = os.getenv("WEBSHARE_USER")
        password = os.getenv("WEBSHARE_PWD")
        dns = os.getenv("WEBSHARE_DNS")
        port = os.getenv("WEBSHARE_PORT")

        return {
            "http": f"http://{username}:{password}@{dns}:{port}/",
            "https": f"http://{username}:{password}@{dns}:{port}/",
        }
