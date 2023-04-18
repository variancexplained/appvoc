#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/framework/web/rest.py                                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 03:15:52 am                                                 #
# Modified   : Tuesday April 18th 2023 12:46:54 pm                                                 #
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
from typing import Union

from aimobile.data.appstore.http.adapter import TimeoutHTTPAdapter
from aimobile.framework.web.params import PROXY_SERVERS, HEADERS

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
        delay: tuple = (1, 8),
    ) -> None:
        self._timeout = timeout
        self._session_retries = session_retries
        self._delay = delay

        self._proxy = None  # The proxy used for the current request
        self._headers = (
            HEADERS  # List of standard headers for rotation if no request header is provided
        )
        self._header = None  # The header used for the current request.

        self._sessions = 0
        self._session = None
        self._response = None
        self._status_code = None

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def status_code(self) -> dict:
        """Returns status_code from the last request."""
        return self._status_code

    @property
    def sessions(self) -> dict:
        """Returns the number of sessions used during the last request."""
        return self._sessions + 1

    @property
    def response(self) -> requests.Response:
        """Returns the response"""
        return self._response

    def get(
        self, url: str, header: Union[dict, list, None] = None, params: dict = None
    ):  # noqa: C901
        """Executes the http request and returns a Response object.

        Args:
            url (str): The base url for the http request
            header (Union[dict,list, None]): A dictionary is interpreted as a single header. If a list
                is provided, one header will be randomly selected for the request and again, for
                any retry sessions. If no header is provided, a header will be randomly selected from a
                list of standard headers for the request and for any subsequent session retries.
            params (dict): The parameters to be added to the url

        """
        self._sessions = 0

        while self._sessions < self._session_retries:
            self._setup(header=header)

            try:
                self._response = self._session.get(
                    url=url, headers=self._header, params=params, proxies=self._proxy
                )
                self._teardown()
                return self

            except Exception as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred. Retrying with session #{self._sessions}."
                self._logger.error(msg)
                self._status_code = e.response.status_code

        self._logger.error(
            "All retry and session limits have been reached. Exiting."
        )  # pragma: no cover
        return self

    def _setup(self, header: Union[list, dict, None]) -> None:
        """Conducts pre-request initializations"""

        self._wait()  # Random hesitation between requests
        self._proxy = self._get_proxy()  # Rotates proxies
        self._header = self._get_header(header=header)

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
        sleep = random.randint(*self._delay)
        time.sleep(sleep)

    def _get_proxy(self) -> dict:
        """Returns proxy servers"""
        username = os.getenv("GEONODE_USERNAME")
        password = os.getenv("GEONODE_PWD")
        while True:
            dns = random.choice(PROXY_SERVERS)
            proxy = {"http": f"http://{username}:{password}@{dns}"}
            if proxy != self._proxies:
                break
        return proxy

    def _get_header(self, header: Union[dict, list, None]) -> dict:
        """Returns a header to use for the request."""
        if header is None:
            return random.choice(self._headers)
        elif isinstance(header, dict):
            return header
        elif isinstance(header, list):
            return random.choice(header)
        else:
            msg = f"Invalid header type: {header}. Type must be in [dict,list,None]."
            self._logger.error(msg)
            raise TypeError(msg)
