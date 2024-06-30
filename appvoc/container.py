#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/container.py                                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:02:56 pm                                                  #
# Modified   : Sunday June 30th 2024 02:01:37 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Framework Dependency Container"""
import logging
import logging.config  # pragma: no cover
import os

from dependency_injector import containers, providers
from urllib3.util import Retry

from appvoc.config import ConfigFileDefault, ConfigFileJBook
from appvoc.data.repo.app import AppDataRepo
from appvoc.data.repo.job import JobRepo, RatingJobRunRepo, ReviewJobRunRepo
from appvoc.data.repo.project import AppDataProjectRepo
from appvoc.data.repo.rating import RatingRepo
from appvoc.data.repo.request import ReviewRequestRepo
from appvoc.data.repo.review import ReviewRepo
from appvoc.data.repo.uow import UoW
from appvoc.infrastructure.cloud.amazon import AWS
from appvoc.infrastructure.cloud.config import CloudConfig
from appvoc.infrastructure.database.config import DatabaseConfig
from appvoc.infrastructure.database.mysql import MySQLDatabase
from appvoc.infrastructure.file.archive import FileArchiver
from appvoc.infrastructure.file.config import FileConfig
from appvoc.infrastructure.file.io import IOService
from appvoc.infrastructure.web.adapter import TimeoutHTTPAdapter
from appvoc.infrastructure.web.asession import ASessionHandler
from appvoc.infrastructure.web.base import PROXY_SERVERS
from appvoc.infrastructure.web.headers import AppleStoreFrontHeader, BrowserHeader
from appvoc.infrastructure.web.session import SessionHandler
from appvoc.infrastructure.web.throttle import AThrottle, LatencyThrottle


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
#                                     FILE CONTAINER                                               #
# ------------------------------------------------------------------------------------------------ #
class FileContainer(containers.DeclarativeContainer):
    io = providers.Singleton(IOService)
    archiver = providers.Singleton(FileArchiver, config=FileConfig)


# ------------------------------------------------------------------------------------------------ #
#                                        DATA                                                      #
# ------------------------------------------------------------------------------------------------ #
class PersistenceContainer(containers.DeclarativeContainer):
    db = providers.Singleton(MySQLDatabase, config=DatabaseConfig)

    app_repo = providers.Singleton(AppDataRepo, database=db, config=FileConfig)
    review_repo = providers.Singleton(ReviewRepo, database=db, config=FileConfig)
    rating_repo = providers.Singleton(RatingRepo, database=db, config=FileConfig)
    job_repo = providers.Singleton(JobRepo, database=db, config=FileConfig)
    project_repo = providers.Singleton(
        AppDataProjectRepo, database=db, config=FileConfig
    )
    rating_jobrun_repo = providers.Singleton(
        RatingJobRunRepo, database=db, config=FileConfig
    )
    review_jobrun_repo = providers.Singleton(
        ReviewJobRunRepo, database=db, config=FileConfig
    )
    review_request_repo = providers.Singleton(
        ReviewRequestRepo, database=db, config=FileConfig
    )

    uow = providers.Singleton(
        UoW,
        database=db,
        app_repo=AppDataRepo,
        review_repo=ReviewRepo,
        rating_repo=RatingRepo,
        app_project_repo=AppDataProjectRepo,
        job_repo=JobRepo,
        rating_jobrun_repo=RatingJobRunRepo,
        review_jobrun_repo=ReviewJobRunRepo,
        review_request_repo=ReviewRequestRepo,
    )


# ------------------------------------------------------------------------------------------------ #
#                                      CLOUD CONTAINER                                             #
# ------------------------------------------------------------------------------------------------ #
class CloudContainer(containers.DeclarativeContainer):
    aws = providers.Singleton(AWS, config=CloudConfig)


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
    config = "jbook" if "jbook" in os.getcwd() else "appvoc"
    return config


# ------------------------------------------------------------------------------------------------ #
#                                       FRAMEWORK                                                  #
# ------------------------------------------------------------------------------------------------ #
class AppVoCContainer(containers.DeclarativeContainer):
    config_file_selector = providers.Selector(
        config_selector,
        jbook=providers.Factory(ConfigFileJBook),
        appvoc=providers.Factory(ConfigFileDefault),
    )

    config = providers.Configuration(
        yaml_files=[
            config_file_selector().logging,
            config_file_selector().web,
            config_file_selector().persistence,
        ]
    )

    logs = providers.Container(LoggingContainer, config=config)

    data = providers.Container(PersistenceContainer)

    file = providers.Container(FileContainer)

    web = providers.Container(WebSessionContainer, config=config)

    cloud = providers.Container(CloudContainer)
