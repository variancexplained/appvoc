#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/container.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:02:56 pm                                                  #
# Modified   : Monday August 21st 2023 07:27:52 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Framework Dependency Container"""
import os
import logging
import logging.config  # pragma: no cover

from dependency_injector import containers, providers
from urllib3.util import Retry

from appstore.infrastructure.io.local import IOService
from appstore.infrastructure.web.adapter import TimeoutHTTPAdapter
from appstore.infrastructure.web.throttle import LatencyThrottle, AThrottle
from appstore.infrastructure.database.mysql import MySQLDatabase
from appstore.data.repo.project import AppDataProjectRepo
from appstore.data.repo.appdata import AppDataRepo
from appstore.data.repo.review import ReviewRepo
from appstore.data.repo.rating import RatingRepo
from appstore.data.repo.request import ReviewRequestRepo
from appstore.data.repo.job import RatingJobRunRepo, ReviewJobRunRepo, JobRepo
from appstore.infrastructure.web.base import PROXY_SERVERS
from appstore.data.repo.uow import UoW
from appstore.infrastructure.web.headers import BrowserHeader, AppleStoreFrontHeader
from appstore.infrastructure.web.session import SessionHandler
from appstore.infrastructure.web.asession import ASessionHandler
from appstore.config import ConfigFileDefault, ConfigFileJBook


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
class PersistenceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(MySQLDatabase, name=config.database.appstore.name)

    appdata_repo = providers.Singleton(AppDataRepo, database=db)
    review_repo = providers.Singleton(ReviewRepo, database=db)
    rating_repo = providers.Singleton(RatingRepo, database=db)
    job_repo = providers.Singleton(JobRepo, database=db)
    rating_jobrun_repo = providers.Singleton(RatingJobRunRepo, database=db)
    review_jobrun_repo = providers.Singleton(ReviewJobRunRepo, database=db)
    review_request_repo = providers.Singleton(ReviewRequestRepo, database=db)

    uow = providers.Singleton(
        UoW,
        database=db,
        appdata_repo=AppDataRepo,
        review_repo=ReviewRepo,
        rating_repo=RatingRepo,
        appdata_project_repo=AppDataProjectRepo,
        job_repo=JobRepo,
        rating_jobrun_repo=RatingJobRunRepo,
        review_jobrun_repo=ReviewJobRunRepo,
        review_request_repo=ReviewRequestRepo,
    )


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
        LatencyThrottle,
        start_delay=config.web.session.throttle.start_delay,
        min_delay=config.web.session.throttle.min_delay,
        max_delay=config.web.session.throttle.max_delay,
        verbose=config.web.session.throttle.verbose,
    )
    athrottle = providers.Resource(
        AThrottle,
        burnin_period=config.web.async_session.athrottle.burnin_period,
        burnin_reset=config.web.async_session.athrottle.burnin_reset,
        burnin_rate=config.web.async_session.athrottle.burnin_rate,
        burnin_threshold_factor=config.web.async_session.athrottle.burnin_threshold_factor,
        rolling_window_size=config.web.async_session.athrottle.rolling_window_size,
        cooldown_factor=config.web.async_session.athrottle.cooldown_factor,
        cooldown_phase=config.web.async_session.athrottle.cooldown_phase,
        tolerance=config.web.async_session.athrottle.tolerance,
        rate=config.web.async_session.athrottle.rate,
        verbose=config.web.async_session.athrottle.verbose,
    )

    browser_headers = providers.Resource(BrowserHeader)

    storefront_headers = providers.Resource(AppleStoreFrontHeader)

    session = providers.Resource(
        SessionHandler,
        timeout=timeout,
        throttle=throttle,
        headers=browser_headers,
        session_retries=config.web.session.retries,
    )

    asession = providers.Resource(
        ASessionHandler,
        throttle=athrottle,
        headers=browser_headers,
        max_concurrency=config.web.async_session.concurrency,
        retries=config.web.async_session.retries,
        timeout=config.web.async_session.timeout,
        proxies=PROXY_SERVERS,
    )


# ------------------------------------------------------------------------------------------------ #
#                                    CONFIG SELECTOR                                               #
# ------------------------------------------------------------------------------------------------ #
def config_selector():
    config = "jbook" if "jbook" in os.getcwd() else "appstore"
    return config


# ------------------------------------------------------------------------------------------------ #
#                                       FRAMEWORK                                                  #
# ------------------------------------------------------------------------------------------------ #
class AppstoreContainer(containers.DeclarativeContainer):
    config_file_selector = providers.Selector(
        config_selector,
        jbook=providers.Factory(ConfigFileJBook),
        appstore=providers.Factory(ConfigFileDefault),
    )

    config = providers.Configuration(
        yaml_files=[
            config_file_selector().logging,
            config_file_selector().web,
            config_file_selector().persistence,
        ]
    )

    logs = providers.Container(LoggingContainer, config=config)

    data = providers.Container(PersistenceContainer, config=config)

    io = providers.Container(IOContainer)

    web = providers.Container(WebSessionContainer, config=config)
