#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/scraper/appstore/container.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:02:56 pm                                                  #
# Modified   : Monday April 10th 2023 01:32:07 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging.config  # pragma: no cover
from dependency_injector import containers, providers
from aimobile.scraper.appstore.database.sqlite import SQLiteDatabase
from aimobile.scraper.appstore.repo.datacentre import DataCentre
from aimobile.scraper.appstore.repo.appdata import AppStoreDataRepo
from aimobile.scraper.appstore.repo.project import AppStoreProjectRepo
from aimobile.scraper.appstore.repo.request import AppStoreRequestRepo
from aimobile.scraper.appstore.config.selector import Config
from aimobile.scraper.appstore.internet.session import SessionHandler


# ------------------------------------------------------------------------------------------------ #
class ServicesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )


# ------------------------------------------------------------------------------------------------ #
class DataCentreContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    print(f"\n{40*'='}\n{config.database}\n{40*'='}")

    database = providers.Singleton(
        SQLiteDatabase,
        filepath=config.database,
    )

    repo = providers.Singleton(
        DataCentre,
        database=database,
        appdata_repository=AppStoreDataRepo,
        project_repository=AppStoreProjectRepo,
        request_repository=AppStoreRequestRepo,
    )


# ------------------------------------------------------------------------------------------------ #
class SessionHandlerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    handler = providers.Singleton(SessionHandler, config=config)


# ------------------------------------------------------------------------------------------------ #
class AppStoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=[Config.file])

    services = providers.Container(ServicesContainer, config=config)

    datacentre = providers.Container(DataCentreContainer, config=config)

    session = providers.Container(SessionHandlerContainer, config=config.scraper)
