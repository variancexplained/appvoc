#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/infrastructure/web/session.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 03:15:52 am                                                 #
# Modified   : Monday July 31st 2023 05:45:41 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import logging
from dotenv import load_dotenv

import requests

from appstore.infrastructure.web.throttle import LatencyThrottle
from appstore.infrastructure.web.adapter import TimeoutHTTPAdapter
from appstore.infrastructure.web.headers import BrowserHeader
from appstore.infrastructure.web.response import response_agent

load_dotenv()


# ------------------------------------------------------------------------------------------------ #
class SessionHandler:
    """Encapsulates an HTTP Session with retry capability.

    Args:
        timeout (TimeoutHTTPAdapter): An HTTP Adapter for managing timeouts and retries at request level.
        session_retries (int): Number of sessions to retry if timeout retry maximum has been reached.
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

        self._sessions = 0
        self._session = None

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def get(self, url: str, header: dict = None, params: dict = None):  # noqa: C901
        """Executes the http request and returns a Response object.

        Args:
            url (str): The base url for the http request
            header (dict): A dictionary containing header parameters.If None provided, standard rotating headers will be used.
            params (dict): The parameters to be added to the url

        """
        self._sessions = 0

        while self._sessions < self._session_retries:
            self._setup(header=header)

            try:
                response = self.make_request(
                    url=url, headers=self._header, params=params, proxies=self._proxy
                )
                latency_seconds = response.latency / 1000
                self._throttle.delay(latency=latency_seconds, wait=True)

            except Exception as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred. \n{e}\nRetrying with session #{self._sessions}."
                self._logger.exception(msg)
            else:
                return response

        self._logger.exception("All retry and session limits have been reached. Exiting.")
        return self

    def _setup(self, header: dict = None) -> None:
        """Conducts pre-request initializations"""

        self._proxy = self._get_proxy()  # From rotating proxies
        self._header = header or next(self._headers)  # From rotating headers

        # Construct session object
        self._session = requests.Session()
        self._session.mount("https://", self._timeout)
        self._session.mount("http://", self._timeout)

        # Set / reset the response
        self._response = None

    @response_agent
    def make_request(
        self, url: str, headers: dict, params: dict, proxies: dict
    ) -> requests.Response:
        return self._session.get(
            url=url,
            headers=headers,
            params=params,
            proxies=proxies,
        )

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
