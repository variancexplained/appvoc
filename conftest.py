#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /conftest.py                                                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:01:48 pm                                                  #
# Modified   : Saturday April 1st 2023 05:12:39 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pytest

from aimobile.container import AIMobile
from aimobile.service.io import IOService

# ------------------------------------------------------------------------------------------------ #
DATAFRAME_FILEPATH = "tests/data/test.csv"
# ------------------------------------------------------------------------------------------------ #
collect_ignore = [
    "aimobile/data/scraper/appstore.py",
    "aimobile/data/scraper/appstore/service/appdata.py",
]


@pytest.fixture(scope="session", autouse=True)
def dataframe():
    df = IOService.read(DATAFRAME_FILEPATH)
    return df


@pytest.fixture(scope="session", autouse=True)
def container():
    container = AIMobile()
    container.init_resources()
    container.wire(modules=["aimobile.container"])

    return container
