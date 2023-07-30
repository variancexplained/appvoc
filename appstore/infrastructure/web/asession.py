#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/infrastructure/web/asession.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 03:15:52 am                                                 #
# Modified   : Saturday July 29th 2023 04:38:08 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import logging
from dotenv import load_dotenv

import asyncio

# import httpx

import aiohttp


from appstore.infrastructure.web.base import PROXY_SERVERS
from appstore.infrastructure.web.headers import BrowserHeader
from appstore.infrastructure.web.throttle import AThrottle

load_dotenv()


# ------------------------------------------------------------------------------------------------ #
class ASessionHandler:
    """Asyncronous Session Handler

    Args:
        session_retries (int): Number of sessions to retry if timeout retry maximum has been reached.

    """

    def __init__(
        self,
        throttle: AThrottle,
        headers: BrowserHeader,
        max_concurrency: int = 10,
        retries: int = 3,
        timeout: int = 30,
        proxies: list = PROXY_SERVERS,
    ) -> None:
        self._throttle = throttle
        self._proxies = proxies
        self._retries = retries
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._headers = iter(headers)
        self._max_concurrency = max_concurrency

        self._proxy = None  # The proxy used for the current request
        self._header = None  # The header used for the current request.

        self._responses = None

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    async def responses(self) -> list:
        """Returns the responses"""
        return self._responses

    async def get(self, urls: list, headers: dict = None) -> list:
        """Entry point returns results from asynchronous http requests

        Args:
            urls (list): List of urls for http requests
        """

        headers = headers or next(self._header)

        conn = aiohttp.TCPConnector()

        concurrency = asyncio.Semaphore(self._max_concurrency)

        async with aiohttp.ClientSession(
            headers=headers,
            connector=conn,
            trust_env=True,
            raise_for_status=True,
            timeout=self._timeout,
        ) as client:
            tasks = [self._make_request(client, url, concurrency) for url in urls]
            self._responses = await asyncio.gather(*tasks)
        return self._responses

    async def _make_request(
        self,
        client: aiohttp.ClientSession,
        url: str,
        concurrency: asyncio.Semaphore,
    ):
        """Executes the http request and returns a Response object.

        Args:
            client (httpx.AsyncClient): The http client executing the http request.
            url (str): The base url for the http request
            concurrency (asyncio.Semaphore): Controls number of concurrent requests.
            headers (dict): A dictionary containing header parameters.If None provided, standard rotating headers will be used.
        """

        proxy = self._get_proxy()

        retries = 0

        async with concurrency:
            while retries < self._retries:
                try:
                    self._throttle.start()
                    async with client.get(url, proxy=proxy, ssl=False) as response:
                        self._throttle.stop()
                        self._throttle.delay()
                        return await response.json()

                except Exception as e:
                    retries += 1
                    msg = f"Exception type {type(e)} occurred.\n{e}\nExecuting retry # {retries}."
                    self._logger.exception(msg)
            msg = "Exhausted retries. Returning to calling environment."
            self._logger.exception(msg)

    def _get_proxy(self) -> dict:
        dns = os.getenv("WEBSHARE_DNS")
        username = os.getenv("WEBSHARE_USER")
        pwd = os.getenv("WEBSHARE_PWD")
        port = os.getenv("WEBSHARE_PORT")
        proxy = f"http://{username}:{pwd}@{dns}:{port}"
        return proxy
