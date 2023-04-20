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
# Modified   : Thursday April 20th 2023 07:27:26 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Framework Dependency Container"""
import logging.config  # pragma: no cover
from dependency_injector import containers, providers
from urllib3.util import Retry

from aimobile.infrastructure.dal.mysql import MySQLDatabase
from aimobile.infrastructure.io.local import IOService
from aimobile.infrastructure.web.adapter import TimeoutHTTPAdapter
from aimobile.infrastructure.web.session import SessionHandler
from aimobile.infrastructure.dal.repo import DAO


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
#                                       DATABASE                                                   #
# ------------------------------------------------------------------------------------------------ #
class DAOContainer(containers.DeclarativeContainer):
    appstore_db = providers.Resource(MySQLDatabase, name="appstore")

    appstore = providers.Resource(DAO, database=appstore_db)

    googleplay_db = providers.Resource(MySQLDatabase, name="googleplay")

    test = providers.Resource(MySQLDatabase, name="test")


# ------------------------------------------------------------------------------------------------ #
#                                         IO                                                       #
# ------------------------------------------------------------------------------------------------ #
class IOContainer(containers.DeclarativeContainer):
    service = providers.Singleton(IOService)


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
        delay=tuple([config.rest.delay_min, config.rest.delay_max]),
    )


# ------------------------------------------------------------------------------------------------ #
#                                       FRAMEWORK                                                  #
# ------------------------------------------------------------------------------------------------ #
class InfrastructureContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["aimobile/framework/config.yml"])

    logs = providers.Container(LoggingContainer, config=config)

    database = providers.Container(DAOContainer)

    io = providers.Container(IOContainer)

    web = providers.Container(WebContainer, config=config.web)


# ------------------------------------------------------------------------------------------------ #
if __name__ == "__main__":
    container = InfrastructureContainer()
    container.init_resources()
