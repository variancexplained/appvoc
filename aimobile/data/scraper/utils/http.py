#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Opportunity Discovery in Mobile Applications                             #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/scraper/utils/http.py                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday April 4th 2023 07:57:55 am                                                  #
# Modified   : Wednesday April 5th 2023 05:18:31 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module for handling HTTP requests"""
import requests
from dataclasses import dataclass, field
from datetime import datetime
from requests.adapters import HTTPAdapter
import time
import logging
import random
from typing import Dict, List

from aimobile.data.scraper.utils.headers import HEADERS, SERVERS
from aimobile.data.scraper.base import IMMUTABLE_TYPES, SEQUENCE_TYPES


# ------------------------------------------------------------------------------------------------ #
class HTTPDefault:
    TIMEOUT = 30
    TOTAL_RETRIES = 5
    SESSIONS = 3
    DELAY = (1, 5)
    BACKOFF_FACTOR = 2
    STATUS_FORCELIST = [104, 429, 500, 502, 503, 504]
    METHOD_WHITELIST = ["HEAD", "GET" "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
    RAISE_ON_REDIRECT = False
    RAISE_ON_STATUS = False


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RetryParams:
    total: int = HTTPDefault.TOTAL_RETRIES
    backoff_factor: int = HTTPDefault.BACKOFF_FACTOR
    allowed_methods: List = field(default_factory=lambda: HTTPDefault.METHOD_WHITELIST)
    status_forcelist: List = field(default_factory=lambda: HTTPDefault.STATUS_FORCELIST)
    raise_on_redirect: bool = HTTPDefault.RAISE_ON_REDIRECT
    raise_on_status: bool = HTTPDefault.RAISE_ON_STATUS
    sessions: int = 3

    def as_dict(self) -> dict:
        """Returns a dictionary representation of the the parameter object."""
        return {k: self._export_config(v) for k, v in self.__dict__.items()}

    @classmethod
    def _export_config(cls, v):
        """Returns v with Configs converted to dicts, recursively."""
        if isinstance(v, IMMUTABLE_TYPES):
            return v
        elif isinstance(v, SEQUENCE_TYPES):
            return type(v)(map(cls._export_config, v))
        elif isinstance(v, datetime):
            return v.strftime("%m/%d/%Y, %H:%M")
        elif isinstance(v, dict):
            return {kk: cls._export_config(vv) for kk, vv in v}
        else:
            try:
                return v.__class__.__name__
            except:  # noqa 722
                return "Mutable Object"


# ------------------------------------------------------------------------------------------------ #


class TimeoutHTTPAdapter(HTTPAdapter):
    """Wraps an HTTP request with timeout capability"""

    def __init__(self, *args, **kwargs):
        if "timeout" in kwargs:
            self._timeout = kwargs["timeout"]
            del kwargs["timeout"]
        else:
            self._timeout = HTTPDefault.TIMEOUT

        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        if kwargs["timeout"] is None:
            kwargs["timeout"] = self._timeout
        return super().send(request, **kwargs)


# ------------------------------------------------------------------------------------------------ #
class HTTPRequest:
    """Wrapper for the requests module.

    Args:
        retry_strategy (urllib3.util.Retry): Instance of the urllib3 Retry object that controls
            the number and timing of retries.
        timeout (int): Seconds allowed for a response. Default is 30 seconds.
        delay (tuple): Lower and upper bound in seconds of random sleep delays. Default (1,5).

    """

    def __init__(
        self,
        timeout: TimeoutHTTPAdapter,
        delay: tuple = HTTPDefault.DELAY,
    ) -> None:
        self._timeout = timeout
        self._delay = delay

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def get(self, url, headers: dict = None, params: dict = None) -> requests.Response:
        """Performs the HTTP request, retrying if necessary, according to parameters

        Args:
            url (str): The base url for the http request.
            headers (dict): HTTP request header.
            params (dict): Parameters for the url
        """
        sessions = 0
        while sessions < self._sessions:

            session = requests.Session()
            session.mount("https://", self._timeout)
            session.mount("http://", self._timeout)
            try:
                # Random delay
                sleep = random.randint(*self._delay)
                time.sleep(sleep)
                # Rotate proxy servers
                proxy = random.randint(0, len(SERVERS) - 1)
                proxies = {"http": SERVERS[proxy], "https": SERVERS[proxy]}
                # Execute session request
                response = session.get(url=url, headers=headers, params=params, proxies=proxies)
                self._logger.debug(
                    f"\nRequest status code: {response.status_code}. Session: {session}"
                )
                return response

            except requests.exceptions.Timeout as e:
                sessions += 1
                msg = f"A {type(e)} exception occurred after {self._retries} retries. Invoking new session #{sessions}."
                self._logger.error(msg)
            except requests.exceptions.TooManyRedirects as e:
                sessions += 1
                msg = f"A {type(e)} exception occurred. Likely a problem with the url: {url}."
                self._logger.error(msg)
                break
            except requests.exceptions.ConnectionError as e:
                sessions += 1
                msg = f"A {type(e)} exception occurred after {self._retries} retries. Invoking new session #{sessions}."
                self._logger.error(msg)
            except requests.exceptions.JSONDecodeError as e:
                sessions += 1
                msg = f"A {type(e)} exception occurred after {self._retries} retries. Unable to decode response."
                self._logger.error(msg)
                break
            except requests.exceptions.InvalidURL as e:
                sessions += 1
                msg = f"A {type(e)} exception occurred. Likely a problem with the url: {url}."
                self._logger.error(msg)
                break
            except requests.exceptions.InvalidHeader as e:
                sessions += 1
                msg = f"A {type(e)} exception occurred. Check headers.\n{headers}."
                self._logger.error(msg)
                break
            except requests.exceptions.RetryError as e:
                sessions += 1
                msg = f"A {type(e)} exception occurred after {self._retries} retries. Invoking new session #{sessions}."
                self._logger.error(msg)

        self._logger.error("All retry and session limits have been reached. Exiting.")

    def _get_headers(self) -> Dict[str, str]:
        """Returns a randomly selected header"""
        return random.choice(HEADERS)
