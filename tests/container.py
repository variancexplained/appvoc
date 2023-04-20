#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /tests/container.py                                                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday April 19th 2023 01:02:53 pm                                               #
# Modified   : Thursday April 20th 2023 07:56:44 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dependency_injector import containers, providers
from urllib3.util import Retry
import logging.config

from aimobile.infrastructure.web.adapter import TimeoutHTTPAdapter
from aimobile.infrastructure.web.session import SessionHandler
from aimobile.infrastructure.dal.repo import Repo
from aimobile.infrastructure.dal.mysql import MySQLDatabase
from aimobile.service.appstore import appsto


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
#                                         REPO                                                     #
# ------------------------------------------------------------------------------------------------ #
class RepoContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(MySQLDatabase, name=config.database.name)
    repo = providers.Singleton(Repo, database=db)


# ------------------------------------------------------------------------------------------------ #
#                                         WEB                                                      #
# ------------------------------------------------------------------------------------------------ #
class WebContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    retry = providers.Singleton(
        Retry,
        total=config.rest.retry.total_retries,
        backoff_factor=config.rest.retry.backoff_factor,
        status_forcelist=config.rest.retry.status_forcelist,
        allowed_methods=config.rest.retry.allowed_methods,
        raise_on_redirect=config.rest.retry.raise_on_redirect,
        raise_on_status=config.rest.retry.raise_on_status,
    )

    timeout = providers.Resource(
        TimeoutHTTPAdapter,
        timeout=config.rest.timeout,
        max_retries=retry,
    )

    handler = providers.Resource(
        SessionHandler,
        timeout=timeout,
        session_retries=config.rest.session_retries,
        delay_min=config.rest.delay_min,
        delay_max=config.rest.delay_max,
    )

    scraper = providers.Resource(AppStoreScraper, handler=handler)


# ------------------------------------------------------------------------------------------------ #
#                                       FRAMEWORK                                                  #
# ------------------------------------------------------------------------------------------------ #
class TestContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["tests/config.yml"])

    logs = providers.Container(LoggingContainer, config=config)

    web = providers.Container(WebContainer, config=config.web)

    repo = providers.Container(RepoContainer, config=config)
