#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/service/scraper/appstore/__init__.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 12:37:58 pm                                                  #
# Modified   : Saturday April 8th 2023 08:51:20 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from aimobile import exceptions
from aimobile.service.scraper.base import (
    AbstractScraperFactory,
    AbstractAppDataScraper,
    AbstractReviewScraper,
    Repo,
    Entity,
    RequestIterator,
)
from aimobile.utils.io import IOService

home = "aimobile/service/scraper/appstore/"

directories = [
    "aimobile/service/scraper/appstore/envs/test/logs/",
    "aimobile/service/scraper/appstore/envs/test/data/",
    "aimobile/service/scraper/appstore/envs/prod/logs/",
    "aimobile/service/scraper/appstore/envs/prod/data/",
    "aimobile/service/scraper/appstore/envs/dev/logs/",
    "aimobile/service/scraper/appstore/envs/dev/data/",
]
