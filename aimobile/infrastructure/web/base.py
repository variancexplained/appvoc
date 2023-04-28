#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/infrastructure/web/base.py                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 03:22:06 am                                                 #
# Modified   : Thursday April 27th 2023 04:23:52 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Web Infrastructure Base Module"""
from abc import ABC, abstractmethod

from scipy.stats import expon
import numpy as np
from requests import Response


# ------------------------------------------------------------------------------------------------ #
class AutoThrottle(ABC):
    """Manages delays between HTTP requests on a website.

    Args:
        start_delay (int): The initial delay in seconds. Default = 5
        min_delay (int): Minimum number of seconds between requests. Default = 1
        max_delay (int): Maximum number of seconds between requests, unless backing off.
            Default = 30
        lambda_factor (float): The average rate of requests per second. Default = 0.5.
        backoff_factor: Factor by which the request delay is increased each invalid response.
            Default = 2.
        warmup (int): Number of requests before average latency is computed, and used to
            compute the delay.
        concurrency (int): The max number of concurrent requests. Default = 1

    """

    def __init__(
        self,
        start_delay: int = 5,
        min_delay: int = 1,
        max_delay: int = 30,
        lambda_factor: float = 0.5,
        backoff_factor: int = 2,
        concurrency: int = 1,
        timeaware: bool = True,
    ) -> None:
        self._start_delay = start_delay
        self._min_delay = min_delay
        self._max_delay = max_delay
        self._lambda_factor = lambda_factor
        self._backoff_factor = backoff_factor
        self._concurrency = concurrency
        self._timeaware = timeaware

        self._prior_latency = 0
        self._prior_delay = start_delay

        self._distribution = expon(scale=1 / self._lambda_factor)

    @abstractmethod
    def delay(self, latency: float, response: Response) -> float:
        """Computes and returns a delay in seconds based upon response status and latency

        Args:
            latency (float): Seconds between request and response
            response (Response): A requests Response object.
        """

    def _backoff(self, latency: float) -> float:
        """Exponential backoff for invalid server responses, up to max delay."""
        # Apply backoff factor to prior delay
        new_delay = self._prior_delay * self._backoff_factor
        # Ensure delay doesn't exceed max delay
        new_delay = np.min(new_delay, self._max_delay)
        # Reset state: Backoff delays are not stored in history.
        self._prior_latency = latency
        # Viola
        return new_delay


# ------------------------------------------------------------------------------------------------ #
class HTTPVars:
    TIMEOUT = 30
    TOTAL_RETRIES = 5
    SESSIONS = 3
    MAX_PAGES = 99999
    LIMIT = 200
    EPOCH = 40246871
    DELAY_MIN = 1
    DELAY_MAX = 8
    BACKOFF_FACTOR = 2
    STATUS_FORCELIST = [104, 429, 500, 502, 503, 504]
    METHOD_WHITELIST = ["HEAD", "GET" "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
    RAISE_ON_REDIRECT = False
    RAISE_ON_STATUS = False
    ALLOWED_ANOMALIES = 5
    DONE = 222
    NO_CONTENT = 204


# ------------------------------------------------------------------------------------------------ #
# Servers provided courtesy of Geonode
PROXY_SERVERS = [
    "rotating-residential.geonode.com:9000",
    "rotating-residential.geonode.com:9001",
    "rotating-residential.geonode.com:9002",
    "rotating-residential.geonode.com:9003",
    "rotating-residential.geonode.com:9004",
    "rotating-residential.geonode.com:9005",
    "rotating-residential.geonode.com:9006",
    "rotating-residential.geonode.com:9007",
    "rotating-residential.geonode.com:9008",
    "rotating-residential.geonode.com:9009",
    "rotating-residential.geonode.com:9010",
]
