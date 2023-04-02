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
# Modified   : Saturday April 1st 2023 04:47:31 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging.config  # pragma: no cover
from dependency_injector import containers, providers

from aimobile.data.scraper.appstore.database.sqlite import SQLiteDatabase


# ------------------------------------------------------------------------------------------------ #
class ServicesContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )


# ------------------------------------------------------------------------------------------------ #
class AppStoreDatabaseContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    database = providers.Singleton(
        SQLiteDatabase,
        filepath=config.database.appstore,
    )


# ------------------------------------------------------------------------------------------------ #
class GooglePlayDatabaseContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    database = providers.Singleton(
        SQLiteDatabase,
        filepath=config.database.google_play,
    )


# ------------------------------------------------------------------------------------------------ #
class AIMobile(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    services = providers.Container(ServicesContainer, config=config)

    appstore = providers.Container(AppStoreDatabaseContainer, config=config)
