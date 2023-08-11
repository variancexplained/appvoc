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
# Modified   : Friday August 11th 2023 02:32:47 am                                                 #
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

from appstore.data.acquisition.base import App
from appstore.infrastructure.io.local import IOService
from appstore.container import AppstoreContainer
from appstore.infrastructure.web.headers import STOREFRONT
from appstore.data.acquisition.appdata.project import AppDataProject
from appstore.data.acquisition.review.request import ReviewRequest
from tests.data.rating.response import batch
from appstore.data.dataset.appdata import AppDataDataset
from appstore.data.dataset.rating import RatingDataset
from appstore.data.dataset.review import ReviewDataset

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
JOBS_FILEPATH = "tests/data/job/jobs.csv"

APPDATA_DATASET = "tests/data/dataset/appdata.pkl"
RATING_DATASET = "tests/data/dataset/rating.pkl"
REVIEW_DATASET = "tests/data/dataset/review.pkl"

APP_IDS = ["297606951", "544007664", "951937596", "310633997", "422689480"]

APPS = [
    {"id": "297606951", "name": "amazon", "category_id": "6024", "category": "SHOPPING"},
    {"id": "544007664", "name": "youtube", "category_id": "6005", "category": "SOCIAL_NETWORKING"},
    {"id": "951937596", "name": "outlook", "category_id": "6000", "category": "BUSINESS"},
    {
        "id": "1288723196",
        "name": "Microsoft Edge: Web Browser",
        "category_id": "6002",
        "category": "UTILITIES",
    },
    {
        "id": "284815942",
        "name": "Google",
        "category_id": "6002",
        "category": "UTILITIES",
    },
]
EPOCH = "1970-01-01 00:00:00"
collect_ignore = [
    "test_database*.*",
    "appstore/data/acquisition/rating/*.*",
    "appstore/data/acquisition/review/*.*",
]


# ------------------------------------------------------------------------------------------------ #
#                                        APPS                                                      #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def apps():
    apps = []
    for app in APPS:
        a = App(
            id=app["id"], name=app["name"], category_id=app["category_id"], category=app["category"]
        )
        apps.append(a)
    return apps


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
    prior_archive = os.environ["ARCHIVE"]
    os.environ["MODE"] = "test"
    os.environ["ARCHIVE"] = os.environ["ARCHIVE_TEST"]
    dotenv.set_key(dotenv_file, "MODE", os.environ["MODE"])
    dotenv.set_key(dotenv_file, "ARCHIVE", os.environ["ARCHIVE"])
    yield
    os.environ["MODE"] = prior_mode
    os.environ["ARCHIVE"] = prior_archive
    dotenv.set_key(dotenv_file, "MODE", os.environ["MODE"])
    dotenv.set_key(dotenv_file, "ARCHIVE", os.environ["ARCHIVE"])


# ------------------------------------------------------------------------------------------------ #
#                              DEPENDENCY INJECTION                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=True)
def container():
    container = AppstoreContainer()
    container.init_resources()
    container.wire(packages=["appstore.data.acquisition", "appstore.data.dataset"])

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
#                                  APPDATA DATASET                                                 #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def appdata_dataset():
    df = IOService.read(APPDATA_DATASET)
    ds = AppDataDataset(df=df)
    return ds


# ------------------------------------------------------------------------------------------------ #
#                                  RATING DATASET                                                  #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def rating_dataset():
    df = IOService.read(RATING_DATASET)
    ds = RatingDataset(df=df)
    return ds


# ------------------------------------------------------------------------------------------------ #
#                                  REVIEW DATASET                                                  #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def review_dataset():
    df = IOService.read(REVIEW_DATASET)
    ds = ReviewDataset(df=df)
    return ds


# ------------------------------------------------------------------------------------------------ #
#                                    APPDATA REPO ZERO                                             #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def appdata_repo_zero(container):
    repo = container.data.appdata_repo()
    df = repo.getall()
    repo.delete_all()
    repo.save()
    yield repo
    repo.load(data=df)


# ------------------------------------------------------------------------------------------------ #
#                                    APPDATA REPO ZERO                                             #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def appdata_repo(container):
    repo = container.data.appdata_repo()
    data = repo.getall()
    repo.delete_all()
    yield repo
    repo.load(data)


# ------------------------------------------------------------------------------------------------ #
#                                      RATING BATCH                                                #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def rating_batch():
    return batch


# ------------------------------------------------------------------------------------------------ #
#                                         JOB DF                                                   #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def job_df():
    return IOService.read(JOBS_FILEPATH)


# ------------------------------------------------------------------------------------------------ #
#                                       JOB REPO                                                   #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def job_repo(container):
    repo = container.data.job_repo()
    data = repo.getall()
    repo.delete_all()
    yield repo
    repo.load(df=data)


# ------------------------------------------------------------------------------------------------ #
#                                     REVIEW JOBRUN REPO                                           #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def review_jobrun_repo(container):
    repo = container.data.review_jobrun_repo()
    data = repo.getall()
    repo.delete_all()
    yield repo
    repo.load(df=data)


# ------------------------------------------------------------------------------------------------ #
#                                     RATING JOBRUN REPO                                           #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def rating_jobrun_repo(container):
    repo = container.data.rating_jobrun_repo()
    data = repo.getall()
    repo.delete_all()
    yield repo
    repo.load(df=data)


# ------------------------------------------------------------------------------------------------ #
#                                      REVIEW REQUEST                                              #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def review_request():
    app = APPS[4]
    return ReviewRequest(id=app["id"], category_id=app["category_id"])


# ------------------------------------------------------------------------------------------------ #
#                                     RATING RESPONSES                                             #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def rating_responses():
    return [
        None,
        [],
        {},
        {
            "ratingAverage": 4,
            "totalNumberOfReviews": 2,
            "ratingCount": 3,
            "ratingListCount": [
                1,
                2,
                3,
            ],
        },
        {
            "ratingAverage": 4,
            "totalNumberOfReviews": 2,
            "ratingCount": 3,
            "ratingCountList": [1, 2, 3, 4, 5],
        },
    ]


# ------------------------------------------------------------------------------------------------ #
#                                     REVIEW RESPONSES                                             #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def review_responses():
    return [
        None,
        [],
        {"status_code": 300},
        {"status_code": 500},
        {"status_code": 200},
    ]


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
    repo.load(data=df)
    return repo


# ------------------------------------------------------------------------------------------------ #
#                                        REVIEWS                                                   #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def review():
    df = IOService.read(REVIEWS_FILEPATH)
    return df


# ------------------------------------------------------------------------------------------------ #
#                                      REVIEW REPO                                                 #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def review_repo(container):
    return container.data.review_repo


# ------------------------------------------------------------------------------------------------ #
#                                        RATINGS                                                   #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def rating():
    df = IOService.read(RATINGS_FILEPATH)
    return df


# ------------------------------------------------------------------------------------------------ #
#                                      RATING REPO                                                 #
# ------------------------------------------------------------------------------------------------ #
@pytest.fixture(scope="module", autouse=False)
def rating_repo(container):
    return container.data.rating_repo


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
