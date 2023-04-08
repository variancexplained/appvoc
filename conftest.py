#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Opportunity Discovery in Mobile Applications                             #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /conftest.py                                                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:01:48 pm                                                  #
# Modified   : Friday April 7th 2023 06:37:17 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import pytest

from aimobile.container import AIMobile
from aimobile.data.scraper.utils.io import IOService
from aimobile.data.scraper.appstore.entity.project import AppStoreProject


# ------------------------------------------------------------------------------------------------ #
DATAFRAME_FILEPATH = "tests/data/test.csv"
APPDATA = "tests/data/appdata.csv"
PROJECTS = "tests/data/projects.csv"
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
def project():
    return AppStoreProject(name="test_project", description="some test project", term="health")


@pytest.fixture(scope="session", autouse=True)
def appdata():
    appdata = IOService.read(APPDATA)
    return appdata.to_dict(orient="index")


@pytest.fixture(scope="session", autouse=True)
def container():
    container = AIMobile()
    container.init_resources()
    container.wire(
        modules=[
            "aimobile.container",
            "aimobile.data.scraper.appstore.service.builder",
            "aimobile.data.scraper.appstore.dal.datacentre",
        ]
    )

    return container
