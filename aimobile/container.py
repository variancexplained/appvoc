#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/container.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:02:56 pm                                                  #
# Modified   : Saturday April 29th 2023 06:34:47 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Framework Dependency Container"""
import logging.config  # pragma: no cover

from dependency_injector import containers, providers
from urllib3.util import Retry

from aimobile.infrastructure.io.local import IOService
from aimobile.infrastructure.web.adapter import TimeoutHTTPAdapter
from aimobile.infrastructure.web.autothrottle import AutoThrottleLatency
from aimobile.infrastructure.dal.mysql import MySQLDatabase
from aimobile.data.repo.task import TaskRepo
from aimobile.data.repo.appstore import (
    AppStoreAppDataRepo,
    AppStoreReviewRepo,
    AppStoreRatingRepo,
)
from aimobile.infrastructure.web.headers import BrowserHeader, AppleStoreFrontHeader
from aimobile.infrastructure.web.session import SessionHandler


# ------------------------------------------------------------------------------------------------ #
#                                        LOGGING                                                   #
# ------------------------------------------------------------------------------------------------ #
class LoggingContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )


# ------------------------------------------------------------------------------------------------ #
#                                         IO                                                       #
# ------------------------------------------------------------------------------------------------ #
class IOContainer(containers.DeclarativeContainer):
    service = providers.Singleton(IOService)


# ------------------------------------------------------------------------------------------------ #
#                                        DATA                                                      #
# ------------------------------------------------------------------------------------------------ #
class DataStorageContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(MySQLDatabase, name=config.database.appstore.name)

    # The following three repos are presented for testing as the UoW class takes uninstantiated types
    appdata_repo = providers.Singleton(AppStoreAppDataRepo, database=db)
    review_repo = providers.Singleton(AppStoreReviewRepo, database=db)
    rating_repo = providers.Singleton(AppStoreRatingRepo, database=db)
    task_repo = providers.Singleton(TaskRepo, database=db)


# ------------------------------------------------------------------------------------------------ #
#                                   WEB SESSION CONTAINER                                          #
# ------------------------------------------------------------------------------------------------ #
class WebSessionContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    retry = providers.Singleton(
        Retry,
        total=config.web.session.retry.total_retries,
        backoff_factor=config.web.session.retrybackoff_factor,
        status_forcelist=config.web.session.retry.status_forcelist,
        allowed_methods=config.web.session.retry.allowed_methods,
        raise_on_redirect=config.web.session.retry.raise_on_redirect,
        raise_on_status=config.web.session.retry.raise_on_status,
    )

    timeout = providers.Resource(
        TimeoutHTTPAdapter,
        timeout=config.web.session.timeout,
        max_retries=retry,
    )

    throttle = providers.Resource(
        AutoThrottleLatency,
        start_delay=config.web.session.throttle.start_delay,
        min_delay=config.web.session.throttle.min_delay,
        max_delay=config.web.session.throttle.max_delay,
        lambda_factor=config.web.session.throttle.lambda_factor,
        backoff_factor=config.web.session.throttle.backoff_factor,
        concurrency=config.web.session.throttle.concurrency,
    )

    browser_headers = providers.Resource(BrowserHeader)

    storefront_headers = providers.Resource(AppleStoreFrontHeader)

    session = providers.Resource(
        SessionHandler,
    )


# ------------------------------------------------------------------------------------------------ #
#                                       FRAMEWORK                                                  #
# ------------------------------------------------------------------------------------------------ #
class AIMobileContainer(containers.DeclarativeContainer):
    config = providers.Configuration(
        yaml_files=[
            "config/logging.yml",
            "config/persistence.yml",
            "config/web.yml",
        ]
    )

    logs = providers.Container(LoggingContainer, config=config)

    data = providers.Container(DataStorageContainer, config=config)

    io = providers.Container(IOContainer)

    web = providers.Container(WebSessionContainer, config=config)


# ------------------------------------------------------------------------------------------------ #
if __name__ == "__main__":
    container = AIMobileContainer()
    container.wire(packages=["aimobile.data.acquisition.scraper"])
