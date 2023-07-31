#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/infrastructure/web/response.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday July 31st 2023 04:55:52 am                                                   #
# Modified   : Monday July 31st 2023 06:05:00 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import sys
from dataclasses import dataclass
from datetime import datetime
import functools

import requests

from appstore.base import DTO


# ------------------------------------------------------------------------------------------------ #
@dataclass
class Response(DTO):
    response: requests.Response
    status_code: int
    size: int
    latency: float
    throughput: float = None

    def __post_init__(self) -> None:
        self.throughput = self.size / self.latency


# ------------------------------------------------------------------------------------------------ #
def response_agent(func):
    """Wraps response with a Response object."""

    @functools.wraps(func)
    def response_wrapper(*args, **kwargs):
        start = datetime.now()
        r = func(*args, **kwargs)
        end = datetime.now()

        latency = (end - start).total_seconds()
        try:
            size = int(r.headers["content-length"])
        except KeyError:
            size = sys.getsizeof(r.json())
        except Exception:
            size = 0
        throughput = size / latency

        response = Response(
            response=r, status_code=r.status_code, latency=latency, size=size, throughput=throughput
        )
        return response

    return response_wrapper
