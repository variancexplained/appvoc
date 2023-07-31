#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /tests/conftest.py                                                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:01:48 pm                                                  #
# Modified   : Sunday July 30th 2023 09:51:18 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
import pytest
import random
import dotenv
import subprocess
from datetime import datetime

from appstore.infrastructure.io.local import IOService
from appstore.container import AppstoreContainer
from appstore.infrastructure.web.headers import STOREFRONT
from appstore.data.acquisition.appdata.project import AppDataProject

# ------------------------------------------------------------------------------------------------ #
collect_ignore = [""]

# ================================================================================================ #
#                                FRAMEWORK TEST FIXTURES                                           #
# ================================================================================================ #
APPDATA_RATINGS_FILEPATH = "tests/data/appdata/rating/appdata.pkl"
DATAFRAME_FILEPATH = "tests/data/test.csv"
APPDATA_FILEPATH = "tests/data/appdata.csv"
APPDATA_HEALTH_FILEPATH = "tests/data/appstore_health.csv"
REVIEWS_FILEPATH = "tests/data/reviews.csv"
RATINGS_FILEPATH = "tests/data/appstore_ratings.csv"
RESET_SCRIPT = "tests/scripts/reset.sh"
RATING_JOBS_FILEPATH = "tests/data/job/rating.csv"
REVIEW_JOBS_FILEPATH = "tests/data/job/review.csv"
APP_IDS = ["297606951", "544007664", "951937596", "310633997", "422689480"]
APPS = [
    {"id": "297606951", "name": "amazon", "category_id": "6024", "category": "SHOPPING"},
    {"id": "544007664", "name": "youtube", "category_id": "6005", "category": "SOCIAL_NETWORKING"},
    {"id": "951937596", "name": "outlook", "category_id": "6000", "category": "BUSINESS"},
    {"id": "422689480", "name": "gmail", "category_id": "6002", "category": "UTILITIES"},
    {"id": "310633997", "name": "whatsapp", "category_id": "6002", "category": "UTILITIES"},
]
EPOCH = "1970-01-01 00:00:00"
collect_ignore = ["test_database*.*"]


# ------------------------------------------------------------------------------------------------ #
#                                      APP IDS                                                     #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def apps():
    return APPS


# ------------------------------------------------------------------------------------------------ #
#                                        URLS                                                      #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def urls():
    urls = []
    for id in APP_IDS:  # noqa
        url = f"https://itunes.apple.com/us/customer-reviews/id{id}?displayable-kind=11"
        urls.append(url)

    return urls


# ------------------------------------------------------------------------------------------------ #
#                                   RESET TEST DB                                                  #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def reset():
    subprocess.run(RESET_SCRIPT, shell=True)


# ------------------------------------------------------------------------------------------------ #
#                                  SET MODE TO TEST                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=True)
def mode():
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    prior_mode = os.environ["MODE"]
    os.environ["MODE"] = "test"
    dotenv.set_key(dotenv_file, "MODE", os.environ["MODE"])
    yield
    os.environ["MODE"] = prior_mode
    dotenv.set_key(dotenv_file, "MODE", os.environ["MODE"])


# ------------------------------------------------------------------------------------------------ #
#                              DEPENDENCY INJECTION                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=True)
def container():
    container = AppstoreContainer()
    container.init_resources()
    container.wire(packages=["appstore.data.acquisition", "appstore.data.analysis"])

    return container


# ------------------------------------------------------------------------------------------------ #
#                                 DATABASE FIXTURES                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def dataframe():
    df = IOService.read(DATAFRAME_FILEPATH)
    return df


# ------------------------------------------------------------------------------------------------ #
#                                        APPDATA                                                   #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def appdata():
    df = IOService.read(APPDATA_HEALTH_FILEPATH)
    return df


# ------------------------------------------------------------------------------------------------ #
#                                    APPDATA REPO ZERO                                             #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def appdata_repo(container):
    repo = container.data.appdata_repo()
    repo.delete_all()
    repo.save()
    return repo


# ------------------------------------------------------------------------------------------------ #
#                                     RATING JOB_DF                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def rating_job_df(rating_jobs):
    return rating_jobs.sample(1)


# ------------------------------------------------------------------------------------------------ #
#                                     REVIEW JOB_DF                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def review_job_df(review_jobs):
    return review_jobs.sample(1)


# ------------------------------------------------------------------------------------------------ #
#                                       RATING JOBS                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def rating_jobs():
    return IOService.read(RATING_JOBS_FILEPATH)


# ------------------------------------------------------------------------------------------------ #
#                                       REVIEW JOBS                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def review_jobs():
    return IOService.read(REVIEW_JOBS_FILEPATH)


# ------------------------------------------------------------------------------------------------ #
#                                  RATING JOB REPO ZERO                                            #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def rating_job_repo(container):
    repo = container.data.rating_job_repo()
    df = repo.getall()
    repo.delete_all()
    repo.save()
    yield repo
    repo.add(df)
    repo.save()


# ------------------------------------------------------------------------------------------------ #
#                                  REVIEW JOB REPO ZERO                                            #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def review_job_repo(container):
    repo = container.data.review_job_repo()
    df = repo.getall()
    repo.delete_all()
    repo.save()
    yield repo
    repo.add(df)
    repo.save()


# ------------------------------------------------------------------------------------------------ #
#                               APPDATA REPO RATINGS UOW                                           #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def uow(container):
    df = IOService.read(APPDATA_RATINGS_FILEPATH)
    uow = container.data.uow()
    uow.rollback()
    uow.appdata_repo.replace(data=df)
    uow.save()
    return uow


# ------------------------------------------------------------------------------------------------ #
#                                        APPDATA PROJECT                                           #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def appdata_project():
    return AppDataProject(
        controller="AppDataController",
        term="weather",
        status="in_progress",
        page_size=200,
        pages=5,
        vpages=5,
        apps=1000,
        started=datetime.now(),
        updated=datetime.now(),
    )


# ------------------------------------------------------------------------------------------------ #
#                                      APPDATA PROJECT REPO                                        #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def appdata_project_repo(container, appdata_project):
    uow = container.data.uow()
    return uow.appdata_project_repo


# ------------------------------------------------------------------------------------------------ #
#                                  APPSTORE RATINGS REPO                                           #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def appstore_rating_repo(container):
    repo = container.data.rating_repo()
    repo.delete_all()
    df = IOService.read(RATINGS_FILEPATH)
    repo.add(data=df)
    return repo


# ------------------------------------------------------------------------------------------------ #
#                                        REVIEWS                                                   #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def review():
    df = IOService.read(REVIEWS_FILEPATH)
    return df


# ------------------------------------------------------------------------------------------------ #
#                                        RATINGS                                                   #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def rating():
    df = IOService.read(RATINGS_FILEPATH)
    return df


# ------------------------------------------------------------------------------------------------ #
#                                      WEB FIXTURES                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
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


@pytest.fixture(scope="function", autouse=False)
def request_ratings():
    # Note: Taking '/json' of the end of the url. Want actual response object returned.
    d = {
        "url": f"https://itunes.apple.com/{STOREFRONT['country']}/customer-reviews/id{random.choice(APP_IDS)}?displayable-kind=11",
        "headers": STOREFRONT["headers"],
    }
    return d
