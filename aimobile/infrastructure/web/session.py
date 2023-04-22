#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/infrastructure/web/session.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 03:15:52 am                                                 #
# Modified   : Saturday April 22nd 2023 10:14:24 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import random
import time
import logging
from dotenv import load_dotenv
import requests

from aimobile.infrastructure.web.adapter import TimeoutHTTPAdapter
from aimobile.infrastructure.web.base import PROXY_SERVERS, HEADERS

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
        session_retries: int = 3,
        delay_min: int = 1,
        delay_max: int = 8,
    ) -> None:
        self._timeout = timeout
        self._session_retries = session_retries
        self._delay_min = delay_min
        self._delay_max = delay_max

        self._proxy = None  # The proxy used for the current request
        self._header = None  # The header used for the current request.

        self._sessions = 0
        self._session = None
        self._response = None
        self._status_code = None

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    def status_code(self) -> dict:
        """Returns status_code from the last request."""
        return self._status_code

    @property
    def header(self) -> dict:
        """Returns header from the last request."""
        return self._header

    @property
    def proxy(self) -> dict:
        """Returns proxy from the last request."""
        return self._proxy

    @property
    def sessions(self) -> dict:
        """Returns the number of sessions used during the last request."""
        return self._sessions + 1

    @property
    def response(self) -> requests.Response:
        """Returns the response"""
        return self._response

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
                self._response = self._session.get(
                    url=url,
                    headers=self._header,
                    params=params,
                    proxies=self._proxy,
                )
                self._teardown()
                return self

            except Exception as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred. Retrying with session #{self._sessions}."
                self._logger.error(msg)
                self._status_code = 999

        self._logger.error("All retry and session limits have been reached. Exiting.")
        return self

    def _setup(self, header: dict = None) -> None:
        """Conducts pre-request initializations"""

        self._wait()  # Random delay between requests
        self._proxy = self._get_proxy()  # From rotating proxies
        self._header = header or self._get_header()  # From rotating headers

        # Construct session object
        self._session = requests.Session()
        self._session.mount("https://", self._timeout)
        self._session.mount("http://", self._timeout)

        # Set / reset the response
        self._response = None

    def _teardown(self) -> None:
        """Conducts post-request housekeeping"""
        self._status_code = int(self._response.status_code)
        self._logger.debug(
            f"\nRequest status code: {self._response.status_code}. Session: {self._sessions}"
        )

    def _wait(self) -> None:
        """Waits a random number of seconds between delay min and delay max."""
        sleep = random.randint(self._delay_min, self._delay_max)
        time.sleep(sleep)

    def _get_proxy(self) -> dict:
        """Returns proxy servers"""
        username = os.getenv("GEONODE_USERNAME")
        password = os.getenv("GEONODE_PWD")
        while True:
            dns = random.choice(PROXY_SERVERS)
            proxy = {"http": f"http://{username}:{password}@{dns}"}
            if proxy != self._proxy:
                return proxy

    def _get_header(self) -> dict:
        """Returns a header to use for the request."""

        while True:
            header = random.choice(HEADERS)
            if header != self._header:
                return header
