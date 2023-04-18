#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/framework/container.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:02:56 pm                                                  #
# Modified   : Tuesday April 18th 2023 12:50:37 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Framework Dependency Container"""
import logging.config  # pragma: no cover
from dependency_injector import containers, providers
from urllib3.util import Retry

from aimobile.framework.database.mysql import MySQLDatabase
from aimobile.framework.io.local import IOService
from aimobile.framework.web.adapter import TimeoutHTTPAdapter
from aimobile.framework.web.rest import SessionHandler


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
class DatabaseContainer(containers.DeclarativeContainer):
    appstore = providers.Resource(MySQLDatabase, name="appstore")

    googleplay = providers.Resource(MySQLDatabase, name="googleplay")


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
class FrameworkContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["aimobile.framework.config.yml"])

    database = providers.Container(DatabaseContainer)

    io = providers.Container(IOContainer)

    web = providers.Container(WebContainer, config=config.web)
