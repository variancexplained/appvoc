#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/scraper/utils/http.py                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday April 4th 2023 07:57:55 am                                                  #
# Modified   : Tuesday April 4th 2023 05:20:06 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module for handling HTTP requests"""
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from dotenv import load_dotenv
import time
import logging
import random
from typing import Dict

from user_agents import parse


# ------------------------------------------------------------------------------------------------ #
class HTTPDefault:
    TIMEOUT = 30
    TOTAL_RETRIES = 3
    SESSIONS = 3
    DELAY = (1, 5)
    BACKOFF_FACTOR = 2
    STATUS_FORCELIST = [104, 429, 500, 502, 503, 504]
    METHOD_WHITELIST = ["HEAD", "GET" "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]


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
class Requests:
    """Wrapper for the requests module.

    Args:
        timeout (int): Seconds allowed for a response. Default is 30 seconds.
        delay (tuple): Lower and upper bound in seconds of random sleep delays. Default (1,5).
        retries (int): Number of retries in the event of an exception. Default is 5
        backoff_factor (int): The multiplier base for exponential backoff. Default is 2.
        status_forcelist (list): Error codes

    """

    def __init__(
        self,
        timeout: int = HTTPDefault.TIMEOUT,
        delay: tuple = HTTPDefault.DELAY,
        retries: int = HTTPDefault.TOTAL_RETRIES,
        sessions: int = HTTPDefault.SESSIONS,
        backoff_factor: int = HTTPDefault.BACKOFF_FACTOR,
        status_forcelist: list = HTTPDefault.STATUS_FORCELIST,
        method_whitelist: list = HTTPDefault.METHOD_WHITELIST,
    ) -> None:
        self._timeout = timeout
        self._delay = delay
        self._retries = retries
        self._sessions = sessions
        self._backoff_factor = backoff_factor
        self._status_forcelist = status_forcelist
        self._method_whitelist = method_whitelist

        load_dotenv()
        self._proxies = os.getenv("VPN_PROXY")
        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def request(self, url, headers: dict, params: dict) -> requests.Response:
        """Performs the HTTP request, retrying if necessary, according to parameters

        Args:
            url (str): The base url for the http request.
            headers (dict): HTTP request header.
            params (dict): Parameters for the url
        """
        sessions = 0
        while sessions < self._sessions:

            retry_strategy = Retry(
                total=self._retries,
                status_forcelist=self._status_forcelist,
                method_whitelist=self._method_whitelist,
                backoff_factor=self._backoff_factor,
                raise_on_redirect=True,
                raise_on_status=False,
            )
            session = requests.Session()
            session.mount(
                "https://", TimeoutHTTPAdapter(timeout=self._timeout, max_retries=retry_strategy)
            )
            session.mount(
                "http://", TimeoutHTTPAdapter(timeout=self._timeout, max_retries=retry_strategy)
            )
            try:
                # Random delay
                sleep = random.randint(*self._delay)
                time.sleep(sleep)
                return session.get(url=url, headers=headers, params=params, proxies=self._proxies)

            except requests.exceptions.Timeout as e:
                sessions += 1
                msg = f"A {type(e)} exception occurred after {self._retries} retries. Invoking new session #{sessions}."
                self._logger.error(msg)
            except requests.exceptions.TooManyRedirects as e:
                sessions += 1
                msg = f"A {type(e)} exception occurred. Likely a problem with the url: {url}."
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


# ------------------------------------------------------------------------------------------------ #
class Headers:
    """Generates HTTP headers"""

    def _ua_to_ch(self, ua_string: str) -> Dict[str, str]:
        """Converts Chrome User-Agent string to sec-ch (client hint) headers.

        Args:
            ua_string (str): The user_agent string.

        Usage:
            $ python user-agent-to-sec-ch.py "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like G
            ecko) Chrome/99.0.4844.51 Safari/537.36"

            {'sec-ch-ua': ' Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows'}
        """

        parsed = parse(ua_string)
        major_version = parsed.browser.version[0]
        assert parsed.browser.family == "Chrome", "only chrome user agent strings supported"
        return {
            "sec-ch-ua": f' Not A;Brand";v="{major_version}", "Chromium";v="{major_version}", "Google Chrome";v="{major_version}"',
            "sec-ch-ua-mobile": f"?{int(parsed.is_mobile)}",
            "sec-ch-ua-platform": parsed.get_os().split()[0],
        }
