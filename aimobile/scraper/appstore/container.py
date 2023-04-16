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
# Modified   : Sunday April 16th 2023 03:16:54 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging.config  # pragma: no cover
from dependency_injector import containers, providers
from aimobile.scraper.appstore.database.sqlite import SQLiteDatabase
from aimobile.scraper.appstore.database.mysql import MySQLDatabase
from aimobile.scraper.appstore.repo.datacentre import DataCentre
from aimobile.scraper.appstore.repo.appdata import AppStoreDataRepo
from aimobile.scraper.appstore.repo.rating import AppStoreRatingsRepo
from aimobile.scraper.appstore.repo.review import AppStoreReviewRepo
from aimobile.scraper.appstore.config.selector import Config
from aimobile.scraper.appstore.http.session import SessionHandler


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

    sqlite = providers.Singleton(
        SQLiteDatabase,
        filepath=config.database.sqlite,
    )

    mysql = providers.Singleton(
        MySQLDatabase,
        name=config.database.mysql,
    )

    repo = providers.Singleton(
        DataCentre,
        sqlite=sqlite,
        mysql=mysql,
        appdata_repository=AppStoreDataRepo,
        rating_repository=AppStoreRatingsRepo,
        review_repository=AppStoreReviewRepo,
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
