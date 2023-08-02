#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/infrastructure/web/throttle.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 26th 2023 09:48:43 pm                                               #
# Modified   : Tuesday August 1st 2023 09:49:18 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Autothrottle Module"""
from time import sleep
from datetime import datetime
import logging
from typing import Union

from scipy.stats import expon
import numpy as np

from appstore.infrastructure.web.base import Throttle

# ------------------------------------------------------------------------------------------------ #


class LatencyThrottle(Throttle):
    """Throttles based upon the target website latency.

    Args:
        start_delay (int): The initial delay in milliseconds. Default = 3000
        min_delay (int): Minimum number of milliseconds between requests. Default = 1000
        max_delay (int): Maximum number of milliseconds between requests, unless backing off.
            Default = 10000
        backoff_factor: Factor by which the request delay is increased each invalid response.
            Default = 2.
        verbose (int): Degree of verbosity in terms of the number of requests between
            progress reports to the log.

    """

    def __init__(
        self,
        start_delay: int = 3000,
        min_delay: int = 1000,
        max_delay: int = 10000,
        verbose: int = 50,
    ) -> None:
        super().__init__()
        self._start_delay = start_delay
        self._min_delay = min_delay
        self._max_delay = max_delay
        self._verbose = verbose

        self._prior_delay = start_delay
        self._counter = 0
        self._latency = None
        self._latencies = []
        self._wait = []

        self._start = None
        self._end = None

    def start(self) -> None:
        self._start = datetime.now()

    def stop(self) -> None:
        self._end = datetime.now()
        self._latency = (self._end - self._start).total_seconds()
        self._latencies.append(self._latency)

    def delay(self) -> Union[float, None]:
        """Computes and optionally executes a delay, related to request latency and status code.

        Delay is equal to the average of the prior delay and the latency, bounded
        by min and max delay.

        Args:
            latency (float): The time between the last request and its response
            wait (bool): Should the method sleep, or return the delay time.

        """
        # Target delay is the time of round trips allowed per request.
        target_delay = self._latency
        # Compute adjusted delay as average of prior delay and target delay
        new_delay = (target_delay + self._prior_delay) / 2.0
        # New delay should be at least the target delay
        new_delay = max(target_delay, new_delay)
        # New Delay should be between min and max delay
        new_delay = min(max(self._min_delay, new_delay), self._max_delay)
        # Store the new delay
        self._prior_delay = new_delay
        self._wait.append(new_delay)
        # Viola
        self._monitor()
        # Wait
        sleep(new_delay)

    def _monitor(self):
        """Monitors and reports average latency and delay

        Args:
            latency (float): Time between request and server response
        """
        self._counter += 1

        if self._counter % self._verbose == 0:
            min_latency = round(np.min(self._latencies), 2)
            max_latency = round(np.max(self._latencies), 2)
            ave_latency = round(np.mean(self._latencies), 2)
            std_latency = round(np.std(self._latencies), 2)
            ttl_latency = round(np.sum(self._latencies), 2)
            min_delay = round(np.min(self._wait), 2)
            max_delay = round(np.max(self._wait), 2)
            ave_delay = round(np.mean(self._wait), 2)
            std_delay = round(np.std(self._wait), 2)
            ttl_delay = round(np.sum(self._wait), 2)

            width = 32
            msg = f"\n\t{'Min Latency'.rjust(width, ' ')} | {min_latency}\n"
            msg += f"\n\t{'Max Latency'.rjust(width, ' ')} | {max_latency}\n"
            msg += f"\n\t{'Ave Latency'.rjust(width, ' ')} | {ave_latency}\n"
            msg += f"\t{'Std Latency'.rjust(width, ' ')} | {std_latency}\n"
            msg += f"\t{'Total Latency'.rjust(width, ' ')} | {ttl_latency}\n\n"
            msg += f"\t{'Min Delay'.rjust(width, ' ')} | {min_delay}\n"
            msg += f"\t{'Max Delay'.rjust(width, ' ')} | {max_delay}\n"
            msg += f"\t{'Ave Delay'.rjust(width, ' ')} | {ave_delay}\n"
            msg += f"\t{'Std Delay'.rjust(width, ' ')} | {std_delay}\n"
            msg += f"\t{'Total Delay'.rjust(width, ' ')} | {ttl_delay}\n"
            self._logger.debug(msg)

            self._counter = 0
            self._latencies = []
            self._wait = []


# ------------------------------------------------------------------------------------------------ #


