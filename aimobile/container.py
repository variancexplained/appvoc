#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Opportunity Discovery in Mobile Applications                             #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/container.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 07:02:56 pm                                                  #
# Modified   : Wednesday April 5th 2023 05:28:43 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging.config  # pragma: no cover
from dependency_injector import containers, providers

from aimobile.data.scraper.appstore.database.sqlite import SQLiteDatabase
from aimobile.data.scraper.appstore.dal.datacentre import DataCentre
from aimobile.data.scraper.appstore.dal.appdata import AppStoreDataRepo
from aimobile.data.scraper.appstore.dal.project import AppStoreProjectRepo


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

    appstore_db = providers.Singleton(
        SQLiteDatabase,
        filepath=config.database.appstore,
    )

    appstore = providers.Singleton(
        DataCentre,
        database=appstore_db,
        appdata_repository=AppStoreDataRepo,
        project_repository=AppStoreProjectRepo,
    )

    gplay_db = providers.Singleton(
        SQLiteDatabase,
        filepath=config.database.google_play,
    )

    # google_play = providers.Singleton(
    #     DataCentre,
    #     database=gplay_db,
    #     appdata_repo=GooglePlayDataRepo,
    #     project_repo=GooglePlayProjectRepo,
    # )


# ------------------------------------------------------------------------------------------------ #
class AIMobile(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    services = providers.Container(ServicesContainer, config=config)

    datacentre = providers.Container(DataCentreContainer, config=config)
