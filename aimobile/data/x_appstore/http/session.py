#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/x_appstore/http/session.py                                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 03:15:52 am                                                 #
# Modified   : Thursday April 20th 2023 07:26:13 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import random
import time
import logging
import json
from dotenv import load_dotenv
import requests
from typing import Union

from aimobile.data.x_appstore.http.adapter import TimeoutHTTPAdapter
from aimobile.data.x_appstore.http.base import SERVERS, Handler
from atelier.web.rest import retry


# ------------------------------------------------------------------------------------------------ #
class SessionHandler(Handler):
    """Handles HTTP Requests

    Args:
        config (SimpleNamespace): Contains the configuration for the request handler
    """

    def __init__(
        self,
        timeout: TimeoutHTTPAdapter,
        proxies: list,
        session_retries: int = 3,
        delay: tuple = (1, 8),
    ) -> None:
        self._timeout = timeout
        self._proxies = proxies
        self._session_retries = session_retries
        self._delay = delay

        # Initialize method parameters
        self._url = None
        self._headers = None
        self._sessions = 0
        self._response = None
        self._status_code = None

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    @property
    def url(self) -> str:
        """Returns the url sent with the last request."""
        return self._url

    @property
    def headers(self) -> dict:
        """Returns the headers that were sent with the last request"""
        return self._headers

    @property
    def status_code(self) -> dict:
        """Returns status_code from the last request."""
        return self._status_code

    @property
    def proxy(self) -> dict:
        """Returns the proxy server"""
        return self._proxies.get("http")

    @property
    def sessions(self) -> dict:
        """Returns the number of sessions used during the last request."""
        return self._sessions + 1

    @property
    def response(self) -> requests.Response:
        """Returns the response"""
        return self._response

    def get(self, url: str, headers: Union[dict, list], params: dict = None):  # noqa: C901
        """Executes the http request and returns a Response object.

        Args:
            url (str): The base url for the http request
            params (dict): The parameters to be added to the url
            headers (Union[dict,list]): Dictionary or list of dictionaries containing the
                http headers. If headers is a list type, the request module will randomly
                select a header from the list for each session.
        """
        self._sessions = 0
        self._params = params
        self._url = url

        while self._sessions < self._retry_sessions:
            session = self._setup(headers=headers)

            try:
                self._response = session.get(
                    url=self._url, headers=self._headers, params=self._params, proxies=self._proxies
                )
                self._teardown()
                return self

            except requests.exceptions.HTTPError as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._config['retry']['total_retries']} retries. Retrying with new session #{self._sessions}."
                self._logger.error(msg)
                self._status_code = e.response.status_code
            except requests.exceptions.Timeout as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._config['retry']['total_retries']} retries. Retrying with new session #{self._sessions}."
                self._logger.error(msg)
                self._status_code = e.response.status_code
            except requests.exceptions.TooManyRedirects as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred. Likely a problem with the url: {url}. Aborting request."
                self._logger.error(msg)
                self._status_code = e.response.status_code
            except requests.exceptions.ConnectionError as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._config['retry']['total_retries']} retries. Retrying with new session #{self._sessions}."
                self._logger.error(msg)
                self._status_code = e.response.status_code
            except requests.exceptions.JSONDecodeError as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._config['retry']['total_retries']} retries. Unable to decode response. Retrying."
                self._logger.error(msg)
                self._status_code = e.response.status_code
            except json.decoder.JSONDecodeError as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._config['retry']['total_retries']} retries. Unable to decode response. Retrying."
                self._logger.error(msg)
                self._status_code = e.response.status_code
            except requests.exceptions.InvalidURL as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred. Likely a problem with the url: {url}. Aborting request."
                self._logger.error(msg)
                self._status_code = e.response.status_code
                break
            except requests.exceptions.InvalidHeader as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred. Check headers.\n{headers}. Retrying with new session #{self._sessions}."
                self._logger.error(msg)
                self._status_code = e.response.status_code
            except requests.exceptions.RetryError as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._config['retry']['total_retries']} retries. Retrying with new session #{self._sessions}."
                self._logger.error(msg)
                self._status_code = e.response.status_code
            except ValueError as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._config['retry']['total_retries']} retries. Aborting request."
                self._logger.error(msg)
                self._status_code = e.response.status_code
                break
            except requests.exceptions.ChunkedEncodingError as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._config['retry']['total_retries']} retries. Aborting request."
                self._logger.error(msg)
                break
            except requests.exceptions.ContentDecodingError as e:  # pragma: no cover
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._config['retry']['total_retries']} retries. Aborting request."
                self._logger.error(msg)

        self._logger.error(
            "All retry and session limits have been reached. Exiting."
        )  # pragma: no cover
        return self

    def _setup(self, headers: Union[list, dict]) -> None:
        """Conducts pre-request initializations"""

        self._wait()  # Random hesitation between requests
        self._proxies = self._get_proxy()  # Rotates proxies

        # Rotate headers if a sequence type
        self._headers = random.choice(headers) if isinstance(headers, list) else headers

        # Construct session object
        session = requests.Session()
        session.mount("https://", self._timeout)
        session.mount("http://", self._timeout)

        # Set / reset the response
        self._response = None

        return session

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
        load_dotenv()
        username = os.getenv("GEONODE_USERNAME")
        password = os.getenv("GEONODE_PWD")
        while True:
            dns = random.choice(SERVERS)
            proxy = {"http": f"http://{username}:{password}@{dns}"}
            if proxy != self._proxies:
                break
        return proxy
