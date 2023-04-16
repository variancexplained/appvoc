#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/tests/conftest.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:01:48 pm                                                  #
# Modified   : Thursday April 13th 2023 10:08:40 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import pytest
import random
from datetime import datetime

import pandas as pd

from ..container import AppStoreContainer
from .. import IOService
from ..entity.project import AppStoreProject
from ..entity.request import AppStoreRequest
from ..entity.review import AppStoreReview
from ..entity.base import AppStoreCategories
from .. import directories

# ------------------------------------------------------------------------------------------------ #
HOME = "aimobile/scraper/appstore"
DATAFRAME_FILEPATH = os.path.join(HOME, "tests/testdata/test.csv")
APPDATA = os.path.join(HOME, "tests/testdata/appdata.csv")
PROJECTS = os.path.join(HOME, "tests/testdata/projects.csv")
CATEGORIES = [
    {"BOOKS": AppStoreCategories.BOOKS},
    {"BUSINESS": AppStoreCategories.BUSINESS},
    {"GAMES": AppStoreCategories.GAMES},
    {"HEALTH_AND_FITNESS": AppStoreCategories.HEALTH_AND_FITNESS},
]
DEVELOPERS = ["apple", "microsoft", "oracle", "youtube", "meta", "google", "amazon"]
# ------------------------------------------------------------------------------------------------ #
collect_ignore = ["/home/john/projects/aimobile/mysqld.sock"]


# ------------------------------------------------------------------------------------------------ #
def make_directories() -> None:
    """Creates the directories required for logging and database persistence"""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


@pytest.fixture(scope="session", autouse=True)
def dataframe():
    df = IOService.read(DATAFRAME_FILEPATH)
    return df


@pytest.fixture(scope="session", autouse=True)
def project():
    return AppStoreProject(name="health")


@pytest.fixture(scope="session", autouse=True)
def appdata():
    app_list = []
    for i in range(10):
        category = random.choice(CATEGORIES)
        appdata = {}
        appdata["id"] = i
        appdata["name"] = f"app_{i}"
        appdata["description"] = f"lovely app #{i}"
        appdata["category_id"] = list(category.values())[0]
        appdata["category"] = list(category.keys())[0]
        appdata["price"] = random.randrange(0, 2000)
        appdata["rating"] = random.randrange(0, 5)
        appdata["ratings"] = random.randint(10, 9999)
        appdata["developer_id"] = random.randint(1000, 9999)
        appdata["developer"] = random.choice(DEVELOPERS)
        appdata["released"] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        appdata["source"] = "itunes.apple.com"
        app_list.append(appdata)

    return pd.DataFrame(app_list)


@pytest.fixture(scope="session", autouse=True)
def http_request():
    return {
        "url": "https://itunes.apple.com/search?",
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


@pytest.fixture(scope="session", autouse=True)
def request_entity():
    return AppStoreRequest(
        host="itunes.apple.com",
        name="health",
        page=0,
        content_length=322,
        results=25,
        requested=datetime.now(),
        responded=datetime.now(),
        response_time=232,
        status_code=200,
        sessions=2,
        proxy="128.456.78",
    )


@pytest.fixture(scope="session", autouse=True)
def review():
    return AppStoreReview(
        id=1,
        app_id=652145,
        app_name="some_test_app",
        category_id=6013,
        category="test_category",
        author="test_author",
        rating=4.258,
        title="some_title",
        content="love this test app",
        vote_sum=4574,
        vote_count=6523,
        date="April 13, 2023",
        source="my.test.source",
    )


@pytest.fixture(scope="session", autouse=True)
def container():
    make_directories()
    container = AppStoreContainer()
    container.init_resources()
    container.wire(
        modules=[
            "aimobile.scraper.appstore.container",
            "aimobile.scraper.appstore.repo.datacentre",
            "aimobile.scraper.appstore.service.reviews",
            "aimobile.scraper.appstore.service.appdata",
        ]
    )

    return container
