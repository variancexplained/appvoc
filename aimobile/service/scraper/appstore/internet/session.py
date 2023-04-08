#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/service/scraper/appstore/internet/session.py                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 03:15:52 am                                                 #
# Modified   : Saturday April 8th 2023 07:58:59 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from types import SimpleNamespace
import random
import time
import requests
from urllib3.util import Retry

from aimobile.service.scraper.appstore.internet.adapter import TimeoutHTTPAdapter
from aimobile.service.scraper.appstore.internet.base import SERVERS, HEADERS, Handler


# ------------------------------------------------------------------------------------------------ #
class SessionHandler(Handler):
    """Handles HTTP Requests

    Args:
        config (SimpleNamespace): Contains the configuration for the request handler
    """

    def __init__(self, config: SimpleNamespace) -> None:
        self._config = config
        self._timeout = None
        self._url = None
        self._headers = None
        self._proxies = None
        self._sessions = 0

    @property
    def url(self) -> str:
        """Returns the url sent with the last request."""
        return self._url

    @property
    def headers(self) -> dict:
        """Returns the headers that were sent with the last request"""
        return self._headers

    @property
    def proxies(self) -> dict:
        """Returns the proxies that were used in the last request."""
        return self._proxies

    @property
    def sessions(self) -> dict:
        """Returns the number of sessions used during the last request."""
        return self._sessions + 1

    def configure(self) -> None:
        """Configures the timeout adapter with retries."""
        retry = Retry(
            total=self._config.request.retry.total_retries,
            backoff_factor=self._config.request.retry.backoff_factor,
            status_forcelist=self._config.request.retry.status_forcelist,
            allowed_methods=self._config.request.retry.allowed_methods,
            raise_on_redirect=self._config.request.retry.raise_on_redirect,
            raise_on_status=self._config.request.retry.raise_on_status,
        )
        self._timeout = TimeoutHTTPAdapter(
            timeout=self._config.request.time.timeout, max_retries=retry
        )

    def get(self, url: str, headers: dict = None, params: dict = None) -> requests.Response:
        """Executes the http request and returns a Response object.

        Args:
            url (str): The base url for the http request
            params (dict): The parameters to be added to the url
            headers (dict): Dictionary containing the HTTP header. Optional. If not provided,
                the headers will be rotated.
        """
        self._sessions = 0
        self._params = params
        self._url = url
        while self._sessions < self._config.request.retry.sessions:
            session = requests.Session()
            session.mount()
            session.mount("https://", self._timeout)
            session.mount("http://", self._timeout)

            try:
                # Random delay
                sleep = random.randint(
                    self._config.request.time.delay_min, self._config.request.time.delay_max
                )
                time.sleep(sleep)

                # Get headers
                self._headers = headers or self._get_headers()
                # Get proxy servers
                self._proxies = self._get_proxy()
                # Execute the session request
                response = session.get(
                    url=self._url, headers=self._headers, params=self._params, proxies=self._proxies
                )
                # Report response status code
                self._logger.debug(
                    f"\nRequest status code: {response.status_code}. Session: {self._sessions}"
                )
                return response

            except requests.exceptions.Timeout as e:
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._retries} retries. Retrying with new session #{self._sessions}."
                self._logger.error(msg)
            except requests.exceptions.TooManyRedirects as e:
                self._sessions += 1
                msg = f"A {type(e)} exception occurred. Likely a problem with the url: {url}. Aborting request."
                self._logger.error(msg)
                break
            except requests.exceptions.ConnectionError as e:
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._retries} retries. Retrying with new session #{self._sessions}."
                self._logger.error(msg)
            except requests.exceptions.JSONDecodeError as e:
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._retries} retries. Unable to decode response. Aborting request"
                self._logger.error(msg)
                break
            except requests.exceptions.InvalidURL as e:
                self._sessions += 1
                msg = f"A {type(e)} exception occurred. Likely a problem with the url: {url}. Aborting request."
                self._logger.error(msg)
                break
            except requests.exceptions.InvalidHeader as e:
                self._sessions += 1
                msg = f"A {type(e)} exception occurred. Check headers.\n{headers}. Retrying with new session #{self._sessions}."
                self._logger.error(msg)
            except requests.exceptions.RetryError as e:
                self._sessions += 1
                msg = f"A {type(e)} exception occurred after {self._retries} retries. Retrying with new session #{self._sessions}."
                self._logger.error(msg)

        self._logger.error("All retry and session limits have been reached. Exiting.")

    def _get_headers(self) -> dict:
        """Returns a randomly selected header from available HEADERS"""
        return random.choice(HEADERS)

    def _get_proxy(self) -> dict:
        """Returns proxy servers"""
        proxy = random.choice(SERVERS)
        return {"http": proxy, "https": proxy}
