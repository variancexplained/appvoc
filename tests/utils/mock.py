#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /tests/utils/mock.py                                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 03:09:07 am                                                  #
# Modified   : Saturday April 1st 2023 12:25:31 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module contains functions used to mock HTTP requests and related computationally intensive resources."""
import requests
import requests_mock

from aimobile.service.io import IOService

# ------------------------------------------------------------------------------------------------ #
JSON_FILEPATH = "tests/data/test_appdata.json"


# ------------------------------------------------------------------------------------------------ #
def mock_request() -> dict:
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount("mock://", adapter)
    data = IOService.read(JSON_FILEPATH)
    adapter.register_uri("GET", "mock://test.com/", json=data, status_code=200)
    resp = session.get("mock://test.com/")
    return resp
