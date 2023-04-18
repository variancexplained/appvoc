#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/appstore/__init__.py                                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 12:37:58 pm                                                  #
# Modified   : Tuesday April 18th 2023 11:03:24 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from aimobile.framework.exception import exceptions
from aimobile.data.base import (
    AbstractScraperFactory,
    AbstractAppDataScraper,
    AbstractReviewScraper,
    Repo,
    Entity,
    RequestIterator,
)
from aimobile.framework.io.local import IOService

home = "aimobile/scraper/appstore/"

directories = [
    "aimobile/scraper/appstore/envs/test/logs/",
    "aimobile/scraper/appstore/envs/test/data/",
    "aimobile/scraper/appstore/envs/prod/logs/",
    "aimobile/scraper/appstore/envs/prod/data/",
    "aimobile/scraper/appstore/envs/dev/logs/",
    "aimobile/scraper/appstore/envs/dev/data/",
]