class AThrottle(Throttle):
    """Async Throttle based upon the target website latency.

    Args:
        burnin_period (int): The number of requests in the burn-in period. Default is 50
        burnin_reset (int): The number of requests between each burnin period.
        burnin_rate (float): The number of requests per second during the burn-in period. Default is 1
        rolling_window_size (int): Size of the rolling window request latency array.
        cooldown_factor (float): The number by which the delay is multiplied during each cooldown.
        threshold (float): The number of standard deviations above mean latency that would trigger a cooldown.
        tolerance (float): The proportion of the rolling window above threshold that is allowed before cooldown.
        rate (float): The number of requests per second after burn-in. Default is 1.

    """

    def __init__(
        self,
        burnin_period: int = 50,
        burnin_reset: int = 1000,
        burnin_rate: float = 1,
        burnin_threshold_factor: float = 2,
        rolling_window_size: int = 25,
        cooldown_factor: float = 2,
        cooldown_phase: int = 25,
        tolerance: float = 0.8,
        rate: int = 1,
        verbose: int = 50,
    ) -> None:
        super().__init__()
        self._burnin_period = burnin_period
        self._burnin_reset = burnin_reset
        self._burnin_rate = burnin_rate
        self._burnin_threshold_factor = burnin_threshold_factor
        self._rolling_window_size = rolling_window_size
        self._cooldown_factor = cooldown_factor
        self._cooldown_phase = cooldown_phase
        self._tolerance = tolerance
        self._rate = rate
        self._verbose = verbose

        self._counter = 0
        self._cooldown_counter = 0

        self._start = None
        self._end = None
        self._latency = None

        self._burnin_latency_mean = 0
        self._burnin_latency_std = 0
        self._burnin_latency_threshold = 0
        self._burnin_latency = []
        self._latencies = []
        self._delays = []

        self._latency_window = np.zeros(self._rolling_window_size)
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def start(self) -> None:
        self._start = datetime.now()

    def stop(self) -> None:
        self._end = datetime.now()
        self._latency = (self._end - self._start).total_seconds()
        self._latencies.append(self._latency)

    def delay(self) -> Union[float, None]:
        """Computes the delay for the next request."""

        if self._starting_epoch():
            self._reset_epoch()

        if self._burning_in():
            self._burnin()
            delay = self._burnin_delay()
        else:
            delay = self._compute_delay()

        self._counter += 1
        self._delays.append(delay)
        sleep(delay)
        self._monitor()

    def _starting_epoch(self) -> bool:
        """If first request after burn-in, return True, otherwise return False"""
        if self._counter % self._burnin_reset == 0:
            return True
        return False

    def _reset_epoch(self) -> None:
        """Resets latency arrays and associated statistics."""
        self._burnin_latency_mean = 0
        self._burnin_latency_std = 0
        self._burnin_latency_threshold = 0
        self._burnin_latency = []

    def _burning_in(self) -> bool:
        """Returns True if within a burn-in period, returns False otherwise."""
        if self._counter % self._burnin_reset < self._burnin_period:
            return True
        return False

    def _burnin(self) -> float:
        """Captures statistics for the burnin-phase

        Args:
            latency (float): Time between last request and response
        """
        if len(self._burnin_latency) == 0:
            msg = "Starting Burn-in Phase"
            self._logger.debug(msg)

        self._burnin_latency.append(self._latency)
        if len(self._burnin_latency) == self._burnin_period:
            self._burnin_latency_mean = np.mean(self._burnin_latency)
            self._burnin_latency_std = np.std(self._burnin_latency)
            self._burnin_latency_threshold = (
                self._burnin_latency_mean + self._burnin_threshold_factor * self._burnin_latency_std
            )

    def _burnin_delay(self) -> float:
        """Returns the delay during burn-in."""
        return expon.rvs(scale=1 / self._burnin_rate, size=1)[0]

    def _compute_delay(self) -> int:
        """Returns the number of seconds to delay"""
        self._update_running_window(self._latency)
        delay = expon.rvs(scale=1 / self._rate, size=1)[0]
        if self._running_hot():
            delay = self._cooldown(delay)
        return delay

    def _update_running_window(self, latency: float) -> None:
        """Update the rolling window

        Args:
            latency (float): Time between last request and response
        """
        idx = self._counter % self._burnin_period
        self._latency_window[idx] = latency

    def _running_hot(self) -> bool:
        """Returns True if tolerance of window_size is above threshold, and returns False otherwise."""
        return (
            np.sum(np.where(self._latency_window > self._burnin_latency_threshold))
            > self._tolerance * self._rolling_window_size
        )

    def _cooldown(self, delay: float) -> float:
        """If rate has been adjusted and watching the rolling window_size"""
        if self._cooldown_counter == 0:
            delay = delay * self._cooldown_factor
            self._cooldown_counter += 1
            msg = f"\n\nStarting Cool Down Phase. Setting delay to {delay}\n"
            self._logger.debug(msg)

        elif self._cooldown_counter == self._cooldown_phase:
            msg = "Ending Cool Down Phase"
            self._logger.debug(msg)
            self._cooldown_counter = 0
        return delay

    def _monitor(self) -> None:
        if self._counter % self._verbose == 0:
            min_latency = np.min(self._latencies)
            mean_latency = np.mean(self._latencies)
            std_latency = np.std(self._latencies)
            max_latency = np.max(self._latencies)
            min_delay = np.min(self._delays)
            mean_delay = np.mean(self._delays)
            std_delay = np.std(self._delays)
            max_delay = np.max(self._delays)

            self._latencies = []
            self._delays = []

            width = 24
            msg = f"{self.__class__.__name__}:\n:"
            msg += f"\t{'Count:'.rjust(width,' ')} | {self._counter}\n"
            msg += f"\t{'Min Latency:'.rjust(width,' ')} | {min_latency}\n"
            msg += f"\t{'Min Latency:'.rjust(width,' ')} | {min_latency}\n"
            msg += f"\t{'Mean Latency:'.rjust(width,' ')} | {mean_latency}\n"
            msg += f"\t{'Max Latency:'.rjust(width,' ')} | {max_latency}\n"
            msg += f"\t{'Std Latency:'.rjust(width,' ')} | {std_latency}\n\n"
            msg += f"\t{'Min Delay:'.rjust(width,' ')} | {min_delay}\n"
            msg += f"\t{'Mean Delay:'.rjust(width,' ')} | {mean_delay}\n"
            msg += f"\t{'Max Delay:'.rjust(width,' ')} | {max_delay}\n"
            msg += f"\t{'Std Delay:'.rjust(width,' ')} | {std_delay}\n"
            self._logger.debug(msg)
