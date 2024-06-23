#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/infrastructure/web/utils.py                                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday July 31st 2023 06:32:36 pm                                                   #
# Modified   : Wednesday August 2nd 2023 02:27:26 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import sys
import requests


# ------------------------------------------------------------------------------------------------ #
def getsize(response: requests.Response) -> int:
    """Returns the size of an HTTP response object.

    Args:
        response (requests.Response): An HTTP Response object.

    """
    try:
        size = int(response.headers["content-length"])
    except KeyError:
        size = sys.getsizeof(response.json())
    except Exception:
        size = sys.getsizeof(response)
    return size
