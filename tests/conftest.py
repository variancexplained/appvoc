#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /tests/conftest.py                                                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:01:48 pm                                                  #
# Modified   : Thursday April 20th 2023 03:59:12 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pytest
import random

from aimobile.infrastructure.io.local import IOService
from tests.container import TestContainer

# ------------------------------------------------------------------------------------------------ #
collect_ignore = [""]

# ================================================================================================ #
#                                FRAMEWORK TEST FIXTURES                                           #
# ================================================================================================ #

DATAFRAME_FILEPATH = "tests/data/test.csv"
APPDATA_FILEPATH = "tests/data/appdata.csv"
APP_IDS = ["297606951", "544007664", "951937596", "310633997", "422689480"]
STOREFRONTS = [
    {"country": "us", "headers": {"X-Apple-Store-Front": "143441-1,29"}},
    {"country": "au", "headers": {"X-Apple-Store-Front": "143460,29"}},
    {"country": "ca", "headers": {"X-Apple-Store-Front": "143455-6,29"}},
    {"country": "gb", "headers": {"X-Apple-Store-Front": "143444,29"}},
]

collect_ignore = ["test_database*.*"]


# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="session", autouse=True)
def container():
    container = TestContainer()
    container.init_resources()
    return container


# ------------------------------------------------------------------------------------------------ #
#                                 DATABASE FIXTURES                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="session", autouse=True)
def dataframe():
    df = IOService.read(DATAFRAME_FILEPATH)
    return df


# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="session", autouse=True)
def appdata():
    df = IOService.read(APPDATA_FILEPATH)
    return df


# ------------------------------------------------------------------------------------------------ #
#                                      WEB FIXTURES                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="session", autouse=True)
def request_appdata():
    d = {
        "url": "https://itunes.apple.com/search",
        "params": {
            "media": "software",
            "term": "health",
            "country": "us",
            "lang": "en-us",
            "explicit": "yes",
            "limit": 5,
            "offset": 0,
        },
    }
    return d


@pytest.fixture(scope="function", autouse=True)
def request_ratings():
    # Note: Taking '/json' of the end of the url. Want actual response object returned.
    storefront = random.choice(STOREFRONTS)
    d = {
        "url": f"https://itunes.apple.com/{storefront['country']}/customer-reviews/id{random.choice(APP_IDS)}?displayable-kind=11",
        "headers": storefront["headers"],
    }
    return d
