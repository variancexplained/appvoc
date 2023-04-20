#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/infrastructure/web/adapter.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 03:21:04 am                                                 #
# Modified   : Wednesday April 19th 2023 09:34:33 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from requests.adapters import HTTPAdapter

from aimobile.infrastructure.web.params import HTTPVars


# ------------------------------------------------------------------------------------------------ #
class TimeoutHTTPAdapter(HTTPAdapter):
    """Wraps an HTTP request with timeout capability"""

    def __init__(self, *args, **kwargs):
        if "timeout" in kwargs:
            self._timeout = kwargs["timeout"]
            del kwargs["timeout"]
        else:
            self._timeout = HTTPVars.TIMEOUT

        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        if kwargs["timeout"] is None:
            kwargs["timeout"] = self._timeout
        return super().send(request, **kwargs)
