#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/infrastructure/web/utils.py                                               #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
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
