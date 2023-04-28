#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/infrastructure/web/autothrottle.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 26th 2023 09:48:43 pm                                               #
# Modified   : Thursday April 27th 2023 04:39:16 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Autothrottle Module"""
from datetime import datetime
from time import sleep
from typing import Union

from aimobile.infrastructure.web.base import AutoThrottle

# ------------------------------------------------------------------------------------------------ #


class AutoThrottleLatency(AutoThrottle):
    """Manages delays between HTTP requests on a website.

    Args:
        start_delay (int): The initial delay in seconds. Default = 5
        min_delay (int): Minimum number of seconds between requests. Default = 1
        max_delay (int): Maximum number of seconds between requests, unless backing off.
            Default = 10
        lambda_factor (float): The average rate of requests per second. Default = 0.5.
        backoff_factor: Factor by which the request delay is increased each invalid response.
            Default = 2.
        warmup (int): Number of requests before average latency is computed, and used to
            compute the delay.
        concurrency (int): The max number of concurrent requests. Default = 1

    """

    # Lambda factors are indexed by (4)-6 hour time windows, such that:
    #   0 index corresponds to lambda_factor from 12AM-5:59AM, 1 indexes
    #   the 2nd time window from 6AM until 11:59AM, and so on.
    #   the
    __lambda_factors = [1, 0.75, 0.75, 0.5]
    __window_size = 6

    def __init__(
        self,
        start_delay: int = 5,
        min_delay: int = 1,
        max_delay: int = 10,
        lambda_factor: float = 0.5,
        backoff_factor: int = 2,
        concurrency: int = 1,
        timeaware: bool = True,
    ) -> None:
        super().__init__(
            start_delay=start_delay,
            min_delay=min_delay,
            max_delay=max_delay,
            lambda_factor=lambda_factor,
            backoff_factor=backoff_factor,
            concurrency=concurrency,
            timeaware=timeaware,
        )

        # If timeaware, select lambda_factor based upon datetime.
        if self._timeaware:
            self._lambda_factor = self._get_lambda_factor()

    def delay(self, latency: float, response, wait: bool = True) -> Union[float, None]:
        """Computes and optionally executes a delay, related to request latency and status code.

        This method has two modes: wait and non-wait. In wait mode, the method
        computes and executes a delay that adjusts according to server latency and
        response. In non-wait mode, the delay time is immediately returned.
        """

        if response.status_code == 200:
            delay = self._delay(latency=latency)
        else:
            delay = self._backoff(latency=latency)
        if wait:
            sleep(delay)
        else:
            return delay

    def _delay(self, latency: float) -> float:
        """Computes a delay for a successful 200 response status code based on latency magnitude..

        Args:
            latency (float): Latency in milliseconds.

        """
        # Target delay is the number of concurrent round trips allowed per request.
        target_delay = latency / self._concurrency
        # Compute adjusted delay as average of prior delay and target delay
        new_delay = (target_delay + self._prior_delay) / 2.0
        # Generate random delay using exponential distribution with scale = 1 / lambda_factor
        random_factor = float(self._distribution.rvs(size=1))
        # Adjust new_delay using random factor
        new_delay = new_delay + random_factor
        # New delay should be at least the target delay
        new_delay = max(target_delay, new_delay)
        # New Delay should be between min and max delay
        new_delay = min(max(self._min_delay, new_delay), self._max_delay)
        # Store state
        self._prior_delay = new_delay
        self._prior_latency = latency
        # Viola
        return new_delay

    def _get_lambda_factor(self) -> int:
        """Returns the index for the current 6 hour time window."""
        hour = int(datetime.now().strftime("%H"))
        window = hour / self.__window_size
        return self.__lambda_factors[int(window)]
